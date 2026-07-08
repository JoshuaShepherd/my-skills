---
name: tenant-structural-port
description: >
  Phase D (optional deep port) of the Movemental tenant migration — port STRUCTURAL code
  parity from the reference repo (e.g. alan-hirsch) directly, rather than from Stitch
  wireframes, when the design-first stitch path is insufficient. Covers: design-chain audit
  so reference code lands with TENANT design tokens not the reference's, course
  infrastructure diff & port (hooks, custom APIs, learn player, certificates, cohort
  discussions, availability), course frontend parity verification, page inventory & route
  normalization, page-structure port with tenant design, tenant content/copy substitution,
  and final validation/cutover. Use when stitch-migration-validate flags hook/data/UX gaps,
  or the user says "port the course player from the reference", "structural parity",
  "match alan-hirsch course UX", "normalize the routes", "no source-tenant leaks". Run AFTER
  the stitch + backend phases. Tenant-agnostic via TENANT_MANIFEST.md.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, TodoWrite
---

# Tenant structural port (reference-code parity)

Port page structure, route patterns, and course-player UX from the reference repo while
keeping **tenant design tokens** and **tenant content**. The reference shares component
*structure* but not *visual identity* — porting code without a design audit lands hardcoded
source-tenant colors and wrong typography. Scope from `$ARGUMENTS`
(e.g. `course-infra`, `routes`, `pages`, `content`, `validate`).

Reference repo, design theme, content research, and leak patterns all come from
`TENANT_MANIFEST.md`. Never hardcode a tenant; this skill runs across leader repos.

## Charter & guardrails

- "Same look" = match **IA + section order** (pages) and **layout proportions, sidebar
  hierarchy, section types, hub nav, progress UX** (courses) from `{{REFERENCE_REPO}}` —
  re-skinned with tenant semantic tokens.
- Types downstream only; no Drizzle edits for UI; no `simplified/` hand-edits; no
  `src/components/ui/*` restyle; no `"use client"` in layouts; `pnpm` only; branch
  `slice/Sxx-migration-<topic>`.
- Do **not** copy source-tenant demo routes (e.g. `/hero-showcase`, `/ai-lab-archive`,
  `/[orgSlug]/*`) or source-tenant content/strings. Keep tenant-unique routes per manifest.

## 1 — Design-chain audit (run before porting UI)

Read the design chain L1–L5 (`docs/internal/design/L1_TOKENS.md` … `L5_PAGES.md`, charter,
palette) and `{{GLOBALS_CSS}}` / `tailwind.config.ts`. Compare against the reference
**read-only** (note differences; never copy reference token values). Then:

1. **Token audit** — grep `src/components/courses/` for hardcoded hex/`rgb(`/`bg-{color}-{n}`/
   `text-gray-*`; list `file:line` with the fix layer.
2. **L4 inventory** — map every `src/components/courses/` file to a section type in `L4_SECTIONS.md`; flag gaps.
3. **L5 inventory** — confirm `L5_PAGES.md` course table matches `src/app/(public)/courses/`.
4. **HTML prototype parity** (if `public/html/courses/*` exists) — layout reference only; remap colors to tenant tokens.
5. **Dual-mode check** — learn-player components use semantic tokens in light **and** `.dark`.

Apply doc updates (L4/L5/palette/comparison) only after audit; keep prose tenant-neutral.
Delegate token-violation cleanup to `design-chain` / `color-audit` if available.

## 2 — Course infrastructure diff & port

Diff reference vs target:

```bash
diff -rq {{REFERENCE_REPO}}/src/components/courses src/components/courses
diff -rq {{REFERENCE_REPO}}/src/app/\(public\)/courses src/app/\(public\)/courses
diff -rq {{REFERENCE_REPO}}/src/app/api/custom/courses src/app/api/custom/courses
diff -rq {{REFERENCE_REPO}}/src/hooks/custom src/hooks/custom | grep -i course
diff -rq {{REFERENCE_REPO}}/src/lib/content/courses src/lib/content/courses
```

Produce: missing files · differing files (3-way judgment) · tenant-only files (keep) ·
API route parity table · hook parity · recommended PR-sized slices. Then port missing
infra (adapt imports to `@/`): availability helper, access/discussions/assessments APIs,
cohort discussion board, certificate route + print button, etc.

**Merge rules:** keep tenant design tokens (replace reference hardcoded colors with semantic
classes), keep tenant config (`availableSlugs`, flags, slugs), keep tenant `TENANT_ORG_ID`
scoping in API routes, do **not** copy source-tenant strings or course-specific dialogs.
Services return `Result<T>` (never throw); hooks use the existing React Query patterns.
Verify: `pnpm typecheck`, `pnpm test:run -- courses`, `pnpm routes:check`.

## 3 — Course frontend parity verification

3-way merge the learn player (`CourseLearnLayout`, `CourseLearnSidebar`, `CourseTopbar`,
`LessonPanel/Tabs/Content`, `SectionContent`, `use-course-learn`, learn `page.tsx`) — tenant
tokens win on styling. Behavioral targets: action-based sidebar labels, week-level progress,
current week expanded; hub nav (learn/overview/cohort/resources/journal/enroll); all section
types render without runtime error; mark-complete + enrollment + week/lesson nav; protected
route still guarded by middleware. Run `course-ux` on the primary course slug. Minimal diff —
no unrelated refactors. Verify course tests (and e2e if configured).

## 4 — Page inventory & route normalization

Build the route map from `REFERENCE_PLATFORM_UI_INVENTORY.md` and the reference `(public)`
tree; decide redirects from `REFERENCE_PAGE_COMPARISON.md` and the manifest legacy-redirect
table (e.g. `/library → /content`, `/essays → /content/articles`, `/sign-in → /auth/signin`).
Keep tenant-unique routes per manifest; add redirects for normalized legacy paths.

## 5 — Page-structure port with tenant design

Port reference page structure (section order, composition) into target routes, applying tenant
tokens + tenant copy. IA from reference; visual treatment from the tenant design chain. Use
`new-page` for fresh scaffolds. No source-tenant copy or palette.

## 6 — Tenant content & copy substitution

Replace all source-tenant narrative/book titles/framework marketing with tenant content from
`{{CONTENT_RESEARCH}}` and `tenant.config.ts`. Grep leaks (delegate to `tenant-check`):
`rg '{{leak patterns}}' src --glob '!tenant.config.ts'`. Maintain an allowlist in the gap-audit
notes so research filenames don't false-positive.

## 7 — Validation, cutover & docs

`pnpm validate:all && pnpm typecheck && pnpm lint && pnpm build`; course tests; leak grep clean;
`pnpm verify:tenant-org`. Update `REFERENCE_PAGE_COMPARISON.md` per route, design docs, and
README. Emit a slice report; PR ready on `slice/Sxx-migration-*`. Do not merge to `main` until green.

## Acceptance criteria

- [ ] Tenant design tokens are the styling source; reference HTML is layout-only reference
- [ ] L4_SECTIONS / L5_PAGES reflect actual `src/components/courses` and `src/app/(public)/courses`
- [ ] Course learn player matches reference behavior with tenant tokens
- [ ] Routes normalized per comparison doc; tenant-unique routes preserved
- [ ] No source-tenant content leaks in `src/`; `validate:all` + `build` green

## Related skills

`tenant-backend-parity` · `tenant-check` · `course-ux` · `course-ingest` ·
`design-chain` / `color-audit` · `new-page` · `validate` · `tenant-migration-playbook`
