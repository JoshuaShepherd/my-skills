# Stitch route index — prompt library ↔ Next.js routes

Canonical mapping from the **Movemental Base Wireframe** Stitch prompt library (`brad-brisco/docs/build/stitch-prompts.html`) to Next.js routes. Section order in each prompt is the **source of truth** for IA; `L5_PAGES.md` is the code reference.

Use during Prompt 01 gap audit and when filling [COMPONENT_CHECKLIST.md](./COMPONENT_CHECKLIST.template.md).

---

## Foundation and chrome

| Order | Stitch id | Route | Cache slug (typical) |
|-------|-----------|-------|----------------------|
| 0 | foundation | — (Stitch project setup) | `design-system` |
| 1 | chrome | `(public)/layout` | `global-chrome` |

---

## Public routes

| Order | Stitch id | Route | Required sections (summary) |
|-------|-----------|-------|----------------------------|
| 2 | home | `/` | Hero → SocialProof → Pathways → AILab? → ContentSampler → CourseSpotlight → Newsletter → AboutTeaser |
| 3 | about | `/about` | Hero → Bio → MissionQuote → Affiliations → SpeakingMedia → ContactCTA |
| 4 | pathways-hub | `/pathways` | Hero → CardGrid → LearningSequence → InterconnectionMap → ArchiveGrid |
| 5 | pathway-detail | `/pathways/[slug]` | Hero → StickySubNav → Framework → Practices → CaseStudy → Related → FAQ → NextPathway |
| 6 | pathways-map | `/pathways/map` | Header → MapCanvas → Legend → DetailPanel |
| 7 | content-hub | `/content` | Hero → Tabs → Filters → Grid → Pagination |
| 8 | articles-list | `/content/articles` | Header → Featured → Grid → LoadMore |
| 9 | article-detail | `/content/articles/[slug]` | Header → HeroImg → Prose → Sidebar → AuthorBio → Related → Comments? |
| 10 | books-list | `/content/books` | Header → Featured → Grid → Pagination |
| 11 | book-detail | `/content/books/[slug]` | Hero → TOC → Author → Related → Reviews |
| 12 | book-reader | `/content/books/[slug]/read` | ReaderHeader → Prose → FooterNav → ChapterDrawer |
| 13 | podcasts-list | `/content/podcasts` | Header → Featured → SeriesGrid → LatestEpisodes |
| 14 | podcast-detail | `/content/podcasts/[slug]` | SeriesHero → Player → EpisodeList → About → Related |
| 15 | videos-list | `/content/videos` | Header → Featured → Grid → Pagination |
| 16 | video-detail | `/content/videos/[slug]` | Player → Metadata → Transcript → Related → Share |
| 17 | courses-list | `/courses` | Header → Featured → Grid → Filter |
| 18 | course-landing | `/courses/[slug]` | Hero → Stats → LearnList → Syllabus → Instructor → Testimonials → Pricing → FAQ |
| 19 | course-learn | `/courses/[slug]/learn` | TopBar → Sidebar → LessonPanel → Tabs → BottomBar |
| 20 | course-overview | `/courses/[slug]/overview` | Header → Description → FullSyllabus → Requirements → CTA |
| 21 | course-enroll | `/courses/[slug]/enroll` | HubNav → EnrollmentCard → Included → Guarantee |
| 22 | course-cohort | `/courses/[slug]/cohort` | HubNav → LiveCall → Discussion → Facilitators → Calendar |
| 23 | course-resources | `/courses/[slug]/resources` | HubNav → Downloads → Glossary → Links |
| 24 | course-journal | `/courses/[slug]/journal` | HubNav → NewEntry → Timeline → EmptyState |
| 25 | ai-lab | `/ai-lab` | Hero → FeatureCards → ChatPreview → Disclaimer |
| 26 | chat-full | `/chat` | Sidebar → Messages → Input → Suggestions |
| 27 | auth-signin | `/auth/signin` | Logo → Form → OAuth → FooterLink |
| 28 | auth-signup | `/auth/signup` | Logo → Form → OAuth → FooterLink |
| 29 | account-dashboard | `/account` | Sidebar → Welcome → ContinueLearning → Activity → QuickLinks |
| 30 | contact | `/contact` | Header → Form → ContactInfo → MapPlaceholder |
| 31 | pricing | `/pricing` | Header → PlanCards → FAQ → EnterpriseCTA |
| 32 | search | `/search` | SearchBar → Count → Tabs → Results → EmptyState |
| 33 | checkout | `/checkout` | Form → OrderSummary → SecurityNote |
| 34 | assessments-hub | `/assessments` | Header → Cards → HowItWorks (optional / feature flag) |
| 35 | reneighbor | `/reneighbor` | Brad tenant-unique — skip unless manifest includes |

---

## Reference-only routes (Alan Hirsch — port from code, not Stitch)

| Route | Notes |
|-------|-------|
| `/courses/[slug]/certificate` | Completion certificate |
| `/courses/[slug]/player` | Video lesson player variant |
| `/privacy`, `/terms`, `/accessibility` | Legal |
| Tenant-unique | See [TENANT_MANIFEST.md](./TENANT_MANIFEST.template.md) |

---

## Base wireframe style block

Every Stitch prompt includes the shared `BASE_STYLE` block (B&amp;W duotone, grayscale palette, section fidelity rules). During React migration:

- **Structure** from Stitch / this index
- **Colors** from tenant `globals.css` (Prompt 02 token bridge)
- **Copy** from `tenant.config.ts` + research path in manifest

---

*Derived from stitch-prompts.html PROMPTS array. Tenant-agnostic.*
