---
name: type-fix
description: Run type safety checks across all 6 layers, regenerate any failing layers, and loop until all layers pass with zero errors. Follows the lock-before-proceed protocol from _docs/type/.
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Type Safety Fix Loop

Run validation and fix every failing layer bottom-up until `pnpm validate:all` exits 0. Follow the six-layer type safety architecture documented in `_docs/type/`.

## Reference

Read these docs before starting (they define the chain, naming rules, generators, and fix protocol):

- `_docs/type/TYPE_SAFETY.md` — full chain overview, error fixing protocol, commands
- `_docs/type/layers/01-drizzle-schema.md` through `06-ui-components.md` — per-layer validation rules and generators
- `_docs/type/AI_LAB_AND_OTHER_SURFACES.md` — surfaces outside the chain (skip these)
- `_docs/type/PROBLEMATIC_PAGES_TYPE_CHAIN.md` — known runtime issues (context only)

## Protocol

### Phase 1 — Initial assessment

1. Run `pnpm validate:all` to see which layers fail. Capture the full JSON output.
2. If all layers pass (exit 0), report success and stop.
3. If a layer fails, note the **first failing layer** (the chain stops at first failure).

### Phase 2 — Fix loop (bottom-up, one layer at a time)

For the first failing layer, apply the fix:

| Layer | Fix command | What it does |
|-------|------------|--------------|
| 1 — Drizzle Schema | `npx tsx scripts/generate-schema.ts` | Regenerate schema.ts from live DB (requires DATABASE_URL). If DB is unavailable, report and stop. |
| 2 — Zod Schemas | `pnpm generate:schemas` | Regenerate `src/lib/schemas/index.ts` from schema.ts |
| 3 — Services | `pnpm generate:services` | Regenerate all service files + index.ts |
| 4 — API Routes | `pnpm generate:routes` | Regenerate all route files |
| 5 — React Hooks | `pnpm generate:hooks` | Regenerate all hook files + index.ts |
| 6 — UI Components | `pnpm generate:ui` | Regenerate all component files + index.ts |

After running the generator:
1. Re-run that layer's check command (e.g. `pnpm contracts:check` for Layer 2).
2. If it still fails, read the JSON output carefully and fix manually (missing exports, wrong naming, structural issues).
3. Once that layer passes, move to the next layer up.

### Phase 3 — Full re-validation

After all individual layers pass:
1. Run `pnpm validate:all` to confirm the full chain is green.
2. If any layer regressed, go back to Phase 2 for that layer.
3. Repeat until `pnpm validate:all` exits 0.

### Phase 4 — TypeScript check (optional but recommended)

Run `pnpm build:check` (or `NODE_OPTIONS=--max-old-space-size=8192 pnpm typecheck`) to catch any TypeScript type errors introduced by regeneration. If there are TS errors:
1. Trace each error to the lowest affected layer.
2. Fix at that layer (edit the generated file or the generator input).
3. Re-run `pnpm validate:all` to ensure layer validation still passes.
4. Re-run typecheck until clean.

## Rules

- **Lock-before-proceed:** Never work on Layer N until all layers < N pass.
- **Fix bottom-up:** Always fix the lowest failing layer first.
- **Never fix upstream:** Do not change a lower layer to satisfy a higher layer.
- **Generators overwrite:** Running a generator replaces all entity files. Custom logic lives in `custom/` directories and is not affected.
- **Layer 1 needs DB:** Layer 1 regeneration requires a live database connection. If unavailable, report the mismatch and stop — do not guess at schema changes.
- **148 vs 149:** Layer 1 validates 149 tables (includes type-annotated `contentCategories`). Layers 2–6 validate 148 entities (regex excludes type-annotated exports). This is expected.

## Output

After each loop iteration, report:
- Which layer was fixed and how
- Current status of all layers checked so far

At completion, report:
- Final `pnpm validate:all` output
- Any TypeScript errors remaining (if Phase 4 was run)
