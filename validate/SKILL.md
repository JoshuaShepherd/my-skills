---
name: validate
description: Run bottom-up layer validation and fix all errors. Use before starting work on any layer or to check project health. Follow the Lock-Before-Proceed and Error Fixing Protocol in _docs/_build/type/TYPE_SAFETY.md.
user-invocable: true
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Type safety chain — error check and fix

Run layer validation bottom-up. Fix failures **at the failing layer only**, then re-validate until all layers pass.

## 1. Run error check

- **Layers 1–5 (default in this repo):** `pnpm validate:all` — stops at first failure.
- **Include Layer 6 (UI):** `pnpm validate:all:with-ui`.
- **Single layer:** `pnpm db:check` | `pnpm contracts:check` | `pnpm services:check` | `pnpm routes:check` | `pnpm hooks:check` | `pnpm ui:check`

Each script prints **JSON** (`status`, `message`, `missing`, `invalid`); exit **0** = success. Success statuses: `LOCKED` (L1, L2, L3, L5) or `VALIDATED` (L4, L6). Failure = `UNLOCKED`.

**TypeScript (build scope, excludes tests):** `pnpm build:check` — runs `tsc -p tsconfig.build.json`. With `RUN_LAYER_VALIDATION=true`, runs `pnpm validate:all` first.

## 2. Fix errors (until 0 errors)

1. Run `pnpm validate:all` (or `validate:all:with-ui` if you need Layer 6).
2. If a layer fails: **fix only at that layer** (never change a lower layer to satisfy an upper one). Use `message` and `missing` / `invalid`.
3. Re-run from the fixed layer upward (or `pnpm validate:all` again).
4. Repeat until exit 0.

## 3. How to fix by layer

| Layer | Command | If it fails | Action |
|-------|---------|-------------|--------|
| 1 | `pnpm db:check` | schema ≠ DB | Align `src/lib/database/schema.ts` with live DB; see `_docs/_build/type/layers/01-drizzle-schema.md`. |
| 2 | `pnpm contracts:check` | missing Zod exports | `pnpm generate:schemas` or fix `src/lib/schemas/index.ts`; see `02-zod-schemas.md`. |
| 3 | `pnpm services:check` | missing/invalid service | `pnpm generate:services`; see `03-services.md`. |
| 4 | `pnpm routes:check` | missing handlers | `pnpm generate:routes`; see `04-api-routes.md`. |
| 5 | `pnpm hooks:check` | missing hooks / QueryClientProvider | `pnpm generate:hooks`; see `05-react-hooks.md`. |
| 6 | `pnpm ui:check` | missing List component | Scaffold per `06-ui-components.md`; `pnpm generate:ui` when wired (see movemental-visual-editor). |

Layer docs: **`_docs/_build/type/layers/`**. Full protocol: **`_docs/_build/type/TYPE_SAFETY.md`**.

## 4. Report

- If all pass: report which command(s) were run and that layers are LOCKED/VALIDATED.
- If one fails: report layer, JSON summary, and fix approach from the table above.
