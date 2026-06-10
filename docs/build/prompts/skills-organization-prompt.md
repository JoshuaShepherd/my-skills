# Prompt: Reorganize `my-skills` into a logical, maintainable catalog

Use this document as a **step-by-step operator prompt** to reorganize the `my-skills` repository so ~250+ skill bundles are grouped by domain, duplicates are resolved, and install/sync behavior stays predictable for Claude Code, Cursor, and agent runtimes.

> **Audit snapshot (2026-05-30):** ~258 top-level Claude skill bundles, 42 Cursor bundles under `cursor/`, 3 agent bundles under `agents/`, 126 repo-specific overlays across 3 portals, 12 OpenAI vendor skills under `skills-openai/`, plus partial category folders (`analytics/`, `data/`, `design/`, `strategy/`, `stitch/`) containing stale or orphan markdown that does not match current `SKILL.md` bundles.

---

## 0. Read first — what organization can and cannot do

### Runtime discovery (unchanged)

Claude Code and Cursor discover skills from **flat** install paths:

```text
~/.claude/skills/<skill-name>/SKILL.md
~/.cursor/skills/<skill-name>/SKILL.md
```

Category folders **inside** `.claude/skills/` (e.g. `.claude/skills/design/foo/SKILL.md`) are **not** discovered. Organization in `my-skills` is for humans and sync tooling; consumers still symlink **one skill folder → one flat runtime name**.

### What this reorg fixes

| Problem today | After reorg |
|---------------|-------------|
| ~258 bundles at repo root — hard to browse | Domain folders under `claude/<domain>/` |
| `design/`, `analytics/`, etc. hold outdated `.md` copies | Retired; content merged into canonical bundles or `references/` |
| 80 skills duplicated in both top-level and `repo-specific/` | Canonical in `claude/`; overlays only when genuinely different |
| 27 skills in both top-level and `cursor/` | Cursor stays in `cursor/`; shared logic lives in `claude/` once |
| `skills-openai/` at ambiguous top level | Moved to `vendor/skills-openai/` |
| No domain index | `SKILLS_MANIFEST.json` gains `domain` field + `CATALOG.md` |

---

## 1. Target repository layout

Adopt a **runtime-axis-first** layout: prefix by *where the skill installs*, then organize Claude bundles by domain.

```text
my-skills/
├── README.md
├── CATALOG.md                      # human-readable domain index (generated)
├── SKILLS_MANIFEST.json            # machine index (extended)
├── scripts/
│   ├── sync-claude-skills.py       # updated dest_key rules
│   ├── assign-skill-domains.py     # new: domain map + validation
│   └── install-skill.sh              # new: symlink helper
│
├── claude/                         # canonical shared Claude Code skills
│   ├── movemental/                 # platform, TAM, leader research, tenant
│   ├── content/                    # articles, books, courses, pathways
│   ├── research/                   # scrape, transcript, summarize, models
│   ├── design/                     # UI, Tailwind, responsive, visual audit
│   ├── assets/                     # image/video generation, remotion, deliver
│   ├── stitch/                     # Stitch design-build loop
│   ├── studio/                     # content studio export/style/prompt
│   ├── agents/                     # agent builder, RAG, tools, guardrails
│   ├── infrastructure/             # supabase, vercel, stripe, testing, tenant
│   ├── integrations/               # API wrappers (openai, claude, gemini, mcp)
│   ├── codegen/                    # standards, scaffolds, app-architect
│   └── docs/                       # docs-setup, type-safety docs, design-system
│
├── cursor/                         # Cursor-only or Cursor-first skills (flat)
├── agents/                         # ~/.agents/skills bundles (flat)
├── repo-specific/                  # portal overlays (unchanged shape)
│   ├── alan-hirsch/
│   ├── adam-seiz/
│   └── movemental-content-studio/
├── vendor/                         # third-party skill trees (install selectively)
│   └── skills-openai/
├── references/                     # non-skill reference docs (not bundles)
│   └── design/                     # excalidraw, mermaid, breakpoint guides, etc.
└── _reference/                     # upstream vendor mirrors (read-only, no sync)
```

### Install mapping (consumer contract)

| Repo path | Install target |
|-----------|----------------|
| `claude/<domain>/<name>/` | `~/.claude/skills/<name>/` |
| `cursor/<name>/` | `~/.cursor/skills/<name>/` |
| `agents/<name>/` | `~/.agents/skills/<name>/` |
| `repo-specific/<portal>/<name>/` | `<project>/.claude/skills/<name>/` (project-only) |
| `vendor/skills-openai/<name>/` | `~/.claude/skills/<name>/` (opt-in) |

Example:

```bash
REPO="$(pwd)"
ln -sf "$REPO/claude/content/article-author" ~/.claude/skills/article-author
ln -sf "$REPO/cursor/ssot-dashboard" ~/.cursor/skills/ssot-dashboard
ln -sf "$REPO/repo-specific/alan-hirsch/alan-voice" \
  ~/path/to/alan-hirsch/.claude/skills/alan-voice
```

---

## 2. Domain taxonomy — assignment rules

Assign every canonical skill to **exactly one** domain. Use the **`name:` frontmatter field** as the stable identity; folder path is organizational only.

### Domain definitions

| Domain | Purpose | Prefix / name patterns |
|--------|---------|------------------------|
| **movemental** | Movemental platform, leader substrate, TAM, tenant, welcome letter, affiliations, network | `movemental-*`, `movement-leader-*`, `tam-*`, `network-map`, `affiliation-*`, `fragmentation-story`, `voice-designer`, `logo-strip-*`, `stakeholder-map`, `ml-template-*`, `oatmeal-template-*`, `platform-demo-*`, `transformative-learning-*`, `home-consult`, `domain-finder`, `poll-opinion-*`, `nonprofit-pricing-*` |
| **content** | Authoring pipelines: articles, books, courses, pathways, paratext, story | `article-*`, `book-*`, `course-*`, `pathway-*`, `paratext-*`, `week-author`, `story-architect`, `author-*`, `writing-agent-builder`, `dialogue-craft`, `prose-craft`, `nonfiction-craft`, `editorial-lens`, `content-*`, `corpus-*`, `ingest-content`, `scaffold-course`, `validate-course`, `alan-voice` |
| **research** | Ingestion, scraping, transcripts, summarization, model research | `*-scrape`, `youtube-*`, `summarize`, `markitdown`, `academic-research`, `author-research`, `brainstorming`, `ai-model-*`, `review-scrape`, `visual-scrape`, `audio-scrape` |
| **design** | Visual/UI audit, Tailwind, typography, layout, page audit | `design-*`, `frontend-*`, `responsive-*`, `typography-*`, `color-audit`, `icon-*`, `animation`, `visual-*`, `web-design-*`, `web-component-*`, `tailwind-*`, `ckmui-*`, `chat-ui-*`, `ui-hook-*`, `puck-*`, `figma-*`, `html-to-react-*`, `typeset`, `applying-brand-*`, `designer-dashboard`, `audit-experience`, `page-audit`, `new-page`, `add-section-type`, `movemental-page-auditor`, `movemental-narrative-audit`, `movemental-prose` |
| **assets** | Generated media, headshots, remotion, video consult | `asset-*`, `fal-ai-*`, `nano-banana-*`, `image-optimize`, `remotion*`, `video-*`, `pdf-ebook`, `gpt-export`, `scientific-schematics` |
| **stitch** | Google Stitch workflow | `stitch-*` |
| **studio** | Content studio design/export/style | `studio-*` |
| **agents** | Agent construction, RAG, streaming, guardrails | `agent-*`, `create-agent`, `build-rag`, `build-context`, `openai-vector-store`, `data-scraper-agent`, `add-tool`, `add-guardrail`, `configure-handoff`, `debug-traces`, `setup-streaming` |
| **infrastructure** | Auth, DB, deploy, analytics, testing, repo hygiene | `supabase-*`, `postgres-*`, `tenant-*`, `auth-setup`, `stripe-*`, `vercel-*`, `sentry-*`, `posthog-*`, `ga4-*`, `analytics-*`, `telemetry-*`, `security-*`, `seo-setup`, `email-setup`, `ci-setup`, `env-setup`, `migrations-*`, `deploy-to-vercel`, `infrastructure`, `project-setup`, `testing-setup`, `write-tests`, `type-fix`, `type-safety-*`, `e2e-studio-*`, `liveblocks-*`, `nextjs-supabase-*`, `scaffolding`, `repo-cleanup`, `workspace-*`, `validate`, `frontend-cleanup`, `vite-audit`, `react-audit`, `translation-audit`, `feature-constitution` |
| **integrations** | Thin API / MCP skills | `openai-api`, `claude-api`, `gemini-api`, `grok-api`, `context7-mcp`, `github`, `awesome-postgres`, `ai-lab-notebook-gemini` |
| **codegen** | Scaffolds, coding standards, architecture | `codegen`, `coding-standards`, `javascript-typescript-*`, `build-prompt`, `write-instructions`, `fullstack-developer`, `app-architect`, `react-best-practices`, `react-native-*`, `composition-patterns`, `postgres-patterns`, `postgres-schema-design`, `storybook-setup`, `generate`, `visualization-expert`, `visualization-repair`, `add-table` |

### Manual exceptions (assign explicitly)

These names do not match a clean prefix — set domain by hand in the domain map:

| Skill | Domain | Reason |
|-------|--------|--------|
| `alan-voice` | content | Voice profile for content authoring, not platform ops |
| `add-table` | codegen | Schema/table scaffolding utility |
| `generate` | codegen | Generic codegen entry |
| `visualization-expert` / `visualization-repair` | codegen | Chart/viz code, not design audit |
| `storybook-setup` | codegen | Dev tooling scaffold |
| `ai-lab-notebook-gemini` | integrations | API/notebook wrapper |

---

## 3. Step-by-step migration

Execute in order. **Report before move** each phase; use `git mv` to preserve history.

### Phase 1 — Freeze and inventory (no moves yet)

1. Regenerate the manifest:

   ```bash
   python3 scripts/sync-claude-skills.py
   ```

2. Generate a domain assignment file:

   ```bash
   python3 scripts/assign-skill-domains.py --check > _docs/_build/domain-assignment-report.md
   ```

   The script should:
   - List every top-level bundle with proposed domain
   - Flag unassigned names
   - Flag duplicates across `repo-specific/`, `cursor/`, and top-level
   - Flag orphan files in legacy folders (`analytics/`, `design/`, etc.)

3. Review the report. Resolve unassigned skills before Phase 2.

**Exit criteria:** Zero unassigned canonical skills; operator sign-off on domain map.

---

### Phase 2 — Retire legacy category folders

These folders are **not** valid skill bundles — they contain `.md` files without the `skill-name/SKILL.md` structure:

- `analytics/*.md`
- `data/*.md`
- `design/*.md` (+ `design/responsive-design-references/`)
- `strategy/*.md`
- `stitch/*.md`

For each file:

1. **If a top-level `SKILL.md` bundle exists** for the same name (e.g. `animation` ↔ `design/animation.md`):
   - Diff the files. **Keep the `SKILL.md` bundle as canonical** (it is newer/larger in spot checks).
   - If the `.md` copy has unique sections, merge them into the bundle's `references/` subfolder.
   - Delete the orphan `.md` after merge.

2. **If no bundle exists** (e.g. `design/excalidraw.md`, `design/mermaid.md`):
   - Move to `references/design/<name>.md` — reference material, not an installable skill.
   - Optionally later promote to a full skill if it gets frontmatter + trigger description.

3. Remove empty legacy folders when done.

**Exit criteria:** No `analytics/`, `data/`, `design/`, `strategy/`, or `stitch/` folders at repo root (except under `claude/` or `references/`).

---

### Phase 3 — Create `claude/<domain>/` and move canonical bundles

1. Create domain directories under `claude/`.

2. For each top-level skill bundle (directory containing `SKILL.md` or `skill.md` at its root):
   - Look up domain in the assignment map.
   - Move:

     ```bash
     git mv article-author claude/content/article-author
     git mv tam-profile claude/movemental/tam-profile
     # ... repeat for all canonical bundles
     ```

3. **Do not move:**
   - `cursor/`, `agents/`, `repo-specific/`, `vendor/`, `_reference/`, `scripts/`, `.github/`

4. Fix **broken relative links** in moved skills (e.g. `[../movement-leader-substrate/SKILL.md]` → `[../../movemental/movement-leader-substrate/SKILL.md]`). Run:

   ```bash
   rg '\]\(\.\./' claude/ --glob 'SKILL.md'
   ```

**Exit criteria:** No top-level skill bundles remain except `cursor/`, `agents/`, `repo-specific/`, `vendor/`.

---

### Phase 4 — Consolidate vendor and reference trees

1. Move OpenAI skills:

   ```bash
   git mv skills-openai vendor/skills-openai
   ```

2. Keep `_reference/` unchanged (Anthropic samples, upstream mirrors).

3. Populate `references/` from Phase 2 orphan docs.

---

### Phase 5 — Deduplicate `repo-specific/` overlays

Policy:

| Situation | Action |
|-----------|--------|
| `repo-specific/<portal>/<name>/` is **byte-identical** to `claude/<domain>/<name>/` | Delete overlay; document that portal uses canonical |
| Overlay differs slightly (portal-specific paths, examples) | Keep overlay; add `README.md` in overlay noting delta vs canonical |
| Skill exists **only** in `repo-specific/` | Keep; tag as `portal-exclusive` in manifest |
| Skill in `repo-specific/` but canonical should exist | Copy best version to `claude/`; trim overlay to diff-only or delete |

Run a diff pass:

```bash
python3 scripts/assign-skill-domains.py --dedupe-repo-specific
```

Prioritize portals:

1. `alan-hirsch` (88 bundles) — largest overlap with canonical
2. `adam-seiz` (25)
3. `movemental-content-studio` (13)

**Exit criteria:** Every `repo-specific` bundle is either portal-exclusive or documented as an intentional override.

---

### Phase 6 — Reconcile `cursor/` vs `claude/`

For the 27 skills present in both `cursor/<name>/` and canonical `claude/`:

| Skill type | Policy |
|------------|--------|
| Cursor-specific (IDE settings, Cursor SDK) | Keep in `cursor/` only |
| Same skill, two copies | Keep richer `claude/` copy; make `cursor/<name>/` a thin wrapper whose `SKILL.md` says "Load canonical from claude domain X" **or** delete Cursor copy if identical |
| Cursor extended version | Keep both; manifest notes `cursor` as alternate source |

Do **not** block migration on perfect dedup — document alternates in manifest `sources`.

---

### Phase 7 — Update sync script and manifest schema

Extend `scripts/sync-claude-skills.py`:

1. **New dest_key for Claude skills:** `claude/<domain>/<name>/` instead of `<name>/`.

2. **Domain resolution:** After discovering `<repo>/.claude/skills/<name>/`, consult `scripts/skill-domains.json` (generated from assign script) to pick domain folder.

3. **Backward compatibility (optional transition):** If `claude/<domain>/<name>/` missing, fall back to top-level `<name>/` and log a warning.

4. Extend `SKILLS_MANIFEST.json` entries:

   ```json
   {
     "article-author": {
       "domain": "content",
       "dest_path": "claude/content/article-author",
       "runtime_name": "article-author",
       "canonical_repo": "...",
       "sources": [...]
     }
   }
   ```

5. Regenerate manifest and commit.

---

### Phase 8 — Generate human catalog

Create `CATALOG.md` at repo root (generated, not hand-edited):

```bash
python3 scripts/assign-skill-domains.py --write-catalog
```

Structure:

```markdown
# Skill catalog

## movemental (32)
| Skill | Description (first line) | Install |
|-------|--------------------------|---------|
| tam-profile | ... | claude/movemental/tam-profile |
...
```

---

### Phase 9 — Fix anomalies

Clean up known issues discovered in audit:

| Issue | Action |
|-------|--------|
| `remotion 2/` (space in folder name) | Merge into `claude/assets/remotion/` references or rename to `remotion-v2`; spaces break tooling |
| `skills-lock.json` | Move to `scripts/` or document purpose; remove from root if obsolete |
| Duplicate stitch docs at `stitch/*.md` and `claude/stitch/*/SKILL.md` | Phase 2 merge |
| `docs/build/prompts/master-skills-repo-prompt.md` | Update layout table to reference `claude/<domain>/` |

---

### Phase 10 — Update README and install helper

1. Update root `README.md` layout table:

   | Source | Destination in `my-skills` |
   |--------|---------------------------|
   | `<repo>/.claude/skills/<name>/` | `claude/<domain>/<name>/` |
   | `<repo>/.cursor/skills/<name>/` | `cursor/<name>/` |
   | `<repo>/.agents/skills/<name>/` | `agents/<name>/` |
   | `<repo>/skills/repo-specific/<portal>/<name>/` | `repo-specific/<portal>/<name>/` |

2. Add `scripts/install-skill.sh`:

   ```bash
   #!/usr/bin/env bash
   # Usage: install-skill.sh article-author
   # Resolves domain from manifest and symlinks into ~/.claude/skills/
   ```

3. Cross-link from `docs/build/prompts/master-skills-repo-prompt.md` to this document.

---

## 4. Verification checklist

Run after migration:

```bash
# 1. No stray top-level bundles (except allowed dirs)
find . -maxdepth 1 -type d ! -name '.*' ! -name 'claude' ! -name 'cursor' \
  ! -name 'agents' ! -name 'repo-specific' ! -name 'vendor' ! -name '_reference' \
  ! -name 'references' ! -name 'scripts' ! -name 'docs' -exec test -f {}/SKILL.md \; -print

# 2. Every claude bundle has SKILL.md
find claude -name SKILL.md | wc -l   # expect ~240+

# 3. Domain map complete
python3 scripts/assign-skill-domains.py --check
# exit 0

# 4. Manifest regenerates cleanly
python3 scripts/sync-claude-skills.py

# 5. No broken intra-skill links
rg '\]\(\.\./\.\./\.\./' claude/ --glob '*.md' | wc -l   # investigate any hits

# 6. Install smoke test
scripts/install-skill.sh article-author
test -L ~/.claude/skills/article-author
test -f ~/.claude/skills/article-author/SKILL.md
```

**Definition of done:**

1. All canonical Claude skills live under `claude/<domain>/<name>/`.
2. Legacy flat folders (`analytics/`, `design/`, etc.) are gone or moved to `references/`.
3. `SKILLS_MANIFEST.json` includes `domain` and `dest_path`.
4. `CATALOG.md` renders browsable domain index.
5. `README.md` install examples use new paths.
6. Fresh clone + `install-skill.sh` reproduces a working `~/.claude/skills/` surface.

---

## 5. Full domain assignment (canonical top-level bundles)

Use this table as the initial `skill-domains.json`. Adjust only with reason documented in git commit message.

### movemental (32)

`affiliation-audit`, `affiliation-scrape`, `domain-finder`, `fragmentation-story`, `home-consult`, `logo-strip-author`, `ml-template-from-reference`, `movement-leader-substrate`, `movemental-committed-voice-bio`, `movemental-narrative-audit`, `movemental-page-auditor`, `movemental-prose`, `movemental-tenant-provision`, `movemental-welcome-letter`, `movemental-welcome-letter-publish`, `network-map`, `nonprofit-pricing-research`, `oatmeal-template-audit`, `platform-demo-architect`, `poll-opinion-research`, `stakeholder-map`, `tam-audit`, `tam-blind-spots`, `tam-discover`, `tam-headshot-source`, `tam-international`, `tam-network-map`, `tam-profile`, `tam-reflected-understanding`, `tam-score`, `transformative-learning-collaborator`, `voice-designer`

### content (42)

`alan-voice`, `article-audit`, `article-author`, `article-corpus`, `article-plan`, `author-content`, `author-research`, `author-style-guide`, `book-audit`, `book-chunk`, `book-convert`, `book-fix`, `book-frontmatter`, `book-ingest`, `book-pipeline`, `book-rag-push`, `book-validate`, `content-creator`, `content-ingest`, `corpus-ingestion`, `course-audit`, `course-author`, `course-ingest`, `course-scaffold`, `course-section`, `course-ux`, `course-validate`, `dialogue-craft`, `editorial-lens`, `ingest-content`, `nonfiction-craft`, `paratext-audit`, `paratext-author`, `pathway-audit`, `pathway-author`, `pathway-builder`, `prose-craft`, `scaffold-course`, `story-architect`, `validate-course`, `week-author`, `writing-agent-builder`

### research (11)

`academic-research`, `ai-model-insights`, `ai-model-research`, `audio-scrape`, `brainstorming`, `markitdown`, `review-scrape`, `summarize`, `visual-scrape`, `youtube-scrape`, `youtube-transcript`

### design (33)

`add-section-type`, `animation`, `applying-brand-guidelines`, `audit-experience`, `chat-ui-audit`, `ckmui-styling`, `color-audit`, `design-audit`, `design-chain`, `design-chain-audit`, `design-section`, `designer-dashboard`, `figma-prompt`, `frontend-cleanup`, `frontend-design`, `frontend-patterns`, `html-to-react-tailwind`, `icon-audit`, `icon-system`, `new-page`, `page-audit`, `puck-visual-editor`, `responsive-audit`, `responsive-design`, `tailwind-cleanup`, `tailwind-design-system`, `typography-polish`, `typeset`, `ui-hook-wiring-audit`, `visual-design-foundations`, `visual-storytelling-audit`, `web-component-design`, `web-design-guidelines`

> `movemental-narrative-audit`, `movemental-page-auditor`, and `movemental-prose` live under **movemental**, not design — they audit platform narrative, not generic UI.

### assets (28)

`asset-animate`, `asset-audit`, `asset-author-style`, `asset-brand-check`, `asset-composite`, `asset-deliver`, `asset-edit`, `asset-exploded-view`, `asset-generate`, `asset-generation`, `asset-headshot`, `asset-hero-portrait`, `asset-match`, `asset-mockup`, `asset-product-shot`, `asset-prompt-library`, `asset-series`, `asset-text-overlay`, `asset-video-prompt`, `fal-ai-media`, `gpt-export`, `image-optimize`, `nano-banana-pro`, `pdf-ebook`, `remotion`, `remotion-best-practices`, `video-consult`, `video-researcher`

*(Resolve `remotion 2` → merge or rename before move.)*

### stitch (9)

`stitch-build`, `stitch-design`, `stitch-download`, `stitch-export`, `stitch-iterate`, `stitch-loop`, `stitch-react`, `stitch-ui-design`, `stitch-variants`

### studio (5)

`studio-design`, `studio-export`, `studio-prompt`, `studio-style`, `studio-testing`

### agents (20)

`add-guardrail`, `add-tool`, `agent-context`, `agent-create`, `agent-guardrail`, `agent-handoff`, `agent-instructions`, `agent-rag`, `agent-stream`, `agent-test`, `agent-tool`, `agent-trace`, `build-context`, `build-rag`, `configure-handoff`, `create-agent`, `data-scraper-agent`, `debug-traces`, `openai-vector-store`, `setup-streaming`

### infrastructure (47)

`analytics-audit`, `analytics-dashboard`, `analytics-setup`, `auth-setup`, `ci-setup`, `deploy-to-vercel`, `e2e-studio-tests`, `email-setup`, `env-setup`, `feature-constitution`, `ga4-setup`, `liveblocks-workspace`, `migrations-workflow`, `nextjs-supabase-auth`, `posthog-setup`, `postgres-patterns`, `postgres-schema-design`, `project-setup`, `react-audit`, `repo-cleanup`, `security-setup`, `sentry-setup`, `seo-setup`, `stripe-integration`, `stripe-setup`, `supabase-add-tenant-user`, `supabase-analytics`, `supabase-fix-rls`, `supabase-security-audit`, `telemetry-standards`, `tenant-check`, `tenant-migrate`, `tenant-migration`, `testing-setup`, `translation-audit`, `type-fix`, `type-safety-chain`, `validate`, `vercel-analytics`, `vercel-audit`, `vercel-cli-with-tokens`, `vercel-deploy-audit`, `vite-audit`, `workspace-author`, `workspace-organize`, `workspace-strategy`, `write-tests`

### integrations (8)

`ai-lab-notebook-gemini`, `awesome-postgres`, `claude-api`, `context7-mcp`, `gemini-api`, `github`, `grok-api`, `openai-api`

### codegen (11)

`add-table`, `app-architect`, `build-prompt`, `coding-standards`, `composition-patterns`, `fullstack-developer`, `generate`, `javascript-typescript-typescript-scaffold`, `react-best-practices`, `react-native-design`, `storybook-setup`, `visualization-expert`, `visualization-repair`, `write-instructions`

### docs (3)

`docs-design-system`, `docs-setup`, `docs-type-safety`

---

## 6. What stays flat (and why)

| Path | Why not domain-nested |
|------|----------------------|
| `cursor/` | Only 42 skills; Cursor runtime is separate; easy flat browse |
| `agents/` | Only 3–N agent-runtime bundles; mirrors `~/.agents/skills/` |
| `repo-specific/<portal>/` | Portal is the grouping dimension already |
| `vendor/skills-openai/` | Vendor pack; install individually |

---

## 7. Operating principles going forward

1. **New shared skill?** Add under `claude/<domain>/<new-name>/` — never repo root.
2. **Portal-specific override?** Add under `repo-specific/<portal>/<name>/` only when it genuinely differs.
3. **Reference doc, not a skill?** Put in `references/` — no `SKILL.md`, no frontmatter.
4. **Vendor sample?** Put in `_reference/` or `vendor/` — never mix with canonical without explicit flatten policy.
5. **Sync before commit:** Run `python3 scripts/sync-claude-skills.py` when pulling from project repos; domain assignment should persist via `skill-domains.json`.
6. **One runtime name:** Folder path may be `claude/content/article-author/`; install name stays `article-author`.

---

## Appendix — Quick stats reference

| Metric | Count |
|--------|------:|
| Top-level canonical bundles (pre-migration) | ~258 |
| Cursor bundles | 42 |
| Agent bundles | 3+ |
| repo-specific bundles | 126 |
| repo-specific unique names | 90 |
| Overlap: top-level ∩ repo-specific | 80 |
| Overlap: top-level ∩ cursor | 27 |
| skills-openai vendor bundles | 12 |
| Legacy orphan `.md` files (no bundle) | 12 |

When stats match post-migration verification and the checklist in section 4 passes, the catalog is logically organized and ready to maintain.
