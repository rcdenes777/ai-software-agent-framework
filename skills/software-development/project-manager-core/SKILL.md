---
name: project-manager-core
description: Manage software work from discovery through scoped delegation, evidence-based review, human decisions, and durable handoff. Use for project leadership or multi-step implementation coordination; do not use for a simple isolated coding task that needs no management layer.
license: MIT
---

# Project Manager Core

Transform user intent into controlled, traceable execution. Keep product intent, architecture, scope, approvals, synthesis and final claims with the manager. Gerente and Executor are roles, not fixed models.

## Establish current truth

Before planning or resuming consequential work, confirm the current repository, branch, working tree, relevant documentation, configuration, database state and tests. Use this precedence:

1. current code, Git, databases, tests and effective configuration;
2. current canonical project documentation;
3. current task, handoff, status and explicit human decisions;
4. applicable governance and skills;
5. curated memory;
6. historical sessions/documents;
7. inference.

If a lower source could change an action on code, Git, data or infrastructure, verify it in a higher source.

## Manage proportionally

Clarify objective, success, scope, constraints, unknowns and decisions. Separate complexity from risk:

- complexity controls discovery depth, decomposition and coordination;
- risk controls approvals, validation intensity, rollback and independent review.

Use R1/R2/R3 from project governance. Explain human checkpoints in practical language: what changes, why, risks, reversibility, what was and was not verified and what decision is needed.

## Delegate deliberately

Delegate independent, bounded and verifiable work when it improves time, cost, context isolation or confidence. Do not force delegation for trivial or tightly sequential work.

Before delegating, apply a context-and-coupling gate:

- If the task fits in the manager's context with safe headroom and decisions are tightly coupled, prefer one continuous execution thread.
- For low coupling (independent research, read-only inventory, isolated verification), parallel delegation is appropriate.
- For moderate coupling, split into a few cohesive blocks with explicit interfaces, ownership and acceptance criteria.
- For high coupling (shared mutable state, chained decisions, one schema/migration or overlapping files), keep one writer responsible and execute sequentially.
- If a large dependent task does not fit, preserve continuity through durable artifacts and sequential handoffs. If no clean boundary exists, reduce or clarify scope before delegating.

Subagents are a tool for context budget, speed or independent confidence, not a utilization target. Never create one worker per small task merely to maximize delegation.

Choose the cheapest executor already proven capable for the task class. Complexity alone does not justify a more expensive model. Escalate from evidence: persistent low confidence, repeated failure after a changed strategy, critical risk, contradiction, missing capability/context or high cost of reversal.

Every delegated task must define objective, necessary context, directory, included/excluded scope, read/write boundaries, allowed/prohibited commands, risk, acceptance criteria, validation, return format and stop/escalation conditions. Use `executor-handoff-core`.

## Review independently

Executor output is evidence and autorrelato, never approval. Verify the 3–5 highest-impact claims against current authoritative sources, scaled down when fewer claims exist. Ask both:

```text
Is what the Executor reported correct?
What important issue may the Executor have missed?
```

Check scope, diff, tests, assumptions, business decisions, security/data/contract impact, regressions and unverified areas. Confirm actual model/provider/status through runtime metadata when that fact matters; never rely on model self-identification.

If a delegated response is truncated, retrieve the complete durable result before deciding. Redirect a live child early when it leaves scope; do not wait for a predictably invalid result.

Decide one outcome: approve, request correction, escalate review/execution, or request a human decision. A completion claim requires direct final-state verification by the manager.

## Preserve continuity

Keep roadmap (direction) separate from state handoff (current position). Record decisions and authorization changes without silently rewriting the original task. Load historical material only when a current question requires it.

For repeated debugging failure or an apparent missing upstream capability, use [upstream and hypothesis reset](../project-audit-core/references/upstream-and-hypothesis-reset.md).
