# Component checklist template — Stitch migration

> Fork to `COMPONENT_CHECKLIST.md` (in this folder or `docs/build/`) when onboarding a new tenant. Replace `{{TENANT_SLUG}}`, pathway slugs, and tenant-unique rows.

Living matrix: **route → required sections → L4 components → hooks → status**.

**Sources:** [STITCH_ROUTE_INDEX.md](./STITCH_ROUTE_INDEX.md), `L5_PAGES.md`, `L4_SECTIONS.md`.

---

## Status legend

| Status | Meaning |
|--------|---------|
| `SCAFFOLD` | `PlaceholderPage` or empty route |
| `PARTIAL` | Some sections built; gaps documented |
| `BUILT` | All required sections present; Prompt 10 pass |
| `N/A` | Not in tenant scope (see TENANT_MANIFEST) |
| `BLOCKED` | Blocked on backend prompts 11–16 |

---

## Global chrome

| Route / surface | Sections | L4 components | Hooks / config | Stitch # | Status |
|-----------------|----------|-----------------|----------------|----------|--------|
| `(public)/layout` | Header, Footer, Mobile nav | `navigation/site-header`, `site-footer`, `mobile-nav` | tenantConfig, features | 1 | SCAFFOLD |

---

## Home and marketing

| Route | Sections (order) | L4 components | Hooks / config | Stitch # | Status |
|-------|------------------|-----------------|----------------|----------|--------|
| `/` | Hero → SocialProof → Pathways → AILabTeaser? → ContentSampler → CourseSpotlight → Newsletter → AboutTeaser | `home/*` | tenantConfig.hero, content hooks, features.chat | 2 | SCAFFOLD |
| `/about` | Hero → Bio → MissionQuote → Affiliations → SpeakingMedia → ContactCTA | `about/*` | tenantConfig, research profile | 3 | SCAFFOLD |
| `/contact` | Header → Form → ContactInfo → MapPlaceholder | `contact/*` | tenantConfig.contact | 30 | SCAFFOLD |
| `/pricing` | Header → PlanCards → FAQ → EnterpriseCTA | `pricing/*` | static / tenantConfig.pricing | 31 | SCAFFOLD |

---

## Pathways

| Route | Sections (order) | L4 components | Hooks / config | Stitch # | Status |
|-------|------------------|-----------------|----------------|----------|--------|
| `/pathways` | Hero → CardGrid → LearningSequence → InterconnectionMap → ArchiveGrid | `pathways/pathways-hub` | tenantConfig.themes / usePathwaysList | 4 | SCAFFOLD |
| `/pathways/[slug]` | Hero → StickySubNav → Framework → Practices → CaseStudy → Related → FAQ → NextPathway | `pathways/pathway-detail` | pathway by slug | 5 | SCAFFOLD |
| `/pathways/map` | Header → MapCanvas → Legend → DetailPanel | `pathways/pathways-map` | static graph | 6 | SCAFFOLD |

**Tenant pathway slugs:** `{{PATHWAY_SLUG_1}}` … `{{PATHWAY_SLUG_5}}`

---

## Content library

| Route | Sections (order) | L4 components | Hooks | Stitch # | Status |
|-------|------------------|-----------------|-------|----------|--------|
| `/content` | Hero → Tabs → Filters → Grid → Pagination | `content/content-library` | useContentItemsList | 7 | SCAFFOLD |
| `/content/articles` | Header → Featured → Grid → LoadMore | `content/articles/*` | useContentItemsList | 8 | SCAFFOLD |
| `/content/articles/[slug]` | Header → HeroImg → Prose → Sidebar → AuthorBio → Related | `content/articles/detail` | article by slug | 9 | SCAFFOLD |
| `/content/books` | Header → Featured → Grid → Pagination | `content/books/*` | useContentItemsList | 10 | SCAFFOLD |
| `/content/books/[slug]` | Hero → TOC → Author → Related → Reviews | `book-detail/*` | book by slug | 11 | SCAFFOLD |
| `/content/books/[slug]/read` | ReaderHeader → Prose → FooterNav → ChapterDrawer | `book-reader/*` | use-book-reader | 12 | SCAFFOLD |
| `/content/podcasts` | Header → Featured → SeriesGrid → LatestEpisodes | `podcast-library/*` | podcasts hooks | 13 | SCAFFOLD |
| `/content/podcasts/[slug]` | SeriesHero → Player → EpisodeList → About → Related | `podcast-library/detail` | series by slug | 14 | SCAFFOLD |
| `/content/videos` | Header → Featured → Grid → Pagination | `video-library/*` | videos hooks | 15 | SCAFFOLD |
| `/content/videos/[slug]` | Player → Metadata → Transcript → Related → Share | `video-library/detail` | video by slug | 16 | SCAFFOLD |

---

## Courses

| Route | Sections (order) | L4 components | Hooks | Stitch # | Status |
|-------|------------------|-----------------|-------|----------|--------|
| `/courses` | Header → Featured → Grid → Filter | `courses/catalog` | useCoursesList | 17 | SCAFFOLD |
| `/courses/[slug]` | Hero → Stats → LearnList → Syllabus → Instructor → Testimonials → Pricing → FAQ | `courses/CourseSalesLandingContent` | course by slug | 18 | SCAFFOLD |
| `/courses/[slug]/learn` | TopBar → Sidebar → LessonPanel → Tabs → BottomBar | `courses/learn/*` | use-course-learn | 19 | SCAFFOLD |
| `/courses/[slug]/overview` | Header → Description → FullSyllabus → Requirements → CTA | `courses/CourseOverviewContent` | course by slug | 20 | SCAFFOLD |
| `/courses/[slug]/enroll` | HubNav → EnrollmentCard → Included → Guarantee | `courses/CourseEnrollForm` | enrollment | 21 | SCAFFOLD |
| `/courses/[slug]/cohort` | HubNav → LiveCall → Discussion → Facilitators → Calendar | `courses/CourseCohortContent` | cohort | 22 | SCAFFOLD |
| `/courses/[slug]/resources` | HubNav → Downloads → Glossary → Links | `courses/CourseResourcesContent` | resources | 23 | SCAFFOLD |
| `/courses/[slug]/journal` | HubNav → NewEntry → Timeline → EmptyState | `courses/journal` | journal | 24 | SCAFFOLD |
| `/courses/[slug]/certificate` | Certificate view | `courses/learn/Certificate*` | features.certificates | — | SCAFFOLD |

**Shared:** `CourseHubNav` on all `/courses/[slug]/*` sub-routes.

---

## AI, chat, auth, account

| Route | Sections | L4 components | Hooks / config | Stitch # | Status |
|-------|----------|-----------------|----------------|----------|--------|
| `/ai-lab` | Hero → FeatureCards → ChatPreview → Disclaimer | `ai-lab/*` | features.chat | 25 | SCAFFOLD |
| `/chat` | Sidebar → Messages → Input → Suggestions | `chat/*` | chat hooks | 26 | SCAFFOLD |
| `/auth/signin` | Logo → Form → OAuth → FooterLink | `auth/sign-in-form` | features.auth | 27 | SCAFFOLD |
| `/auth/signup` | Logo → Form → OAuth → FooterLink | `auth/sign-up-form` | features.auth | 28 | SCAFFOLD |
| `/account` | Sidebar → Welcome → ContinueLearning → Activity → QuickLinks | `account/*` | session | 29 | SCAFFOLD |

---

## Utility and optional

| Route | Sections | L4 components | Hooks | Stitch # | Status |
|-------|----------|-----------------|-------|----------|--------|
| `/search` | SearchBar → Count → Tabs → Results → EmptyState | `search/*` | search API | 32 | SCAFFOLD |
| `/checkout` | Form → OrderSummary → SecurityNote | `pricing/checkout` | Stripe stub | 33 | SCAFFOLD |
| `/assessments` | Header → Cards → HowItWorks | `assessments/*` | features.assessments | 34 | SCAFFOLD |
| `/reneighbor` | — | — | — | 35 | N/A |

---

## Tenant-unique routes (add rows per TENANT_MANIFEST)

| Route | Sections | L4 components | Status |
|-------|----------|-----------------|--------|
| `{{TENANT_UNIQUE_ROUTE}}` | … | … | SCAFFOLD |

---

## Incomplete template completion rules

When **Status** is `PARTIAL` or Stitch screen lacks a section:

1. Read `{{REFERENCE_REPO}}` equivalent section for behavior and data shape.
2. Build missing section with tenant semantic tokens (`bg-background`, `text-muted-foreground`).
3. Use tenant copy from manifest / `tenant.config.ts` — not Stitch placeholder tenant.
4. Add loading skeleton and empty state for data-driven sections.
5. Set `PARTIAL` with note: synthesized vs from Stitch cache.

---

*Template — copy to COMPONENT_CHECKLIST.md and customize for {{TENANT_SLUG}}.*
