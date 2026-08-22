---
name: skill-evolution-review
description: Review evidence from a bounded batch of completed software tasks, extract only reusable procedural lessons, sanitize them, and stage an approval-ready skill patch. Use only for an explicit skill-review batch or critical-learning review; do not use during ordinary implementation or to edit canonical skills directly.
license: MIT
---

# Skill Evolution Review

Turn verified execution evidence into a small, durable skill improvement without treating every failure as a lesson or every success as a universal rule.

## Preserve the approval boundary

The canonical framework and installed profile links are read-only during review. Write only the requested report and optional unified patch to the staging paths in the task. End with `kanban_request_review`; never publish, commit, push, approve your own patch, or edit a canonical skill directly.

## Review the evidence batch

For each referenced task, establish current truth from its card, affected code, Git state, tests, database evidence, and canonical documentation. Task summaries and model reports are leads, not proof. Do not open credentials, `.env`, authentication files, unrelated sessions, or raw logs.

Classify each candidate:

- `REUSABLE`: a recurring procedure or invariant supported by current evidence;
- `PROJECT_ONLY`: useful for the project handoff, not a general skill;
- `TRANSIENT`: temporary state, one-off failure, version-specific workaround, or stale fact;
- `DUPLICATE`: already covered by a canonical rule;
- `UNPROVEN`: plausible but missing a reproducer, counterexample, or validation.

Only `REUSABLE` candidates may enter a patch.

## Build the smallest sufficient proposal

Prefer refining an existing skill over creating another one. Preserve discriminating trigger text and keep conditional detail in `references/`. A proposed rule must state, directly or through its procedure:

1. the situation that activates it;
2. the invariant or failure it prevents;
3. the smallest safe action;
4. evidence or validation that distinguishes success from appearance;
5. a counterexample or boundary preventing overgeneralization.

Do not encode model names, project phases, local usernames, absolute temporary paths, commits, task IDs, token totals, raw errors, personal preferences, secrets, or facts that current code can answer.

Follow the [review and proposal protocol](references/review-and-proposal-protocol.md) for the report, patch, validation, and escalation format.
