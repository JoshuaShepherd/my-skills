---
name: docs-type-safety
description: Audit and update _docs/_build/type/ (and _docs/_build/architecture/type-safety-chain.md) so documentation matches this codebase — six-layer Drizzle → Zod → services → routes → hooks → UI chain shared with movemental-visual-editor.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Type safety documentation — audit and update

Keep **`_docs/_build/type/`** and **`_docs/_build/architecture/type-safety-chain.md`** aligned with the **ai-agents** codebase and with the sibling **movemental-visual-editor** chain shape.

## Canonical paths (this repo)

| Path | Role |
|------|------|
| `_docs/_build/type/README.md` | Index |
| `_docs/_build/type/TYPE_SAFETY.md` | Overview, naming, error protocol |
| `_docs/_build/type/layers/*.md` | Per-layer validation rules |
| `_docs/_build/type/validation/VALIDATION_STATUS.md` | Optional status snapshot |
| `_docs/_build/architecture/type-safety-chain.md` | Architecture summary + `build:check` |

Do **not** use `_docs/type/` (alan-hirsch layout); this service uses **`_docs/_build/type/`**.

## Before starting

1. Read every file under `_docs/_build/type/` plus `_docs/_build/architecture/type-safety-chain.md`.
2. Collect ground truth from **`src/lib/database/schema.ts`**, **`src/lib/schemas/index.ts`**, **`src/lib/services/simplified/`**, **`src/app/api/simplified/`**, **`src/hooks/simplified/`**, and **`src/components/simplified/`** (if present).
3. Read **`package.json`** scripts (`validate:all`, `validate:all:with-ui`, `build:check`, `generate:*`).

## Audit checklist

Compare docs to code. Fix incorrect paths, commands, layer counts, and references to `generate:ui` / Layer 6 (this repo may not wire `pnpm generate:ui` yet).

1. **Commands** — every `pnpm` / `npx tsx` line must match `package.json`.
2. **Multi-tenancy** — docs should reference `.cursor/rules/multi-tenancy.mdc`, `organization_id`, `getTenantOrgId()`.
3. **validate:all** — must state layers 1–5; `validate:all:with-ui` for layer 6.
4. **build:check** — `tsconfig.build.json`, `RUN_LAYER_VALIDATION`, `VERCEL` / `SKIP_PREBUILD` behavior.
5. **Cross-links** — README ↔ TYPE_SAFETY ↔ architecture ↔ layer files.

## After updating

1. Run `pnpm build:check` (or `pnpm exec tsc -p tsconfig.build.json --noEmit`).
2. Optionally run `pnpm validate:all` and refresh `validation/VALIDATION_STATUS.md` if you maintain it.

## Related skills

- **`.claude/skills/validate/SKILL.md`** — run validators when verifying doc claims.
- **`.claude/skills/type-safety-chain/SKILL.md`** — bootstrap or repair the chain with Supabase MCP.
