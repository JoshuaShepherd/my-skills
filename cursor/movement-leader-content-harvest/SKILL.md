---
name: movement-leader-content-harvest
description: >-
  Comprehensively discover and migrate every external content source for one movement leader
  except books — articles, blogs, YouTube, Vimeo, podcasts, audio, sermons, talks, interviews,
  journals, academic papers, courses, newsletters, and long-form social. Runs the full 00–09
  content-gathering pipeline for any leader slug in movement-leader-websites. Use when harvesting
  content, migrating external sources, running content gathering, or closing migration gaps for a
  movement leader writer.
disable-model-invocation: true
---

# Movement Leader Content Harvest

Find **all sources of all content** for one movement leader, **except books**, and pull that content (or a durable pointer) into the leader's website repo. This is **migration and gap-closing** — it moves existing content in from where it already lives. It does **not** write new articles or generate content.

The governing question for every item: **"If this platform vanished tomorrow, would we still have the content?"**

## Invocation

```
/movement-leader-content-harvest {leader-slug}
/movement-leader-content-harvest Hugh Halter
/movement-leader-content-harvest deb-hirsch --from-step 02
/movement-leader-content-harvest hugh-halter --players youtube,podcasts --dry-run
/movement-leader-content-harvest rowland-smith --refresh
```

Run from the **monorepo root** (`movement-leader-websites/`) unless you are already inside a leader repo.

### Arguments

| Flag | Effect |
|------|--------|
| `{leader-slug}` or display name | Required unless cwd is inside a leader repo. Fuzzy-match `Hugh Halter` → `hugh-halter`. |
| `--from-step N` | Resume from step N (00–09). Read tracker first; do not redo completed steps unless `--refresh`. |
| `--to-step N` | Stop after step N (default: 09). |
| `--players a,b,…` | Restrict sweep to named categories (see [players-checklist.md](reference/players-checklist.md)). Default: all 14. |
| `--dry-run` | Inventory + disposition only; no FETCH files written. Still writes tracker + canonical list. |
| `--refresh` | Reconcile against existing `CONTENT_SOURCES.md` / tracker instead of starting clean. |

**Books are out of scope.** Log any book to `books-seen.md` and defer to corpus-upload.

---

## Resolve the tenant

1. If the user gave a slug or name, normalize to kebab-case and confirm `{MONOREPO_ROOT}/{slug}/` exists.
2. If cwd is `{MONOREPO_ROOT}/{slug}/` (has `package.json` or `docs/movement_leader_research/`), use that slug.
3. Exclude non-tenant dirs: `_template`, `_template-full`, `docs`, `scripts`, `shared`, `reports`, `node_modules`.
4. Set paths for the run:
   - `TENANT_ROOT` = `{MONOREPO_ROOT}/{slug}/`
   - `TENANT_SLUG` = `{slug}`
   - `TRACKER` = `{TENANT_ROOT}/docs/movement_leader_research/content/HARVEST_TRACKER.md`
   - `REGISTRY` = `{MONOREPO_ROOT}/docs/build/skills/content-gathering/CONTENT_REGISTRY.md`

If ambiguous, ask once. If no dossier exists at all, step 01 bootstraps identity from one web search.

---

## Execution protocol (run to completion)

**Read this skill, then execute steps 00–09 sequentially for `TENANT_SLUG`.** Do not stop between steps unless blocked (missing identity, disambiguation failure, or user `--to-step`). After **every** step, update `HARVEST_TRACKER.md` before continuing.

For each step, **read the full step prompt** from `docs/build/skills/content-gathering/` and follow it exactly, substituting `{TENANT_SLUG}` and `{MONOREPO_ROOT}` paths:

| Step | Read and execute | Phase |
|------|------------------|-------|
| 00 | `docs/build/skills/content-gathering/00-charter-and-guardrails.md` | Charter |
| 01 | `docs/build/skills/content-gathering/01-observe-dossier-and-seed.md` | Observe |
| 02 | `docs/build/skills/content-gathering/02-sweep-owned-web-and-video.md` | Sweep |
| 03 | `docs/build/skills/content-gathering/03-sweep-podcasts-audio-talks.md` | Sweep |
| 04 | `docs/build/skills/content-gathering/04-sweep-articles-academic-interviews.md` | Sweep |
| 05 | `docs/build/skills/content-gathering/05-sweep-newsletters-social-courses.md` | Sweep |
| 06 | `docs/build/skills/content-gathering/06-disposition-and-dedup.md` | Decide |
| 07 | `docs/build/skills/content-gathering/07-fetch-harvest-and-transcribe.md` | Pull |
| 08 | `docs/build/skills/content-gathering/08-write-inventory-and-manifest.md` | Publish |
| 09 | `docs/build/skills/content-gathering/09-verify-coverage-gate-and-registry.md` | Gate |

Also read `docs/build/skills/content-gathering/MASTER_PLAYBOOK.md` once at the start (paths relative to monorepo root).

### Step 01 tracker bootstrap

If `HARVEST_TRACKER.md` does not exist:

```bash
cp docs/build/skills/content-gathering/HARVEST_TRACKER_TEMPLATE.md \
   {TENANT_ROOT}/docs/movement_leader_research/content/HARVEST_TRACKER.md
```

### Parallel sweeps (steps 02–05)

Steps 02–05 are independent. You may run **≤2–3 in parallel** (separate subagents), but each must write `_raw-finds.md` rows and update the tracker **before** ending. Never exceed 3 concurrent web sweeps — rate limits apply. Step 06 merges all raw finds.

### `--dry-run` override

Skip file writes in step 07. Still run disposition (06) and write inventory stubs (08) with `harvested_path` blank or `DRY-RUN`. Do not mark `verified` in step 09.

### `--refresh` override

In steps 06–08, reconcile against existing `CONTENT_SOURCES.md` and `harvest-manifest.json`: append new finds, mark dead links, do not duplicate items already in the skip set.

---

## Disposition rubric (step 06)

| Disposition | When |
|-------------|------|
| **FETCH** | At-risk host, or primary text by the leader → store verbatim file in `docs/harvest/` |
| **LINK** | Durable on a healthy third-party platform → catalog URL + metadata only |
| **TRANSCRIBE** | Primary A/V we want as text but can't extract cleanly this pass |
| **SKIP** | Wrong person, re-share, already-have, or **book** → `books-seen.md` |

Bias: **owned + old/fragile primary text → FETCH; healthy third-party → LINK.**

---

## Outputs (per tenant)

All paths under `{TENANT_ROOT}/`:

| Path | Purpose |
|------|---------|
| `docs/movement_leader_research/content/HARVEST_TRACKER.md` | Live progress board (updated every step) |
| `docs/movement_leader_research/content/_raw-finds.md` | Raw sweep rows (steps 02–05) |
| `docs/movement_leader_research/content/_canonical-items.md` | De-duped + dispositioned list (step 06) |
| `docs/movement_leader_research/content/CONTENT_SOURCES.md` | Canonical master inventory |
| `docs/movement_leader_research/content/harvest-manifest.json` | Machine-readable mirror |
| `docs/movement_leader_research/content/sources-swept.md` | Coverage audit log |
| `docs/movement_leader_research/content/books-seen.md` | Books deferred to corpus-upload |
| `docs/harvest/{type}/…` | FETCHed verbatim files with front-matter |

**Reference implementation:** `andrew-jones` — `docs/videos/` and `docs/articles/old-blogs/` show target shape.

---

## Discovery tools (preference order)

1. **WebSearch** — channels, archives, author pages, guest appearances
2. **WebFetch** — enumerate channel/feed/archive pages
3. **Bash** — RSS/sitemap via `curl`; `yt-dlp` if available for YouTube metadata/captions
4. **Browser MCP** — JS-heavy platforms (Vimeo showcases, Substack) when WebFetch fails

Enumerate to exhaustion: channel RSS, podcast feed, blog sitemap, author-archive pagination — not page one.

---

## Key rules

1. **Everything except books.** Comprehensive across all 14 player categories in [players-checklist.md](reference/players-checklist.md).
2. **Observe before searching.** Read `docs/movement_leader_research/` dossier first; never re-fetch `docs/articles/`, `docs/videos/`, `docs/harvest/`.
3. **"Checked, none found" is required** — record in tracker and `sources-swept.md`.
4. **De-duplicate across platforms.** One canonical item + alternate URLs.
5. **Migration, not creation.** FETCH files are verbatim source with attribution front-matter. No fabricated URLs, dates, or titles.
6. **Persist as you go.** Write rows and files before ending a step or turn.
7. **No app code changes.** Only write under `docs/movement_leader_research/content/`, `docs/harvest/`, and existing `docs/articles|videos/` conventions.
8. **Gate honestly.** Mark `verified` in step 09 only when all 8 coverage checks pass; update `CONTENT_REGISTRY.md`.

---

## Session report (print when done)

When the pipeline finishes (or stops at `--to-step`), print:

1. `TENANT_SLUG` and final tracker status (`verified` / `harvested` / `swept` / `blocked`)
2. Categories swept: N/14
3. Items by disposition: FETCH / LINK / TRANSCRIBE / SKIP
4. Files written to `docs/harvest/` (count + `find` verification)
5. Transcribe queue size and any gate failures
6. `CONTENT_REGISTRY.md` row updated (if step 09 passed)

---

## Additional resources

- 14 player categories: [reference/players-checklist.md](reference/players-checklist.md)
- Pipeline diagram + batch strategy: `docs/build/skills/content-gathering/MASTER_PLAYBOOK.md`
- Cross-tenant status: `docs/build/skills/content-gathering/CONTENT_REGISTRY.md`
- Tracker template: `docs/build/skills/content-gathering/HARVEST_TRACKER_TEMPLATE.md`

---

## Downstream pipeline (after step 09)

Harvest ends at repo inventory. For Supabase upload:

| Step | Skill / CLI | Purpose |
|------|-------------|---------|
| 0 | **`movement-leader-harvest-manifest`** / `pnpm harvest:build-manifest` | Reconcile manifest from existing `docs/harvest/` files |
| 1 | **`movement-leader-media-transcribe`** / `pnpm harvest:transcribe` | YouTube captions + podcast Whisper → `docs/harvest/transcripts/` |
| 2 | **`movement-leader-harvest-ingest`** / `pnpm harvest:ingest` | Manifest → `videos`, `podcast_episodes`, `archive_items` (draft) |
| 3 | `pnpm harvest:verify` | Reconcile manifest counts vs DB |

Books remain **`movemental-leader-corpus-upload`**, not this pipeline.
