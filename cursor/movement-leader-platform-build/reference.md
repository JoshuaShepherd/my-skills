# Platform build reference

Supporting detail for `movement-leader-platform-build`. Read sections as needed during audit and build.

---

## Audit inspection

### Route inventory

```bash
find src/app -name 'page.tsx' | sort
find src/app -name 'layout.tsx' | sort
```

### Placeholder / stub detection

```bash
rg 'PlaceholderPage|TODO|coming soon' src/app src/components -l
rg 'dangerouslySetInnerHTML' src -l   # fake migrations
```

### Component discovery

```bash
rg -l 'Hero|Footer|Header|Breadcrumb' src/components
ls src/components/
```

### Shell checks

| Item | Look for |
|------|----------|
| Movemental chrome | `src/components/` or layout wrapper with network signal + account menu |
| Leader header | wordmark, nav Themes · Library · Formation · About, search |
| Site footer | multi-column footer with explore/more/legal |
| Floating AI Lab | persistent chat FAB |

### Theme page load-bearing sections

On `/themes/[slug]` verify all four:

1. **Cases (plural)** — multiple witnesses, not one story
2. **AI Lab invitation** — bound to theme reframing question
3. **Distortion warnings** — what this theme is NOT
4. **Invitation / next step** — one concrete CTA

### Identity assets

```bash
ls public/images/ 2>/dev/null
rg 'og:image|openGraph' src/app -l
rg 'wordmark|portrait' src/lib/config/tenant.config.ts
```

---

## Zone map

| Zone | Routes / scope |
|------|----------------|
| `shell` | chrome, header, footer, floating AI Lab |
| `home` | `/` |
| `themes` | `/themes`, `/themes/[slug]`, `/themes/[slug]/experience`, `/themes/map` |
| `library` | `/library/**` |
| `formation` | `/formation/**` |
| `about` | `/about`, `/contact`, `/organizations` |
| `chrome` | `/auth/**`, `/account/**`, `/checkout/**`, `/verify-email` |
| `footer` | `/ai-lab/**`, `/pricing`, `/donate`, `/facilitators`, `/search`, legal, `/[orgSlug]/**`, `/lp/**`, `/certificates/**` |

---

## Build prompt template

Save to `docs/build/prompts/build-remaining-{tenant}-{YYYY-MM-DD}.md`:

```markdown
# Build remaining — {Tenant Name} ({YYYY-MM-DD})

> Generated from `docs/build/checklists/components/{tenant}-audit-{YYYY-MM-DD}.md`
> Run with `.cursor/skills/movement-leader-platform-build/SKILL.md` or `.claude/skills/movement-leader-platform-build/SKILL.md`

## Context

- **Tenant:** {slug}
- **Design source:** `docs/design/README.md`, L1–L5 layer docs, `src/app/globals.css`
- **Type safety:** `docs/internal/type/TYPE_SAFETY.md` — hooks for data, fix bottom-up
- **Config:** `src/lib/config/tenant.config.ts`
- **Reference pages:** {list 2–3 most complete pages in this repo to mirror}

## Gates

A page is **not done** until every **(R)** item below is `[x]` and wired to real data.

## Build order

### 1. Shell (blocker)

{list [ ] and [~] shell items with checklist section names}

### 2. Hubs

{home, themes hub, library hub, formation hub, about — grouped}

### 3. Detail templates

{theme 12-section page, article, book, course, etc.}

### 4. Secondary / footer routes

{ai-lab, pricing, legal, search, …}

### 5. Enrichment (optional)

{JSON-LD, theme experience, share cards, …}

## Per-page specs

For each page, carry section structure from the master checklist. Example:

### `/themes/[slug]` — Theme page

| Section | Status | Build notes |
|---------|--------|-------------|
| Breadcrumb **(R)** | [ ] | Use existing Breadcrumb component; BreadcrumbList JSON-LD |
| Cases (plural) **(R)** | [~] | Wire to `src/lib/content/themes/` or pathway data |
| … | | |

**Hooks/data:** {entity hooks required}
**L4 to reuse:** {existing section components}
**Stitch prompt** (if generating fresh): {aesthetic description matching tenant tokens}

## Validation (final phase)

```bash
pnpm typecheck
pnpm validate:all
pnpm build
```

Fix type-safety chain bottom-up before declaring complete.
```

---

## Type safety gates

Applies equally to all movement-leader templates.

### Read order

1. `docs/internal/type/TYPE_SAFETY.md`
2. `src/lib/database/schema.ts` (Layer 1 — source of truth)
3. `src/lib/config/tenant.config.ts` (tenant strings/flags)

### Rules for UI work

| Rule | Detail |
|------|--------|
| Data in UI | Only via `src/hooks/simplified/*.hooks.ts` or `src/hooks/custom/*.hooks.ts` |
| New fetch in component | **Forbidden** — add/use a hook |
| New entity shape | Must exist in `schema.ts`; run generators if scaffold missing |
| Custom business logic | `src/lib/services/custom/`, `src/app/api/custom/` |
| Generated files | Do not hand-edit `src/lib/schemas/index.ts`, generated services/routes/hooks/ui |
| Type drift | Fix lowest layer first; never patch upper layer to match UI wish |

### Validation commands

```bash
pnpm db:check          # Layer 1
pnpm contracts:check   # Layer 2
pnpm services:check    # Layer 3
pnpm routes:check      # Layer 4
pnpm hooks:check       # Layer 5
pnpm ui:check          # Layer 6
pnpm validate:all      # all layers
pnpm typecheck
pnpm build
```

Run after any change that touches entity data, hooks, or API routes.

### Wiring checklist item → data

1. Identify content type (theme, article, book, course, …)
2. Grep hooks: `rg '{entity}' src/hooks/`
3. If hook exists → use in Server or Client component via hook
4. If static tenant content → `src/lib/content/` or `tenant.config.ts`
5. If DB entity missing from hooks → verify table in schema → use generated hook or add `custom/` hook

---

## Design system gates

### Read order

1. `docs/design/README.md`
2. `docs/design/DESIGN_CHARTER.md`
3. Relevant `docs/design/layers/L*.md`
4. `docs/design/patterns/*.md` for section recipes
5. `src/app/globals.css` (live L1 tokens)

### Before creating a component

```bash
rg '{SectionName}|{pattern}' src/components -l
ls src/components/home/ src/components/themes/ 2>/dev/null
```

Prefer extending an existing L4 section over creating a parallel component.

### Token compliance

- ✅ `bg-primary`, `text-muted-foreground`, `border-border`
- ❌ `bg-[#1a1a1a]`, `text-gray-500`, `bg-zinc-900`

### Page patterns

- **Hub:** hero + grid/cards + closing CTA
- **Detail:** breadcrumb + hero + sections + related + AI Lab door
- **Theme page:** sticky section nav + 12 sections in checklist order

---

## Delegation pattern

For full-platform builds, spawn Task agents per zone:

```
Task: movement-leader-platform-build — zone themes
  - Read design L4/L5 + type safety docs
  - Build only items marked [ ] or [~] in audit for themes zone
  - Update audit file checkboxes
  - Run pnpm typecheck before returning
```

Orchestrator merges zone results, runs final `validate:all` + `build`.
