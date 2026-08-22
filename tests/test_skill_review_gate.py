from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import types
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill-review-gate.py"
SPEC = importlib.util.spec_from_file_location("skill_review_gate", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(gate)


def arguments(state_dir: Path, framework: Path, threshold: int = 4) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        state_dir=str(state_dir),
        framework_root=str(framework),
        threshold=threshold,
        assignee="executor-gpt",
        model="gpt-5.6-sol",
        provider="openai-codex",
        reasoning="xhigh",
        dry_run=True,
    )


def payload(task_id: str, summary: str = "done", board: str = "default") -> dict:
    return {
        "hook_event_name": "kanban_task_completed",
        "cwd": "/project",
        "extra": {
            "task_id": task_id,
            "board": board,
            "assignee": "executor-deep",
            "profile_name": "executor-deep",
            "run_id": 1,
            "summary": summary,
        },
    }


class SkillReviewGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.state_dir = root / "state"
        self.framework = root / "framework"
        self.framework.mkdir()
        self.args = arguments(self.state_dir, self.framework)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def state(self) -> dict:
        return json.loads((self.state_dir / "state.json").read_text(encoding="utf-8"))

    def test_four_distinct_completions_create_one_xhigh_review(self) -> None:
        for index in range(1, 4):
            result = gate.process_hook(self.args, payload(f"t_a{index}"))
            self.assertEqual(result["status"], "counted")
        result = gate.process_hook(self.args, payload("t_a4"))
        self.assertEqual(result["status"], "review_created")
        state = self.state()
        self.assertEqual(state["pending"], [])
        self.assertEqual(len(state["reviews"]), 1)
        self.assertEqual(state["reviews"][0]["reasoning"], "xhigh")
        self.assertEqual(state["reviews"][0]["trigger"], "threshold")

    def test_duplicate_completion_does_not_increment(self) -> None:
        gate.process_hook(self.args, payload("t_dup"))
        result = gate.process_hook(self.args, payload("t_dup"))
        self.assertEqual(result["status"], "duplicate")
        self.assertEqual(len(self.state()["pending"]), 1)

    def test_critical_marker_triggers_immediately_without_persisting_summary(self) -> None:
        sensitive_text = f"{gate.CRITICAL_MARKER} tenant isolation diagnosis"
        result = gate.process_hook(self.args, payload("t_critical", sensitive_text))
        self.assertEqual(result["trigger"], "critical")
        serialized = (self.state_dir / "state.json").read_text(encoding="utf-8")
        self.assertNotIn("tenant isolation diagnosis", serialized)

    def test_phase_marker_triggers_pending_batch(self) -> None:
        gate.process_hook(self.args, payload("t_phase1"))
        result = gate.process_hook(self.args, payload("t_phase2", gate.PHASE_MARKER))
        self.assertEqual(result["trigger"], "phase")
        self.assertEqual(len(self.state()["reviews"][0]["source_task_ids"]), 2)

    def test_review_completion_is_not_counted(self) -> None:
        created = gate.process_hook(self.args, payload("t_s1", gate.CRITICAL_MARKER))
        review_task = created["review_task_id"]
        # Dry-run task IDs are not normal Kanban IDs, so emulate a real ID in state.
        state_path = self.state_dir / "state.json"
        state = self.state()
        state["reviews"][0]["task_id"] = "t_review1"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        result = gate.process_hook(self.args, payload("t_review1"))
        self.assertEqual(result["status"], "review_completion_ignored")
        self.assertEqual(self.state()["pending"], [])
        self.assertTrue(review_task.startswith("dry_"))

    def test_ignore_marker_does_not_increment(self) -> None:
        result = gate.process_hook(self.args, payload("t_ignore", gate.IGNORE_MARKER))
        self.assertEqual(result["status"], "ignored")
        self.assertEqual(self.state()["pending"], [])

    def test_boards_have_independent_counters(self) -> None:
        for index in range(1, 4):
            gate.process_hook(self.args, payload(f"t_boarda{index}", board="a"))
        gate.process_hook(self.args, payload("t_boardb1", board="b"))
        self.assertEqual(len(self.state()["reviews"]), 0)
        result = gate.process_hook(self.args, payload("t_boarda4", board="a"))
        self.assertEqual(result["status"], "review_created")
        state = self.state()
        self.assertEqual([item["task_id"] for item in state["pending"]], ["t_boardb1"])

    def test_patch_scope_rejects_paths_outside_skills(self) -> None:
        unsafe = "--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-old\n+new\n"
        with self.assertRaises(gate.GateError):
            gate._patch_paths(unsafe)

    def test_patch_scope_allows_skill_addition(self) -> None:
        safe = (
            "--- /dev/null\n"
            "+++ b/skills/software-development/example/SKILL.md\n"
            "@@ -0,0 +1 @@\n"
            "+content\n"
        )
        self.assertEqual(
            gate._patch_paths(safe),
            [Path("skills/software-development/example/SKILL.md")],
        )

    def test_secret_pattern_is_rejected(self) -> None:
        with self.assertRaises(gate.GateError):
            gate._scan_secrets("API_KEY=" + "sk" + "-" + ("x" * 24))

    def test_valid_skill_patch_is_checked_in_temporary_copy(self) -> None:
        skill = self.framework / "skills/software-development/example/SKILL.md"
        skill.parent.mkdir(parents=True)
        original = (
            "---\nname: example\n"
            "description: Provide a sufficiently specific example procedure for validation.\n"
            "---\n\n# Example\n\nOriginal.\n"
        )
        skill.write_text(original, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.framework, check=True)
        subprocess.run(["git", "add", "."], cwd=self.framework, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "base"],
            cwd=self.framework,
            check=True,
        )
        skill.write_text(original + "\nReusable addition.\n", encoding="utf-8")
        patch_text = subprocess.run(
            ["git", "diff", "--", "skills/software-development/example/SKILL.md"],
            cwd=self.framework,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        patch_path = Path(self.temp.name) / "proposal.patch"
        patch_path.write_text(patch_text, encoding="utf-8")
        skill.write_text(original, encoding="utf-8")
        paths = gate.validate_proposal(self.framework, patch_path)
        self.assertEqual(paths, [Path("skills/software-development/example/SKILL.md")])


if __name__ == "__main__":
    unittest.main()
