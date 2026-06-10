---
name: migrations-workflow
description: "Manage the full Drizzle ORM migration lifecycle — generate, review, apply, rollback, and sync with Supabase. Covers the safe workflow for schema changes, CI migration checks, and multi-environment migration strategy. Use when making any database schema change."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Manage database migrations: $ARGUMENTS

$ARGUMENTS can include:
- "generate" — generate a new migration from schema changes
- "apply" — apply pending migrations to the target environment
- "rollback" — roll back the last migration
- "status" — show applied vs pending migrations
- "sync" — align local schema with live Supabase DB (audit only, no changes)
- "new <description>" — generate a named migration (e.g. "new add-user-profiles")
- Empty — interactive: show status, then ask what to do

---

## Before Starting

1. Read `src/lib/database/schema.ts` — current schema definition
2. Check `drizzle/` or `migrations/` directory for existing migration files
3. Read `drizzle.config.ts` if it exists
4. Use Supabase MCP to check live DB state: `mcp__supabase__list_tables`
5. Run `pnpm db:check` to see current layer 1 alignment status

---

## Architecture

```
drizzle/
  migrations/
    0001_initial.sql         ← Applied migration (committed, never edited)
    0002_add_profiles.sql    ← Applied migration
    0003_pending.sql         ← Generated, not yet applied
  meta/
    _journal.json            ← Migration history (managed by Drizzle Kit)

drizzle.config.ts            ← Drizzle Kit config
src/lib/database/
  schema.ts                  ← Single source of truth — edit this, then generate
  db.ts                      ← Drizzle client
```

---

## Drizzle Config

Ensure `drizzle.config.ts` exists:

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/lib/database/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  // Only migrate tables defined in schema (don't touch others)
  tablesFilter: ["!_prisma_*", "!schema_migrations"],
  verbose: true,
  strict: true,
});
```

---

## The Safe Workflow — Schema Changes

Always follow this order. Never skip steps.

### Step 1 — Edit the schema (Source of Truth)

Edit `src/lib/database/schema.ts` only. Examples:

```typescript
// Adding a column:
export const profiles = pgTable("profiles", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id").notNull().unique(),
  bio: text("bio"),                            // ← new column
  avatarUrl: text("avatar_url"),               // ← new column
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Adding an index:
export const profilesUserIdx = index("profiles_user_idx")
  .on(profiles.userId);

// Adding a new table:
export const userPreferences = pgTable("user_preferences", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id").references(() => profiles.userId, { onDelete: "cascade" }),
  theme: text("theme").default("system"),
  emailNotifications: boolean("email_notifications").default(true),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

### Step 2 — Generate the migration

```bash
pnpm drizzle:gen
# or with description:
pnpm drizzle-kit generate --name "add-user-profiles"
```

This creates `drizzle/migrations/XXXX_add-user-profiles.sql`. **Review this file before applying.**

### Step 3 — Review the generated SQL

```bash
cat drizzle/migrations/$(ls drizzle/migrations | tail -1)
```

Check for:
- Expected `ALTER TABLE ADD COLUMN` or `CREATE TABLE` statements
- No unexpected `DROP` statements
- Correct data types and constraints
- Indexes and foreign keys as intended

**Never apply a migration you haven't read.**

### Step 4 — Apply to local/dev

```bash
pnpm drizzle:push
```

`drizzle:push` applies schema directly (for dev iteration — no migration files needed). Use this when rapidly iterating on schema design.

### Step 5 — Apply via migrations (staging/prod)

```bash
pnpm drizzle-kit migrate
```

This runs pending `.sql` files in order against `DATABASE_URL`.

### Step 6 — Verify alignment

```bash
pnpm db:check
```

Should report `LOCKED` — schema matches live DB.

---

## Rollback Strategy

Drizzle Kit does not have built-in rollback. To roll back a migration:

### Option A — Down migration (recommended for destructive changes)

Before applying a destructive migration, write a manual down migration:

```sql
-- drizzle/migrations/0003_add-column.down.sql  (manual, not auto-generated)
ALTER TABLE profiles DROP COLUMN IF EXISTS bio;
ALTER TABLE profiles DROP COLUMN IF EXISTS avatar_url;
```

Apply the down migration manually if rollback is needed:
```bash
psql $DATABASE_URL -f drizzle/migrations/0003_add-column.down.sql
```

Then update `drizzle/meta/_journal.json` to remove the entry.

### Option B — Additive-only changes (safest)

Prefer additive schema changes (new columns, new tables) over destructive ones (DROP, ALTER type). Additive changes are easily reversible — just remove the column in a subsequent migration.

**Never drop production columns without a deprecation period.**

---

## Multi-Environment Strategy

### Development
```bash
# Fast iteration — push schema directly (no migration files)
pnpm drizzle:push
```

### Staging (Supabase branch)
```bash
# Create a Supabase branch for testing migrations
# Use Supabase MCP: mcp__supabase__create_branch
# Apply migrations to branch
DATABASE_URL=<branch-connection-string> pnpm drizzle-kit migrate
```

### Production
1. Migrations are applied via CI (never manually in prod)
2. Add to `package.json` prebuild: `pnpm drizzle-kit migrate` (or keep manual)
3. Always back up production DB before running migrations

---

## Adding to CI

Add a migration check to `.github/workflows/ci.yml`:

```yaml
- name: Check pending migrations
  run: |
    # Fail CI if there are uncommitted schema changes without a migration
    pnpm drizzle-kit check
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Or add a `prebuild` script:
```json
{
  "scripts": {
    "prebuild": "pnpm drizzle-kit migrate"
  }
}
```

---

## Common Operations

### List all tables in live DB
Use Supabase MCP: `mcp__supabase__list_tables` with `schema: "public"`

### Check migration status
```bash
pnpm drizzle-kit status
```

### Generate types after schema change
```bash
# Re-generate TypeScript types if using Supabase generated types
pnpm supabase gen types typescript --project-id <id> > src/lib/database/types.ts

# Or regenerate Drizzle layer 2 schemas
pnpm generate:schemas
```

### Reset a dev database
```bash
# Drop and recreate (dev only — DESTRUCTIVE)
pnpm drizzle-kit drop
pnpm drizzle:push
# Or run seed script if available
pnpm db:seed
```

---

## Naming Conventions

Migration names should describe the change:

| Change | Migration name |
|---|---|
| Add table | `0010_create-user-preferences` |
| Add column | `0011_add-bio-to-profiles` |
| Drop column | `0012_remove-deprecated-legacy-field` |
| Add index | `0013_index-articles-slug` |
| Rename table | `0014_rename-posts-to-articles` |
| Backfill data | `0015_backfill-article-slugs` |

---

## Verify

1. `pnpm db:check` → `LOCKED` — schema aligned with DB
2. `pnpm typecheck` — no TS errors after schema change
3. `pnpm generate:schemas` → regenerate Zod contracts
4. `pnpm validate:all` — all 6 layers pass after schema change

---

## Anti-Patterns

- NEVER edit migration `.sql` files after they've been applied — generate a new migration instead
- NEVER use `drizzle:push` in production — use migration files so changes are tracked
- NEVER `DROP COLUMN` or `DROP TABLE` without a deprecation period in production
- NEVER commit schema changes without a corresponding migration file
- NEVER modify `drizzle/meta/_journal.json` manually unless you know exactly what you're doing
- NEVER skip `pnpm db:check` after applying migrations — always verify alignment
