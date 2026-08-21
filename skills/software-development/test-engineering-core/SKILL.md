---
name: test-engineering-core
description: Define or review a proportionate software-validation strategy that proves requirements and critical invariants. Use when acceptance, regression, data, security, migration, or test adequacy needs explicit analysis.
license: MIT
---

# Test Engineering Core

Determine what evidence would prove the requested behavior and expose likely failure. Do not implement tests unless that is explicitly part of the assignment.

## Build the strategy

1. Identify requirement, user-visible outcome and affected invariants.
2. Map likely failures and regression surface.
3. Select the smallest useful combination of static checks, unit, integration, end-to-end, migration/rehearsal, security, performance and manual validation.
4. Define environment, fixtures/data effects, safe commands and objective pass/fail criteria.
5. State what is not covered and why.

Scale to risk:

- R1: targeted check and relevant regression.
- R2: success/failure paths, integration boundaries and broader regression.
- R3: critical invariants, realistic environment, rollback/recovery where applicable and independent review for the risk domain.

Do not over-test simple changes. Do not under-test a small patch with critical impact. A green test is insufficient if it does not prove the requirement or uses the wrong assumptions.

## Review existing evidence

Confirm commands actually ran, results match claims, failures were not hidden, generated artifacts did not pollute the worktree and unexecuted tests are explicit. Cross-check planned behavior, implementation, tests and evidence.

Return risk profile, required test level, concrete plan, acceptance criteria, residual gaps and notes for the Executor/Manager.
