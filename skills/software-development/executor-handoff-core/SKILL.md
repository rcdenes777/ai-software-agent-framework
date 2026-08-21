---
name: executor-handoff-core
description: Turn an approved software objective into a bounded, executable assignment with explicit permissions, tests, evidence, return format, and escalation conditions. Use immediately before delegating implementation, audit, or verification work.
license: MIT
---

# Executor Handoff Core

Create an assignment that an Executor can complete without inheriting hidden conversation context or inventing product decisions.

## Required assignment

Include only fields relevant to the task, but never omit a material boundary:

```text
OBJECTIVE
NECESSARY CONTEXT
WORKING DIRECTORY
IN SCOPE / OUT OF SCOPE
READ BOUNDARY
WRITE AUTHORITY: NONE | RESTRICTED | BROAD_EXPLICIT
ALLOWED / PROHIBITED OPERATIONS
RISK: R1 | R2 | R3, with reason
ACCEPTANCE CRITERIA
VALIDATION AND TEST LIMITS
RETURN FORMAT
STOP / ESCALATION CONDITIONS
```

Avoid a vague “free” write category. Broad access must be explicit. For read-only work, define how before/after integrity will be checked without assuming a clean worktree.

Give enough project context to understand the task, not the entire history. State which current files or documents are authoritative. Preserve unrelated user changes and sensitive material.

## Executor contract

The Executor must stay within scope, inspect current sources, make the smallest sufficient change, run proportionate validation and never silently decide product, architecture or permission expansion.

After 2–3 technically similar failed attempts without new understanding, stop varying the same solution. List facts and tested hypotheses, run the smallest useful experiment and return a block if uncertainty remains.

## Return contract

Ask for a compact, verdict-first response:

1. verdict/status;
2. critical findings;
3. changes and paths;
4. evidence (`file:line`, command/result, diff or equivalent);
5. tests run, results and tests not run;
6. risks and ambiguities;
7. remaining work;
8. confidence and escalation reason when uncertainty matters.

Use markers only when they improve clarity: `[FACT]`, `[HYPOTHESIS]`, `[RISK]`, `[PENDING DECISION]`, `[RECOMMENDATION]`, `[BLOCKED]`.

Do not impose a rigid response length or schema when narrative evidence is more useful. Do not require model-specific names such as Pro/Flash in a reusable handoff.
