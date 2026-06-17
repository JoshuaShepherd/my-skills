# Skill catalog

Generated: 2026-06-11T18:35:08.127241+00:00

**Total canonical Claude skills:** 263

Install any skill flat into `~/.claude/skills/<name>/` (see `scripts/install-skill.sh`).

## agents (20)

| Skill | Description | Path |
|-------|-------------|------|
| `add-guardrail` | Add input or output guardrails to an agent — use when asked to validate, filter, or protect agent input/output, block un | `claude/agents/add-guardrail` |
| `add-tool` | Create or modify an agent tool — use when asked to add a new capability to an agent, build a search/retrieval/analysis/A | `claude/agents/add-tool` |
| `agent-context` | Build or modify user context systems — profile assembly, RunContract payloads, context schemas, catalog validation. Use  | `claude/agents/agent-context` |
| `agent-create` | Scaffold a new OpenAI Agents SDK agent with instructions, tools, API route, and bridge wiring. Use when creating a new s | `claude/agents/agent-create` |
| `agent-guardrail` | Add input/output guardrails to an agent pipeline — validation, content filtering, safety rules. Use when adding safety o | `claude/agents/agent-guardrail` |
| `agent-handoff` | Configure multi-agent handoffs — agent registry, delegation rules, and routing logic. Use when setting up agent-to-agent | `claude/agents/agent-handoff` |
| `agent-instructions` | Author or refine agent system prompts using composable instruction layers (identity, theme, mode, style, context). Use w | `claude/agents/agent-instructions` |
| `agent-rag` | Build or modify a RAG retrieval pipeline — vector store search, corpus routing, citation rendering, book fidelity. Use w | `claude/agents/agent-rag` |
| `agent-stream` | Work on SSE streaming, plain-text transport, ChatKit events, and session continuity. Use when debugging or modifying age | `claude/agents/agent-stream` |
| `agent-test` | Write tests for agents — unit tests for tools/instructions/routing, smoke tests for end-to-end behavior, e2e specs for A | `claude/agents/agent-test` |
| `agent-tool` | Create or modify an OpenAI Agents SDK tool with Zod params, caching, metrics, and agent registration. Use when adding to | `claude/agents/agent-tool` |
| `agent-trace` | Debug agent execution with tracing — analyze traces, tool calls, durations, errors, and performance metrics. Use when in | `claude/agents/agent-trace` |
| `build-context` | Work on agent context — use when asked to build, modify, or debug the user context system for an agent, including contex | `claude/agents/build-context` |
| `build-rag` | Build or modify a RAG (retrieval-augmented generation) pipeline — use when asked to set up vector search, file_search to | `claude/agents/build-rag` |
| `configure-handoff` | Configure agent handoffs — use when asked to set up multi-agent routing, delegate conversations between specialist agent | `claude/agents/configure-handoff` |
| `create-agent` | Scaffold and develop AI agents — use when asked to create, build, or set up a new AI agent, including agent definition,  | `claude/agents/create-agent` |
| `data-scraper-agent` | Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sport | `claude/agents/data-scraper-agent` |
| `debug-traces` | Debug agent execution using traces — use when asked to investigate slow responses, diagnose tool failures, analyze guard | `claude/agents/debug-traces` |
| `openai-vector-store` | > | `claude/agents/openai-vector-store` |
| `setup-streaming` | Set up or debug agent streaming — use when asked to implement SSE streaming, handle ChatKit event types, fix stream stal | `claude/agents/setup-streaming` |

## assets (29)

| Skill | Description | Path |
|-------|-------------|------|
| `art` | Generate illustrations, technical diagrams, mermaid flowcharts, infographics, header images, thumbnails, comics, and PAI | `claude/assets/art` |
| `asset-animate` | Create micro-animations from still images — parallax, Ken Burns, floating particles, breathing effects, cinemagraphs. Ge | `claude/assets/asset-animate` |
| `asset-audit` | Audit image assets across the project to find missing, broken, or mismatched images — trigger phrases include "audit ima | `claude/assets/asset-audit` |
| `asset-author-style` | Define and maintain a consistent visual identity for an author/thought leader across all image assets. Creates a style g | `claude/assets/asset-author-style` |
| `asset-brand-check` | Audit generated image assets against the platform's brand guidelines. Use before publishing to verify color palette, typ | `claude/assets/asset-brand-check` |
| `asset-composite` | Combine multiple generated images into a single composite — grids, collages, mood boards, before/after comparisons, or s | `claude/assets/asset-composite` |
| `asset-deliver` | Package generated prompts or assets into a polished interactive HTML page with tabbed navigation, one-click copy buttons | `claude/assets/asset-deliver` |
| `asset-edit` | Edit or refine an existing image using Nano Banana 2's conversational editing. Use when an asset needs color correction, | `claude/assets/asset-edit` |
| `asset-exploded-view` | Generate deconstructed/exploded view prompts using Nano Banana 2. Use for scroll-stop content, framework visualizations, | `claude/assets/asset-exploded-view` |
| `asset-generate` | Generate image assets using Nano Banana 2 (Gemini Flash Image). Use when creating hero images, course covers, book cover | `claude/assets/asset-generate` |
| `asset-headshot` | Create polished headshots and avatars from existing author photos using Nano Banana 2. Handles background replacement, r | `claude/assets/asset-headshot` |
| `asset-hero-portrait` | Create wide-format hero images featuring an author/thought leader from existing photos using Nano Banana 2. Handles back | `claude/assets/asset-hero-portrait` |
| `asset-match` | Audit where images are needed across the project (heroes, covers, cards, OG images) vs what's available in public/images | `claude/assets/asset-match` |
| `asset-mockup` | Place generated images into real-world context mockups — laptop screens, phone frames, book mockups, poster frames, bill | `claude/assets/asset-mockup` |
| `asset-product-shot` | Generate clean product/object photography prompts using Nano Banana 2. Use for book mockups, course materials, merchandi | `claude/assets/asset-product-shot` |
| `asset-prompt-library` | Manage reusable NB2 prompt templates for recurring asset types. Use to store, retrieve, list, or customize prompt templa | `claude/assets/asset-prompt-library` |
| `asset-series` | Generate a visually consistent set of image assets using Nano Banana 2. Use for course module covers, book chapter heade | `claude/assets/asset-series` |
| `asset-text-overlay` | Generate images with precise text rendering using Nano Banana 2. Use for social cards, OG images, course certificates, m | `claude/assets/asset-text-overlay` |
| `asset-video-prompt` | Generate video transition prompts for AI video models (Runway, Kling, Pika, Higgsfield). Creates start/end frame descrip | `claude/assets/asset-video-prompt` |
| `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-vid | `claude/assets/fal-ai-media` |
| `gpt-export` | Generate 21 markdown knowledge files + custom instructions for creating a Custom GPT strategic consultant from the curre | `claude/assets/gpt-export` |
| `image-optimize` | Optimize images from the local images repo (convert to WebP, generate responsive variants, resize) and upload to Supabas | `claude/assets/image-optimize` |
| `nano-banana-pro` | Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). Use when the user asks to create an image, generate a  | `claude/assets/nano-banana-pro` |
| `pdf-ebook` | Convert any file format (markdown, text, HTML) into a professionally styled PDF e-book using WeasyPrint. Supports single | `claude/assets/pdf-ebook` |
| `remotion` | Programmatic video creation with React via Remotion — compositions, animations, motion graphics, rendered to MP4. Includ | `claude/assets/remotion` |
| `remotion-best-practices` | Best practices for Remotion - Video creation in React | `claude/assets/remotion-best-practices` |
| `scientific-schematics` | Create publication-quality scientific diagrams using Nano Banana Pro AI with smart iterative refinement. Uses Gemini 3 P | `claude/assets/scientific-schematics` |
| `video-consult` | Consult on video production for a course — scripture grounding, narrative arc, storyboard, scene structure, and script.  | `claude/assets/video-consult` |
| `video-researcher` | Research real-world statistics, insights, and compelling data about online courses, completion rates, learning effective | `claude/assets/video-researcher` |

## codegen (16)

| Skill | Description | Path |
|-------|-------------|------|
| `add-table` | Add a new database table and generate all six layers. Use when adding a new entity to the platform. | `claude/codegen/add-table` |
| `app-architect` | Generate a full architectural documentation package for any app, project, or feature — a _PURPOSE.md narrative plus indi | `claude/codegen/app-architect` |
| `authoring-skills` | > | `claude/codegen/authoring-skills` |
| `build-prompt` | > | `claude/codegen/build-prompt` |
| `coding-standards` | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. | `claude/codegen/coding-standards` |
| `composition-patterns` |  | `claude/codegen/composition-patterns` |
| `fullstack-developer` | \| | `claude/codegen/fullstack-developer` |
| `generate` | Regenerate a specific layer (schemas, services, routes, hooks, ui) or all layers. Use after schema changes or when gener | `claude/codegen/generate` |
| `javascript-typescript-typescript-scaffold` | You are a TypeScript project architecture expert specializing in scaffolding production-ready Node.js and frontend appli | `claude/codegen/javascript-typescript-typescript-scaffold` |
| `react-best-practices` | React performance optimization guidelines from Mastra Engineering. This skill should be used when writing, reviewing, or | `claude/codegen/react-best-practices` |
| `react-native-design` | Master React Native styling, navigation, and Reanimated animations for cross-platform mobile development. Use when build | `claude/codegen/react-native-design` |
| `react-native-skills` |  | `claude/codegen/react-native-skills` |
| `storybook-setup` | Set up Storybook 8 for Next.js 15 or Vite + React — component dev environment, story scaffolding, shadcn/ui integration, | `claude/codegen/storybook-setup` |
| `visualization-expert` | \| | `claude/codegen/visualization-expert` |
| `visualization-repair` | > | `claude/codegen/visualization-repair` |
| `write-instructions` | Author or refine agent instructions — use when asked to write a system prompt, create or update agent instructions, comp | `claude/codegen/write-instructions` |

## content (44)

| Skill | Description | Path |
|-------|-------------|------|
| `alan-voice` | Write, edit, or audit content in Alan Hirsch's exact voice — using the same five voice markers, argument patterns, rheto | `claude/content/alan-voice` |
| `article-audit` | Audit a complete article against all criteria — Alan's five voice markers, SEO/GEO requirements, section architecture, c | `claude/content/article-audit` |
| `article-author` | Write a complete evergreen pillar article in Alan Hirsch's voice — with corpus research from his books, full SEO/GEO arc | `claude/content/article-author` |
| `article-corpus` | Look up passages, themes, and arguments from Alan Hirsch's book corpus — both from the local markdown files and the Supa | `claude/content/article-corpus` |
| `article-plan` | Strategically plan a single evergreen article — pillar assignment, keyword targeting, section outline, corpus references | `claude/content/article-plan` |
| `author-content` | Write course content for a specific element (M.N.X) of a transformational course — readings, video scripts, reflection q | `claude/content/author-content` |
| `author-research` | Deep research for book authors — searches Google Scholar, Internet Archive, JSTOR, Google Books/Ngram, Library of Congre | `claude/content/author-research` |
| `author-style-guide` | Create or update the author visual style guide that ensures consistent lighting, color grade, and composition across all | `claude/content/author-style-guide` |
| `book-audit` | > | `claude/content/book-audit` |
| `book-chunk` | > | `claude/content/book-chunk` |
| `book-convert` | > | `claude/content/book-convert` |
| `book-fix` | > | `claude/content/book-fix` |
| `book-frontmatter` | > | `claude/content/book-frontmatter` |
| `book-ingest` | > | `claude/content/book-ingest` |
| `book-pipeline` | > | `claude/content/book-pipeline` |
| `book-rag-push` | > | `claude/content/book-rag-push` |
| `book-validate` | > | `claude/content/book-validate` |
| `career` | Career management skill covering resume coaching (review, score, tailor, audit), job evaluation, rubric development, con | `claude/content/career` |
| `content-creator` | \| | `claude/content/content-creator` |
| `content-ingest` | Ingest, organize, and structure raw content (book chapters, transcripts, articles, research notes) into the repository's | `claude/content/content-ingest` |
| `corpus-ingestion` | > | `claude/content/corpus-ingestion` |
| `course-audit` | Audit the course learn experience — checks section components, sidebar rendering, progress tracking, responsiveness, des | `claude/content/course-audit` |
| `course-author` | Generate course content for a specific section of the transformation loop, following the actual Forgotten Ways course st | `claude/content/course-author` |
| `course-ingest` | Ingest course content from markdown files into the database. Parses manifest + module files, validates, and upserts cour | `claude/content/course-ingest` |
| `course-scaffold` | Scaffold a new 8-week course with all canonical section types, database rows, and optional markdown file structure. Use  | `claude/content/course-scaffold` |
| `course-section` | Create a new course section component following the existing section pattern. Use when adding new content types to cours | `claude/content/course-section` |
| `course-ux` | Audit and fix course player UX against LMS best practices — layout proportions, progressive disclosure, progress psychol | `claude/content/course-ux` |
| `course-validate` | Validate a course against the Transformational Course Charter — checks Four Necessities, section completeness, word coun | `claude/content/course-validate` |
| `dialogue-craft` | Dialogue craft for fiction and conversational AI agents — subtext, character voice differentiation, pacing, exposition h | `claude/content/dialogue-craft` |
| `editorial-lens` | Multi-level editorial review — from developmental editing (structure, argument, arc) through line editing (prose quality | `claude/content/editorial-lens` |
| `ingest-content` | Ingest course content from markdown files or a content directory into the database — parsing, validating, and upserting  | `claude/content/ingest-content` |
| `nonfiction-craft` | Non-fiction writing craft — argument construction, evidence handling, essay structure, chapter architecture, research in | `claude/content/nonfiction-craft` |
| `paratext-audit` | Audit paratext (supporting content) across all platform surfaces — courses, books, articles, exercises, field experiment | `claude/content/paratext-audit` |
| `paratext-author` | Write missing or stub paratext for any platform surface — books, courses, podcast episodes — in Alan Hirsch's voice. Que | `claude/content/paratext-author` |
| `pathway-audit` | Audit a pathway page against the canonical 12-section architecture. Reports what's missing, what's below spec, what's co | `claude/content/pathway-audit` |
| `pathway-author` | Write or update content for a pathway page — any single section or a full pathway. Follows the canonical 12-section arch | `claude/content/pathway-author` |
| `pathway-builder` | Build type-safe React pathway pages from pathway_sections database content — generates types, hooks, section components, | `claude/content/pathway-builder` |
| `plain-prose` | Write clear, plain prose, and strip register-jargon out of text that already has it. Use this whenever writing prose tha | `claude/content/plain-prose` |
| `prose-craft` | Core writing craft skill — sentence-level quality, rhythm, voice, show-don't-tell, sensory detail, pacing, and line-leve | `claude/content/prose-craft` |
| `scaffold-course` | Scaffold a new 8-week transformational course — creating the database rows, ingestion script, and optional markdown cont | `claude/content/scaffold-course` |
| `story-architect` | Narrative structure skill for fiction and creative non-fiction — plot architecture, character arcs, scene construction,  | `claude/content/story-architect` |
| `validate-course` | Validate a course against the Transformational Course Charter — checking 8-week structure, Four Necessities compliance,  | `claude/content/validate-course` |
| `week-author` | Draft a complete course week — all transformation loop sections in Alan Hirsch's voice, grounded in corpus, following th | `claude/content/week-author` |
| `writing-agent-builder` | Architect AI agents that write well — system prompt design, voice integration, tool selection, RAG for source material,  | `claude/content/writing-agent-builder` |

## design (37)

| Skill | Description | Path |
|-------|-------------|------|
| `add-section-type` | Create a new course section component and register it in the section router. Use when adding a new section type to the c | `claude/design/add-section-type` |
| `animation` | Add scroll animations, micro-interactions, or page transitions to a component using GSAP. Use when a section needs motio | `claude/design/animation` |
| `applying-brand-guidelines` | This skill applies consistent corporate branding and styling to all generated documents including colors, fonts, layouts | `claude/design/applying-brand-guidelines` |
| `audit-experience` | Audit the course learn experience for section coverage, sidebar rendering, layout, design token compliance, tenant isola | `claude/design/audit-experience` |
| `chat-ui-audit` | Audit and fix chat-based AI UI (chatbots, agents, floating chat) against production best practices from Claude, ChatGPT, | `claude/design/chat-ui-audit` |
| `ckmui-styling` | Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS util | `claude/design/ckmui-styling` |
| `color-audit` | Expert color palette audit for movemental — verify semantic token completeness, WCAG contrast compliance, 60-30-10 distr | `claude/design/color-audit` |
| `design-audit` | Audit a page or component against the Digital Curator design spec (DESIGN.md) and movemental project conventions. Use to | `claude/design/design-audit` |
| `design-chain` | Audit and enforce the five-layer design chain (tokens → Tailwind → primitives → sections → pages) across all components  | `claude/design/design-chain` |
| `design-chain-audit` | Unified design chain audit for Movemental — flushes drift across all 5 layers (Stitch → tokens → primitives → components | `claude/design/design-chain-audit` |
| `design-section` | Design a new UI section or component for movemental using DESIGN.md conventions — tonal stacking, primitives, semantic t | `claude/design/design-section` |
| `designer-dashboard` | Apply the Stitch → tokens → primitives → components → layouts design chain to React/Tailwind dashboard UI for cohesive,  | `claude/design/designer-dashboard` |
| `figma-prompt` | Generate a complete Figma Make prompt package — Context Primer, Checkpoint, Section Build Prompts, and Iteration Templat | `claude/design/figma-prompt` |
| `frontend-cleanup` | Audit a React/Next.js codebase for unused components, -v2 naming debt, and folder disorganization. Archives dead code an | `claude/design/frontend-cleanup` |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to  | `claude/design/frontend-design` |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. | `claude/design/frontend-patterns` |
| `html-to-react-tailwind` | Convert HTML/CSS/JS files into production-ready React components with Tailwind CSS. Handles CSS-to-utility mapping, JS-t | `claude/design/html-to-react-tailwind` |
| `icon-audit` | Audit and fix icon usage for movemental — mixed libraries, wrong sizes, hardcoded colors, missing accessibility, and ill | `claude/design/icon-audit` |
| `icon-system` | Establish or validate the canonical Icon wrapper component, size token scale, stroke weight conventions, and illustratio | `claude/design/icon-system` |
| `movemental-ink` | > | `claude/design/movemental-ink` |
| `new-page` | Scaffold a new public page following project conventions. Use when adding a new route under (public). | `claude/design/new-page` |
| `oatmeal-editorial-ui` | > | `claude/design/oatmeal-editorial-ui` |
| `page-audit` | Holistic audit of any movemental.com page — UI, content, architecture, UX, and conversion — writes a markdown report and | `claude/design/page-audit` |
| `puck-visual-editor` | Build, extend, and persist Puck visual editors with React/Next.js and Supabase. Use whenever the user mentions Puck, @pu | `claude/design/puck-visual-editor` |
| `responsive-audit` | Audit and fix responsiveness issues for movemental — breakpoint coverage, layout collapse, touch targets, typography sca | `claude/design/responsive-audit` |
| `responsive-design` | Implement modern responsive layouts using container queries, fluid typography, CSS Grid, and mobile-first breakpoint str | `claude/design/responsive-design` |
| `scholarly-authority-ui` | > | `claude/design/scholarly-authority-ui` |
| `scholarly-editorial-ui` | > | `claude/design/scholarly-editorial-ui` |
| `tailwind-cleanup` | Scan and fix Tailwind anti-patterns for movemental — hardcoded colors, arbitrary values, raw HTML bypassing shadcn/primi | `claude/design/tailwind-cleanup` |
| `tailwind-cleanup-general` | Design-agnostic Tailwind best-practice cleanup that conforms to the current repo's design schema; documents the schema (charter→tokens→primitives→components→layouts) first if undocumented, then fixes. Symlinked into all repos. | `claude/design/tailwind-cleanup-general` |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use whe | `claude/design/tailwind-design-system` |
| `typeset` | Improve typography by fixing font choices, hierarchy, sizing, weight consistency, and readability. Makes text feel inten | `claude/design/typeset` |
| `typography-polish` | Audit and fix typography across movemental — heading hierarchy, Inter font compliance, display tracking, eyebrow convent | `claude/design/typography-polish` |
| `ui-hook-wiring-audit` | Audit and fix UI component data wiring — verifies every component renders the correct data by tracing rendered fields ba | `claude/design/ui-hook-wiring-audit` |
| `visual-design-foundations` | Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when  | `claude/design/visual-design-foundations` |
| `visual-storytelling-audit` | Cross-platform audit of visual storytelling components — cards, grids, stats, comparisons, numbered steps, section rhyth | `claude/design/visual-storytelling-audit` |
| `web-component-design` | Master React, Vue, and Svelte component patterns including CSS-in-JS, composition strategies, and reusable component arc | `claude/design/web-component-design` |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit  | `claude/design/web-design-guidelines` |

## docs (3)

| Skill | Description | Path |
|-------|-------------|------|
| `docs-design-system` | Audit and update design documentation in _docs/_build/design/ to match the actual UI stack (tokens, Tailwind, shadcn pri | `claude/docs/docs-design-system` |
| `docs-setup` | Bootstrap the canonical two-part _docs directory for any context-coded project in the Claude/AntiGravity environment. Cr | `claude/docs/docs-setup` |
| `docs-type-safety` | Audit and update the type safety documentation in _docs/type/ to match the actual codebase state. Ensures docs are the s | `claude/docs/docs-type-safety` |

## infrastructure (48)

| Skill | Description | Path |
|-------|-------------|------|
| `analytics-audit` | Audit the analytics implementation across all providers (GA4, PostHog, Vercel Analytics, Supabase) — verifies events fir | `claude/infrastructure/analytics-audit` |
| `analytics-dashboard` | Build React analytics dashboard components for this platform — KPI metric cards, time series charts (Recharts), funnel v | `claude/infrastructure/analytics-dashboard` |
| `analytics-setup` | Bootstrap the complete analytics stack for this Next.js 15 + Supabase project — GA4 (org-wide + per-tenant), PostHog, Ve | `claude/infrastructure/analytics-setup` |
| `auth-setup` | Set up Supabase Auth for Next.js 15 (App Router) or Vite + React — sign-up, sign-in, OAuth providers, session middleware | `claude/infrastructure/auth-setup` |
| `ci-setup` | Set up GitHub Actions CI/CD pipeline for Next.js 15 or Vite + Express — lint, typecheck, unit tests, e2e tests, build va | `claude/infrastructure/ci-setup` |
| `deploy-to-vercel` | Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy  | `claude/infrastructure/deploy-to-vercel` |
| `e2e-studio-tests` | Run e2e tests in the Studio app. Use when asked to run e2e tests, run studio tests, playwright tests, or test the featur | `claude/infrastructure/e2e-studio-tests` |
| `email-setup` | Set up transactional email via Resend for Next.js 15 or Vite + Express — React Email templates, send helpers, welcome/ma | `claude/infrastructure/email-setup` |
| `env-setup` | Scaffold and validate environment variables for Next.js 15 or Vite + Express — Zod-validated env schema, .env.example wi | `claude/infrastructure/env-setup` |
| `feature-constitution` | Export a platform feature as a product constitution — data model, API contracts, business rules, and acceptance criteria | `claude/infrastructure/feature-constitution` |
| `ga4-setup` | Set up Google Analytics 4 for this Next.js 15 multi-tenant platform — org-wide property, per-tenant custom dimensions, t | `claude/infrastructure/ga4-setup` |
| `liveblocks-workspace` | Work with the Liveblocks + BlockNote collaborative workspace — add features, debug content rendering, configure rooms, m | `claude/infrastructure/liveblocks-workspace` |
| `migrations-workflow` | Manage the full Drizzle ORM migration lifecycle — generate, review, apply, rollback, and sync with Supabase. Covers the  | `claude/infrastructure/migrations-workflow` |
| `nextjs-supabase-auth` | Expert integration of Supabase Auth with Next.js App Router Use when: supabase auth next, authentication next.js, login  | `claude/infrastructure/nextjs-supabase-auth` |
| `postgres-best-practices` | Comprehensive PostgreSQL reference covering performance optimization, schema design, indexing, query patterns, connectio | `claude/infrastructure/postgres-best-practices` |
| `postgres-patterns` | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best pract | `claude/infrastructure/postgres-patterns` |
| `postgres-schema-design` | Comprehensive PostgreSQL-specific table design reference covering data types, indexing, constraints, performance pattern | `claude/infrastructure/postgres-schema-design` |
| `posthog-setup` | Set up PostHog product analytics for this Next.js 15 + Supabase multi-tenant platform — person identification, group ana | `claude/infrastructure/posthog-setup` |
| `project-setup` | Bootstrap a production-ready React + Tailwind + Supabase + Sentry app — either Next.js 15 (App Router) or Vite + React R | `claude/infrastructure/project-setup` |
| `react-audit` | Audit React 19 configuration and usage patterns for correctness and optimization — hooks, components, error boundaries,  | `claude/infrastructure/react-audit` |
| `repo-cleanup` | > | `claude/infrastructure/repo-cleanup` |
| `security-setup` | Harden a Next.js 15 or Vite + Express app for production — Content Security Policy headers, rate limiting (Upstash Redis | `claude/infrastructure/security-setup` |
| `sentry-setup` | Set up Sentry error monitoring for a Vite + React 19 SPA with Express API — client SDK, server SDK, error boundaries, so | `claude/infrastructure/sentry-setup` |
| `seo-setup` | Set up SEO infrastructure for Next.js 15 — Metadata API (title, description, OG, Twitter), dynamic sitemap.xml, robots.t | `claude/infrastructure/seo-setup` |
| `stripe-integration` | Implement Stripe payment processing for robust, PCI-compliant payment flows including checkout, subscriptions, and webho | `claude/infrastructure/stripe-integration` |
| `stripe-setup` | Set up Stripe payments for Next.js 15 or Vite + Express — subscriptions, one-time payments, webhooks, customer portal, b | `claude/infrastructure/stripe-setup` |
| `supabase-add-tenant-user` | Provision a new multi-tenant user on a Supabase-backed app with one auth user → one user_profiles row → one owned organi | `claude/infrastructure/supabase-add-tenant-user` |
| `supabase-analytics` | Set up Supabase-native analytics for this multi-tenant platform — custom analytics_events table (RLS-scoped per org), pe | `claude/infrastructure/supabase-analytics` |
| `supabase-fix-rls` | Take an RLS finding from supabase-security-audit (or a free-form description of an RLS issue) and apply a reviewed fix v | `claude/infrastructure/supabase-fix-rls` |
| `supabase-security-audit` | Audit a Supabase project for security issues — RLS, auth config, role grants, storage, functions, and exposed secrets. R | `claude/infrastructure/supabase-security-audit` |
| `telemetry-standards` | PostHog event tracking standards for Supabase Studio. Use when reviewing | `claude/infrastructure/telemetry-standards` |
| `tenant-check` | Audit components for hardcoded tenant strings, non-semantic colors, or missing feature flags. Use before PR review or to | `claude/infrastructure/tenant-check` |
| `tenant-migrate` | Audit and execute multi-tenant platform migration — determines what's needed when cloning a fully-built Movemental tenan | `claude/infrastructure/tenant-migrate` |
| `tenant-migration` | End-to-end migration skill for spinning up a new movement leader platform from an existing tenant baseline. Covers repo  | `claude/infrastructure/tenant-migration` |
| `testing-setup` | Bootstrap Vitest (unit + integration) and Playwright (e2e) test infrastructure for Next.js 15 or Vite + React — config f | `claude/infrastructure/testing-setup` |
| `translation-audit` | > | `claude/infrastructure/translation-audit` |
| `type-fix` | Run type safety checks across all 6 layers, regenerate any failing layers, and loop until all layers pass with zero erro | `claude/infrastructure/type-fix` |
| `type-safety-chain` | Implement the full six-layer type safety chain in a new project — DB → Drizzle schema → Zod schemas → services → API rou | `claude/infrastructure/type-safety-chain` |
| `validate` | Run bottom-up layer validation and fix all errors. Use before starting work on any layer or to check project health. Fol | `claude/infrastructure/validate` |
| `vercel-analytics` | Set up Vercel Analytics (page views, custom events) and Speed Insights (Core Web Vitals) for this Next.js 15 project. Ze | `claude/infrastructure/vercel-analytics` |
| `vercel-audit` | Audit Vercel deployment configuration for correctness and optimization — vercel.json, serverless functions, environment  | `claude/infrastructure/vercel-audit` |
| `vercel-cli-with-tokens` | Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tok | `claude/infrastructure/vercel-cli-with-tokens` |
| `vercel-deploy-audit` | Audit a Vite+Express workspace for Vercel deployment issues — API connectivity, env vars, serverless bundling, CORS, sym | `claude/infrastructure/vercel-deploy-audit` |
| `vite-audit` | Audit Vite configuration for correctness and optimization — build performance, plugins, resolve config, dev server, envi | `claude/infrastructure/vite-audit` |
| `workspace-author` | Write new workspace documents — articles, research notes, project docs, and ebook sections — following Brad Brisco's voi | `claude/infrastructure/workspace-author` |
| `workspace-organize` | Audit and fix workspace doc organization — frontmatter hygiene, section placement, sidebar rendering, and frontend-safe  | `claude/infrastructure/workspace-organize` |
| `workspace-strategy` | Strategic planning for the workspace doc system — content roadmaps, agentic workflow design, context coding architecture | `claude/infrastructure/workspace-strategy` |
| `write-tests` | Write agent tests — use when asked to add unit tests, smoke tests, or E2E tests for agents, including tool tests, instru | `claude/infrastructure/write-tests` |

## integrations (8)

| Skill | Description | Path |
|-------|-------------|------|
| `ai-lab-notebook-gemini` | > | `claude/integrations/ai-lab-notebook-gemini` |
| `awesome-postgres` | A curated list of awesome PostgreSQL software, libraries, tools and resources, inspired by awesome-m awesome postgres, p | `claude/integrations/awesome-postgres` |
| `claude-api` | Build, refine, and master agents using the Anthropic Claude API and @anthropic-ai/sdk. Covers messages API, tool use, ex | `claude/integrations/claude-api` |
| `context7-mcp` | This skill should be used when the user asks about libraries, frameworks, API references, or needs code examples. Activa | `claude/integrations/context7-mcp` |
| `gemini-api` | Build, refine, and master agents using the Google Gemini API and @google/generative-ai SDK. Covers generateContent, func | `claude/integrations/gemini-api` |
| `github` | Interact with GitHub using the `gh` CLI — PRs, issues, CI runs, code review, and API queries. Use when checking PR statu | `claude/integrations/github` |
| `grok-api` | Build, refine, and master agents using the xAI Grok API — OpenAI-compatible endpoint with grok-4.20 and grok-4-1-fast mo | `claude/integrations/grok-api` |
| `openai-api` | Build, refine, and master agents using the OpenAI API — Chat Completions, Responses API, and OpenAI Agents SDK. Covers f | `claude/integrations/openai-api` |

## movemental (33)

| Skill | Description | Path |
|-------|-------------|------|
| `affiliation-audit` | Audit collected affiliation data against logo strip and social proof best practices. Evaluates logo quality, grouping st | `claude/movemental/affiliation-audit` |
| `affiliation-scrape` | Research organizations a leader is affiliated with AND fetch logos for them. Output is a JSON record optimized for rende | `claude/movemental/affiliation-scrape` |
| `domain-finder` | Analyzes a project's docs and code to generate domain name candidates, check availability, compare registrar pricing, an | `claude/movemental/domain-finder` |
| `fragmentation-story` | > | `claude/movemental/fragmentation-story` |
| `home-consult` | Strategic consultation for a movement leader home page — mandatory sections rubric, scroll-stop strategy (Spline/NB2/GSA | `claude/movemental/home-consult` |
| `logo-strip-author` | Author a complete social proof / logo strip section for an author or leader — copy, grouping strategy, TypeScript conten | `claude/movemental/logo-strip-author` |
| `ml-template-from-reference` | Build an HTML/CSS/JS movement-leader template (home + content library + articles) whose visual design matches a provided | `claude/movemental/ml-template-from-reference` |
| `movement-leader-substrate` | Author the machine-readable substrate document for a movement leader — identity resolution, relational traversal, concep | `claude/movemental/movement-leader-substrate` |
| `movemental-committed-voice-bio` | Generate the Committed Voices onboarding entry for a specific movement leader from their research dossier. Use when aske | `claude/movemental/movemental-committed-voice-bio` |
| `movemental-narrative-audit` | > | `claude/movemental/movemental-narrative-audit` |
| `movemental-page-auditor` | Audit any Movemental page (HTML mockup or production React) across six passes — narrative sequencing, copy & language, t | `claude/movemental/movemental-page-auditor` |
| `movemental-prose` | Audit and fix line-level prose in Movemental articles, book chapters, field guides, paratext, emails, and site copy. Cat | `claude/movemental/movemental-prose` |
| `movemental-publish-gate` | Pre-publication quality gate for research and authoritative content headed to movemental.ai. Run before posting any arti | `claude/movemental/movemental-publish-gate` |
| `movemental-tenant-provision` | Provision Movemental movement-leader tenants end-to-end on Supabase — runs Phase 0 prerequisite security/auth gates firs | `claude/movemental/movemental-tenant-provision` |
| `movemental-welcome-letter` | Draft the Movemental dashboard welcome letter for a specific movement leader from their fragmentation-story dossier. Use | `claude/movemental/movemental-welcome-letter` |
| `movemental-welcome-letter-publish` | Publish a finished Movemental dashboard welcome letter to the production Supabase database so the named movement leader  | `claude/movemental/movemental-welcome-letter-publish` |
| `network-map` | Map relationships, co-authorships, endorsements, and organizational connections across movement leaders. Reads existing  | `claude/movemental/network-map` |
| `nonprofit-pricing-research` | Produce transparent, defensible pricing intelligence for AI-literacy and applied AI training engagements for nonprofits. | `claude/movemental/nonprofit-pricing-research` |
| `oatmeal-template-audit` | Audit and refine an HTML page in `1-html/by-template-family/ml-templates/oatmeal/` against the canonical Oatmeal templat | `claude/movemental/oatmeal-template-audit` |
| `platform-demo-architect` | Interactive 9-step process to design a cutting-edge, best-case platform demo for a specific audience — audience intel, p | `claude/movemental/platform-demo-architect` |
| `poll-opinion-research` | Research public opinion, polling data, and sentiment trends using Pew Research, Gallup, Ipsos, Eurobarometer, YouGov, an | `claude/movemental/poll-opinion-research` |
| `stakeholder-map` | Deep-research Youthfront stakeholders and map their full connection networks for donor cultivation | `claude/movemental/stakeholder-map` |
| `tam-audit` | Audit the TAM master list for gaps, staleness, scoring inconsistencies, demographic imbalances, and missing research — p | `claude/movemental/tam-audit` |
| `tam-blind-spots` | Search the structural blind spots that network mapping misses — domain practitioners, justice/reconciliation voices, wor | `claude/movemental/tam-blind-spots` |
| `tam-discover` | Discover new movement leader candidates for the Movemental TAM using network-based and content-based search strategies | `claude/movemental/tam-discover` |
| `tam-headshot-source` | Surgically acquire one verified headshot per movement leader — official sources first, identity checks, direct download, | `claude/movemental/tam-headshot-source` |
| `tam-international` | Discover and research international movement leaders outside US/anglophone networks — mapping the global TAM | `claude/movemental/tam-international` |
| `tam-network-map` | Map relationships, co-authorships, endorsements, and organizational connections between movement leaders in the TAM | `claude/movemental/tam-network-map` |
| `tam-profile` | Score a movement leader's fit with the Movemental platform — a consulting deliverable (Fit Score 1–10, NOTs assessment,  | `claude/movemental/tam-profile` |
| `tam-reflected-understanding` | Generate a reflected understanding document for a movement leader — a second-person mirror of their calling, audience, c | `claude/movemental/tam-reflected-understanding` |
| `tam-score` | Score and rank movement leader candidates using the Seven Gates and 100-point Movemental rubric | `claude/movemental/tam-score` |
| `transformative-learning-collaborator` | Expert peer collaborator for transformative learning design — thinks with you about course architecture, content alignme | `claude/movemental/transformative-learning-collaborator` |
| `voice-designer` | Build detailed voice profiles for characters, narrators, brands, or AI agents — covering diction, syntax, rhythm, worldv | `claude/movemental/voice-designer` |

## research (11)

| Skill | Description | Path |
|-------|-------------|------|
| `academic-research` | Deep academic research using free open-access sources — Semantic Scholar, OpenAlex, arXiv, PubMed Central, and CORE. Sea | `claude/research/academic-research` |
| `ai-model-insights` | Analyze AI model research (from ai-model-research) and generate strategic insights — capability comparisons, cost projec | `claude/research/ai-model-insights` |
| `ai-model-research` | Live browser research on all major AI models — OpenAI, Gemini, Claude, and Grok. Extracts authoritative model profiles,  | `claude/research/ai-model-research` |
| `audio-scrape` | Scrape podcast episodes, sermons, and audio sources — discovers via iTunes Search API, parses RSS feeds, downloads audio | `claude/research/audio-scrape` |
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying  | `claude/research/brainstorming` |
| `markitdown` | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcrip | `claude/research/markitdown` |
| `review-scrape` | Scrape book reviews from Goodreads and Amazon — fetches actual review text, ratings, dates, and reviewer metadata. Organ | `claude/research/review-scrape` |
| `summarize` | Summarizes, condenses, or extracts text, transcripts, and key points from URLs, articles, web pages, PDFs, podcasts, You | `claude/research/summarize` |
| `visual-scrape` | Extract visuals (charts, diagrams, illustrations) from a PDF book and generate contextual markdown — each image paired w | `claude/research/visual-scrape` |
| `youtube-scrape` | Scrape YouTube channel videos — fetches metadata, downloads transcripts via yt-dlp, chunks for search, and pulls comment | `claude/research/youtube-scrape` |
| `youtube-transcript` | Extract a plain-text transcript from any YouTube video URL. Returns timestamped and full-text versions of the transcript | `claude/research/youtube-transcript` |

## stitch (9)

| Skill | Description | Path |
|-------|-------------|------|
| `stitch-build` | Create a Stitch project and generate screens from a feature specification or user description. Calls Stitch MCP tools di | `claude/stitch/stitch-build` |
| `stitch-design` | Unified entry point for Stitch design work. Handles prompt enhancement (UI/UX keywords, atmosphere), design system synth | `claude/stitch/stitch-design` |
| `stitch-download` | Browse Stitch projects, download all screens (HTML + screenshots), and generate an organized local gallery with an index | `claude/stitch/stitch-download` |
| `stitch-export` | Generate a screen-by-screen feature specification for a Stitch project — documenting what each screen does, its content, | `claude/stitch/stitch-export` |
| `stitch-iterate` | Refine and edit existing Stitch screens using targeted prompts. Uses edit_screens to adjust content, functionality, or s | `claude/stitch/stitch-iterate` |
| `stitch-loop` | Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern | `claude/stitch/stitch-loop` |
| `stitch-react` | Convert Stitch screens to React components — fetches and caches designs locally, extracts design tokens, decomposes HTML | `claude/stitch/stitch-react` |
| `stitch-ui-design` | Expert guidance for crafting effective prompts in Google Stitch, the AI-powered UI design tool by Google Labs. This skil | `claude/stitch/stitch-ui-design` |
| `stitch-variants` | Generate design variants of existing Stitch screens to explore alternative approaches. Controls creative range, aspects  | `claude/stitch/stitch-variants` |

## studio (5)

| Skill | Description | Path |
|-------|-------------|------|
| `studio-design` | Generate a rich AI Studio design prompt for any mock-up or prototype — pages, dashboards, heroes, apps. Combines AntiGra | `claude/studio/studio-design` |
| `studio-export` | Generate a feature constitution — data model, product story, and acceptance criteria for a platform slice/feature. Desig | `claude/studio/studio-export` |
| `studio-prompt` | Generate a complete AI Studio prompt package — System Instructions, Build Prompt, and Iteration Templates — for any UI f | `claude/studio/studio-prompt` |
| `studio-style` | Generate a 1-pager style foundation prompt for AI Studio — hero, typography section, and card grid only. Establishes the | `claude/studio/studio-style` |
| `studio-testing` | Testing strategy for Supabase Studio. Use when writing tests, deciding what | `claude/studio/studio-testing` |
