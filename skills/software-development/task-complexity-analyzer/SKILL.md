---
name: task-complexity-analyzer
description: Assess software-task complexity separately from operational risk to guide decomposition, planning depth, executor fit, and review effort. Use when task shape or uncertainty materially affects coordination.
license: MIT
---

# Task Complexity Analyzer

Complexity describes coordination and reasoning difficulty. Risk describes the consequence of error. Report both; never route a model from complexity alone.

## Complexity

- LOW: isolated, understood, few dependencies, straightforward validation.
- MEDIUM: bounded feature or several connected changes with known patterns.
- HIGH: multiple components, business rules, integration or significant uncertainty.
- VERY HIGH: architectural interaction, migration, concurrency or broad regression surface.
- ULTRA HIGH: project-wide change, many unknowns or major irreversible design decisions.

Consider scope, dependency graph, ambiguity, novelty, affected contracts, environment, test complexity and reversibility. File count alone is not decisive.

## Risk

- R1: localized and readily reversible.
- R2: meaningful functional/contract impact or several areas.
- R3: security, money, integrity/isolation of data, migration, concurrency, incompatible public contract or difficult reversal.

## Output

Return task, complexity with evidence, risk with evidence, unknowns, recommended decomposition/planning depth, validation intensity and executor requirements.

Recommend the cheapest executor already proven capable for this class. Escalate based on missing capability, evidence, failure or risk controls—not merely because the label is HIGH.
