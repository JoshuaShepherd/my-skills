---
name: type-safety-chain
description: "Implement the full six-layer type safety chain in a new project — DB → Drizzle schema → Zod schemas → services → API routes → React hooks. Installs dependencies, writes all infrastructure files, generates all layers from the live database, and validates each layer bottom-up. Use for new projects that need this architecture from scratch, or to verify and repair an existing chain. Supabase MCP required for DB verification."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, mcp__supabase__list_tables, mcp__supabase__execute_sql, mcp__supabase__get_project, mcp__supabase__list_projects, mcp__supabase__generate_typescript_types
---

Implement the full type safety chain for: $ARGUMENTS

$ARGUMENTS should include:
- The Supabase project ID to connect to (e.g. `vhaiiiykcukrlyvwlgip`), OR "list" to browse projects
- Optionally: "verify-only" to audit an existing chain without writing files
- Optionally: "schema-only" to only generate the Drizzle schema (Layer 1) and stop
- Optionally: "generate-all" to regenerate all layers after schema is already in place
- Empty — ask the user for the Supabase project and target directory

---

## Purpose

This skill bootstraps or verifies the complete **six-layer type safety chain** used in this platform:

```
Layer 1: Drizzle Schema      src/lib/database/schema.ts          (source of truth)
Layer 2: Zod Schemas         src/lib/schemas/index.ts            (runtime contracts)
Layer 3: Services            src/lib/services/simplified/        (business logic)
Layer 4: API Routes          src/app/api/simplified/             (HTTP endpoints)
Layer 5: React Hooks         src/hooks/simplified/               (data fetching)
Layer 6: UI Components       src/components/simplified/          (presentation — wired externally)
```

Types flow **downstream only**. Never import a higher layer into a lower one. This skill implements Layers 1–5 and validates 1–6 when Layer 6 exists.

---

## Phase 0 — Identify the Target

Before doing anything:

1. If `$ARGUMENTS` is empty or "list", call `mcp__supabase__list_projects` and show available projects. Ask the user which project to target and which local directory is the project root.

2. If a project ID is given, call `mcp__supabase__get_project` to confirm the project is accessible and note the project URL and region.

3. Ask the user: **"Is this a new project (full bootstrap) or an existing project (verify/repair)?"**
   - **New project** → proceed through all phases
   - **Existing project** → skip Phase 2, go directly to Phase 4 (verify the existing chain)
   - **verify-only mode** → read existing files, call MCP, report gaps, no writes

4. Ask the user: **"Which reference project should I compare the chain structure against?"** The canonical reference is `alan-hirsch`. If the user names a project, note it. The reference is used only to verify the chain shape — not to copy code verbatim.

5. Confirm the target working directory. All paths in this skill are relative to that root.

---

## Phase 1 — Verify Database via Supabase MCP

Use `mcp__supabase__execute_sql` on the target project to count and list tables:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

Record the full table list. This is the **ground truth** the Drizzle schema must match.

Also run:

```sql
SELECT
  table_name,
  column_name,
  data_type,
  udt_name,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position
LIMIT 500;
```

This gives column-level insight for verifying schema accuracy.

Report to the user:
- Total table count found in DB
- First 20 table names (preview)
- Any tables that exist in the DB but not in the local schema (if schema.ts already exists)
- Any tables in the local schema that don't exist in the DB

---

## Phase 2 — Install Dependencies (New Projects Only)

For a new project, check `package.json` to see if these packages are already installed. Install any that are missing:

### Required packages

```bash
# Core DB + ORM
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit drizzle-zod

# Validation
pnpm add zod

# React Query (data fetching for hooks)
pnpm add @tanstack/react-query

# Dev tools
pnpm add -D tsx dotenv
```

Check TypeScript config — the project needs `"moduleResolution": "bundler"` or `"node16"` for path aliases to work. If `tsconfig.json` doesn't have `"@/*"` path aliases configured, add them:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## Phase 3 — Write Infrastructure Files (New Projects Only)

Write these files only if they don't already exist. Never overwrite hand-written files — ask before overwriting.

### 3a. Drizzle config

**`drizzle.config.ts`** (project root):

```typescript
import { config as dotenvConfig } from "dotenv";
import { defineConfig } from "drizzle-kit";

dotenvConfig({ path: ".env" });
dotenvConfig({ path: ".env.local" });

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not set");
}

export default defineConfig({
  schema: "./src/lib/database/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL,
  },
});
```

### 3b. Database client

**`src/lib/database/client.ts`**:

```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not set");
}

const queryClient = postgres(process.env.DATABASE_URL);
export const db = drizzle(queryClient, { schema });
```

### 3c. Tenant util

**`src/lib/tenant.ts`**:

```typescript
/**
 * Tenant context: one organization per deployment via TENANT_ORG_ID.
 * Services use this to scope queries by organization_id.
 */
export function getTenantOrgId(): string | null {
  const id = process.env.TENANT_ORG_ID;
  return id ?? null;
}
```

### 3d. Query utils (for hooks)

**`src/hooks/simplified/query-utils.ts`**:

```typescript
/**
 * Shared query utilities for generated hooks.
 */
export function buildQueryString(filters?: Record<string, unknown>): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value !== undefined && value !== null) {
      params.set(key, String(value));
    }
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}
```

### 3e. Base service

**`src/lib/services/simplified/base.service.ts`** — write the full SimplifiedService base class:

```typescript
import { eq, and, asc, desc, type SQL } from "drizzle-orm";
import type { PgTable } from "drizzle-orm/pg-core";
import type { z } from "zod";
import { db } from "@/lib/database/client";
import { getTenantOrgId } from "@/lib/tenant";

// ---- Result<T> Pattern ----

export type Ok<T> = { success: true; data: T };
export type Err = { success: false; error: { code: string; message: string } };
export type Result<T> = Ok<T> | Err;

// ---- Helpers ----

function toSnakeCase(s: string): string {
  return s.replace(/[A-Z]/g, (ch) => `_${ch.toLowerCase()}`);
}

const META_KEYS = new Set(["limit", "offset", "search"]);

// ---- SimplifiedService Base Class ----

export abstract class SimplifiedService<
  TTable extends PgTable,
  TSelect,
  TInsert,
  TUpdate,
  TFilters extends { limit?: number; offset?: number },
> {
  protected table: TTable;
  protected selectSchema: z.ZodType<TSelect>;
  protected insertSchema: z.ZodType<TInsert>;
  protected updateSchema: z.ZodType<TUpdate>;
  protected filtersSchema: z.ZodType<TFilters>;

  constructor(
    table: TTable,
    selectSchema: z.ZodType<TSelect>,
    insertSchema: z.ZodType<TInsert>,
    updateSchema: z.ZodType<TUpdate>,
    filtersSchema: z.ZodType<TFilters>,
  ) {
    this.table = table;
    this.selectSchema = selectSchema;
    this.insertSchema = insertSchema;
    this.updateSchema = updateSchema;
    this.filtersSchema = filtersSchema;
  }

  protected ok<T>(data: T): Ok<T> {
    return { success: true, data };
  }

  protected fail(code: string, message: string): Err {
    return { success: false, error: { code, message } };
  }

  protected buildFilterConditions(filters?: TFilters): SQL[] {
    const conditions: SQL[] = [];
    if (!filters) return conditions;
    const tableAny = this.table as any;
    for (const [key, value] of Object.entries(filters)) {
      if (META_KEYS.has(key) || value === undefined || value === null) continue;
      const col = tableAny[key] ?? tableAny[toSnakeCase(key)];
      if (col) conditions.push(eq(col, value));
    }
    return conditions;
  }

  async list(filters?: TFilters): Promise<Result<TSelect[]>> {
    try {
      const tableAny = this.table as any;
      const conditions = this.buildFilterConditions(filters);
      if ("organization_id" in tableAny && tableAny.organization_id != null) {
        const tenantOrgId = getTenantOrgId();
        if (!tenantOrgId) {
          return this.fail("TENANT_NOT_CONFIGURED", "TENANT_ORG_ID is required for this resource.");
        }
        conditions.unshift(eq(tableAny.organization_id, tenantOrgId));
      }
      const limit = filters?.limit ?? 50;
      const offset = filters?.offset ?? 0;
      const where = conditions.length > 0 ? and(...conditions) : undefined;
      const rows = await (db as any).select().from(this.table).where(where).limit(limit).offset(offset);
      return this.ok(rows as TSelect[]);
    } catch (e: any) {
      return this.fail("LIST_ERROR", e.message);
    }
  }

  async getById(id: string): Promise<Result<TSelect | null>> {
    try {
      const tableAny = this.table as any;
      if (!tableAny.id) return this.fail("NO_ID_COLUMN", "Table does not have an id column");
      if ("organization_id" in tableAny && tableAny.organization_id != null) {
        const tenantOrgId = getTenantOrgId();
        if (!tenantOrgId) return this.fail("TENANT_NOT_CONFIGURED", "TENANT_ORG_ID is required.");
        const rows = await (db as any).select().from(this.table)
          .where(and(eq(tableAny.id, id), eq(tableAny.organization_id, tenantOrgId))).limit(1);
        return this.ok((rows[0] as TSelect) ?? null);
      }
      const rows = await (db as any).select().from(this.table).where(eq(tableAny.id, id)).limit(1);
      return this.ok((rows[0] as TSelect) ?? null);
    } catch (e: any) {
      return this.fail("GET_ERROR", e.message);
    }
  }

  async create(data: TInsert): Promise<Result<TSelect>> {
    try {
      const parsed = this.insertSchema.parse(data);
      const rows = await (db as any).insert(this.table).values(parsed).returning();
      return this.ok(rows[0] as TSelect);
    } catch (e: any) {
      if (e.name === "ZodError") return this.fail("VALIDATION_ERROR", e.message);
      return this.fail("CREATE_ERROR", e.message);
    }
  }

  async update(id: string, data: TUpdate): Promise<Result<TSelect>> {
    try {
      const existing = await this.getById(id);
      if (!existing.success) return existing;
      if (existing.data === null) return this.fail("NOT_FOUND", `Record with id ${id} not found`);
      const parsed = this.updateSchema.parse(data);
      const tableAny = this.table as any;
      if (!tableAny.id) return this.fail("NO_ID_COLUMN", "Table does not have an id column");
      const rows = await (db as any).update(this.table).set(parsed).where(eq(tableAny.id, id)).returning();
      if (rows.length === 0) return this.fail("NOT_FOUND", `Record with id ${id} not found`);
      return this.ok(rows[0] as TSelect);
    } catch (e: any) {
      if (e.name === "ZodError") return this.fail("VALIDATION_ERROR", e.message);
      return this.fail("UPDATE_ERROR", e.message);
    }
  }

  async delete(id: string): Promise<Result<{ deleted: boolean }>> {
    try {
      const existing = await this.getById(id);
      if (!existing.success) return existing;
      if (existing.data === null) return this.fail("NOT_FOUND", `Record with id ${id} not found`);
      const tableAny = this.table as any;
      if (!tableAny.id) return this.fail("NO_ID_COLUMN", "Table does not have an id column");
      const rows = await (db as any).delete(this.table).where(eq(tableAny.id, id)).returning();
      if (rows.length === 0) return this.fail("NOT_FOUND", `Record with id ${id} not found`);
      return this.ok({ deleted: true });
    } catch (e: any) {
      return this.fail("DELETE_ERROR", e.message);
    }
  }

  async getBySlug(slug: string): Promise<Result<TSelect | null>> {
    try {
      const tableAny = this.table as any;
      if (!tableAny.slug) return this.fail("NO_SLUG_COLUMN", "Table does not have a slug column");
      if ("organization_id" in tableAny && tableAny.organization_id != null) {
        const tenantOrgId = getTenantOrgId();
        if (!tenantOrgId) return this.fail("TENANT_NOT_CONFIGURED", "TENANT_ORG_ID is required.");
        const rows = await (db as any).select().from(this.table)
          .where(and(eq(tableAny.slug, slug), eq(tableAny.organization_id, tenantOrgId))).limit(1);
        return this.ok((rows[0] as TSelect) ?? null);
      }
      const rows = await (db as any).select().from(this.table).where(eq(tableAny.slug, slug)).limit(1);
      return this.ok((rows[0] as TSelect) ?? null);
    } catch (e: any) {
      return this.fail("GET_BY_SLUG_ERROR", e.message);
    }
  }

  async listByColumn(
    column: string,
    value: unknown,
    orderByColumn?: string,
    direction: "asc" | "desc" = "asc",
  ): Promise<Result<TSelect[]>> {
    try {
      const tableAny = this.table as any;
      if (!tableAny[column]) return this.fail("NO_COLUMN", `Table does not have column: ${column}`);
      let query = (db as any).select().from(this.table).where(eq(tableAny[column], value));
      if (orderByColumn && tableAny[orderByColumn]) {
        query = query.orderBy((direction === "desc" ? desc : asc)(tableAny[orderByColumn]));
      }
      const rows = await query;
      return this.ok(rows as TSelect[]);
    } catch (e: any) {
      return this.fail("LIST_BY_COLUMN_ERROR", e.message);
    }
  }
}
```

### 3f. Generation scripts

Write each script to `scripts/`. These read `schema.ts` and generate the upper layers. Copy each script exactly as shown below — do not alter the logic.

**`scripts/generate-schema.ts`** — introspects the live DB and writes `src/lib/database/schema.ts`. Full file contents: read from the reference project at `scripts/generate-schema.ts`. This script handles:
- Connecting to `DATABASE_URL` (from `.env.local`)
- Fetching tables, columns, foreign keys, unique constraints
- Topological sorting by FK dependencies
- Mapping PostgreSQL types to Drizzle column builders
- Using `id()`, `createdAt()`, `updatedAt()` helpers for standard patterns
- Writing `src/lib/database/schema.ts`

**`scripts/generate-zod-schemas.ts`** — reads `schema.ts`, writes `src/lib/schemas/index.ts`. For each table generates:
- `EntitySelectSchema`, `EntityInsertSchema`, `EntityUpdateSchema`, `EntityFiltersSchema`
- Types: `Entity`, `EntityCreate`, `EntityUpdate`, `EntityFilters`
- `BaseFiltersSchema` with `limit`, `offset`, `search`
- Entity filter extensions for `id`, `status`, `user_id`, `content_type` when those columns exist

**`scripts/generate-services.ts`** — reads `schema.ts`, writes `src/lib/services/simplified/<kebab>.service.ts` for each table + `index.ts` barrel. Each service class:
- Named `EntityService` (PascalCase)
- Extends `SimplifiedService<typeof tableVar, Entity, EntityCreate, EntityUpdate, EntityFilters>`
- Exports a singleton: `export const entityVarService = new EntityService()`

**`scripts/generate-routes.ts`** — reads `schema.ts`, writes `src/app/api/simplified/<kebab>/route.ts` for each table. Each route exports `GET`, `POST`, `PATCH`, `DELETE` handlers following the standard pattern (filters in query params for GET/DELETE, body for POST/PATCH, `id` extracted from body for PATCH).

**`scripts/generate-hooks.ts`** — reads `schema.ts`, writes `src/hooks/simplified/<kebab>.hooks.ts` + `index.ts` barrel. Each file exports:
- `entityVarKeys` query key factory
- `useEntityList(filters?)` — useQuery calling GET
- `useEntity(id)` — useQuery with `enabled: !!id`
- `useEntityCreate()` — useMutation calling POST, invalidates lists
- `useEntityUpdate()` — useMutation calling PATCH, invalidates lists + detail
- `useEntityDelete()` — useMutation calling DELETE, invalidates lists
- Imports `buildQueryString` from `./query-utils`

> **Important:** When writing the generation scripts, read the actual scripts from the reference project (`scripts/generate-*.ts`) via the Read tool and write them verbatim. Do not recreate them from scratch — use the exact, battle-tested implementations.

### 3g. Validation scripts

Write each validation script to `scripts/`. Read from the reference project and write verbatim:

| Script | What it validates |
|--------|------------------|
| `scripts/validate-db-alignment.ts` | Layer 1: schema.ts table count === DB table count |
| `scripts/validate-semantic-alignment.ts` | Layer 2: all Zod exports exist for every table |
| `scripts/validate-services-alignment.ts` | Layer 3: service file + class + extends SimplifiedService |
| `scripts/validate-routes-alignment.ts` | Layer 4: route file + GET/POST/PATCH/DELETE exports |
| `scripts/validate-hooks-alignment.ts` | Layer 5: hooks file + keys + all 4 hook exports + QueryClientProvider |
| `scripts/validate-ui-alignment.ts` | Layer 6: List component exists importing from hooks |

### 3h. Package.json scripts

Add to `package.json` scripts (merge, don't replace existing):

```json
{
  "scripts": {
    "drizzle:gen": "drizzle-kit generate",
    "drizzle:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio",
    "db:check": "tsx scripts/validate-db-alignment.ts",
    "generate:schemas": "tsx scripts/generate-zod-schemas.ts",
    "contracts:check": "tsx scripts/validate-semantic-alignment.ts",
    "generate:services": "tsx scripts/generate-services.ts",
    "services:check": "tsx scripts/validate-services-alignment.ts",
    "generate:routes": "tsx scripts/generate-routes.ts",
    "routes:check": "tsx scripts/validate-routes-alignment.ts",
    "generate:hooks": "tsx scripts/generate-hooks.ts",
    "hooks:check": "tsx scripts/validate-hooks-alignment.ts",
    "generate:ui": "tsx scripts/generate-ui-components.ts",
    "ui:check": "tsx scripts/validate-ui-alignment.ts",
    "validate:all": "pnpm db:check && pnpm contracts:check && pnpm services:check && pnpm routes:check && pnpm hooks:check && pnpm ui:check"
  }
}
```

---

## Phase 4 — Generate Layer 1: Drizzle Schema

Run:

```bash
npx tsx scripts/generate-schema.ts
```

This reads the live database and writes `src/lib/database/schema.ts`. After completion:

1. Read the generated file and count the `export const X = pgTable(` lines.
2. Compare to the DB table count from Phase 1.
3. Run `pnpm db:check` (or `npx tsx scripts/validate-db-alignment.ts`) and show the JSON output.
4. **Required status: LOCKED** (both counts must match).

If the count doesn't match:
- Use `mcp__supabase__execute_sql` to list the specific tables that are missing or extra
- Manually inspect the generated schema for type-annotated exports (`export const X: PgTableWithColumns<any> = pgTable(`) — these are counted by the validator but not by the L2–L6 scripts
- Report the discrepancy to the user before proceeding

---

## Phase 5 — Generate Layer 2: Zod Schemas

Run:

```bash
pnpm generate:schemas
```

Then validate:

```bash
pnpm contracts:check
```

Show the JSON output. **Required status: LOCKED.**

If any schemas are missing:
- Run `pnpm generate:schemas` again to regenerate
- If still missing, the table likely has a type annotation in schema.ts — check if it needs to be added to the generator's regex

---

## Phase 6 — Generate Layer 3: Services

Run:

```bash
pnpm generate:services
```

Then validate:

```bash
pnpm services:check
```

Show the JSON output. **Required status: LOCKED.**

Confirm `src/lib/services/simplified/base.service.ts` exists. If missing, write it from Phase 3e above.

---

## Phase 7 — Generate Layer 4: API Routes

Run:

```bash
pnpm generate:routes
```

Then validate:

```bash
pnpm routes:check
```

Show the JSON output. **Required status: VALIDATED** (GET/POST/PATCH/DELETE present for each entity).

---

## Phase 8 — Generate Layer 5: React Hooks

Run:

```bash
pnpm generate:hooks
```

Then validate:

```bash
pnpm hooks:check
```

Show the JSON output. **Required status: LOCKED.**

Note: The hooks validator also checks that `src/app/providers.tsx` (or equivalent) exports a `QueryClientProvider`. If this file doesn't exist in the target project, create it or ask the user where React Query is initialized. The `QueryClientProvider` must wrap the app tree for hooks to work.

If providers.tsx doesn't exist, create a minimal one:

```typescript
// src/app/providers.tsx
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
```

---

## Phase 9 — Cross-Reference with Supabase MCP

After generation, perform a final DB cross-reference:

1. Use `mcp__supabase__execute_sql` to list all tables in the target project.
2. Read `src/lib/database/schema.ts` and count `pgTable` exports.
3. Compare:
   - Tables in DB but not in schema → missing from Layer 1
   - Tables in schema but not in DB → schema has phantom tables
4. For any mismatch: report to the user with exact table names.

Also spot-check a sample table by comparing its columns:

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = '<sample_table>'
ORDER BY ordinal_position;
```

Read the corresponding Drizzle definition in `schema.ts` and verify the columns match.

---

## Phase 10 — Run Full Validation

```bash
pnpm validate:all
```

Show the complete output. All layers must pass:

| Layer | Command | Required Status |
|-------|---------|-----------------|
| 1 | `pnpm db:check` | LOCKED |
| 2 | `pnpm contracts:check` | LOCKED |
| 3 | `pnpm services:check` | LOCKED |
| 4 | `pnpm routes:check` | VALIDATED |
| 5 | `pnpm hooks:check` | LOCKED |
| 6 | `pnpm ui:check` | VALIDATED (skip if no L6 yet) |

If any layer fails, fix bottom-up:
- **Layer 1 fails**: regenerate schema, align with DB
- **Layer 2 fails**: run `pnpm generate:schemas`, or fix the generator regex for type-annotated tables
- **Layer 3 fails**: run `pnpm generate:services`, check base.service.ts exists
- **Layer 4 fails**: run `pnpm generate:routes`
- **Layer 5 fails**: run `pnpm generate:hooks`, check providers.tsx has QueryClientProvider
- **Layer 6 fails**: run `pnpm generate:ui` (or note that L6 is not yet implemented)

---

## Phase 11 — Final Report

Output a structured report:

```markdown
## Type Safety Chain: Implementation Complete

### Database
- **Project:** [supabase project ID]
- **Tables in DB:** [N]
- **Tables in schema.ts:** [N]
- **Alignment:** LOCKED ✓ / UNLOCKED ✗

### Layer Status
| Layer | Name | Status | Count |
|-------|------|--------|-------|
| 1 | Drizzle Schema | LOCKED | N tables |
| 2 | Zod Schemas | LOCKED | N entities |
| 3 | Services | LOCKED | N services |
| 4 | API Routes | VALIDATED | N routes |
| 5 | React Hooks | LOCKED | N hook files |
| 6 | UI Components | VALIDATED / NOT YET | N components |

### Files Written
- `drizzle.config.ts`
- `src/lib/database/client.ts`
- `src/lib/database/schema.ts` (generated from DB)
- `src/lib/tenant.ts`
- `src/lib/schemas/index.ts` (generated)
- `src/lib/services/simplified/base.service.ts`
- `src/lib/services/simplified/index.ts` + N entity services
- `src/app/api/simplified/<N entity routes>`
- `src/hooks/simplified/query-utils.ts`
- `src/hooks/simplified/index.ts` + N hook files
- `scripts/generate-schema.ts`
- `scripts/generate-zod-schemas.ts`
- `scripts/generate-services.ts`
- `scripts/generate-routes.ts`
- `scripts/generate-hooks.ts`
- `scripts/validate-*.ts` (6 validation scripts)

### Issues / Gaps
- [Any tables that don't match, missing columns, schema discrepancies]
- [Any layers that failed validation and were fixed or need attention]

### Next Steps
- Wire Layer 6 (UI): run `pnpm generate:ui` then use the `/stitch-react` or `/new-page` skill to build pages
- Add custom services to `src/lib/services/custom/` for non-CRUD logic
- Add custom hooks to `src/hooks/custom/` for non-entity queries
- Set `TENANT_ORG_ID` in `.env.local` if tables have `organization_id` columns
- Run `pnpm validate:all` any time schema changes are made
```

---

## Naming Conventions

All names in upper layers derive from the Drizzle `export const <varName> = pgTable(...)` variable name:

| Transform | Rule | Example (input: `bookChapters`) |
|-----------|------|----------------------------------|
| PascalCase | `s[0].toUpperCase() + s.slice(1)` | `BookChapters` |
| kebab-case | Replace `([a-z])([A-Z])` → `$1-$2`, lowercase | `book-chapters` |
| Schema exports | `BookChaptersSelectSchema`, `BookChaptersInsertSchema`, etc. | — |
| Service class | `BookChaptersService extends SimplifiedService` | — |
| Service file | `book-chapters.service.ts` | — |
| Route path | `src/app/api/simplified/book-chapters/route.ts` | — |
| Hook keys | `bookChaptersKeys` | — |
| Hook functions | `useBookChaptersList`, `useBookChaptersCreate`, etc. | — |
| Hook file | `book-chapters.hooks.ts` | — |

---

## Critical Rules

1. **Types flow downstream only.** Never import from a higher layer into a lower one.
2. **Fix bottom-up.** If Layer 3 fails, don't patch the service file — check if Layer 1/2 is correct first.
3. **Generated files are not hand-edited.** If a generated file needs custom logic, add it in the `custom/` directories (`src/lib/services/custom/`, `src/hooks/custom/`, `src/app/api/custom/`).
4. **DB is the source of truth.** Never add tables to schema.ts that don't exist in the database.
5. **Never run MCP destructive operations.** Only use `execute_sql` for `SELECT` statements (read-only introspection). Never `INSERT`, `UPDATE`, `DELETE`, or `DROP` via MCP.
6. **Lock-before-proceed.** Validate each layer before generating the next. Never skip layers.
7. **`base.service.ts` is never overwritten by generators.** The generate-services script explicitly skips it.
