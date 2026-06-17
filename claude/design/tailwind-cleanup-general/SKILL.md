---
name: tailwind-cleanup-general
description: Design-agnostic Tailwind best-practice cleanup that conforms to the CURRENT repo's design schema. If the schema is already documented, it enforces it; if not, it first documents the schema as a layered charter (charter → tokens → primitives → components → layouts) by reading the repo, then runs the cleanup and applies fixes. Use whenever a Tailwind/CSS best-practice pass is needed in any repo and you want fixes that stay inside the established design system instead of imposing a new one. Triggers: "clean up the tailwind", "tailwind audit", "make the styling consistent", "enforce the design system", "document then clean up the styles".
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Run a best-practice Tailwind cleanup that stays **inside the design system this repo already uses**. This skill is intentionally **design-agnostic**: it does not assume shadcn, Material-3, an "ink" system, CSS-variable arbitrary values, or any particular palette. It discovers what the repo does, treats the *best* of that as the standard, documents it if it isn't already, and then makes the code consistent with it.

Target: $ARGUMENTS (a path, a glob, or empty). If empty, scan `src/` (or the repo's main source root).

> Golden rule: **conform, don't convert.** Never swap one design language for another. If the repo uses `bg-[var(--paper)]`, that is the standard here — do not "fix" it to `bg-card`. If the repo uses shadcn semantic tokens, enforce those. Your job is internal consistency and best practice *within* the established schema, never a redesign.

---

## Phase 0 — Discover the design schema

Read before doing anything. Build a mental model of how THIS repo expresses design.

1. **Tailwind version & config**
   - `tailwind.config.{ts,js,cjs,mjs}` (v3) or `@theme` / `@import "tailwindcss"` in CSS (v4). Note which.
   - Inventory the `theme.extend` (or `@theme`) keys: colors, spacing, fontSize, fontFamily, borderRadius, shadows.
2. **Token source of truth**
   - `globals.css` / `app.css` / `index.css`: `:root` custom properties, `@layer base`, `@layer components`.
   - CSS-variable conventions (`--primary`, `--stitch-*`, `--ink`, HSL vs hex, etc.).
3. **Existing design docs** — search `docs/`, repo root, `.stitch/`, README for any of: `DESIGN.md`, `design-charter`, `tokens`, `style-guide`, `brand`, `components.md`. These may already be the charter.
4. **Primitives** — `src/components/ui/`, `components/primitives/`, or equivalent. Are they vendored (shadcn) or repo-owned?
5. **Conventions** — does the repo use a `cn()`/`clsx` helper? `dark:` variants? a container/section primitive? a type scale (Display/Eyebrow/Prose)?

Write a one-paragraph summary of the detected schema and the **dominant correct pattern** for each axis (color, spacing, type, radius, elevation, layout). The dominant pattern = what the well-built parts of the repo already do, not the legacy outliers.

---

## Phase 1 — Decide: documented or not?

The schema is **"documented"** when a reader could, from the docs alone, know the canonical token names, the primitives and their intended use, and the layout system — enough to check code against it.

- **Already documented** (a real `DESIGN.md`/charter + token reference exists and matches the code) → load it, treat it as authority, skip to Phase 3.
- **Not documented, or docs are stale/contradicted by code** → do **Phase 2** first. Documenting is part of the job, not optional.

State which branch you're taking and why.

---

## Phase 2 — Document the schema (only if undocumented)

Codify what the repo **already does best** into a layered charter under `docs/design/`. Derive every statement from the actual code — do not invent new rules, colors, or components. Where the repo is inconsistent, pick the pattern used by the newest / most-correct / most-frequent code and name it canonical (note the outliers as "to be cleaned up").

Write these in order; each builds on the last:

1. **`docs/design/00-charter.md`** — the design philosophy in prose. What this product's UI is trying to be (extracted from the code: density, tone, light/dark, elevation philosophy, motion). The non-negotiable principles. 5–12 bullet "laws" the cleanup will enforce.
2. **`docs/design/01-tokens.md`** — the authoritative token tables: colors (name → value → when to use), spacing scale, type scale (font families + sizes + weights), radius, elevation/shadow, breakpoints. Mark each token's source (config key or CSS var). List **banned raw values** and their token replacement.
3. **`docs/design/02-primitives.md`** — each base component (Button, Card/Surface, Input, Badge, Eyebrow, Display, Container, Section, etc.): its props, variants, and the canonical className recipe. State which are vendored (do-not-edit) vs repo-owned.
4. **`docs/design/03-components.md`** — composite/feature components and recurring patterns (nav, cards grids, stat tiles, forms, empty states). How they compose primitives. Anti-patterns seen in the wild.
5. **`docs/design/04-layouts.md`** — shells, page scaffolds, grid systems, responsive rules, the container/measure system, and where each layout is used.

Add an index line to `docs/design/README.md` (create if absent). Keep each doc tight and reference real file paths (`Component.tsx:NN`). These docs become the charter the cleanup is checked against — and the durable artifact for the next run.

---

## Phase 3 — Scan against the charter

Now audit the target scope for deviations from the documented schema. Severities below; exact rules come from **this repo's** tokens.md, not a fixed list.

1. **Hardcoded values bypassing tokens (Critical)** — raw hex/rgb/hsl in `className` or `style`, color utilities outside the token set (`bg-white`, `text-gray-500`, `bg-blue-600`, arbitrary `bg-[#…]`) when the repo has a semantic token for them. Replace with the repo's token. *(If the repo's standard IS arbitrary CSS vars, those are correct — flag only raw literals that should be a named var.)*
2. **Arbitrary values that duplicate the scale (High)** — `p-[12px]`, `text-[18px]`, `rounded-[6px]`, `gap-[…]` where a scale token exists. Keep `clamp()`/`calc()` and genuinely one-off values; flag the rest.
3. **Elevation / border drift (High)** — shadows or decorative section borders that violate the charter's elevation philosophy. Conform to the documented approach (token shadow, tonal stacking, or whatever the charter says).
4. **Raw HTML instead of primitives (Medium)** — hand-rolled `<button>`, ad-hoc card `<div>`s, manual heading tracking, container `max-w-… mx-auto px-…` blocks that should use the documented primitive.
5. **Variant/utility hygiene (Medium)** — duplicate utilities, conflicting utilities (`p-4 p-6`, `flex block`), `dark:` usage inconsistent with the charter's light/dark stance, `className` string concat that should go through `cn()`.
6. **Framework best practices (Low)** — Tailwind v4 canonical forms (`bg-linear-to-*`, `aspect-4/5`) **only if the repo is v4**; ordering; dead classes; orphaned class fragments.

Produce the report (format below) **before** editing.

---

## Phase 4 — Fix

1. **Fix at the source layer.** If a needed token/primitive is missing, add it to the charter's source (config / globals / primitive) first, then use it. Update the relevant `docs/design/*.md` if you introduce a token.
2. **Never edit vendored primitives** (`ui/*` from shadcn, etc.) unless the charter marks them repo-owned.
3. **Batch by file**, batch by anti-pattern. Minimize edits.
4. **Stay in-schema.** Every replacement must be a token/primitive that already exists in the charter (or one you deliberately added to it).
5. **Verify**: run the repo's `typecheck`, `lint`, and `build` (whatever exists). Fix regressions. A cleanup that breaks the build is not done.

---

## Output format

```
## Tailwind Cleanup Report — <repo>

### Schema
- Tailwind: v<3|4> · token system: <detected> · primitives: <vendored|owned>
- Charter: <found at docs/design | newly documented in this run>

### Documentation (if Phase 2 ran)
- docs/design/00-charter.md … 04-layouts.md  (created/updated)

### Violations  (Critical: X · High: X · Medium: X · Low: X)
| File:line | Category | Found | Fix (in-schema) |
|---|---|---|---|

### Files modified
- path — N fixes

### Verification
- typecheck: ✅/❌ · lint: ✅/❌ · build: ✅/❌
```

---

## Rules

- **Conform, never convert.** The current repo's best pattern is the standard. No redesigns, no cross-pollinating another repo's design language.
- Always scan and present the report before applying fixes.
- Documenting the schema (Phase 2) is mandatory when it's undocumented — charter first, then tokens, primitives, components, layouts, then fixes.
- Don't touch vendored primitives, generated files, or `node_modules`.
- Respect the repo's existing choices on dark mode, arbitrary CSS vars, and elevation — enforce *consistency*, not your preference.
- Leave the `docs/design/` charter behind so the next run is a Phase-1 "already documented" fast path.
