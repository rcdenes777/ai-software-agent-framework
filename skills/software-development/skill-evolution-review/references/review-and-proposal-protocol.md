# Review and proposal protocol

## Inputs

Use only the task IDs and paths named in the review assignment. Read the minimum current evidence needed to decide whether a lesson is reusable. If evidence is unavailable after a bounded check, mark the candidate `UNPROVEN`; do not reconstruct it from memory.

## Sanitization

Before writing, remove:

- prompts, conversational phrasing and model self-reports;
- names, personal data, credentials and authentication material;
- raw logs, full stack traces and copied database contents;
- project names, phase numbers, task IDs, commits and temporary paths;
- prices, quotas and transient model/provider behavior;
- recommendations that current upstream code or documentation contradicts.

Retain only the generalized trigger, invariant, failure mode, safe procedure, validation and meaningful exception.

## Report

Write the requested Markdown report with:

```text
VERDICT: NO_CHANGE | PATCH_READY | BLOCKED
BATCH: supplied batch identifier
EVIDENCE CHECKED: paths, tests or database invariants — no raw content
CANDIDATES: classification and one-line reason
AFFECTED SKILLS: names or none
VALIDATION: commands/results and what remains unverified
RISKS: duplication, overfitting, compatibility or missing evidence
```

Keep it compact. Do not paste task summaries.

## Patch

When the verdict is `PATCH_READY`, write a standard unified Git patch to the requested `.patch` path.

- Only add or modify paths under `skills/software-development/`.
- Do not delete or rename files.
- Do not modify framework governance, profiles, memories, configuration or repositories outside the framework.
- Make the patch apply cleanly to the current canonical framework.
- Prefer one cohesive change; split unrelated lessons into separate later reviews.

When the verdict is `NO_CHANGE` or `BLOCKED`, do not create an empty or speculative patch.

## Validation and handoff

Validate frontmatter, linked references, duplication, path scope and relevant technical invariants. Run a credential-pattern scan on the staged outputs. Then request Kanban review and return only verdict, output paths, evidence categories, residual risk and any human decision needed.
