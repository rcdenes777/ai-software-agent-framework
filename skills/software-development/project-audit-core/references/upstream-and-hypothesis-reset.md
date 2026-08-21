# Upstream investigation and hypothesis reset

Use this procedure before creating a Bridge, wrapper, compatibility layer or structural workaround for an apparent limitation in software that may have changed.

## Prove the current capability

1. Convert the symptom into one precise technical question.
2. Check installed version, effective configuration and relevant local code.
3. Search canonical documentation, issues, pull requests, commits, releases, examples and upstream tests.
4. Distinguish discussion, proposed change, merged implementation and released availability.
5. Identify the exact configuration or syntax.
6. Run the smallest reproducible local test.
7. Decide from objective evidence such as code, test output, database, log or manifest.

Use a workaround only when evidence shows that the capability is absent from the usable version, does not meet the requirement, has a confirmed bug, or creates incompatible risk. Record that evidence and a removal condition where practical.

## Reset hypotheses

Activate when logs and attempts grow without proportional understanding, solutions keep varying the same premise, complexity rises, or documentation contradicts behavior.

```text
STOP
→ list verified facts
→ separate/discard hypotheses temporarily
→ ignore existing workarounds as explanations
→ ask one testable question
→ recheck upstream/version/configuration
→ run a minimal test
→ reintroduce only useful history
```

An Executor applies this locally to its assignment and must not redefine global architecture, requirements, scope or permissions. If still blocked, return verified facts, hypotheses tested/discarded, minimal test/result, remaining uncertainty, missing context and a recommendation.

The Manager must not simply resend the same task. Add context, change the hypothesis/test, reduce the scope or escalate for an evidenced reason.
