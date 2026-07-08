# Route cluster section specs

Per-cluster section order, routes, and L4 component paths for `stitch-page-port`.
Routes/copy are tenant-agnostic; pathway names, featured titles, and the AI assistant
label come from `TENANT_MANIFEST.md`. Stitch order numbers reference the shared
`{{STITCH_PROMPTS_HTML}}` library. Section order is authoritative from the Stitch prompt
library; if sources disagree, **Stitch prompt order wins for IA** — log conflicts in the gap audit.

---

## Global chrome (Stitch order 1) → `(public)/layout.tsx`

- **Header (sticky):** Logo → `tenantConfig.logo.text` · primary nav (Pathways · Content
  dropdown [Articles, Books, Podcasts, Videos] · Courses · Chat · About) · utility (Search ·
  Theme toggle · Account/Sign in).
- **Footer:** four-column link grid (Explore · About · Legal · Connect) · bottom bar
  `© {year} {tenantConfig.name} · Powered by Movemental`.
- **Mobile:** hamburger <768px; footer stacks single column.
- Components: `navigation/site-header.tsx`, `site-footer.tsx`, `mobile-nav.tsx`,
  optional `theme/theme-toggle.tsx`. Links respect feature flags.

---

## Home & marketing (Stitch orders 2–3, 30–31)

### `/` — homepage
1. Hero (split: headline + subhead + 2 CTAs | portrait)
2. Social proof (logo strip + optional testimonial)
3. Pathways grid (5 cards — manifest pathway titles)
4. AI Lab teaser — gate `features.chat`
5. Content sampler (Articles / Books / Courses tabs, 3 cards each)
6. Course spotlight (featured course card)
7. Newsletter (email + subscribe)
8. About teaser (bio paragraph + link `/about`)

Optional if enabled: Assessment CTA (`features.assessments`), Concierge/Intake.

| Section | Path | Data |
|---------|------|------|
| Hero | `home/hero.tsx` | `tenantConfig.hero` |
| SocialProof | `home/social-proof.tsx` | static |
| PathwaysGrid | `home/pathways-grid.tsx` | `tenantConfig.themes` / `usePathwaysList` |
| AILabTeaser | `home/ai-lab-teaser.tsx` | `tenantConfig.chat`, `features.chat` |
| ContentSampler | `home/content-sampler.tsx` | `useContentItemsList` (stub if empty) |
| CourseSpotlight | `home/course-spotlight.tsx` | `useCoursesList` (stub if empty) |
| Newsletter | `home/newsletter.tsx` | `tenantConfig.newsletter` |
| AboutTeaser | `home/about-teaser.tsx` | `tenantConfig` |

### `/about` (order 3)
Hero (name, role, portrait) → Bio (3–4 paras ~680px) → Mission pull quote →
Affiliations logo grid → Speaking & media list → Contact CTA. Content from research profile.

### `/contact` (order 30)
Header → Form (`contact/contact-form.tsx`, `tenantConfig.contact`) → Contact info column → optional map placeholder.

### `/pricing` (order 31)
Header → 3-tier plan cards (`pricing/pricing-plans.tsx`, static until Stripe) → billing toggle → FAQ → enterprise CTA.

---

## Pathways (Stitch orders 4–6)

| Route | Order | Cache |
|-------|-------|-------|
| `/pathways` | 4 | pathways-hub.html |
| `/pathways/[slug]` | 5 | pathway-detail.html |
| `/pathways/map` | 6 | pathways-map.html |

- **`/pathways`:** Hero → pathway card grid (5 large cards) → learning sequence
  (Start → Explore → Practice → Integrate) → interconnection map placeholder → archive/browse grid.
- **`/pathways/[slug]`:** Hero + Start CTA → sticky sub-nav (Overview · Framework · Practices ·
  Resources · FAQ) → framework overview (2-col + diagram) → key practices (numbered expandable) →
  case study split → related content (3-card) → FAQ accordion → next pathway CTA.
- **`/pathways/map`:** header + filter controls → map canvas (SVG/styled nodes) → legend → detail panel.
- Components: `pathways/pathways-hub.tsx`, `pathway-detail.tsx`, `pathways-map.tsx`;
  slug data from `lib/content/pathways/` or `tenantConfig.themes`. Hook: `usePathwaysList` if present.

---

## Content library (Stitch orders 7–16)

| # | Route | Cache slug |
|---|-------|-----------|
| 7 | `/content` | content-hub |
| 8 | `/content/articles` | articles-list |
| 9 | `/content/articles/[slug]` | article-detail |
| 10 | `/content/books` | books-list |
| 11 | `/content/books/[slug]` | book-detail |
| 12 | `/content/books/[slug]/read` | book-reader |
| 13 | `/content/podcasts` | podcasts-list |
| 14 | `/content/podcasts/[slug]` | podcast-detail |
| 15 | `/content/videos` | videos-list |
| 16 | `/content/videos/[slug]` | video-detail |

Section summaries:
- `/content`: Hero + search · type tabs · filter bar · 12-card grid · pagination.
- `/content/articles`: header · featured hero card · 3-col grid · load more · loading skeleton.
- `/content/articles/[slug]`: article header · hero image · prose column · sticky TOC sidebar ·
  author bio · related · comments placeholder.
- `/content/books`: featured split hero · 4-col cover grid · pagination.
- `/content/books/[slug]`: cover + metadata hero · TOC accordion · author · related · reviews placeholder.
- `/content/books/[slug]/read`: reader shell — minimal chrome, progress, chapter nav, drawer TOC, warmer bg (no marketing sections).
- Podcasts / Videos: follow Stitch section lists.

Components mirror the reference decomposition: `content/{articles,books,book-reader,podcast-library,video-library}/`.
Hooks: `useContentItemsList`, `use-book-reader` (static empty state if absent).

---

## Courses (Stitch orders 17–24)

Requires course infrastructure — if hooks/components are missing, run `tenant-structural-port`
(course infra) first OR implement with static stubs and flag in the gap audit.

| # | Route |
|---|-------|
| 17 | `/courses` |
| 18 | `/courses/[slug]` |
| 19 | `/courses/[slug]/learn` |
| 20 | `/courses/[slug]/overview` |
| 21 | `/courses/[slug]/enroll` |
| 22 | `/courses/[slug]/cohort` |
| 23 | `/courses/[slug]/resources` |
| 24 | `/courses/[slug]/journal` |

- **Hub nav** (below site header, all sub-routes): Learn · Overview · Cohort · Resources · Journal · Enroll (tab bar, active state).
- **`/courses`:** featured course card · 2-col grid · Available / Coming soon filter.
- **`/courses/[slug]`:** hero + enroll CTAs · stats bar · learn list · syllabus accordion · instructor · testimonials · pricing · FAQ.
- **`/courses/[slug]/learn`:** top bar + progress · left sidebar module accordion · lesson panel ·
  tabs (Content/Notes/Discussion) · prev/next bar. Match reference `CourseLearnLayout` proportions, tenant tokens only.
- Components: `courses/CourseHubShell.tsx`, `CourseHubNav.tsx`, `courses/learn/{CourseLearnLayout,CourseLearnSidebar,LessonPanel}.tsx`.
- Run `course-ux` after the learn player is built.

---

## AI / chat / auth / account (Stitch orders 25–29)

| # | Route | Notes |
|---|-------|-------|
| 25 | `/ai-lab` | Hero + Start CTA · 3 feature cards · sample chat preview · disclaimer |
| 26 | `/chat` | Left sidebar (new chat + history) · message panel · input + suggested prompts; label `{{AI_ASSISTANT_LABEL}}` |
| 27 | `/auth/signin` | Centered card form · OAuth Google row · cross-links; gate `features.auth` |
| 28 | `/auth/signup` | Create if missing |
| 29 | `/account` | Sidebar (Profile · My Learning · Bookmarks · Library · Settings) · welcome · continue-learning cards · recent activity |

**Route normalization:** replace a single `/auth` placeholder with `/auth/signin` + `/auth/signup`;
add redirect `/auth → /auth/signin`. Chat: if `!features.chat`, still build the shell but show
`tenantConfig.chat.offlineMessage` (or hide nav links only — document the product choice).
Components: `ai-lab/`, `chat/`, `auth/`, `account/`.

---

## Utility / legal / tenant-unique (Stitch orders 32–35 + non-Stitch)

| # | Route | Notes |
|---|-------|-------|
| 32 | `/search` | search bar prefilled · results count · filter tabs · mixed results · empty-state variant |
| 33 | `/checkout` | split form + order summary · secure note · static until Stripe |
| 34 | `/assessments` | optional — gate `features.assessments`; else omit nav link |
| 35 | tenant-unique | **excluded unless the manifest lists it in scope** |

Legal/info routes (no Stitch prompt — port minimal prose structure from the reference):
`/privacy`, `/terms`, `/accessibility`, `/donate?`, `/newsletter`, plus manifest
tenant-unique routes (e.g. `/frameworks`, `/organizations`). For each: read the checklist,
convert from cache if present else port minimal structure from the reference, replace
`PlaceholderPage`, update checklist. Never introduce another tenant's unique routes.
