---
name: project-audit-core
description: Audit the current state of an existing software project before planning, delegation, workaround design, or consequential changes. Use for read-only repository, architecture, documentation, risk, and source-of-truth discovery.
license: MIT
---

# Project Audit Core

Inspect and report; do not implement fixes unless the user separately authorizes them.

## Establish identity and state

Confirm path, repository, branch, commit, remotes when relevant, worktrees, tracked/untracked modifications and divergence. Preserve user work and avoid commands that mutate or normalize state.

## Find authoritative sources

Inventory current README, governance/agent rules, project profile/context, roadmap, task, handoff/status, architecture, tests and configuration. Classify statements as:

- `[CONFIRMED]`: verified in current code, Git, database, test or effective configuration;
- `[DOCUMENTED]`: present only in current documentation;
- `[HISTORICAL]`: from old reports/sessions;
- `[UNKNOWN]`: requires evidence or a human decision.

Do not read secret values. Check presence or shape only when necessary and authorized.

## Discover architecture and health

Identify relevant stack, modules, data stores, migrations, auth/authz, infrastructure, deployment and test systems. Inspect only as broadly as the audit objective requires. Report inconsistencies, technical debt, stale documents, abandoned workspaces and cleanup candidates without deleting them.

## Diagnose difficult failures

Treat a tight feedback loop as an explicit diagnostic deliverable whenever practical: record one safe command or procedure that reproduces the exact symptom, its expected failing signal, determinism and execution time. Minimize the case, rank a small set of falsifiable hypotheses and instrument one prediction at a time. After a correction, prove the regression at the highest practical seam and remove temporary instrumentation.

If the failure cannot be reproduced safely, do not manufacture certainty. Preserve the evidence boundary, add bounded observability or compare authoritative states, and report which hypotheses remain unproven.

## Risk and output

Use R1/R2/R3 for operational impact and separate it from implementation complexity. Lead with verdict and highest-impact findings, then evidence, unknowns, risks, safe next actions and decisions required.

When the task concerns a possibly missing feature, version-dependent behavior or a proposed workaround, read [upstream and hypothesis reset](references/upstream-and-hypothesis-reset.md).
