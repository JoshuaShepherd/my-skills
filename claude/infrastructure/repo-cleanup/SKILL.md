---
name: repo-cleanup
description: >
  Holistic single-repo hygiene pass for context-coded React + Next.js/Vite + Tailwind + Supabase + Vercel + OpenAI/Anthropic/Gemini stacks. Use when a repo needs its docs triaged, dead code archived, stale HTML/templates removed, unused deps flagged, and its CLAUDE.md / AGENTS.md / .claude skill surface re-tightened so Cursor and Claude Code have a clean working context. Always archives (does not delete) under `_archive/<YYYY-MM-DD>/`. Defers component- and style-level work to $frontend-cleanup and $tailwind-cleanup; defers type-chain repair to $validate.
argument-hint: '[scope: docs|code|html|deps|assets|all] (default: all)'
user-invocable: true
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
  - "Write"
  - "Glob"
  - "Grep"
  - "Agent"
  - "TodoWrite"
---

# Repo Cleanup

A holistic hygiene pass on a single repository, tuned for context-coding with Cursor and Claude Code on this stack:

- **Frontend:** React, Next.js (App Router) or Vite, Tailwind, shadcn
- **Backend / data:** Supabase (Postgres, Auth, Storage), Drizzle, Zod
- **Deploy:** Vercel
- **AI:** OpenAI API, Anthropic Claude API, Google Gemini API, OpenAI Agents SDK / Vercel AI SDK

The skill triages docs, archives unused code and HTML scratch, flags unused dependencies, tightens the `.claude/` surface, and leaves a manifest of every move. Everything is reversible.

`$ARGUMENTS` selects the scope: `docs`, `code`, `html`, `deps`, `assets`, or `all` (default).

---

## Core principles (read first)

1. **Archive, do not delete.** Every move lands in `_archive/<YYYY-MM-DD>/` with a manifest. Use `git mv` so blame survives.
2. **Report first, act second.** Phases 1–3 produce a report at `_docs/_build/repo-cleanup-<YYYY-MM-DD>.md`. Wait for explicit confirmation before Phase 4 (archive). Phase 5 verifies.
3. **Stack-aware, not stack-assumed.** Detect what's actually present (`package.json`, `next.config.*`, `vite.config.*`, `supabase/`, `drizzle.config.*`). Only run checks relevant to detected layers.
4. **Defer to focused skills.** This is the cross-cutting coordinator. Use:
   - $frontend-cleanup — unused React components, `-v2` debt, folder restructure
   - $tailwind-cleanup — hardcoded colors, arbitrary values, primitive bypasses
   - $validate — six-layer type-chain alignment (db → schemas → services → routes → hooks → ui)
   - $fewer-permission-prompts — `.claude/settings.json` allowlist tidy
   - $docs-type-safety — type-doc currency (if `_docs/type/` exists)
   - $tenant-check — multi-tenant config audit (if movemental-style)
5. **Protect context-coding affordances.** Never move: `CLAUDE.md`, `AGENTS.md`, `README.md`, `LICENSE`, `.claude/`, `.cursor/`, `.github/`, config files, migrations, generated code. See the "Never touch" list below.
6. **One repo at a time.** This skill operates on a single repo. Multi-repo cleanup happens by running it multiple times.

---

## Phase 0 — Sniff the stack

Before any cleanup, detect what's in the repo. Read these files (skip silently if absent) and write a stack profile:

```bash
# Identity
package.json                      # name, scripts, deps; presence of next/vite/react/tailwind
CLAUDE.md                         # repo conventions, six-layer chain status, pinned MCP IDs
AGENTS.md                         # agent-specific rules (often points to .claude/skills/)
README.md                         # public surface

# Framework
next.config.{ts,js,mjs}           # Next.js
vite.config.{ts,js,mts}           # Vite
src/app/ vs src/pages/            # App Router vs Pages Router
proxy.ts middleware.ts            # Next 16 vs Next 14 middleware

# Styling
tailwind.config.{ts,js}           # Tailwind v3
src/app/globals.css               # check for `@theme` (Tailwind v4)
components.json                   # shadcn

# Data
drizzle.config.{ts,js,mts}        # Drizzle
supabase/                         # Supabase project (migrations, functions)
.env.example .env.local           # env contracts

# AI
src/agents/ packages/agent-runtime/   # Agents SDK / blueprint pattern
src/lib/ai/ src/lib/openai*       # AI client wrappers
@openai/agents @ai-sdk/* @anthropic-ai/sdk @google/generative-ai  # in package.json deps

# Build infra
vercel.json                       # Vercel project config
scripts/                          # custom CLI scripts (validate-*, generate-*)
.claude/ .cursor/                 # context-coding surface
```

Record findings in the TodoWrite list so subsequent phases can branch on them.

---

## Phase 1 — Discovery

Build six inventories. For large repos, delegate the listings to `Agent({ subagent_type: "Explore", ... })` so your main context window stays clean.

### 1a. Doc inventory

```bash
# Markdown files outside vendor/build directories
find . -type f -name "*.md" \
  -not -path "./node_modules/*" \
  -not -path "./.next/*" \
  -not -path "./.vercel/*" \
  -not -path "./dist/*" \
  -not -path "./build/*" \
  -not -path "./_archive/*" \
  -not -path "./.git/*"
```

For each: path, size, last-modified, first heading, and whether it's referenced by `CLAUDE.md`, `AGENTS.md`, `README.md`, any `.claude/skills/**/SKILL.md`, or any `docs/build/prompts/*.md`.

### 1b. Top-level loose files

Anything in the repo root that is not a config file, a canonical doc, or a directory. Classic offenders:

- `*_REPORT.md`, `*_AUDIT.md`, `*_SUMMARY.md`, `*_COMPLETE.md`, `*_DIAGNOSIS.md`, `*_NOTES.md` — completed work-product
- `RECIPE-*.md` — one-off recipes
- `cursor.md` (if `CLAUDE.md` exists and is canonical)
- `*.bak`, `*.backup`, `*.old`, `*.orig`, `*~`
- Stray `*.html` not under `public/` or a known templates path
- Stray `*.zip`, `*.tar`, `*.tgz`

### 1c. Code inventory (lightweight; defer the heavy lift)

This skill does **not** rebuild the full import graph — `$frontend-cleanup` does that. Here we look only for **obvious** dead-code signals:

- Directories with version suffixes: `-v2`, `-v3`, `-new`, `-old`, `-backup`, `-deprecated`, `-temp`, `-wip`, `-draft`, `-copy`, `-legacy`, `-experimental`
- Files matching `*.bak.ts`, `*.old.tsx`, `*.unused.*`, `* copy.tsx`, `* copy 2.tsx`
- `src/components/_archive/` or `src/_old/` (already-archived, can be moved into `_archive/`)
- Empty directories under `src/`
- Top-level scripts (`*.mjs`, `*.cjs`, `*.sh`) not referenced by `package.json` scripts or any markdown

### 1d. HTML / templates / prototypes

Common dumping grounds in this stack:

```
html/                    docs/html/             docs/build/stitch/
templates/               src/templates/         public/templates/
prototype/  prototypes/  scratch/  sandbox/
*.html in repo root
```

For each `.html` file: is it referenced by code? Is the parent directory still active per `CLAUDE.md`? Stitch source HTML is usually fine to archive once the React migration of that screen is shipped — confirm against the active migration list before moving.

### 1e. Asset inventory (public/)

```bash
find public/ -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" -o -name "*.pdf" -o -name "*.mp4" -o -name "*.mov" -o -name "*.zip" \)
```

For each: total bytes, last-modified, and any `grep` reference from `src/`. Special handling:

- `favicon.ico`, `robots.txt`, `sitemap.xml`, `manifest.json`, `.well-known/*` — never archive
- `og/*.png`, `social/*.png` — referenced by `Metadata.openGraph` even if `grep` misses it. Check `metadata.ts` files.

### 1f. Dependency inventory

Use `pnpm dlx knip` if available, else `pnpm dlx depcheck`. If neither, do a manual sweep:

```bash
# List runtime deps not imported anywhere under src/
node -e "const p=require('./package.json'); console.log(Object.keys({...p.dependencies||{}, ...p.devDependencies||{}}).join('\\n'))" \
  | while read dep; do
      if ! grep -rq "['\"]${dep}\(/.*\)*['\"]" src/ scripts/ 2>/dev/null; then
        echo "MAYBE-UNUSED: $dep"
      fi
    done
```

False-positive watch: `tsx`, `dotenv-cli`, peer deps like `@types/*` matching their runtime, Tailwind plugins, PostCSS plugins, ESLint configs, Drizzle Kit, Husky/lint-staged, Sentry CLI. Flag these as "review" not "remove."

### 1g. `.claude/` surface check

```bash
# Symlink coverage
ls -la .claude/skills/ 2>/dev/null | head
# Settings allowlist
cat .claude/settings.json 2>/dev/null
cat .claude/settings.local.json 2>/dev/null
```

Symptoms of drift:

- Broken symlinks in `.claude/skills/` (target path doesn't exist)
- Skills in `.claude/skills/` that no longer exist in `my-skills/`
- `settings.local.json` referencing absolute paths from a different machine
- Allowlist entries for skills not symlinked into the repo

(Run $fewer-permission-prompts to compact the allowlist after this skill finishes.)

---

## Phase 2 — Classification & triage

Sort every item into one of these buckets:

| Bucket | Criteria | Default action |
|---|---|---|
| **Keep** | Canonical doc, active code, referenced asset, declared dep, live skill, recent (≤ 60 days) work-log | Leave in place |
| **Archive** | Not referenced anywhere; last-modified > 90 days; classified as completed work-product or shadowed-by-newer | Move to `_archive/<YYYY-MM-DD>/<bucket>/` |
| **Rename/Restructure** | Live code under a version-suffixed path (`-v2`) where original is dead | Promote to canonical name; archive the dead original |
| **Review** | Ambiguous: dynamically imported, referenced only in a doc, peer-of-installed | Flag in the report; do nothing automatically |
| **Never touch** | See list below | Do not move under any condition |

### Never-touch list

```
README.md                         (top-level)
CLAUDE.md                         (every directory)
AGENTS.md                         (every directory)
LICENSE LICENSE.md COPYING
package.json pnpm-workspace.yaml pnpm-lock.yaml
tsconfig*.json eslint.config.*
next.config.* vite.config.* tailwind.config.* postcss.config.*
drizzle.config.* components.json vercel.json
proxy.ts middleware.ts
src/app/ src/pages/ src/components/ src/lib/ src/hooks/ src/agents/
                                   (the dirs themselves; specific orphan
                                    files inside them can still be archived
                                    after import-graph confirmation)
public/favicon.ico public/robots.txt public/sitemap.xml public/manifest.json
public/.well-known/
supabase/migrations/               (NEVER move; migrations are history)
drizzle/migrations/                (same)
.claude/ .cursor/ .github/ .vscode/
.env.example                       (env contract)
```

### Doc-triage shortcuts

| Filename pattern | Default classification | Notes |
|---|---|---|
| `*_REPORT.md`, `*_AUDIT.md`, `*_SUMMARY.md` | Archive if > 30 days and not referenced | Completed work product |
| `*_DIAGNOSIS.md`, `*_FIX.md` | Archive once the fix is shipped | Verify against `git log` for the fix commit |
| `*_COMPLETE.md`, `*_SETUP_COMPLETE.md`, `*_IMPLEMENTATION.md` | Archive | Onboarding receipts |
| `RECIPE-*.md`, `RUNBOOK-*.md` | Keep if referenced, else archive | These often live in `docs/build/` |
| `*-NOTES.md`, `*-LOG.md` | Keep if recent, else archive | Personal scratch — keep if author still iterates |
| `_inbox/`, `_drafts/`, `_scratch/` | Archive contents > 30 days old | Don't delete; the inbox pattern is intentional |
| `_quarantine/` | Leave alone | Already an intentional archive |
| `BOOK_CORPUS_QUARANTINE.md` and similar provenance docs | Keep | Quarantine notes are load-bearing |

---

## Phase 3 — Report

Write the cleanup plan to `_docs/_build/repo-cleanup-<YYYY-MM-DD>.md`. Required sections:

```markdown
# Repo Cleanup Plan — <YYYY-MM-DD>

**Repo:** `<repo name>`
**Stack detected:** Next.js 16 | Vite + React | Tailwind v4 | Supabase | Drizzle | Vercel | OpenAI Agents | Anthropic | Gemini
**Scope:** docs + code + html + deps + assets
**Total items inventoried:** N
**Total items proposed for archive:** N
**Bytes reclaimed if approved:** ~X MB

## Stack profile
- Framework: ...
- Styling: ...
- Data: ...
- AI providers in use: ...
- Context-coding surface: `.claude/skills/` symlink count, settings.json allowlist size

## Buckets

### Keep (N items)
_Not enumerated unless verbose mode requested._

### Archive (N items)
| Path | Size | Last-modified | Reason | Destination |
|---|---|---|---|---|
| `RECIPE-VIDEO-TO-TRANSCRIPT.md` | 4.2 KB | 2026-03-01 | Completed recipe, referenced only by an archived report | `_archive/2026-05-13/docs/RECIPE-VIDEO-TO-TRANSCRIPT.md` |
| `src/components/Header-v2/` | 22 KB | 2026-02-14 | Shadowed by `src/components/Header/` (active) | `_archive/2026-05-13/code/components/Header-v2/` |
| `html/dashboard-export.html` | 91 KB | 2025-12-04 | Stitch export; React migration shipped 2026-02 | `_archive/2026-05-13/html/dashboard-export.html` |
| `public/old-hero.png` | 1.4 MB | 2025-11-20 | Not referenced; replaced by `public/hero-2026.png` | `_archive/2026-05-13/public/old-hero.png` |

### Rename/Restructure (N items)
| From | To | Reason |
|---|---|---|

### Review (N items)
| Path | Suspicion | Action requested |
|---|---|---|

### Unused dependencies (N items, manual review)
| Package | Why flagged | Likely action |
|---|---|---|

### `.claude/` hygiene
- Broken symlinks: N
- Skills referenced in settings but not symlinked: N
- Outdated `additionalDirectories` paths: N

## Verification commands (run after archive)
```bash
pnpm typecheck
pnpm lint
pnpm build:check   # if present
pnpm validate:all  # if six-layer chain repo
git status         # confirm only intended moves
```

## How to revert
Every move below is in one commit. To revert: `git revert <commit-sha>`.
The `_archive/2026-05-13/MANIFEST.md` lists every move with its origin.
```

**Stop here.** Print the report path and the headline numbers, and ask: *"Approve Phase 4 (archive) for the items in the Archive bucket? Reply `yes` to proceed, `yes minus deps` to skip the dep changes, or list specific paths to exclude."*

---

## Phase 4 — Archive (only after confirmation)

### 4a. Create the archive root

```bash
DATE=$(date +%Y-%m-%d)
ARCHIVE_ROOT="_archive/${DATE}"
mkdir -p "${ARCHIVE_ROOT}"/{docs,code,html,public,scripts}
```

If `_archive/<DATE>/` already exists (a previous run today), append a sequence: `2026-05-13-2`, `-3`, etc.

### 4b. Move with `git mv`

For each item in the **Archive** bucket:

```bash
git mv "<from>" "${ARCHIVE_ROOT}/<bucket>/<basename>"
```

For directories, preserve the original parent path under the bucket:

```bash
# src/components/Header-v2/ → _archive/2026-05-13/code/components/Header-v2/
mkdir -p "${ARCHIVE_ROOT}/code/components"
git mv "src/components/Header-v2" "${ARCHIVE_ROOT}/code/components/Header-v2"
```

Never use `rm`. Never use `mv` outside of `git mv` (loses rename detection).

### 4c. Handle Rename/Restructure

For each row in the Rename/Restructure bucket:

```bash
# Promote the live -v2 to canonical, archive the dead original
git mv "src/components/Header" "${ARCHIVE_ROOT}/code/components/Header-original"
git mv "src/components/Header-v2" "src/components/Header"
```

Then update imports. Search-and-replace, but only in `src/`, `scripts/`, and `tests/`:

```bash
grep -rl "components/Header-v2" src/ scripts/ tests/ \
  | xargs sed -i 's|components/Header-v2|components/Header|g'
```

### 4d. Write the manifest

`_archive/<DATE>/MANIFEST.md`:

```markdown
# Archive Manifest — <YYYY-MM-DD>

Generated by $repo-cleanup. Each entry: original path → archive path, reason, originating cleanup report.

## Moves
- `RECIPE-VIDEO-TO-TRANSCRIPT.md` → `docs/RECIPE-VIDEO-TO-TRANSCRIPT.md` — completed recipe
- `src/components/Header-v2/` → `code/components/Header-v2/` — promoted to canonical name; original archived alongside
- ...

## Renames
- `src/components/Header-v2/` → `src/components/Header/` (canonical promotion)
- `src/components/Header/` → `_archive/2026-05-13/code/components/Header-original/` (the dead original)

## Source report
`_docs/_build/repo-cleanup-<YYYY-MM-DD>.md`

## To revert this cleanup
```
git revert <commit-sha>
```
```

### 4e. Suggested dep removals (do not auto-edit `package.json`)

Print the list of likely-unused deps to the chat with one `pnpm remove ...` line per package, ready to copy. Do **not** modify `package.json` automatically — the false-positive rate on unused-dep detection is too high to risk auto-removal.

### 4f. `.claude/` tidy

- Remove broken symlinks: `find .claude/skills -xtype l -print -delete` (only after the user confirms).
- For symlinks pointing at moved-or-missing skills, repoint or remove.
- Suggest the user run $fewer-permission-prompts after this skill completes.

---

## Phase 5 — Verify

After the archive commit lands, run the appropriate stack-aware checks:

```bash
pnpm install                       # in case removed deps were already gone
pnpm typecheck                     # always
pnpm lint                          # always
pnpm build:check 2>/dev/null || true
pnpm validate:all 2>/dev/null || true   # six-layer chain repos only
pnpm test:run 2>/dev/null || true       # if a fast unit suite exists
```

If any check fails, the first reflex is **`git revert HEAD`** and re-examine the report. Do not patch forward from a broken cleanup; the whole point of `git mv` is reversibility.

If all checks pass, write a one-paragraph summary to the bottom of the cleanup report:

```markdown
## Result
Cleanup committed at `<sha>`. typecheck ✓ · lint ✓ · build:check ✓ · validate:all ✓.
Bytes reclaimed: X MB. Items archived: N. Items renamed: N.
Deps still pending manual review: N (see Phase 4e).
```

---

## Stack-specific addenda

Run these in addition to the generic phases when the layer is detected. Each is intentionally short — defer the deep work to the named skill.

### React + Next.js (App Router)

- Check for orphaned `page.tsx` files in `src/app/` (folder exists but route is unreachable via nav/sitemap).
- Look for `app/**/loading.tsx` and `app/**/error.tsx` that are empty or default-only — leave them; they are intentional.
- `src/middleware.ts` vs `proxy.ts`: Next 16 uses `proxy.ts`. If both exist and the project is Next 16, `middleware.ts` is stale.
- Defer component-level cleanup to $frontend-cleanup.

### React + Vite

- Confirm `index.html` references the live entry (`src/main.tsx` or `src/index.tsx`).
- `vite-project/` nested folders inside a parent app (seen in some Movemental tenants) are usually scaffolds — verify before archiving.

### Tailwind

- Defer hardcoded-color / arbitrary-value / shadow violations to $tailwind-cleanup.
- Look for unused custom plugins in `tailwind.config.*` (`plugins: [...]`).
- If `src/app/globals.css` has `@theme inline` (Tailwind v4) and a `tailwind.config.ts` also exists, the config file is usually a stale leftover — flag for review.

### Supabase

- `supabase/migrations/`: **never archive**. Migrations are history.
- `supabase/functions/`: archive only if the function is unreferenced by any client AND has no recent deploy.
- Look for stale `supabase/.temp/` and `supabase/.branches/` — these are local-dev caches, can be added to `.gitignore` if not already.
- Out-of-date `database.types.ts`: do not archive; suggest re-running `supabase gen types typescript`.

### Vercel

- `vercel.json`: keep. Check for `crons:` entries that point at archived routes — flag for review.
- `.vercel/` directory: should be `.gitignored`; if checked in, flag.
- Stale env keys referenced in `vercel.json` `env:` block that don't exist in `.env.example` — flag.

### Drizzle / six-layer chain

- If `scripts/validate-*.ts` and `scripts/generate-*.ts` exist, this is a six-layer-chain repo.
- Generated layers (`src/lib/schemas/`, `src/lib/services/simplified/`, `src/app/api/simplified/`, `src/hooks/simplified/`) — do not archive individual files; they regenerate from the schema. If a layer is suspect, run $validate.
- `src/lib/db/schema.ts` is source of truth — never archive.

### AI surface (OpenAI / Anthropic / Gemini / Agents SDK)

- `src/agents/<slug>/` directories with no API route and no UI reference: candidate for archive (verify against `src/app/api/agents/`).
- Static instruction overrides loaded via `AI_LAB_INSTRUCTION_OVERRIDE_PATH` etc. — do not move if the env var still resolves at runtime.
- `exported-ai-lab-instructions.json` and similar prompt exports: keep — they're an SSOT snapshot.
- Old prompt-pack JSON dumps in `_docs/_prompts/` > 90 days: candidate for archive if a newer pack supersedes them.
- `src/lib/openai*`, `src/lib/anthropic*`, `src/lib/gemini*` wrappers: keep if any agent or route imports them; archive if all callers have been migrated to a shared adapter.
- Look for hard-coded API keys in source (defense-in-depth check). If found, **stop the cleanup**, alert the user, and route to $env-setup.

### Documentation (`docs/`)

- Files referenced by `CLAUDE.md`, `AGENTS.md`, or any active `SKILL.md`: keep.
- `docs/build/prompts/*.md`: keep if the prompt is still cited; archive if the prompt was for a one-time build that shipped.
- `docs/_inbox/` and `docs/_drafts/`: archive items > 30 days untouched.
- `docs/arguments/`, `docs/design/`, `docs/05-agents/_inventory.md`, `docs/09-skills/_registry.md`: SSOT — keep.

### `.claude/` and `.cursor/`

- Broken symlinks: remove (after confirmation).
- `settings.local.json` with absolute paths from a different machine: open and edit to use this machine's paths, or delete and regenerate via $fewer-permission-prompts.
- `additionalDirectories` entries pointing at paths that don't exist: prune.

---

## Output format (chat)

When the skill finishes a phase, print one of:

```
✓ Phase 1: discovered 412 items (docs 187, code 144, html 12, public 47, deps 38)
✓ Phase 2: classified — keep 318, archive 76, rename 6, review 12
✓ Phase 3: report written to _docs/_build/repo-cleanup-2026-05-13.md
  → 76 items proposed for archive · ~12.4 MB reclaim · 8 deps flagged for review
  → Reply `yes` to proceed, `yes minus deps`, or list paths to exclude.
✓ Phase 4: archived under _archive/2026-05-13/ (commit a3f7c12) — manifest written
✓ Phase 5: verified — typecheck ✓ · lint ✓ · build:check ✓ · validate:all ✓
```

If the user does not confirm Phase 4, stop after Phase 3 cleanly. The report and inventory remain on disk; rerun the skill to resume.

---

## Don't-do list

- **Don't delete.** Always archive. The `_archive/<DATE>/` folder is the only valid destination.
- **Don't auto-edit `package.json`.** Print the suggested `pnpm remove` lines; let the user apply.
- **Don't touch Supabase migrations or Drizzle migrations.** Ever.
- **Don't try to be the import-graph builder.** Defer that to $frontend-cleanup.
- **Don't run on a dirty working tree.** Check `git status` first; if anything is uncommitted, ask the user to commit or stash before proceeding.
- **Don't run on a repo without git.** `git rev-parse --git-dir` must succeed.
- **Don't cross repo boundaries.** Operate on the cwd repo only. Symlinks pointing outside the repo are followed for **reading** but never moved.
- **Don't archive the cleanup report itself.** Subsequent runs should be able to read prior reports.

---

## Related skills

Invoke these alongside or after `repo-cleanup`:

- $frontend-cleanup — for the deep React import-graph and component-tree work
- $tailwind-cleanup — for hardcoded colors, arbitrary values, shadow violations
- $validate — six-layer type-chain check
- $fewer-permission-prompts — compact `.claude/settings.json` allowlist
- $docs-type-safety — keep `_docs/type/` current after schema changes
- $tenant-check — multi-tenant repo configuration audit (movemental tenants)
- $env-setup — re-establish `.env.example` and rotate any leaked secrets
- $analytics-audit — verify analytics wiring after route or component moves

A clean order for a full pass:

1. `git status` clean
2. `$repo-cleanup` (this skill) — coarse pass, archive obvious bloat
3. `$frontend-cleanup` — component-tree precision pass
4. `$tailwind-cleanup` — style-token precision pass
5. `$validate` — type-chain integrity
6. `$fewer-permission-prompts` — final settings tidy
7. Commit and run `pnpm build`
