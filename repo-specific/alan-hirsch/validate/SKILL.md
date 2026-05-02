---
name: validate
description: Run bottom-up layer validation and fix all errors. Use before starting work on any layer or to check project health. Follow the Lock-Before-Proceed and Error Fixing Protocol.
user-invocable: true
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Type safety chain: error check and fix

Run the six-layer validation bottom-up. Fix any failures at the failing layer only, then re-validate until all layers pass.

## 1. Run error check

- **Full chain:** `pnpm validate:all` — checks layers 1 → 6, stops at first failure.
- **Single layer:**  
  `pnpm db:check` | `pnpm contracts:check` | `pnpm services:check` | `pnpm routes:check` | `pnpm hooks:check` | `pnpm ui:check`

Each script prints **JSON** (status, message, missing, invalid); exit **0** = success, **1** = failure. Success = `LOCKED` (L1, L2, L3, L5) or `VALIDATED` (L4, L6). Failure = `UNLOCKED`.

## 2. Fix errors (until 0 errors)

1. Run `pnpm validate:all`.
2. If a layer fails: **fix only at that layer** (never change a lower layer to satisfy an upper one). Use the script’s `message` and `missing`/`invalid` to see what’s wrong.
3. Re-run from the fixed layer: run that layer’s command, then each higher layer (or `pnpm validate:all` again).
4. Repeat until `pnpm validate:all` exits 0 and every layer reports LOCKED or VALIDATED.

## 3. How to fix by layer

| Layer | Command | If it fails | Action |
|-------|---------|-------------|--------|
| 1 | `pnpm db:check` | schemaTables ≠ dbTables | Align `src/lib/database/schema.ts` with live DB; see _docs/type/layers/01-drizzle-schema.md. |
| 2 | `pnpm contracts:check` | missing > 0 | Add/fix Zod exports per table; run `pnpm generate:schemas` or edit `src/lib/schemas/index.ts`; see 02-zod-schemas.md. |
| 3 | `pnpm services:check` | missing/invalid | Add/fix service per entity (SimplifiedService); run `pnpm generate:services`; see 03-services.md. |
| 4 | `pnpm routes:check` | missing route/handlers | Add/fix route GET/POST/PATCH/DELETE; run `pnpm generate:routes`; see 04-api-routes.md. |
| 5 | `pnpm hooks:check` | missing hooks/exports | Add/fix hooks file + QueryClientProvider; run `pnpm generate:hooks`; see 05-react-hooks.md. |
| 6 | `pnpm ui:check` | missing component / wrong import | Add/fix List component importing from hooks; run `pnpm generate:ui`; see 06-ui-components.md. |

Layer docs live in `_docs/type/layers/`. Full protocol: _docs/type/TYPE_SAFETY.md (Error Testing and Cleanup, Error Fixing Protocol, How to Fix Errors by Layer).

## 4. Report

- If all pass: report “All 6 layers valid.”
- If one fails: report which layer failed, the script output (status, message, first missing/invalid items), and the fix approach from the table above.
