# Agent runbook — Stitch page-by-page migration (Prompts 00–16)

> **How to use this file:** Copy each **Copy-paste prompt** block into an agent session (Cursor, Claude Code). Substitute `{{VAR}}` from [TENANT_MANIFEST.md](./TENANT_MANIFEST.template.md) (fork the template first). Invoke the listed Claude skill when present — skills encode guardrails this runbook references.
>
> **Audience:** Any agent migrating any Movemental leader under `movement-leader-websites/`.
>
> **Not in scope here:** Tailwind class translation alone. This runbook covers the full product migration: wireframe intake → semantic design → L4 sections → L5 pages → hooks → backend → validation.

---

## Prerequisites — read before Prompt 00

### Mandatory files (target repo)

```
docs/build/stitch-migration/TENANT_MANIFEST.md      ← fork from template; fill all {{VAR}}
docs/build/stitch-migration/COMPONENT_CHECKLIST.md  ← fork from template
docs/build/stitch-migration/STITCH_ROUTE_INDEX.md
src/lib/config/tenant.config.ts
src/app/globals.css
```

### Canonical upstream (shared)

| Role | Path |
|------|------|
| Stitch HTML prompt library | `{{STITCH_PROMPTS_HTML}}` → typically `../../../brad-brisco/docs/build/stitch-prompts.html` |
| Reference platform (structure + hooks patterns) | `{{REFERENCE_REPO}}` → typically `../../../alan-hirsch` |
| **`stitch-react` skill** (HTML/Tailwind → React/Next.js/Tailwind) | `{{STITCH_REACT_SKILL}}` → `../../../brad-brisco/.claude/skills/stitch-react/SKILL.md` |

### Local orchestration skills (in target repo `.claude/skills/`)

| Skill | Phase |
|-------|-------|
| `tenant-migration-playbook` | Hub — dispatch to sub-skills |
| `stitch-intake-audit` | 01 |
| `stitch-token-bridge` | 02 |
| `stitch-page-port` | 03–09 |
| `stitch-migration-validate` | 10 |
| `tenant-backend-parity` | 11–16 |

---

## The `stitch-react` skill — when and how agents use it

The **`stitch-react`** skill is the **conversion primitive**. It lives in the Brad Brisco prototype repo and converts cached Stitch HTML (Tailwind utility classes, B&W wireframe palette) into production **React Server/Client Components** with **Next.js App Router** conventions and **tenant semantic tokens** (not wireframe hex).

**Do not** re-implement fetch/decompose logic when this skill is available. **`stitch-page-port`** wraps `stitch-react` with tenant manifest copy, feature gates, hook wiring, and incomplete-template synthesis.

### stitch-react phases (interface contract)

Agents should read the full skill file at `{{STITCH_REACT_SKILL}}`. Expected phases:

| Phase | Name | What it does |
|-------|------|--------------|
| **0** | Fetch & cache | Download HTML + PNG from Stitch MCP → `.stitch/designs/{page-slug}.{html,png,meta.json}`. Use `scripts/fetch-stitch.sh` for GCS signed URLs. |
| **1** | Visual audit | Read cached HTML + PNG; note section boundaries (`data-section`, headings, alternating `bg-white`/`bg-gray-50`). |
| **Archive** | Archive Protocol | Move existing `page.tsx` → `page-old.tsx` before replacing. Never delete without archive. |
| **2–4** | Decompose | Split HTML into L4 section components under `src/components/{area}/`. One section ≈ one file. Plan approval if >4 new sections. |
| **5** | Token bridge | Replace `#111`, `#666`, `#F7F7F7`, etc. with semantic classes per `docs/build/notes/stitch-token-bridge.md`. |
| **6** | Compose page | Server Component `page.tsx` importing sections in checklist order. `"use client"` only in interactive sections. |
| **7** | States | Loading / empty / error in client sections. Empty DB → empty state UI, never fake data. |
| **8** | Report | Emit conversion report: screens converted, archived files, new paths, hooks vs stubs, gaps. |

### What stitch-react does NOT do (stitch-page-port handles these)

- Substitute tenant copy from `tenant.config.ts` / research docs
- Feature-gate sections (`features.chat`, `features.courses`, …)
- Synthesize checklist sections missing from Stitch HTML
- Wire Layer-5 hooks from `src/hooks/custom/`
- Update `COMPONENT_CHECKLIST.md` or run build gates

---

## Prompt 00 — Charter and guardrails

> **Run first.** Establishes scope, branch, and non-negotiables.  
> **Skill:** `tenant-migration-playbook` Step 1

### Copy-paste prompt

```
You are migrating a Movemental thought-leader tenant from Google Stitch wireframes into production React + Supabase-backed data layers.

## Read first (mandatory)
- docs/build/stitch-migration/TENANT_MANIFEST.md
- docs/build/stitch-migration/AGENT_RUNBOOK.md (this file)
- docs/build/stitch-migration/COMPONENT_CHECKLIST.md
- docs/build/stitch-migration/STITCH_ROUTE_INDEX.md

## Context
- UPSTREAM: Stitch screens from {{STITCH_PROJECT_NAME}} ({{STITCH_PROMPTS_HTML}})
- TARGET: movement-leader-websites/{{TENANT_SLUG}}
- REFERENCE CODE: {{REFERENCE_REPO}}
- STITCH → REACT PRIMITIVE: {{STITCH_REACT_SKILL}} — read and follow for HTML decomposition
- PAGE ORCHESTRATION: .claude/skills/stitch-page-port/SKILL.md
- TENANT AUDIT: {{TENANT_MIGRATE_SKILL}}

## Product goal
Replace PlaceholderPage scaffolds with L4 sections + L5 pages that:
1. Match reference IA — section order from STITCH_ROUTE_INDEX, L5_PAGES, Stitch prompt spec
2. Use tenant design — semantic tokens from {{GLOBALS_CSS}} ({{DESIGN_THEME}}). NOT Stitch B&W hex in production.
3. Use tenant content — tenantConfig + {{CONTENT_RESEARCH}}. No Stitch placeholder tenant (Brad Brisco) or reference tenant ({{SOURCE_TENANT_NAME}}) copy unless config enables those features.

## Tenant (from manifest)
- TENANT_SLUG: {{TENANT_SLUG}}
- TENANT_ORG_ID: {{TENANT_ORG_ID}}
- Feature flags: {{TENANT_CONFIG}} — build UI with gates; align with DB in Prompt 15

## Non-negotiables
- Types flow downstream only (schema → zod → services → routes → hooks → UI). Never modify Drizzle schema for UI.
- Do not hand-edit generated simplified/ files.
- No tenant-specific strings in components; use tenantConfig / useTenant().
- Do not modify src/components/ui/* for styling; fix L1 tokens or L4 section classes.
- Never add "use client" to src/app/layout.tsx.
- Archive existing page.tsx → page-old.tsx before replacing (stitch-react Archive Protocol).
- pnpm only. Branch: slice/Sxx-stitch-<topic>. No direct commits to main.
- NEVER ship dangerouslySetInnerHTML HTML dumps — real JSX only.
- NEVER copy Stitch #111/#666 hex into components — map to bg-foreground, text-muted-foreground, etc.

## Incomplete template policy
When a page is PlaceholderPage OR a Stitch screen omits a checklist section:
1. Read STITCH_ROUTE_INDEX + L5_PAGES + COMPONENT_CHECKLIST for required sections
2. Implement missing sections in tenant design (spacing rhythm, shadcn primitives, manifest copy slots)
3. If section exists in {{REFERENCE_REPO}}, port structure — re-skin with tenant tokens
4. Mark row PARTIAL in REFERENCE_PAGE_COMPARISON with note "Stitch gap: {section}"
5. Do NOT delete routes or reorder sections without documenting

## Deliverables for this session
Before writing code, output:
1. Branch name (slice/Sxx-stitch-* or slice/Sxx-backend-*)
2. Stitch screen ID(s) or cached .stitch/designs/ paths in scope
3. Routes / layers touched
4. Which numbered prompts (01–16) this slice covers
5. Blockers: missing Stitch screens, MCP auth, zero DB content for enabled feature

Wait for confirmation if scope touches >12 new component files or requires new API routes.
```

---

## Prompt 01 — Stitch intake, cache, and gap audit

> **No React conversion in this prompt.**  
> **Skill:** `stitch-intake-audit` · **Delegate fetch to:** `stitch-react` Phase 0

### Copy-paste prompt

```
Stitch intake and gap audit for {{TENANT_SLUG}}.

## Goal
Ensure every in-scope route has cached HTML + PNG locally, mapped to the correct Next.js route, with a gap report against COMPONENT_CHECKLIST.md — BEFORE any React conversion.

## Stitch project
- Name: {{STITCH_PROJECT_NAME}}
- Prompt library: {{STITCH_PROMPTS_HTML}}
- Skill: {{STITCH_REACT_SKILL}} (fetch-only / Phase 0)
- MCP: stitch__list_projects / stitch__list_screens / stitch__get_screen

## Steps

### A. Fetch and cache (stitch-react Phase 0)
For each screen in scope:
1. get_screen → htmlCode.downloadUrl, screenshot.downloadUrl
2. Save to .stitch/designs/{page-slug}.html, .png, .meta.json
3. Use scripts/fetch-stitch.sh if present; else curl -L

Page slug: lowercase, hyphenated ("Homepage" → homepage).

### B. Build screen ↔ route map
Create/update docs/build/notes/stitch-screen-route-map.md:

| Stitch order | Screen title | page-slug | Next route | Scaffold status |
|--------------|--------------|-----------|------------|-----------------|
| 1 | Global chrome | global-chrome | layout | CACHED / MISSING |
| 2 | Homepage | homepage | / | PlaceholderPage / BUILT |

Scaffold status = grep src/app for PlaceholderPage on that route.

### C. Gap audit per route
Compare four signals:
1. Sections in Stitch prompt ({{STITCH_PROMPTS_HTML}} → PROMPTS[].text)
2. Sections in COMPONENT_CHECKLIST.md
3. Sections in cached HTML (grep data-section / headings)
4. Current React page

Output:

| Route | Required sections | In Stitch HTML | In React | Action |
|-------|-------------------|----------------|----------|--------|

### D. Diagnose fake migrations
rg 'dangerouslySetInnerHTML|const html =' src -l
Flag hits for real-JSX conversion in Prompts 03–09.

## Deliverables
1. .stitch/designs/ populated (or MISSING list for human Stitch generation)
2. docs/build/notes/stitch-screen-route-map.md
3. docs/build/notes/stitch-gap-audit-{date}.md with prioritized conversion order:
   Foundation → chrome → home → pathways → content → courses → ai/chat/auth → utility/legal

## Do not
- Convert to React (Prompts 03–09)
- Change globals.css tokens (Prompt 02)

Report summary and blockers.
```

---

## Prompt 02 — Token bridge (wireframe → tenant semantic tokens)

> **Run once per tenant before any page conversion.**  
> **Skill:** `stitch-token-bridge`

### Copy-paste prompt

```
Token bridge: Stitch B&W wireframe palette → {{DESIGN_THEME}} semantic tokens for {{TENANT_SLUG}}.

## Read first
- .stitch/designs/design-system.html (or tailwind.config in any screen <head>)
- {{GLOBALS_CSS}} and tailwind.config.ts
- TENANT_MANIFEST → {{DESIGN_THEME}}, {{DESIGN_CHARTER}}
- {{REFERENCE_REPO}}/docs/internal/design/DESIGN_CHARTER.md (if present)

## Wireframe palette (NEVER ship in components)
| Role | Hex |
| Page bg | #FFFFFF / #F7F7F7 |
| Text primary | #111111 |
| Text secondary | #666666 |
| Border | #E0E0E0 |
| Primary CTA | #111111 fill, white text |

## Semantic mapping (production)
| Stitch intent | Tailwind / CSS variable |
| Page background | bg-background |
| Alt section | bg-muted |
| Primary text | text-foreground |
| Secondary text | text-muted-foreground |
| Borders | border-border |
| Primary CTA | bg-primary text-primary-foreground |
| Cards | bg-card border-border |

## Typography bridge
| Wireframe | Tenant |
| Serif headlines (Georgia) | font-heading (next/font in layout.tsx) |
| Sans body | font-sans |
| Mono metadata | font-mono |

## Tasks
1. Extract spacing rhythm from Stitch HTML (py-16, max-w-7xl, 8px grid) → docs/internal/design/SPACING_NOTES.md
2. Update globals.css ONLY if tenant lacks a required role — ask before changing existing values
3. Ensure tailwind.config.ts fontFamily extends next/font CSS variables
4. Write docs/build/notes/stitch-token-bridge.md — contract for all page conversions

## Rules
- No wireframe hex in tailwind.config named colors
- Do not re-extract tokens per page after this
- Dark mode: every token used must have .dark {} pair

## Deliverables
- docs/build/notes/stitch-token-bridge.md
- Minimal globals.css / tailwind.config.ts changes (approved)
- pnpm typecheck passes

Stop here — do not convert pages.
```

---

## Prompt 03 — Global chrome

> **Stitch order 1.** Run before page clusters.  
> **Skill:** `stitch-page-port` (chrome cluster) + `stitch-react` Phases 2–6

### Copy-paste prompt

```
Migrate global header and footer from Stitch wireframe to {{TENANT_SLUG}} React.

## Sources
- Stitch: .stitch/designs/global-chrome.html
- Reference: {{REFERENCE_REPO}}/src/components/navigation/
- Checklist: COMPONENT_CHECKLIST.md → Global chrome
- Token bridge: docs/build/notes/stitch-token-bridge.md
- Skill: {{STITCH_REACT_SKILL}} (decompose chrome; exclude from per-page conversions)

## Target files
- src/app/(public)/layout.tsx — SiteHeader + main + SiteFooter
- src/components/navigation/site-header.tsx
- src/components/navigation/site-footer.tsx
- src/components/navigation/mobile-nav.tsx

## Required structure (Stitch spec)
### Header (sticky)
Logo → tenantConfig.logo · Pathways · Content dropdown · Courses · Chat · About · Search · Theme · Account

### Footer
Four-column grid · © {year} tenantConfig.name · Powered by Movemental

### Mobile
Hamburger <768px; footer stacks

## Conversion rules
- Chrome lives in layout ONLY — exclude header/footer from individual page stitch-react runs
- shadcn: NavigationMenu, Sheet, Button, DropdownMenu
- Feature-gate nav items: {features.courses && <CoursesLink />}
- Semantic tokens only
- Server layout where possible; client only for mobile menu + theme toggle

## Verify
- [ ] Header/footer on all (public) routes
- [ ] tenantConfig.logo, tenantConfig.copyright
- [ ] pnpm typecheck
- [ ] COMPONENT_CHECKLIST chrome → BUILT

Update REFERENCE_PAGE_COMPARISON if present.
```

---

## Prompt 04 — Home and marketing pages

> **Stitch orders 2–3, 30–31.**  
> **Skill:** `stitch-page-port` · **Primitive:** `stitch-react` per route

### Copy-paste prompt (4a — Homepage)

```
Stitch → React migration: Homepage (/) for {{TENANT_SLUG}}.

## Invoke skills
1. Read {{STITCH_REACT_SKILL}} — follow Archive Protocol + decompose phases
2. Read .claude/skills/stitch-page-port/SKILL.md — tenant copy + feature gates + synthesis

## Sources
- Stitch: .stitch/designs/homepage.html + .png
- Stitch spec: STITCH_ROUTE_INDEX order 2, id=home
- Reference: {{REFERENCE_REPO}}/src/app/(public)/page.tsx + src/components/home/
- Checklist: COMPONENT_CHECKLIST.md → "/"
- Token bridge: docs/build/notes/stitch-token-bridge.md

## Required section order (exact)
1. Hero — headline + subhead + 2 CTAs | portrait
2. Social proof — logo strip
3. Pathways grid — 5 cards (manifest pathway titles)
4. AI Lab teaser — if features.chat
5. Content sampler — Articles/Books/Courses tabs
6. Course spotlight
7. Newsletter
8. About teaser → /about

Optional: Assessment CTA (features.assessments), Concierge/Intake

## L4 components
| Section | Path | Data |
| Hero | home/hero.tsx | tenantConfig.hero |
| SocialProof | home/social-proof.tsx | static / public/images/orgs |
| PathwaysGrid | home/pathways-grid.tsx | tenantConfig.themes / usePathwaysList |
| AILabTeaser | home/ai-lab-teaser.tsx | features.chat |
| ContentSampler | home/content-sampler.tsx | useContentItemsList (empty state if no data) |
| CourseSpotlight | home/course-spotlight.tsx | useCoursesList |
| Newsletter | home/newsletter.tsx | tenantConfig.newsletter |
| AboutTeaser | home/about-teaser.tsx | tenantConfig |

## Per-route procedure (stitch-page-port)
1. Visual audit — HTML + PNG
2. Read reference page for data-wiring patterns
3. Archive page.tsx → page-old.tsx
4. Delegate HTML decomposition to stitch-react OR follow its phase checklist manually
5. Apply token bridge — no wireframe hex
6. Wire hooks if they exist; else static manifest copy + flag for Prompts 13–14
7. Compose Server Component page.tsx with feature gates at page level
8. Handle loading/empty/error in client sections

## Incomplete template
For each checklist section NOT in Stitch HTML: synthesize from {{REFERENCE_REPO}} structure + tenant tokens + manifest copy. Mark PARTIAL if Stitch gap.

## Tenant copy
Use TENANT_MANIFEST pathway table + {{CONTENT_RESEARCH}} — NOT Brad/Alan placeholder names.

Verify: pnpm typecheck, one h1, COMPONENT_CHECKLIST "/" → BUILT or PARTIAL. Emit stitch-react Phase 8 report.
```

### Copy-paste prompt (4b — About, Contact, Pricing)

```
Stitch → React: About, Contact, Pricing for {{TENANT_SLUG}}.

## Routes
| Route | Stitch order | Cache |
| /about | 3 | about.html |
| /contact | 30 | contact.html |
| /pricing | 31 | pricing.html |

For each route: follow stitch-page-port procedure + stitch-react decomposition.

### /about sections
Hero → Bio (3–4 paras) → MissionQuote → Affiliations → SpeakingMedia → ContactCTA

### /contact sections
Header → Form (tenantConfig.contact) → ContactInfo → MapPlaceholder

### /pricing sections
Header → PlanCards → FAQ → EnterpriseCTA

Content from {{CONTENT_RESEARCH}} and tenantConfig.

Verify checklist rows. Archive page-old.tsx per route.
```

---

## Prompt 05 — Pathways pages

> **Stitch orders 4–6.**

### Copy-paste prompt

```
Stitch → React: Pathways cluster for {{TENANT_SLUG}}.

## Routes
| # | Route | Cache slug |
| 4 | /pathways | pathways-hub |
| 5 | /pathways/[slug] | pathway-detail |
| 6 | /pathways/map | pathways-map |

## Reference
{{REFERENCE_REPO}}/src/app/(public)/pathways/
{{REFERENCE_REPO}}/src/components/pathways/
src/lib/content/pathways/ or tenantConfig.themes

## Section requirements (summary)
- /pathways: Hero → CardGrid (5) → LearningSequence → InterconnectionMap → ArchiveGrid
- /pathways/[slug]: Hero → StickySubNav → Framework → Practices → CaseStudy → Related → FAQ → NextPathway
- /pathways/map: Header → MapCanvas → Legend → DetailPanel

## Pathway slugs (from manifest)
{{PATHWAY_SLUG_1}} … {{PATHWAY_SLUG_5}} with titles from TENANT_MANIFEST

## Hooks
usePathwaysList / usePathwayBySlug if present; else static modules in lib/content/pathways/

Per route: stitch-react decomposition, token bridge, archive protocol, checklist update.
```

---

## Prompt 06 — Content library pages

> **Stitch orders 7–16.**

### Copy-paste prompt

```
Stitch → React: Content library cluster for {{TENANT_SLUG}}.

## Routes (convert in order)
| # | Route | Cache slug |
| 7 | /content | content-hub |
| 8 | /content/articles | articles-list |
| 9 | /content/articles/[slug] | article-detail |
| 10 | /content/books | books-list |
| 11 | /content/books/[slug] | book-detail |
| 12 | /content/books/[slug]/read | book-reader |
| 13 | /content/podcasts | podcasts-list |
| 14 | /content/podcasts/[slug] | podcast-detail |
| 15 | /content/videos | videos-list |
| 16 | /content/videos/[slug] | video-detail |

## Reference
{{REFERENCE_REPO}}/src/app/(public)/content/
{{L4_SECTIONS}} → Content Sections

## L4 directory
src/components/content/ — mirror reference decomposition

## Hooks
useContentItemsList, use-book-reader, podcast/video hooks — wire if exist; empty state if zero DB rows

## Book reader
Immersive shell: minimal chrome, progress, chapter nav, drawer TOC — NO marketing sections

## Feature flags
If !features.articles: route may show coming-soon OR hide nav link — document product choice in manifest

For each route: archive page-old.tsx, stitch-react decompose, token bridge, checklist BUILT/PARTIAL.
```

---

## Prompt 07 — Course pages

> **Stitch orders 17–24.** May require `tenant-structural-port` or `../migration/02` first.

### Copy-paste prompt

```
Stitch → React: Courses cluster for {{TENANT_SLUG}}.

## Preconditions
If src/hooks/custom/use-course-learn.ts or course API routes missing:
- Run tenant-structural-port OR docs/build/prompts/migration/02-course-infrastructure-diff-and-port.md first
- OR implement UI with static stubs and flag BLOCKED in checklist

## Routes
| # | Route |
| 17 | /courses |
| 18 | /courses/[slug] |
| 19 | /courses/[slug]/learn |
| 20 | /courses/[slug]/overview |
| 21 | /courses/[slug]/enroll |
| 22 | /courses/[slug]/cohort |
| 23 | /courses/[slug]/resources |
| 24 | /courses/[slug]/journal |

## Hub nav (all sub-routes)
Learn · Overview · Cohort · Resources · Journal · Enroll — CourseHubNav + CourseHubShell

## Learn player
Match {{REFERENCE_REPO}} CourseLearnLayout proportions (sidebar ~25–30%, content ~70–75%), tenant tokens only.
Run /course-ux after learn player built.

## Reference-only routes (port from code, not Stitch)
/courses/[slug]/certificate, /courses/[slug]/player — if features.certificates

Per route: stitch-page-port + stitch-react. Wire use-course-learn when available.
```

---

## Prompt 08 — AI, chat, auth, account

> **Stitch orders 25–29.**

### Copy-paste prompt

```
Stitch → React: AI / chat / auth / account for {{TENANT_SLUG}}.

## Routes
| # | Route | Notes |
| 25 | /ai-lab | Hero + feature cards + chat preview |
| 26 | /chat | Sidebar + messages + input; label {{AI_ASSISTANT_LABEL}} |
| 27 | /auth/signin | Centered card + OAuth |
| 28 | /auth/signup | Create if missing |
| 29 | /account | Sidebar dashboard shell |

## Route normalization
Replace /auth placeholder with /auth/signin + /auth/signup; redirect /auth → /auth/signin

## Feature gates
- features.chat: if false, hide nav links; chat page may show offlineMessage
- features.auth: gate signup/signin

## Auth constraints
Supabase @supabase/ssr only — never auth-helpers-nextjs

Components: ai-lab/, chat/, auth/, account/
```

---

## Prompt 09 — Info, utility, optional, legal

> **Stitch orders 32–35 + non-Stitch legal routes.**

### Copy-paste prompt

```
Stitch → React: Utility and legal pages for {{TENANT_SLUG}}.

## Stitch routes
| # | Route |
| 32 | /search |
| 33 | /checkout |
| 34 | /assessments | gate features.assessments |
| 35 | tenant-unique | ONLY if manifest includes (e.g. /reneighbor is EXCLUDED for most tenants) |

## Non-Stitch legal (port minimal structure from reference)
/privacy, /terms, /accessibility, /donate?, /newsletter
Plus manifest tenant-unique routes

## Rules
- Checkout: static until Stripe wired
- Legal: leader-specific copy placeholders flagged for human review
- Skip excluded routes per TENANT_MANIFEST

Per route: stitch-react if cache exists; else port reference structure + tenant tokens.
```

---

## Prompt 10 — UI validation gate

> **Run after every UI slice (03–09).**  
> **Skill:** `stitch-migration-validate`

### Copy-paste prompt

```
Stitch migration UI validation gate for {{TENANT_SLUG}}.

Scope: {LIST ROUTES IN THIS SLICE}

## Commands
pnpm typecheck
pnpm lint
pnpm build
rg 'PlaceholderPage' src/app
rg 'dangerouslySetInnerHTML' src
rg '#111111|#666666' src/components --glob '*.tsx'

PlaceholderPage allowed only on routes checklist explicitly defers.

## Visual verification
For each converted route:
1. Compare .stitch/designs/{slug}.png with dev screenshot
2. Section order vs COMPONENT_CHECKLIST.md
3. Light + dark mode spot check

## Documentation updates
1. COMPONENT_CHECKLIST.md — SCAFFOLD | PARTIAL | BUILT | N/A | BLOCKED
2. docs/internal/engineering/REFERENCE_PAGE_COMPARISON.md
3. Close gaps in docs/build/notes/stitch-gap-audit-*.md
4. README migration checklist

## Conversion report (stitch-react Phase 8)
- Screens converted
- Archived page-old files
- New component paths
- Hooks wired vs static stubs
- Issues flagged for Prompts 11–16 or tenant-structural-port

## PR checklist
- [ ] Branch slice/Sxx-stitch-*
- [ ] No hex in components
- [ ] tenantConfig for copy
- [ ] Feature flags respected
- [ ] No {{SOURCE_TENANT_NAME}} / {{STITCH_PLACEHOLDER_TENANT}} leaks
- [ ] CI green

Do not merge until Prompt 10 passes.
```

---

## Prompt 11 — Supabase org and tenant identity

> **Skill:** `tenant-backend-parity` §11 · `tenant-migrate` Phase 1

### Copy-paste prompt

```
Supabase org and tenant identity audit for {{TENANT_SLUG}}.

## Read first
- TENANT_MANIFEST.md
- .env.local.example
- {{TENANT_CONFIG}}
- {{TENANT_MIGRATE_SKILL}} Phase 1

## Supabase MCP — project {{SUPABASE_PROJECT_ID}}

1. Org row: SELECT ... FROM organizations WHERE slug = '{{TENANT_SLUG}}';
   Confirm id == {{TENANT_ORG_ID}}. If missing: STOP — do not create without approval.

2. Content counts by organization_id: books, articles, courses, podcasts, videos, pathways

3. Storage: bucket media-library, prefix {{STORAGE_PREFIX}}

4. AI/vector if features.chat: org-scoped corpus; OPENAI_VECTOR_STORE_ID tenant-specific

5. Env alignment: TENANT_ORG_ID, DATABASE_URL, NEXT_PUBLIC_SUPABASE_URL

6. Middleware: no hardcoded {{SOURCE_TENANT_SLUG}} paths

## Deliverable
docs/build/notes/supabase-org-audit-{{TENANT_SLUG}}-{date}.md

Do not INSERT/UPDATE orgs. Do not port UI in this prompt.
```

---

## Prompt 12 — Type-safety chain port

> **Skill:** `tenant-backend-parity` §12 · `type-safety-chain`

### Copy-paste prompt

```
Type-safety chain port for {{TENANT_SLUG}}.

Branch: slice/Sxx-backend-type-chain

## Inventory (report first)
Diff {{REFERENCE_REPO}} vs target:
- src/lib/db, scripts/
- src/hooks/simplified/
- src/lib/services/

## Port missing generators; run:
pnpm generate:zod
pnpm generate:services
pnpm generate:routes
pnpm generate:hooks
pnpm validate:all

## Rules
- Never hand-edit src/hooks/simplified/* or generated zod
- Every service filters by organization_id / {{TENANT_ORG_ID}}
- Never modify Drizzle schema for UI convenience
- db:generate only with human coordination

Report pass/fail per layer.
```

---

## Prompt 13 — Services and API routes parity

### Copy-paste prompt

```
Services and API routes parity for {{TENANT_SLUG}}.

diff -rq {{REFERENCE_REPO}}/src/app/api <target>/src/app/api
diff -rq {{REFERENCE_REPO}}/src/lib/services <target>/src/lib/services

Port missing handlers. Routes call services, not raw db.
Priority when courses enabled: progress, access, discussions, assessments
Plus /api/search, chat/agent when features on.

Confirm organization_id scoping. Do not port {{SOURCE_TENANT_SLUG}}-only demo routes.

Verify: pnpm routes:check && pnpm services:check
```

---

## Prompt 14 — Hooks layer parity

### Copy-paste prompt

```
Hooks layer parity for {{TENANT_SLUG}}.

diff -rq {{REFERENCE_REPO}}/src/hooks/{simplified,custom} <target>/...

Build UI→hook map from COMPONENT_CHECKLIST.md.

Port priority custom hooks: use-course-learn, progress/enrollment, chat, content readers.

After each hook ports: wire corresponding stitch-migrated section (replace static stub).
Zero DB rows → keep hook wired, show empty state.

Verify: pnpm hooks:check
Update checklist hook column.
```

---

## Prompt 15 — Tenant config and feature alignment

### Copy-paste prompt

```
Align {{TENANT_CONFIG}} with Supabase content counts for {{TENANT_SLUG}}.

## Read
- Prompt 11 audit doc
- tenant.schema.ts
- {{CONTENT_RESEARCH}}

## Update
1. nav — canonical routes (/content not /library)
2. hero, pathways, featured content slugs
3. contentTypes.*.availableSlugs
4. features.* — must match DB counts (false if zero rows)
5. chat / aiLab labels → {{AI_ASSISTANT_LABEL}}

Schema-valid. pnpm typecheck.

Run /tenant-check or manifest leak grep patterns on src/.
```

---

## Prompt 16 — Backend validation and cutover

### Copy-paste prompt

```
Full migration validation and cutover for {{TENANT_SLUG}}.

## Commands (fix bottom-up on failure)
pnpm db:check
pnpm contracts:check
pnpm services:check
pnpm routes:check
pnpm hooks:check
pnpm ui:check
pnpm validate:all
pnpm verify:tenant-org
pnpm build

## Tests
pnpm test:run
pnpm test:run -- courses (if courses enabled)

## Documentation
1. REFERENCE_PAGE_COMPARISON.md — recalculate totals, today's date
2. COMPONENT_CHECKLIST.md — all P0 routes BUILT or N/A
3. TENANT_MANIFEST — note migration complete date

## Definition of done
| Layer | Criterion |
| IA | Checklist section order |
| UI | No PlaceholderPage, no dangerouslySetInnerHTML, semantic tokens |
| Types | validate:all green |
| Tenant | verify:tenant-org green, no leaks |
| Features | flags match DB |

## Optional Phase D
If course player or route gaps remain: docs/build/prompts/migration/ (Alan structural port)

Output PR body with test plan. Do not push unless user asks.
```

---

## Per-route ad-hoc prompt

When a route is not covered by Prompts 04–09, use [PROMPT_TEMPLATE.md](./PROMPT_TEMPLATE.md).

---

## Cluster reference (section orders)

Full section specs live in `.claude/skills/stitch-page-port/references/clusters.md`. Summary:

| Cluster | Stitch orders | Routes |
|---------|---------------|--------|
| Global chrome | 1 | `(public)/layout` |
| Home & marketing | 2–3, 30–31 | `/`, `/about`, `/contact`, `/pricing` |
| Pathways | 4–6 | `/pathways`, `/pathways/[slug]`, `/pathways/map` |
| Content | 7–16 | `/content/*` |
| Courses | 17–24 | `/courses/*` |
| AI / auth | 25–29 | `/ai-lab`, `/chat`, `/auth/*`, `/account` |
| Utility | 32–34 | `/search`, `/checkout`, `/assessments?` |

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Stitch MCP auth fails | Ask human for project ID; manually download HTML/PNG to `.stitch/designs/` |
| Screen missing from Stitch | Log MISSING in gap audit; human generates from `stitch-prompts.html` |
| Checklist section not in Stitch HTML | Synthesize from reference + tokens (incomplete template policy) |
| Hook missing | Static stub + flag BLOCKED; run Prompts 13–14 |
| Course learn UX wrong | Phase D: `../migration/02–03` or `tenant-structural-port` |
| Raw HTML in page.tsx | Re-run stitch-react; grep `dangerouslySetInnerHTML` |
| Wireframe hex in components | Re-apply Prompt 02 token bridge |
| Alan/Brad copy in UI | Prompt 15 + leak grep from TENANT_MANIFEST |

---

*Tenant-agnostic agent runbook. Fork TENANT_MANIFEST.template.md per leader. Last updated: 2026-07-04.*
