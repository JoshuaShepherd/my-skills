---
name: movement-leader-platform-build
description: >-
  Audits a movement-leader tenant against the master component checklist, writes a
  gap-remediation build prompt to docs/build/prompts/, then implements missing pages
  and components in the repo's existing design system with full type-safety compliance.
  Use when running the platform checklist, auditing component gaps, building remaining
  pages, platform build, master-component-checklist, or remediating missing shell/themes/
  library/formation routes. Run from any movement-leader repo root.
disable-model-invocation: true
---

# Movement Leader Platform Build

End-to-end: **audit** → **build prompt** → **implement** → **validate**.

Run from the **tenant repo root** (`movement-leader-websites/{slug}/`, `alan-hirsch/`, or `brad-brisco/`).

## Invocation

```
/movement-leader-platform-build
/movement-leader-platform-build audit-only
/movement-leader-platform-build build-only
/movement-leader-platform-build --zone themes
/movement-leader-platform-build --zone shell,home,themes
```

| Flag | Effect |
|------|--------|
| (default) | Phases 1–5: audit → prompt → build → validate |
| `audit-only` | Phases 1–2 only; stop after build prompt for human review |
| `build-only` | Phase 3+ using latest `docs/build/prompts/build-remaining-*.md` |
| `--zone {name}` | Limit audit/build to zone(s): `shell`, `home`, `themes`, `library`, `formation`, `about`, `chrome`, `footer` |

Infer tenant slug from repo folder name or `tenant.config.ts`.

---

## Read first (mandatory)

| Doc | Path |
|-----|------|
| Master checklist | `docs/build/checklists/components/master-component-checklist.md` |
| Design charter | `docs/design/README.md` + `docs/design/DESIGN_CHARTER.md` |
| Design layers | `docs/design/layers/L1_TOKENS.md` … `L5_PAGES.md` |
| Type safety | `docs/internal/type/TYPE_SAFETY.md` (or `shared/docs/type/TYPE_SAFETY.md` in monorepo) |
| Tenant config | `src/lib/config/tenant.config.ts` |
| Env contract | `src/lib/env.ts` |

If the master checklist is missing, stop — it must exist at the path above.

---

## Phase 1 — Audit

Follow the agent protocol in the master checklist (steps 1–4). Do **not** edit the master file.

1. Copy master → `docs/build/checklists/components/{tenant}-audit-{YYYY-MM-DD}.md`
2. For every checklist item, inspect:
   - Routes: `src/app/**/page.tsx`, `layout.tsx`, `route.ts`
   - Components: `src/components/**`
   - Data: `tenant.config.ts`, `src/lib/content/**`, hooks in `src/hooks/simplified/` and `src/hooks/custom/`
3. Mark each item `[x]`, `[~]`, or `[ ]` with file path or `missing`
4. At the top of the audit file, write:
   - Percent complete per zone
   - Every **(R)** item still `[ ]` or `[~]`
   - Four load-bearing theme sections status (plural cases, bound AI Lab, distortion warnings, one concrete next step)
   - Mandatory identity assets (portrait, wordmark, default OG)

Use inspection helpers from [reference.md](reference.md).

Stop here if `audit-only`.

---

## Phase 2 — Build prompt

Write `docs/build/prompts/build-remaining-{tenant}-{YYYY-MM-DD}.md` using the template in [reference.md](reference.md#build-prompt-template).

The prompt must:

- List every `[ ]` and `[~]` item grouped by page in **dependency order**: shell → hubs → detail templates → enrichment
- Instruct building in **this repo's design system** — read design layer docs; reuse L4 sections; semantic tokens only; no new visual language
- Carry each page's section structure from the checklist
- Treat **(R)** items as gates — a page is not done until required items pass
- Specify hook/entity wiring for data-backed sections (Layer 5 hooks → never new services without type-chain compliance)
- Include a final validation phase: `pnpm typecheck`, `pnpm validate:all`, `pnpm build`

Stop after Phase 2 if `audit-only` was requested. Otherwise continue unless the user said to pause for review.

---

## Phase 3 — Build (dependency order)

Execute the build prompt. For each page/zone:

### Design rules (non-negotiable)

1. **Tokens first** — colors/spacing/type from L1 → L2; never hardcode hex or raw palette (`text-gray-600`)
2. **Reuse L4** — grep `src/components/` before creating; extend existing section components
3. **`tenantConfig` for copy** — no hardcoded tenant strings in components
4. **Server page, client leaves** — `page.tsx` Server Component; `"use client"` only where needed
5. **Lucide icons** — no Material Symbols
6. **Match sibling pages** — read the most complete page in the same zone and mirror structure

### Type safety rules (non-negotiable)

Apply to every data-backed feature. Full rules: [reference.md](reference.md#type-safety-gates).

1. **Never invent types** — derive from Layer 1 schema or existing Zod exports
2. **UI reads via hooks** — `src/hooks/simplified/` or `src/hooks/custom/`; no direct DB in components
3. **New entity touch** — if a checklist item needs data not in hooks: trace entity in `schema.ts` → use existing hook or add custom hook in `src/hooks/custom/` (not inline fetch)
4. **Do not edit generated layers** to satisfy UI — fix bottom-up per TYPE_SAFETY.md
5. After entity-touching work: run affected layer checks before moving on

### Build sequence

```
1. Shell: Movemental chrome, leader header, footer, floating AI Lab button
2. Hubs: /, /themes, /library, /formation, /about
3. Detail templates: theme page, article, book, course, etc.
4. Secondary/footer routes: /ai-lab, /pricing, legal, search, …
5. Enrichment: JSON-LD, optional sections, theme experience variant
```

For each item built, update the audit working copy checkbox to `[x]` with the new file path.

Delegate large zones via **Task** agents (one per zone), each re-reading design + type docs.

---

## Phase 4 — Validate

Run from repo root:

```bash
pnpm typecheck
pnpm validate:all    # or layer checks if validate:all unavailable
pnpm build
```

Fix failures bottom-up (schema → schemas → services → routes → hooks → UI → pages).

Re-run until clean. Update audit summary with final completion percentages.

---

## Phase 5 — Session report

Print:

- Tenant slug and date
- Audit file path and overall % complete
- Build prompt path
- Zones built this session
- Remaining **(R)** gaps
- Validation results (pass/fail per command)

---

## Do not

- Edit `master-component-checklist.md` (master stays pristine)
- Introduce new design tokens or visual language without explicit user approval
- Use `PlaceholderPage` as a finished state for **(R)** routes
- Skip typecheck/validate after data wiring changes
- Hardcode Movemental brand assets on tenant pages

## Additional resources

- Audit commands, prompt template, type gates: [reference.md](reference.md)
