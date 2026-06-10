---
name: tenant-migrate
description: Audit and execute multi-tenant platform migration — determines what's needed when cloning a fully-built Movemental tenant (e.g. alan-hirsch) to bootstrap a new one (e.g. brad-brisco). Inspects Supabase via MCP, audits tenant config, env vars, feature flags, storage buckets, database org row, codebase leaks, middleware, and Vercel deployment. Does NOT handle visual theming (globals.css) or image assets — those are separate concerns. Use when onboarding a new thought leader onto the platform.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, TodoWrite, mcp__supabase__execute_sql, mcp__supabase__list_tables, mcp__supabase__get_project, mcp__supabase__list_projects
---

# Tenant Migration Skill

Audit and execute the full migration checklist when cloning an existing Movemental tenant platform (the **source**, e.g. `alan-hirsch`) to create a new tenant deployment (the **target**, e.g. `brad-brisco`).

## Context

This is a **multi-tenant thought leader platform**. Each tenant is:
- A separate Git repo/deployment sharing the same codebase structure
- Scoped to one `organizations` row in a shared Supabase database via `TENANT_ORG_ID`
- Visually differentiated via `globals.css` CSS variables and `tenant.config.ts`

The source repo (alan-hirsch) is the reference implementation. New tenants clone the repo, then must change every tenant-specific surface. This skill audits what's been done and what remains.

## Execution Steps

### Phase 1: Database & Org Identity (Supabase MCP)

Use the Supabase MCP (project `vhaiiiykcukrlyvwlgip`, `public` schema) to verify:

1. **Organization row exists**:
   ```sql
   SELECT id, name, slug, description FROM organizations WHERE slug = '<target-slug>';
   ```
   If missing, report that the org must be created first. Do NOT create it automatically.

2. **TENANT_ORG_ID matches**:
   - Read `.env.local.example` for the documented `TENANT_ORG_ID`
   - Confirm it matches the org row's `id`

3. **Content scoped to this org**:
   ```sql
   SELECT 'books' AS type, count(*) FROM books WHERE organization_id = '<org-id>'
   UNION ALL SELECT 'articles', count(*) FROM articles WHERE organization_id = '<org-id>'
   UNION ALL SELECT 'courses', count(*) FROM courses WHERE organization_id = '<org-id>'
   UNION ALL SELECT 'podcast_episodes', count(*) FROM podcast_episodes WHERE organization_id = '<org-id>'
   UNION ALL SELECT 'videos', count(*) FROM videos WHERE organization_id = '<org-id>';
   ```
   Report counts. Zero counts for enabled content types are warnings.

4. **Storage buckets**: Check if the tenant has a storage folder:
   ```sql
   SELECT name FROM storage.buckets WHERE name LIKE '%media%';
   ```
   Note: tenant images typically live under `media-library/<tenant-slug>/` in Supabase Storage.

5. **Vector store** (if AI features enabled): Check if `OPENAI_VECTOR_STORE_ID` is documented or if the org has corpus content:
   ```sql
   SELECT count(*) FROM book_chapters WHERE book_id IN (SELECT id FROM books WHERE organization_id = '<org-id>');
   ```

### Phase 2: Tenant Config Audit

Read and audit `src/lib/config/tenant.config.ts`:

1. **Name/identity fields** — Must NOT reference the source tenant:
   - `name`, `tagline`, `description`, `copyright`
   - `logo.text`, `logo.imageUrl`, `logo.markLightUrl`, `logo.markDarkUrl`
   - `about.heading`, `about.leadSentence`, `about.body`, `about.credentials`
   - `contact.email`, `contact.speakingNote`
   - `search.placeholder` (should not say "Search Alan's...")
   - `newsletter.headline`, `newsletter.subline`, `newsletter.leadMagnet`
   - `quote.text`, `quote.cite`

2. **Feature flags** — `features.*` should reflect what the new tenant actually has:
   - If `features.books === true`, there must be books in the DB for this org
   - If `features.courses === true`, there must be courses
   - If `features.chat === true`, AI/agent infrastructure must be configured
   - If `features.assessments === true`, assessment records must exist
   - If `features.podcasts === true`, podcast episodes must exist

3. **Chat config** — All chat strings reference source tenant's name/voice:
   - `chat.welcomeMessage`, `chat.disclaimer`, `chat.featuredSubline`
   - `chat.firstMessageHost`, `chat.assistantLabel`
   - `chat.floatingDocsAriaLabel`

4. **Themes/pathways** — These are deeply tenant-specific:
   - `themes[]` slugs, titles, descriptions, coverImages
   - `frameworks.items[]` slugs and descriptions
   - `pathwayCta.*` content
   - `home.router.options[]` and `home.router.ctas[]`

5. **Organizations/partners** — `organizations.items[]` must be the new tenant's partners, not the source's

6. **Pricing** — `pricing.plans[]` may differ per tenant

7. **Author profile (EEAT)** — `authorProfile.*` must reflect the new author

8. **Hero** — `hero.*` heading, subheading, CTAs, imageUrl, backgroundImageUrl

9. **Content type descriptions** — `contentTypes.*` descriptions reference source tenant's domain

10. **Home page sections** — `home.*` section copy

### Phase 3: Environment Variables

Read `.env.local.example` and verify:

1. `TENANT_ORG_ID` — Must be the new tenant's org UUID
2. `DATABASE_URL` — Same shared Supabase instance
3. `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Same project
4. `OPENAI_API_KEY` / `OPENAI_MODEL` — If chat enabled
5. `OPENAI_VECTOR_STORE_ID` — Tenant-specific vector store for RAG
6. `AI_LAB_AGENT_URL` / `AI_LAB_AGENT_API_KEY` — If using external agent
7. `STRIPE_SECRET_KEY` / `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` — Tenant-specific Stripe account
8. `SENTRY_DSN` / `SENTRY_PROJECT` — Tenant-specific Sentry project
9. `COURSE_PREVIEW_HMAC_SECRET` — Must match studio if using course preview

### Phase 4: Codebase Grep for Source Tenant Leaks

Search the entire `src/` directory for hardcoded references to the source tenant:

```
Grep for: "Alan Hirsch", "alan-hirsch", "alanhirsch", "Alan's", "mDNA", "APEST", "Forgotten Ways", "5Q", "Reframation"
```

Exclude:
- `tenant.config.ts` (that's the config file itself)
- `node_modules/`, `.next/`, `_docs/`
- Comments in generated files

Any hits in components, pages, or services are violations that must be fixed.

### Phase 5: Middleware & Auth

Read `src/middleware.ts` and verify:
- Protected route patterns still make sense for the new tenant
- No hardcoded paths specific to the source tenant

### Phase 6: Vercel Deployment

Check for Vercel project linkage:
- `.vercel/project.json` — Should reference the new tenant's Vercel project
- Environment variables must be set in Vercel dashboard for all required vars

## Output Format

Generate a structured migration report:

```markdown
# Tenant Migration Report: [source] → [target]

## Status Summary
- Database org: [PASS/FAIL/MISSING]
- Tenant config: [X/Y fields migrated]
- Env vars: [CONFIGURED/NEEDS ATTENTION]
- Source tenant leaks: [N violations found]
- Middleware/auth: [PASS/NEEDS REVIEW]
- Vercel deployment: [LINKED/NOT LINKED]

## Critical (must fix before launch)
1. ...

## Warnings (should fix)
1. ...

## Passed
1. ...

## Recommended Next Steps
1. ...
```

## Important Rules

- **Never modify the Drizzle schema** for migration purposes
- **Never create database rows** without explicit user approval
- **Use Supabase MCP** for all database queries — do not guess structure
- **If MCP is unavailable**, report what you can from code inspection alone and note which DB checks were skipped
- **Visual theming (globals.css) and image assets are out of scope** — handle those separately via `/color-audit`, `/asset-match`, or manual design work
- **The tenant.config.ts + .env.local are the two files that MUST change** for every migration — everything else is structural
- **Run `/tenant-check` after migration** to verify no hardcoded strings leaked through
