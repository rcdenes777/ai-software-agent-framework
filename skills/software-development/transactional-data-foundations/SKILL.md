---
name: transactional-data-foundations
description: Use when building PostgreSQL transactional data foundations.
license: MIT
---

# Transactional Data Foundations

Build the smallest auditable PostgreSQL foundation that proves data integrity before routes, UI, or broad domain expansion. Use for additive schema, tenant isolation, exact quantities/money, concurrency, idempotency, immutable history, migrations, permission backfills, and rollback validation.

## Control scope before writing

1. Confirm the authorized package, database boundary, branch/worktree, write paths, prohibited systems, and approved owner decisions.
2. Separate the minimum foundation from future domain entities. A foundation usually needs only the master record required by the invariant, operation/idempotency record, current position/projection, and immutable event/movement record.
3. Treat “freeze the design”, “minimum only”, or “do not expand further” as an immediate contraction of new work. Finish the smallest end-to-end slice and list deferred entities explicitly. Propose removal of expansion already present; remove it only when that cleanup is within explicit write authority.
4. Do not turn a foundation package into routes, screens, purchases, finance, full workflow state machines, or speculative configuration.

## Encode invariants at multiple layers

Use complementary controls rather than trusting one layer:

- exact PostgreSQL types such as `numeric(p,s)` and string serialization at the service/API boundary;
- tenant-leading unique indexes and composite foreign keys where a business link must remain tenant-local, or an equivalent database constraint that proves the same boundary;
- `CHECK` constraints for non-negativity, reserved ≤ physical, valid conditions, and coherent states;
- service validation for product/unit policy and tenant ownership;
- transaction-scoped audit/event writes;
- an immutable trigger for confirmed ledger/history tables when updates/deletes must never be normal operations.

A projection or balance is never the only history. Mutations must create a durable operation/event record in the same transaction.

## Concurrency and deterministic locking

1. Canonicalize and validate all decimal strings without binary floating point.
2. Reject duplicate position keys inside one operation.
3. Sort keys deterministically (for example product UUID then enum condition) before inserting missing rows or taking locks.
4. Lock every affected row using the same database `ORDER BY ... FOR UPDATE` order used by all callers.
5. Update with conditional predicates that reassert the invariants (`new physical >= 0`, `new reserved >= 0`, `new reserved <= new physical`). Treat zero affected rows as an invariant conflict.
6. Persist movement snapshots, idempotency result, and audit in the same transaction.
7. Test two batches that name the same positions in reverse request order; both must follow the canonical lock order without deadlock.

## Idempotency

Scope keys by tenant with a unique constraint. Store a canonical payload hash and the committed result.

- First call inserts the operation and completes all effects atomically.
- Exact replay returns the stored result without a second movement.
- Same key with different canonical content is a conflict.
- When cross-class key reuse must conflict, keep one shared uniqueness boundary such as `(tenant, key)` and include the operation class/discriminator in the canonical hash. Uniqueness on `(tenant, class, key)` defines a different contract because it permits reuse across classes.
- Handle concurrent first use deliberately: after a competing unique insert resolves, read the committed operation and return its stored result for an exact replay or a conflict for different canonical content. Under snapshot isolation that cannot observe the winner, roll back and restart the transaction with a bounded retry before reading. Do not leak a raw uniqueness error or observe an incomplete operation.
- Validation or concurrency failure rolls back the operation row too.
- A committed operation without a result is an invariant error, not permission to rerun effects.

## Additive migration workflow

1. Generate the migration without reading repository secrets; direct dotenv to an empty path and provide a non-routable placeholder URL when generation does not need a connection.
2. Inspect generated SQL directly. Generation success is not migration proof.
3. For composite foreign keys, ensure the referenced composite unique index is created **before** the `ALTER TABLE ... FOREIGN KEY`; some generators emit an invalid order.
4. Apply from an empty, explicitly authorized ephemeral PostgreSQL database.
5. If application fails, inspect the real database error and read the migration journal/tables to prove transaction rollback before editing.
6. Apply again after correction, then apply a second time to prove journal idempotency.
7. Run schema-generation consistency; it must report no unplanned delta.
8. Read back migration count, trigger state, and test-data counts before declaring success.

Never use `db:push`, destructive cleanup, a production database, or an unverified connection target as a migration shortcut. A controlled staging rehearsal is acceptable only when explicitly authorized and backed by a recovery plan.

## Permission catalogs and backfills

Keep pure permission constants/matrices in a module that does not import database services. Both provisioning and backfill import that pure module; this prevents circular ESM initialization.

- Test direct import through each public entrypoint, not only the import order used by unit tests.
- Calculate and apply catalog rows plus grants inside one transaction.
- Make dry-run use the same calculation without writes.
- Make rollback atomic and limited to the introduced codes/profiles.
- Preserve custom grants: do not delete a global catalog row while any remaining grant references it.
- Test new-tenant provisioning, dry-run, application, replay, rollback, second rollback, and a custom profile grant.

## Authorization-safe responses

Apply authorization to the response projection as well as to the command. Do not return an internal service or database object directly when it can contain cost, identity, tenant, audit, or other restricted fields.

- Shape mutation and read responses through the same effective role policy.
- Verify an authorized role receives the sensitive field and an unauthorized role does not receive the field at all; a null or masked value is not equivalent when the contract requires omission.
- Cover mutation responses, idempotent replays, and subsequent reads. A secure GET does not compensate for a leaking POST response.
- Run this proof through the real authentication, serialization, and PostgreSQL path after a correction; unit tests and typecheck alone do not prove confidentiality.

## Validation campaign

For integrity-critical work (R3 when the project uses that scale), require:

- static/unit tests for decimal normalization, unit rules, condition rules, delta mapping, and lock sorting;
- PostgreSQL E2E for constraints, tenant-crossing attempts, authorized/unauthorized response projection, exact replay, conflicting replay including cross-class key reuse, concurrent contention, reverse-order batches, immutable history, backfill, and rollback;
- typecheck and build;
- migration from empty plus repeated migration;
- final database readback proving test cleanup;
- direct review of schema, generated SQL, service transaction, tests, Git diff, and staging state.

Record every failed first attempt that materially changed the fix, but distinguish product failure from a faulty test expectation. Never hide a failed migration or test behind the final green run.

## Stop conditions

Stop and escalate if the work needs a real credential/database, destructive action, a broader business decision, an unapproved entity/workflow, or a lock/invariant strategy not authorized by the owner.

See `references/postgresql-migration-backfill-validation.md` for concrete diagnostic and verification recipes.
