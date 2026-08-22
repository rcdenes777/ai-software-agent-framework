---
name: domain-language-core
description: Establish and maintain a verified shared vocabulary for business-domain software work. Use when ambiguous, overloaded, or inconsistent domain terms affect requirements, code, data, tests, or handoffs; do not use merely to rename ordinary technical identifiers.
license: MIT
---

# Domain Language Core

Create a small shared vocabulary that reduces ambiguity across human decisions, documentation, code, database, tests and delegated work. A glossary records language; it does not invent business rules or outrank current authoritative sources.

## Establish authority and scope

Read current code, schema, tests, canonical domain documentation and explicit owner decisions using project source precedence. Identify the bounded context before defining a term; the same word may legitimately mean different things in different contexts.

If a canonical glossary or domain document already exists, update that artifact rather than creating a competing `CONTEXT.md`. If none exists, propose the smallest discoverable location and create it only within authorized documentation scope.

## Curate the vocabulary

For each term that materially changes interpretation, record only:

- canonical term and concise meaning;
- bounded context when necessary;
- important invariant or relationship already proven by an authoritative source;
- aliases to avoid when they cause real ambiguity.

Challenge overloaded names, synonyms for one concept and one word used for several concepts. Compare the proposed meaning against current code and business documentation. If they disagree, report the contradiction and invoke the appropriate human decision gate; never silently rewrite the domain to match whichever source was read first.

Keep the glossary compact. Exclude implementation trivia, temporary project state, task instructions, personal information, secrets and rules recoverable cheaply from current code.

## Preserve decisions without bureaucracy

Record an architectural decision only when it is hard to reverse, would be surprising without context and reflects a real trade-off. Keep the decision concise, link its evidence and owner approval, and do not use an ADR to legitimize an assumption.

## Carry language into execution

Use canonical terms consistently in plans, tickets, APIs, schema, code, tests and reports when doing so improves clarity. A manager should pass only the task-relevant vocabulary to an executor, along with the authoritative artifact, rather than loading the entire domain history.

Validate terminology changes by searching current artifacts for conflicting meanings and by checking affected requirements, contracts and tests. Report unresolved contradictions separately from accepted vocabulary.

Adapted from the domain-modeling discipline in `mattpocock/skills` (MIT), with this framework's source precedence and human-decision controls.
