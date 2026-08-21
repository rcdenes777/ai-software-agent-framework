---
name: decision-gate-core
description: Identify and present owner decisions before consequential software actions. Use when product, architecture, security, data, cost, destructive operations, external publication, or hard-to-reverse choices exceed existing authorization.
license: MIT
---

# Decision Gate Core

Do not decide on behalf of the owner or treat a recommendation as approval.

## Classify

- BLOCKING: work cannot safely continue without a decision or new authority.
- IMPORTANT: independent work may continue, but the affected branch must wait.
- INFORMATIVE: ordinary implementation detail already within approved scope.

Use a gate for product/business rules, high-impact architecture or technology changes, security/privacy policy, data migration/integrity, destructive or difficult-to-reverse operations, material cost, incompatible public contracts, deployment/publication and scope expansion.

Do not create approval bureaucracy for reversible internal details already authorized.

## Present for a non-programmer

Record:

```text
DECISION ID AND QUESTION
WHY IT EXISTS
PRACTICAL EFFECT
RISKS AND REVERSIBILITY
OPTIONS AND TRADE-OFFS
TECHNICAL RECOMMENDATION (not approval)
WHAT WAS / WAS NOT VERIFIED
WHAT THE OWNER MUST ANSWER
WORK THAT CAN CONTINUE INDEPENDENTLY
```

After the owner decides, record the decision, date/context and resulting authorization without rewriting the original task silently.
