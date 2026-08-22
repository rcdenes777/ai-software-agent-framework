# PostgreSQL migration and backfill validation recipes

Use these Drizzle/TypeScript recipes after the schema/service design is already approved. Treat stock/reservation names and module paths as examples to adapt, not universal schema requirements. Substitute only an explicitly authorized ephemeral database URL; never read repository `.env` values to discover a target.

## 1. Generate without loading repository secrets

For Drizzle projects whose config imports `dotenv/config`, redirect dotenv to an empty path and use a non-routable placeholder because generation is schema-only:

```bash
DOTENV_CONFIG_PATH=/dev/null \
DATABASE_URL=postgres://isolated:isolated@127.0.0.1:1/isolated \
npm run db:generate -- --name <migration_name>
```

Then read the generated SQL. In particular, a composite FK such as `(tenant_id, produto_id)` requires a matching unique key on the referenced columns **before** the FK statement executes. If generation puts the index later, reorder the SQL and keep the snapshot unchanged when the logical schema did not change.

## 2. Expose a hidden migrator error

When a CLI spinner exits nonzero without the database cause, invoke the framework migrator programmatically so the PostgreSQL code/query is printed:

```bash
DOTENV_CONFIG_PATH=/dev/null DATABASE_URL="$APPROVED_EPHEMERAL_URL" \
node --import tsx --input-type=module -e "
  import postgres from 'postgres';
  import { drizzle } from 'drizzle-orm/postgres-js';
  import { migrate } from 'drizzle-orm/postgres-js/migrator';
  const client = postgres(process.env.DATABASE_URL, { max: 1 });
  try { await migrate(drizzle(client), { migrationsFolder: './drizzle' }); }
  finally { await client.end(); }
"
```

A PostgreSQL `42830` on a composite FK means the referenced column set was not unique at the instant the FK was created. Fix statement order; do not weaken tenant isolation.

After a failed run, query only the approved ephemeral database and confirm the migration journal/tables. A transaction-safe failure should leave no partial migration entry or functional table from that migration.

## 3. Repeatability campaign

```bash
DOTENV_CONFIG_PATH=/dev/null DATABASE_URL="$APPROVED_EPHEMERAL_URL" npm run db:migrate
DOTENV_CONFIG_PATH=/dev/null DATABASE_URL="$APPROVED_EPHEMERAL_URL" npm run db:migrate
DOTENV_CONFIG_PATH=/dev/null DATABASE_URL="$APPROVED_EPHEMERAL_URL" npm run test:e2e:<package>
```

Then read back:

- migration count/latest timestamp;
- trigger enabled state;
- zero test tenants/domain rows after cleanup;
- zero unexpected permission catalog rows/grants.

Run generation once more with a new name; it must report no schema changes and create no extra migration.

## 4. Deterministic lock proof

A credible stock/reservation test needs both:

1. two concurrent operations that compete for more than the available balance, proving only one commits and the invariant remains true;
2. two multi-position batches whose request orders are reversed, proving canonical sorting makes both acquire `FOR UPDATE` locks in the same order.

Also test exact decimal boundaries, non-fractional units, rejected/non-stock conditions, tenant-crossing links, exact idempotent replay, and same-key/different-payload conflict.

## 5. Permission module and rollback proof

Avoid `access-foundations ↔ backfill` circular imports. Put codes, matrix, and pure profile lookup in a third module with no database import. Verify both entrypoints directly:

```bash
node --import tsx --input-type=module -e "await import('./src/auth/backfill-module.ts')"
node --import tsx --input-type=module -e "await import('./src/auth/access-foundations.ts')"
```

Wrap catalog + grant application in one transaction. Rollback must also be one transaction. Before deleting a global permission code, use `NOT EXISTS` (or equivalent) to retain it when any custom grant still references it. E2E should create a custom profile grant, prove rollback preserves both grant and catalog row, and prove a second rollback is idempotent.

## 6. Immutable history

If confirmed movement/event rows must never be rewritten, add a custom migration with a `BEFORE UPDATE OR DELETE` trigger and test both operations fail. Test cleanup may disable that exact trigger only inside a transaction-scoped disposable database that cannot be reused as staging or production, and must re-enable it in `finally`; otherwise clean through isolated fixtures instead.
