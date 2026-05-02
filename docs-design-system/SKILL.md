---
name: docs-design-system
description: Audit and update design documentation in _docs/_build/design/ to match the actual UI stack (tokens, Tailwind, shadcn primitives, domain components, pages). Keeps DESIGN_SYSTEM_SSOT.md and the design chain aligned with src/.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Design System Documentation Audit & Update

Audit design docs under `_docs/_build/design/` (and the `_docs/design/` symlink) against the **live codebase** so documentation stays the single source of truth for **how the design chain is implemented** in this repo.

**Ground truth file:** `_docs/_build/design/DESIGN_SYSTEM_SSOT.md` — update this first when reconciling; then align `DESIGN_CHAIN.md`, `DESIGN_CHARTER.md`, and `layers/*.md` as needed.

Target: $ARGUMENTS

If no target is provided, audit the full `_docs/_build/design/` tree and `src/app/globals.css`, `tailwind.config.ts`, `src/components/ui/`, and `src/components/` (excluding `_archive/`).

## Design chain (reference)

Bottom-up: **D0** charter → **D1** tokens (`globals.css`, `tailwind.config.ts`) → **D2** primitives (`src/components/ui/`) → **D3** domain components → **D4** patterns/layouts → **D5** pages → **D6** motion.

Design values flow **downstream** only (see `.cursor/rules/react-nextjs-best-practices.mdc` design chain).

## Before starting

1. Read `DESIGN_SYSTEM_SSOT.md`, `DESIGN_CHAIN.md`, `DESIGN_CHARTER.md`, and `_docs/_build/design/README.md`.
2. Read `src/app/globals.css` (including `@theme`, `:root`, `.dark`).
3. Read `tailwind.config.ts` (`theme.extend` and any relevant keys).
4. List `src/components/ui/*.tsx` and top-level folders under `src/components/` (excluding `ui`, `_archive`).

## Ground truth collection

From the **codebase** (not from prose docs alone):

### D1 — Tokens

- Note primary/surface/semantic CSS variables in `:root` and `.dark`.
- Note `@theme` → `--color-*` mappings in `globals.css`.
- Note font stacks (`--font-heading`, `--font-body`, `next/font` usage in `src/app/layout.tsx` if relevant).

### D2 — Primitives

- File list under `src/components/ui/`.
- Confirm policy: no styling edits in `ui/` for product fixes.

### D3 — Domain components

- Top-level feature folders under `src/components/`.
- Any new high-traffic patterns (hero, nav, chat shell) and their paths.

### D4–D5

- Key layout files: `src/app/(public)/layout.tsx`, shared headers/footers, layout client wrappers.
- Sample a few `page.tsx` files for composition patterns.

### D6

- Keyframes and animation utilities in `tailwind.config.ts` and `globals.css`.

### Tenant

- Confirm `tenant.config.ts` has no hardcoded colors/fonts for UI chrome.

## Audit checklist

Compare docs against ground truth. Flag and fix:

1. **Wrong palette or fonts** — e.g. charter says Montserrat/amethyst but code uses Lora/`#bd0036`.
2. **Wrong paths** — `_docs/design/` vs `_docs/_build/design/` (both valid if symlink exists).
3. **Stale layer docs** — `layers/D1-tokens.md` etc. contradict `globals.css`.
4. **Missing primitives** — new `ui/` components not mentioned.
5. **Broken links** — e.g. `PATHWAYS_DESIGN_ALIGNMENT.md` only under `_public/proposals/`.
6. **Tailwind version** — v4 `@import "tailwindcss"` vs legacy `@tailwind` directives in examples.

## Update rules

- Refresh `DESIGN_SYSTEM_SSOT.md` with accurate tables and “last reviewed” date.
- Edit `DESIGN_CHAIN.md` / `DESIGN_CHARTER.md` to match implementation **or** add explicit “legacy narrative” notes if product intentionally keeps aspirational copy (prefer matching code).
- Keep README index links correct; fix relative links to `_public/` proposals when needed.
- Do not move design research into `_build/` — proposals stay in `_docs/_public/` per `CONSTITUTION.md`.

## After updating

1. Grep for `_docs/design` and spot-check that symlink `_docs/design` → `_docs/_build/design` still exists.
2. Ensure no doc claims a token name that does not exist in `globals.css`.
3. Optional: `pnpm lint` on touched TSX if examples were updated.
