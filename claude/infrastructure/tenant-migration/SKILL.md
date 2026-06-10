---
name: tenant-migration
description: "End-to-end migration skill for spinning up a new movement leader platform from an existing tenant baseline. Covers repo setup, Vercel deployment, env vars, org/tenant config, Supabase storage, Claude/Cursor project files, docs cleanup, front-end customization, and post-migration verification. The default migration strategy for all new tenant platforms."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, WebFetch
---

Migrate or plan a new tenant platform: $ARGUMENTS

$ARGUMENTS can include:
- "plan <leader-name>" — Generate a migration plan for a new leader (no changes made)
- "execute <leader-name>" — Execute the migration interactively (step-by-step with confirmation)
- "audit <repo-path>" — Audit an already-migrated repo for leftover source-tenant contamination
- "verify <repo-path>" — Run full post-migration verification checklist
- "env-classify" — Show the shared vs tenant-specific env var classification
- Empty — explain the migration process and ask what to do

---

## Migration Philosophy

This is NOT a clone script. This is a **disciplined platform replication procedure** for a multi-tenant thought leader platform where:

- Architecture, stack, infrastructure, and code patterns are **standardized across all tenants**
- The differences between tenants are **controlled and enumerated** — they live in specific files, not scattered throughout
- Every new tenant starts from a **known-good baseline** (currently Alan Hirsch repo) and is carefully converted

The goal is: **create a new tenant from a standardized baseline while correctly handling all tenant-specific changes and all infrastructure setup.**

The anti-goal is: "make another Alan site" or "copy and pray."

---

## Source Baseline

Unless specified otherwise, migrations start from the **Alan Hirsch tenant app** at:
```
~/Desktop/dev/repos/movemental-sites/alan-hirsch
```

This is the current reference implementation with the most complete feature set.

---

## What Changes Between Tenants

### Always Different (Tenant-Specific)
- `src/lib/config/tenant.config.ts` — name, tagline, themes, features, content, hero, pricing, organizations
- `src/app/globals.css` — CSS variables (colors, fonts, radius) — the visual identity
- `tailwind.config.ts` — only if custom design tokens are added beyond CSS vars
- `TENANT_ORG_ID` env var — points to different organization in shared Supabase
- `public/images/` — all imagery (headshots, art, books, logos, orgs)
- `public/favicon.svg`, `public/manifest.webmanifest` — branding
- `package.json` name field
- Homepage hero content and potentially homepage section composition
- `CLAUDE.md` — tenant-specific instructions and references
- `.cursorrules` and `.cursor/rules/` — tenant-specific AI context

### Usually Identical (Shared Architecture)
- All 148 database tables (shared Supabase instance, scoped by org_id)
- Six-layer type safety chain (schema → zod → services → routes → hooks → UI)
- Middleware auth logic
- All content page templates (articles, books, courses, podcasts, videos)
- All services, hooks, API routes
- Component library (`src/components/ui/`)
- AI agent infrastructure
- Scripts and generators
- Test infrastructure

### Sometimes Different (Assess Per Tenant)
- Homepage section composition (which sections appear, order)
- Which feature flags are enabled
- Navigation labels
- Which content types are active
- Pricing tiers and Stripe products
- AI Lab configuration and agent persona
- Which pathways/themes are defined

---

## Migration Procedure — Step by Step

### PHASE 0: PRE-FLIGHT

Before touching anything:

- [ ] **Confirm the new leader's organization exists in Supabase**
  - Query: `SELECT id, name, slug FROM organizations WHERE slug = '<leader-slug>';`
  - If not: create the org record first. The `TENANT_ORG_ID` is the foundation of everything.
  - Use Supabase MCP: `mcp__supabase__execute_sql` against project `vhaiiiykcukrlyvwlgip`

- [ ] **Confirm content exists for the org**
  - Check: books, articles, courses associated with that org_id
  - If empty: plan content ingestion as a follow-up, but proceed with migration

- [ ] **Choose a repo name and slug**
  - Convention: `~/Desktop/dev/repos/<leader-slug>` (e.g., `brad-brisco`, `mike-frost`)
  - This becomes the directory name, package.json name, and Vercel project name

- [ ] **Confirm no existing repo at that path**
  ```bash
  ls ~/Desktop/dev/repos/<leader-slug> 2>/dev/null && echo "EXISTS — STOP" || echo "Clear"
  ```

---

### PHASE 1: REPO CREATION

**Goal:** Clean new repo with no Git history from the source.

```bash
# 1. Copy the source repo (excluding build artifacts and local state)
rsync -av --progress \
  --exclude='.next' \
  --exclude='node_modules' \
  --exclude='.vercel' \
  --exclude='.env' \
  --exclude='.env.local' \
  --exclude='.turbo' \
  --exclude='reports' \
  --exclude='.stitch' \
  --exclude='public/.image-backups' \
  --exclude='public/images/.backup' \
  ~/Desktop/dev/repos/movemental-sites/alan-hirsch/ \
  ~/Desktop/dev/repos/<leader-slug>/

# 2. Remove source Git history — start fresh
cd ~/Desktop/dev/repos/<leader-slug>
rm -rf .git

# 3. Initialize new repo
git init
git checkout -b main

# 4. Create GitHub repo and set remote
gh repo create <github-org>/<leader-slug> --private --source=. --remote=origin

# 5. Initial commit (before any tenant changes)
git add -A
git commit -m "init: bootstrap from movemental platform baseline"
git push -u origin main
```

**Why fresh Git history:** The source repo's commit history is Alan-specific. A new tenant should have clean history starting from "baseline." This prevents `git log` confusion, avoids leaking source tenant context into the new repo, and keeps the new repo's history meaningful.

**Critical check:** After this step, `git remote -v` must show the NEW repo's remote, not the source.

---

### PHASE 2: PACKAGE IDENTITY

```bash
cd ~/Desktop/dev/repos/<leader-slug>
```

- [ ] **Update `package.json`**
  - Change `"name"` to `"<leader-slug>"`

- [ ] **Update `public/manifest.webmanifest`**
  - Change `name` and `short_name` to the leader's platform name

---

### PHASE 3: TENANT CONFIGURATION (The Core Change)

This is where the new tenant's identity is established.

#### 3A. `src/lib/config/tenant.config.ts`

This file controls everything the user sees. For migration, methodically update:

| Section | What to change |
|---|---|
| `name` | Leader's full name |
| `tagline` | Leader's tagline |
| `description` | Leader's meta description |
| `logo` | Path to new logo in `public/images/logo/` |
| `copyright` | Updated copyright holder |
| `features` | Enable/disable per leader (articles, books, courses, podcasts, chat, etc.) |
| `contentTypes` | Labels and descriptions for each content type |
| `chat` | AI Lab persona, title, placeholders, disclaimers |
| `themes` / `pathways` | Leader's own pathways (or remove if not applicable) |
| `hero` | Homepage hero content |
| `about` | About section content |
| `organizations` | Leader's affiliated organizations |
| `pricing` | Subscription tiers (update or disable) |
| `newsletter` | Newsletter CTA copy |

**Do NOT:**
- Change the TypeScript interface/schema shape (that's shared)
- Remove required fields (set them to appropriate defaults)
- Add new fields without updating `tenant.schema.ts` first

#### 3B. `src/app/globals.css`

Replace the visual identity:

| Token | Purpose |
|---|---|
| `--primary`, `--primary-foreground` | Brand primary color |
| `--background`, `--foreground` | Page background and text |
| `--accent`, `--accent-foreground` | Accent/callout color |
| `--card`, `--card-foreground` | Card surfaces |
| `--muted`, `--muted-foreground` | Muted/secondary text |
| `--font-heading` | Heading typeface |
| `--font-body` | Body typeface |
| Surface hierarchy tokens | Tonal system for the new palette |
| Dark mode section | Full dark mode palette inversion |

**Tip:** Design the new palette in HSL. The current system uses HSL values throughout. Maintain WCAG AA contrast ratios.

#### 3C. Homepage Composition

Review `src/app/(public)/page.tsx`:
- Decide which homepage sections to keep, remove, or reorder
- The sections are modular: `<Hero />`, `<SocialProof />`, `<Pathways />`, `<AILabTeaser />`, etc.
- Feature-flagged sections (like `tenantConfig.features.chat && <AILabTeaser />`) auto-hide when disabled

#### 3D. `src/app/layout.tsx`

- Update font imports if the new tenant uses different typefaces
- Update `APP_URL` default if the production domain is known
- Metadata is driven by `tenantConfig` — no manual changes needed there

---

### PHASE 4: IMAGERY AND MEDIA

#### 4A. Local Images (`public/images/`)

Replace all source-tenant imagery:

| Directory | Content | Action |
|---|---|---|
| `public/images/logo/` | Brand logo(s) | Replace |
| `public/images/headshots/` | Leader headshots | Replace |
| `public/images/books/` | Book covers | Replace (if leader has books) |
| `public/images/art/` | Hero art, textures, pathway art | Replace or regenerate |
| `public/images/orgs/` | Organization logos | Replace |
| `public/favicon.svg` | Browser favicon | Replace |

**Use the `asset-generate` skill** for creating new imagery with Nano Banana 2 where needed.

**Naming convention:** Keep the same directory structure. Image filenames can change but update all references in `tenant.config.ts` and component files.

#### 4B. Supabase Storage (`media-library` bucket)

Images served from Supabase storage are organized by tenant/org. For the new tenant:

- [ ] Verify the `media-library` bucket has a folder for the new org
- [ ] Upload leader-specific media (profile photos, book covers, etc.)
- [ ] The platform uses `NEXT_PUBLIC_SUPABASE_URL` to construct image URLs — no code change needed since all tenants share the Supabase instance

**Verify paths:** Search for hardcoded Supabase storage URLs that reference the source tenant:
```bash
grep -r "storage/v1/object" src/ --include="*.ts" --include="*.tsx"
```

---

### PHASE 5: ENVIRONMENT VARIABLES

#### 5A. Env Var Classification

**Shared across all tenants** (same value, from `~/.env.shared`):
- `DATABASE_URL` / `DIRECT_DATABASE_URL` / pooler variants
- `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_ACCESS_TOKEN`
- `OPENAI_API_KEY` / `GOOGLE_GENERATIVE_AI_API_KEY`
- `YOUTUBE_API_KEY`
- `RESEND_API_KEY` / `RESEND_FROM_DOMAIN`
- `GITHUB_TOKEN`

**Tenant-specific** (different per tenant):
- `TENANT_ORG_ID` — **CRITICAL**: must be the new org's UUID
- `NEXT_PUBLIC_APP_URL` — production domain
- `STRIPE_SECRET_KEY` / `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` / `STRIPE_WEBHOOK_SECRET` — per-tenant Stripe account
- `SENTRY_PROJECT` / `NEXT_PUBLIC_SENTRY_DSN` / `SENTRY_DSN` — per-tenant Sentry project
- `AI_LAB_AGENT_URL` / `AI_LAB_AGENT_API_KEY` — if tenant has custom agent endpoint
- `OPENAI_VECTOR_STORE_ID` — per-tenant vector store for corpus RAG
- `COURSE_PREVIEW_HMAC_SECRET` — per-tenant signing secret
- `SIGNUP_INVITE_CODE` — per-tenant gate

**Shared but potentially overridden:**
- `SENTRY_ORG` — same org unless separate Sentry org
- `OPENAI_MODEL` — same default unless tenant needs different model
- `RESEND_FROM_NAME` — sender name per tenant

#### 5B. Local Setup

```bash
cd ~/Desktop/dev/repos/<leader-slug>

# 1. Create .env.local from template
cp .env.local.example .env.local

# 2. Update TENANT_ORG_ID to the new org's UUID
# 3. Update .env.local.example with new org's reference query
# 4. Shared vars are loaded from ~/.env.shared via direnv — verify:
echo $DATABASE_URL  # should be set from parent .envrc
```

#### 5C. Vercel Env Setup

```bash
# After Vercel project is linked (Phase 6):
vercel env ls  # audit what's set

# Add tenant-specific vars:
vercel env add TENANT_ORG_ID production preview development
vercel env add NEXT_PUBLIC_APP_URL production
# ... repeat for all tenant-specific vars
```

**DANGER ZONE:** If `TENANT_ORG_ID` is wrong or missing, the entire app will show empty content or the wrong tenant's content. This is the single most critical env var.

---

### PHASE 6: VERCEL DEPLOYMENT

#### 6A. Create Vercel Project

```bash
cd ~/Desktop/dev/repos/<leader-slug>

# Link to Vercel (creates new project)
vercel link
# Follow prompts:
#   - Scope: your Vercel team
#   - Link to existing? No — create new
#   - Project name: <leader-slug>
#   - Framework: Next.js (auto-detected)
#   - Root directory: ./
```

#### 6B. Verify Linkage

```bash
# Confirm the .vercel/project.json points to the NEW project
cat .vercel/project.json
# Should show new projectId and orgId

# Confirm Git remote is correct
git remote -v
# Should show the NEW repo, not alan-hirsch
```

**Past issue:** GitHub ↔ Vercel ↔ branch confusion has caused cross-tenant deploys. Triple-check:
1. `git remote -v` → new repo
2. `.vercel/project.json` → new Vercel project
3. Vercel dashboard → project settings → Git → correct repo connected

#### 6C. Environment Variables in Vercel

Set ALL required env vars before the first deploy:
```bash
# Use vercel env add for each, or bulk import:
vercel env pull .env.vercel.local  # pull current (should be empty for new project)
```

Minimum required for first deploy:
- `TENANT_ORG_ID`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `DATABASE_URL`

#### 6D. First Deploy

```bash
# Preview deploy first (not production)
vercel deploy

# Verify the preview URL works:
# - Homepage loads
# - Correct branding shows
# - Content appears (not empty)
# - No Alan Hirsch references visible

# Only after verification:
vercel deploy --prod
```

---

### PHASE 7: CLAUDE / CURSOR PROJECT FILES

These files contain tenant-specific AI context and must be updated.

#### 7A. CLAUDE.md

Update or rewrite:
- [ ] Project name references (alan-hirsch → leader-slug)
- [ ] Any Alan-specific instructions or content references
- [ ] Supabase project ID reference (stays same if shared instance)
- [ ] Keep all architecture/convention docs — they're shared

#### 7B. `.claude/` directory

- [ ] `.claude/settings.json` — review for tenant-specific hooks or commands
- [ ] `.claude/settings.local.json` — likely needs no change (local prefs)
- [ ] `.claude/projects/` memory — **DELETE entirely**. Memory from the source tenant is irrelevant and potentially confusing. Start fresh.
  ```bash
  rm -rf .claude/projects/
  ```
- [ ] `.claude/skills/` — **KEEP as-is**. Skills are platform-level, not tenant-specific.

#### 7C. `.cursorrules` and `.cursor/rules/`

- [ ] Update `.cursorrules` if it references tenant-specific docs
- [ ] Review `.cursor/rules/*.mdc` files — they're mostly platform conventions (keep)
- [ ] Remove any rules that reference Alan-specific content, pathways, or themes

---

### PHASE 8: DOCUMENTATION CLEANUP

#### 8A. Keep (Platform Documentation)
- `_docs/CONSTITUTION.md`
- `_docs/_build/` — engineering docs, prompts, type safety docs
- `_docs/_build/_prompts/engineering/` — audit prompts

#### 8B. Remove or Prune
- `_docs/_temp/` — contains Alan-specific analysis, RLS findings, AI Lab specs
  - Keep: architectural findings that apply to all tenants
  - Remove: content-specific analysis, tenant-specific notes
- `_docs/_build/_prompts/` subdirs with Alan-specific content prompts
- `_docs/_build/_uploads/` — source tenant MCP queries

#### 8C. Rewrite
- `_docs/README.md` — update for new tenant
- Any STATUS_REPORT or similar that references Alan-specific state

#### 8D. Decision Framework
Ask: "Does this doc describe the **platform** or does it describe **Alan's content/brand**?"
- Platform docs → keep
- Content/brand docs → remove or rewrite

---

### PHASE 9: SEARCH AND DESTROY — SOURCE TENANT CONTAMINATION

Run these searches against the new repo to catch leftover references:

```bash
# Source tenant name in code
grep -ri "alan hirsch" src/ --include="*.ts" --include="*.tsx" -l
grep -ri "alan hirsch" _docs/ -l
grep -ri "alanhirsch" src/ --include="*.ts" --include="*.tsx" -l

# Source domain
grep -ri "alanhirsch.com" src/ -l

# Source org ID (get from source .env.local)
grep -r "SOURCE_ORG_UUID_HERE" src/ -l

# Hardcoded source imagery paths
grep -ri "alan" public/images/ -l

# Source tenant in metadata/SEO
grep -ri "alan" src/app/layout.tsx
grep -ri "alan" public/manifest.webmanifest
```

**Every hit must be resolved.** Most will be in `tenant.config.ts` (which you already updated), but check for leaks in:
- Component files with hardcoded strings
- SEO metadata
- Alt text on images
- Email templates
- Error messages or placeholder text

---

### PHASE 10: INSTALL, BUILD, VERIFY

```bash
cd ~/Desktop/dev/repos/<leader-slug>

# 1. Install dependencies
pnpm install

# 2. Typecheck
pnpm typecheck

# 3. Build
pnpm build

# 4. Run locally
pnpm dev
# Visit http://localhost:3000 and verify:
#   - Correct branding (name, colors, fonts)
#   - Content loads (books, articles, courses if content exists)
#   - No source tenant references
#   - Feature flags work (disabled features are hidden)
#   - Auth flow works
#   - Dark mode works with new palette

# 5. Run tests
pnpm test:run

# 6. Layer validation
pnpm validate:all
```

---

## Failure Modes — What Commonly Goes Wrong

| # | Failure | Symptom | Prevention |
|---|---|---|---|
| 1 | Wrong `TENANT_ORG_ID` | Empty content pages, wrong tenant's data | Verify org UUID with SQL query before setting |
| 2 | Source Git remote still attached | Pushes go to Alan's repo | `rm -rf .git && git init` at Phase 1 |
| 3 | `.vercel/project.json` from source | Deploys to Alan's Vercel project | Delete `.vercel/` before `vercel link` |
| 4 | Hardcoded "Alan Hirsch" in components | Source name appears in new tenant site | Run contamination search (Phase 9) |
| 5 | Source CSS palette not replaced | New site looks like Alan's site | Update ALL CSS vars in globals.css |
| 6 | Source images not replaced | Alan's headshot/books on new site | Replace all of `public/images/` |
| 7 | Source `.claude/projects/` memory copied | AI assistant has Alan-context hallucinations | Delete `.claude/projects/` directory |
| 8 | Shared env vars missing | Build fails or runtime crashes | Verify direnv loads `~/.env.shared` |
| 9 | Stripe keys not updated | Payments go to wrong account | Set tenant-specific Stripe keys |
| 10 | Sentry DSN not updated | Errors report to wrong project | Create new Sentry project for tenant |
| 11 | `APP_URL` still set to alanhirsch.com | OG images, canonical URLs wrong | Update in layout.tsx and env |
| 12 | Source font imports in layout.tsx | Wrong typeface renders | Update Google Fonts imports |
| 13 | Vector store ID from source | AI chat retrieves Alan's corpus | Create new vector store or clear |
| 14 | Dark mode palette not updated | Light mode looks right, dark mode is still plum | Update BOTH light and dark sections in globals.css |
| 15 | Pathway/theme slugs from source | 404s on pathway pages | Update theme definitions in tenant.config.ts |

---

## Post-Migration Verification Checklist

Run `/tenant-migration verify <repo-path>` or manually check:

### Identity
- [ ] `package.json` name matches leader-slug
- [ ] `tenant.config.ts` has no source tenant references
- [ ] `globals.css` has new color palette (not plum/parchment unless intentional)
- [ ] `layout.tsx` imports correct fonts
- [ ] `manifest.webmanifest` has new name
- [ ] `favicon.svg` is new

### Content
- [ ] Homepage shows correct leader name and tagline
- [ ] Books page shows leader's books (or is disabled)
- [ ] Articles page shows leader's articles (or is disabled)
- [ ] Courses page shows leader's courses (or is disabled)
- [ ] No "Alan Hirsch" text anywhere on the site

### Infrastructure
- [ ] `git remote -v` shows new repo
- [ ] `.vercel/project.json` has new project ID
- [ ] `TENANT_ORG_ID` is correct UUID
- [ ] Vercel env vars are set
- [ ] Preview deploy succeeds
- [ ] Production deploy succeeds (when ready)

### Visual
- [ ] Brand colors correct in light mode
- [ ] Brand colors correct in dark mode
- [ ] Fonts render correctly
- [ ] All images are new tenant's (no source tenant imagery)
- [ ] Logo is correct

### Technical
- [ ] `pnpm typecheck` passes
- [ ] `pnpm build` succeeds
- [ ] `pnpm test:run` passes
- [ ] `pnpm validate:all` passes
- [ ] No console errors in browser dev tools

### Contamination Search
- [ ] `grep -ri "alan hirsch" src/` returns 0 results (after tenant.config.ts update)
- [ ] `grep -ri "alanhirsch.com" src/` returns 0 results
- [ ] No source org UUID in any file

---

## Process Improvement Recommendations

1. **Extract a baseline branch/tag:** Rather than copying from Alan's repo each time, maintain a `baseline` branch or tag that strips all tenant-specific content. New tenants fork from baseline, not from Alan.

2. **Tenant config generator script:** Create `scripts/init-tenant.ts` that takes a leader name, slug, and org ID, then scaffolds `tenant.config.ts` with placeholder values and correct structure.

3. **Standardize media pipeline:** Create a `scripts/scaffold-tenant-media.ts` that creates the correct `public/images/` directory structure with placeholder images and a manifest of what needs to be replaced.

4. **Env var template per tenant:** Store a `_docs/env-template.md` that explicitly lists every env var with its classification (shared/tenant-specific) and setup instructions.

5. **Post-migration CI check:** Add a GitHub Action that runs the contamination search on every PR to prevent source tenant references from creeping back in.

6. **Shared component library:** Long-term, extract `src/components/ui/` and shared services into an npm package or git submodule so updates propagate to all tenants automatically instead of requiring re-migration.
