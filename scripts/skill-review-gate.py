#!/usr/bin/env python3
"""Deterministic, approval-gated skill review for Hermes Kanban completions.

The hook records only task references and routing metadata. It never stores
completion summaries, messages, logs, credentials, or model responses.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Iterator


STATE_VERSION = 1
DEFAULT_THRESHOLD = 4
MAX_SEEN_TASKS = 1024
REVIEW_TITLE_PREFIX = "[skill-review]"
CRITICAL_MARKER = "[SKILL-REVIEW:CRITICAL]"
PHASE_MARKER = "[PHASE-COMPLETE]"
IGNORE_MARKER = "[SKILL-REVIEW:IGNORE]"
ALLOWED_PATCH_ROOT = PurePosixPath("skills/software-development")
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:DEEPSEEK_)?API_KEY\s*=\s*\S+", re.IGNORECASE),
)


class GateError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def empty_state(threshold: int) -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "threshold": threshold,
        "pending": [],
        "reviews": [],
        "seen_task_ids": [],
        "last_error": None,
    }


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(temporary)
        raise


@contextlib.contextmanager
def locked_state(state_dir: Path, threshold: int) -> Iterator[tuple[Path, dict[str, Any]]]:
    state_dir.mkdir(parents=True, exist_ok=True)
    lock_path = state_dir / "state.lock"
    state_path = state_dir / "state.json"
    with lock_path.open("a+", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            try:
                state = json.loads(state_path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                state = empty_state(threshold)
            except (json.JSONDecodeError, OSError) as exc:
                raise GateError(f"invalid state file: {exc}") from exc
            if not isinstance(state, dict) or state.get("version") != STATE_VERSION:
                raise GateError("unsupported skill-review state version")
            state["threshold"] = threshold
            try:
                yield state_path, state
            finally:
                _atomic_json(state_path, state)
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def _payload_record(payload: dict[str, Any]) -> tuple[dict[str, str], str]:
    if payload.get("hook_event_name") != "kanban_task_completed":
        raise GateError("unexpected hook event")
    extra = payload.get("extra")
    if not isinstance(extra, dict):
        raise GateError("hook payload has no extra object")
    task_id = str(extra.get("task_id") or "").strip()
    if not re.fullmatch(r"t_[A-Za-z0-9]+", task_id):
        raise GateError("hook payload has an invalid task id")
    summary = str(extra.get("summary") or "")
    record = {
        "task_id": task_id,
        "board": str(extra.get("board") or "default")[:120],
        "assignee": str(extra.get("assignee") or "")[:120],
        "profile": str(extra.get("profile_name") or "")[:120],
        "run_id": str(extra.get("run_id") or "")[:40],
        "completed_at": utc_now(),
    }
    return record, summary


def _batch_id(records: list[dict[str, str]]) -> str:
    material = "\n".join(record["task_id"] for record in records).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:12]


def _review_body(
    *, batch_id: str, records: list[dict[str, str]], framework_root: Path, state_dir: Path,
) -> str:
    task_lines = "\n".join(f"- {item['task_id']} (board: {item['board']})" for item in records)
    proposal = state_dir / "proposals" / f"{batch_id}.md"
    patch = state_dir / "proposals" / f"{batch_id}.patch"
    return f"""OBJECTIVE
Review the completed Kanban tasks below for reusable procedural lessons. Sanitize and consolidate only lessons supported by current code, tests, database evidence, or canonical documentation.

TASK REFERENCES
{task_lines}

CANONICAL FRAMEWORK (READ ONLY)
{framework_root}

OUTPUTS
- Review report: {proposal}
- Optional unified Git patch: {patch}

BOUNDARIES
- Do not modify the canonical framework, profiles, Git branches, databases, sessions, memories, or task logs.
- Never copy raw logs, prompts, personal data, secrets, credentials, temporary paths, transient commits, or project-specific state into a skill.
- Reject one-off failures, duplicated rules, model-specific advice, and claims without evidence.
- A patch may only add or modify files under skills/software-development/. Do not delete or rename files.
- Record affected skill, evidence, general invariant, counterexample, validation, residual risk, and whether the proposal is NO_CHANGE or PATCH_READY.
- End by calling kanban_request_review; never self-approve or publish.
"""


def create_review_task(
    *, batch_id: str, records: list[dict[str, str]], framework_root: Path,
    state_dir: Path, assignee: str, model: str, provider: str, reasoning: str,
    dry_run: bool,
) -> str:
    if dry_run:
        return f"dry_{batch_id}"
    try:
        from hermes_cli import kanban_db as kb
    except ImportError as exc:
        raise GateError("Hermes runtime is unavailable to create the review card") from exc

    boards = {item["board"] for item in records}
    board = records[-1]["board"] if len(boards) == 1 else None
    body = _review_body(
        batch_id=batch_id,
        records=records,
        framework_root=framework_root,
        state_dir=state_dir,
    )
    with kb.connect_closing(board=board) as connection:
        return kb.create_task(
            connection,
            title=f"{REVIEW_TITLE_PREFIX} batch {batch_id}",
            body=body,
            assignee=assignee,
            created_by="skill-review-gate",
            workspace_kind="scratch",
            workspace_path=None,
            idempotency_key=f"skill-review-gate:{batch_id}",
            max_runtime_seconds=1800,
            skills=["skill-evolution-review"],
            max_retries=1,
            model_override=model,
            provider_override=provider,
            reasoning_effort=reasoning,
            initial_status="running",
            board=board,
        )


def resolve_framework_root(raw: str) -> Path:
    if raw and raw != "auto":
        return Path(raw).resolve()
    hermes_home = Path(os.environ.get("HERMES_HOME") or "").resolve()
    linked_skill = hermes_home / "skills/software-development/skill-evolution-review"
    if linked_skill.exists():
        resolved = linked_skill.resolve()
        if len(resolved.parents) >= 3:
            candidate = resolved.parents[2]
            if (candidate / ".git").is_dir():
                return candidate
    raise GateError("cannot resolve the canonical framework from the installed skill link")


def process_hook(args: argparse.Namespace, payload: dict[str, Any]) -> dict[str, Any]:
    record, summary = _payload_record(payload)
    state_dir = Path(args.state_dir).resolve()
    framework_root = resolve_framework_root(args.framework_root)
    with locked_state(state_dir, args.threshold) as (_, state):
        seen = list(state.get("seen_task_ids") or [])
        if record["task_id"] in seen:
            return {"status": "duplicate", "task_id": record["task_id"]}
        seen.append(record["task_id"])
        state["seen_task_ids"] = seen[-MAX_SEEN_TASKS:]

        for review in state.get("reviews") or []:
            if review.get("task_id") == record["task_id"]:
                review["status"] = "completed"
                review["completed_at"] = utc_now()
                state["last_error"] = None
                return {"status": "review_completion_ignored", "task_id": record["task_id"]}

        if IGNORE_MARKER in summary or summary.startswith(REVIEW_TITLE_PREFIX):
            return {"status": "ignored", "task_id": record["task_id"]}

        pending = list(state.get("pending") or [])
        pending.append(record)
        same_board = [item for item in pending if item.get("board") == record["board"]]
        critical = CRITICAL_MARKER in summary
        phase_boundary = PHASE_MARKER in summary
        if not critical and not phase_boundary and len(same_board) < args.threshold:
            state["pending"] = pending
            state["last_error"] = None
            return {
                "status": "counted",
                "pending": len(same_board),
                "threshold": args.threshold,
            }

        trigger = "critical" if critical else "phase" if phase_boundary else "threshold"
        selected = same_board if critical or phase_boundary else same_board[: args.threshold]
        batch_id = _batch_id(selected)
        try:
            review_task_id = create_review_task(
                batch_id=batch_id,
                records=selected,
                framework_root=framework_root,
                state_dir=state_dir,
                assignee=args.assignee,
                model=args.model,
                provider=args.provider,
                reasoning=args.reasoning,
                dry_run=args.dry_run,
            )
        except Exception as exc:
            state["pending"] = pending
            state["last_error"] = {"at": utc_now(), "error": type(exc).__name__}
            raise

        selected_ids = {item["task_id"] for item in selected}
        state["pending"] = [item for item in pending if item["task_id"] not in selected_ids]
        state.setdefault("reviews", []).append({
            "batch_id": batch_id,
            "task_id": review_task_id,
            "source_task_ids": [item["task_id"] for item in selected],
            "trigger": trigger,
            "reasoning": args.reasoning,
            "status": "created",
            "created_at": utc_now(),
            "framework_commit": _git_head(framework_root),
        })
        state["last_error"] = None
        return {
            "status": "review_created",
            "batch_id": batch_id,
            "review_task_id": review_task_id,
            "trigger": trigger,
        }


def _git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _patch_paths(patch_text: str) -> list[PurePosixPath]:
    old_paths: list[str] = []
    new_paths: list[str] = []
    for line in patch_text.splitlines():
        if line.startswith("--- "):
            old_paths.append(line[4:].split("\t", 1)[0].strip())
        elif line.startswith("+++ "):
            new_paths.append(line[4:].split("\t", 1)[0].strip())
    if not new_paths or len(old_paths) != len(new_paths):
        raise GateError("proposal is not a complete unified patch")
    paths: list[PurePosixPath] = []
    for old, new in zip(old_paths, new_paths):
        if new == "/dev/null":
            raise GateError("skill deletion is not allowed")
        candidate = new[2:] if new.startswith("b/") else new
        path = PurePosixPath(candidate)
        if path.is_absolute() or ".." in path.parts:
            raise GateError(f"unsafe patch path: {candidate}")
        if path != ALLOWED_PATCH_ROOT and ALLOWED_PATCH_ROOT not in path.parents:
            raise GateError(f"patch path outside the skill root: {candidate}")
        if old != "/dev/null":
            old_candidate = old[2:] if old.startswith("a/") else old
            if PurePosixPath(old_candidate) != path:
                raise GateError("skill renames are not allowed")
        paths.append(path)
    return sorted(set(paths), key=str)


def _scan_secrets(text: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise GateError("proposal contains a credential-like pattern")


def validate_skills(root: Path) -> None:
    skills_root = root / ALLOWED_PATCH_ROOT
    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            raise GateError(f"missing frontmatter: {skill_file}")
        try:
            closing = lines[1:].index("---") + 1
        except ValueError as exc:
            raise GateError(f"unterminated frontmatter: {skill_file}") from exc
        frontmatter = "\n".join(lines[1:closing])
        name_match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
        description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)
        if not name_match or name_match.group(1) != skill_file.parent.name:
            raise GateError(f"invalid skill name: {skill_file}")
        if not description_match or len(description_match.group(1).strip()) < 20:
            raise GateError(f"missing or weak skill description: {skill_file}")
        for target in re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (skill_file.parent / target).resolve()
            if not resolved.is_file():
                raise GateError(f"missing skill reference: {skill_file} -> {target}")


def validate_proposal(framework_root: Path, patch_path: Path) -> list[PurePosixPath]:
    patch_text = patch_path.read_text(encoding="utf-8")
    _scan_secrets(patch_text)
    paths = _patch_paths(patch_text)
    check = subprocess.run(
        ["git", "apply", "--check", str(patch_path)], cwd=framework_root,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check.returncode != 0:
        raise GateError(f"git apply --check failed: {check.stderr.strip()[:400]}")
    with tempfile.TemporaryDirectory(prefix="skill-review-validate-") as temporary:
        candidate_root = Path(temporary) / "repo"
        shutil.copytree(framework_root, candidate_root, ignore=shutil.ignore_patterns(".git"))
        applied = subprocess.run(
            ["git", "apply", str(patch_path)], cwd=candidate_root,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if applied.returncode != 0:
            raise GateError(f"temporary patch apply failed: {applied.stderr.strip()[:400]}")
        validate_skills(candidate_root)
        for path in paths:
            target = candidate_root / path
            if target.is_file():
                _scan_secrets(target.read_text(encoding="utf-8"))
    return paths


def publish(args: argparse.Namespace) -> dict[str, Any]:
    if not args.approved:
        raise GateError("publication requires the explicit --approved flag")
    state_dir = Path(args.state_dir).resolve()
    framework_root = Path(args.framework_root).resolve()
    patch_path = state_dir / "proposals" / f"{args.batch_id}.patch"
    if not patch_path.is_file():
        raise GateError(f"proposal patch not found: {patch_path}")
    paths = validate_proposal(framework_root, patch_path)
    backup_root = state_dir / "publish-backups" / args.batch_id
    if backup_root.exists():
        raise GateError(f"publication backup already exists: {backup_root}")
    for path in paths:
        source = framework_root / path
        destination = backup_root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copy2(source, destination)
        else:
            destination.with_suffix(destination.suffix + ".absent").touch()
    applied = subprocess.run(
        ["git", "apply", str(patch_path)], cwd=framework_root,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if applied.returncode != 0:
        raise GateError(f"publication failed: {applied.stderr.strip()[:400]}")
    try:
        validate_skills(framework_root)
    except Exception:
        for path in paths:
            target = framework_root / path
            saved = backup_root / path
            absent = saved.with_suffix(saved.suffix + ".absent")
            if saved.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(saved, target)
            elif absent.exists() and target.exists():
                target.unlink()
        raise
    with locked_state(state_dir, DEFAULT_THRESHOLD) as (_, state):
        for review in state.get("reviews") or []:
            if review.get("batch_id") == args.batch_id:
                review["status"] = "published"
                review["published_at"] = utc_now()
                review["approved_by"] = args.approved_by
    return {
        "status": "published",
        "batch_id": args.batch_id,
        "paths": [str(path) for path in paths],
        "backup": str(backup_root),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    hook = subparsers.add_parser("hook", help="process a kanban completion payload from stdin")
    hook.add_argument("--state-dir", required=True)
    hook.add_argument("--framework-root", default="auto")
    hook.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    hook.add_argument("--assignee", default="executor-gpt")
    hook.add_argument("--model", default="gpt-5.6-sol")
    hook.add_argument("--provider", default="openai-codex")
    hook.add_argument("--reasoning", default="xhigh")
    hook.add_argument("--dry-run", action="store_true")
    hook.add_argument("--payload-file", help="read a synthetic payload from a file instead of stdin")
    status = subparsers.add_parser("status", help="show sanitized gate state")
    status.add_argument("--state-dir", required=True)
    proposal = subparsers.add_parser("validate-proposal", help="validate a staged skill patch")
    proposal.add_argument("--framework-root", required=True)
    proposal.add_argument("--patch", required=True)
    publication = subparsers.add_parser("publish", help="apply an approved staged skill patch")
    publication.add_argument("--state-dir", required=True)
    publication.add_argument("--framework-root", required=True)
    publication.add_argument("--batch-id", required=True)
    publication.add_argument("--approved", action="store_true")
    publication.add_argument("--approved-by", default="human")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "hook":
            if args.threshold < 2 or args.threshold > 20:
                raise GateError("threshold must be between 2 and 20")
            if args.payload_file:
                payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
            else:
                payload = json.load(sys.stdin)
            result = process_hook(args, payload)
        elif args.command == "status":
            path = Path(args.state_dir).resolve() / "state.json"
            result = json.loads(path.read_text(encoding="utf-8")) if path.exists() else empty_state(DEFAULT_THRESHOLD)
        elif args.command == "validate-proposal":
            paths = validate_proposal(Path(args.framework_root).resolve(), Path(args.patch).resolve())
            result = {"status": "valid", "paths": [str(path) for path in paths]}
        else:
            result = publish(args)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        # Shell hooks are observers and must not break task completion. Keep the
        # wire response valid and omit user/task content from the error.
        print(json.dumps({"status": "error", "error": type(exc).__name__}, sort_keys=True))
        return 0 if args.command == "hook" else 1


if __name__ == "__main__":
    raise SystemExit(main())
