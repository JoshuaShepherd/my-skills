---
name: movement-leader-harvest-manifest
description: >-
  Build or reconcile harvest-manifest.json from an existing movement leader content set —
  docs/harvest markdown, legacy docs/articles|videos, CSV/JSON catalogs, and LINK-only media rows.
  Classifies type/disposition, assigns stable ids, validates file paths for ZenWrite bundle upload
  and pnpm harvest:ingest. Use when creating a manifest, fixing manifest drift, preparing a
  harvest zip, or mapping a folder of files to ingest-ready rows for any leader slug.
disable-model-invocation: true
---

# Movement Leader Harvest Manifest Builder

Produce a **correct, ingest-ready** `harvest-manifest.json` for one tenant from whatever files and catalogs already exist. This skill is the **manifest factory** — it does not sweep the web (see **`movement-leader-content-harvest`**) and does not upload to Supabase (see **`movement-leader-harvest-ingest`**).

## Invocation

```
/movement-leader-harvest-manifest {leader-slug}
/movement-leader-harvest-manifest danielle-strickland --from-harvest-only
/movement-leader-harvest-manifest rowland-smith --merge-existing --validate
/movement-leader-harvest-manifest hugh-halter --supplement links.csv
```

Run from **`movement-leader-websites/`** monorepo root unless cwd is inside a leader repo.

### CLI (preferred first pass)

```bash
pnpm harvest:build-manifest -- --slug {leader-slug}
pnpm harvest:build-manifest -- --slug danielle-strickland --dry-run
pnpm harvest:build-manifest -- --slug rowland-smith --merge-existing
pnpm harvest:build-manifest -- --slug hugh-halter --supplement docs/movement_leader_research/content/link-only.json
pnpm harvest:validate-manifest -- --slug danielle-strickland
pnpm harvest:build-bundle -- --repo ./danielle-strickland --out ./danielle-strickland-bundle.zip
```

| Flag | Effect |
|------|--------|
| `--slug` | Required leader slug |
| `--dry-run` | Print summary + validation; do not write |
| `--merge-existing` | Keep LINK/TRANSCRIBE rows from current manifest not found on disk |
| `--supplement PATH` | Merge JSON array or CSV of extra rows (LINK media, catalog-only) |
| `--from-harvest-only` | Only scan `docs/harvest/`; ignore legacy `docs/articles/` |
| `--force-ids` | Regenerate ids for files missing frontmatter `id` |

---

## Resolve the tenant

1. Normalize user input to kebab-case `{slug}`.
2. Confirm `{MONOREPO_ROOT}/{slug}/` exists (or cwd is that repo).
3. Set paths:

| Variable | Path |
|----------|------|
| `MANIFEST` | `{slug}/docs/movement_leader_research/content/harvest-manifest.json` |
| `HARVEST_ROOT` | `{slug}/docs/harvest/` |
| `CONTENT_DIR` | `{slug}/docs/movement_leader_research/content/` |

Exclude: `_template`, `_template-full`, `docs`, `scripts`, `shared`, `reports`.

---

## Workflow (execute in order)

Copy this checklist and mark steps as you go:

```
- [ ] 1. Inventory sources
- [ ] 2. Classify each item (type + disposition)
- [ ] 3. Assign stable ids + harvested_path
- [ ] 4. Merge LINK-only / catalog rows
- [ ] 5. Write manifest + summary
- [ ] 6. Validate (CLI + ingest preview)
```

### Step 1 — Inventory sources

Scan **in priority order** (do not double-count):

1. **`docs/harvest/{type}/*.md`** — primary; frontmatter is authoritative when present
2. **`docs/harvest/transcripts/*.md`** — attach to existing media rows; do not duplicate as articles
3. **Legacy folders** (if `--merge-existing` or no harvest dir): `docs/articles/`, `docs/videos/`, `docs/podcasts/`
4. **Existing manifest** — preserve LINK/TRANSCRIBE/SKIP rows when merging
5. **Supplement file** — CSV/JSON for platform-only media (YouTube, podcast feeds)

Run: `pnpm harvest:build-manifest -- --slug {slug} --dry-run` and read the printed source counts.

### Step 2 — Classify type and disposition

**Type** comes from (first match wins):

1. Frontmatter `type:` field
2. Parent directory under `docs/harvest/` (see [reference/type-taxonomy.md](reference/type-taxonomy.md))
3. Heuristics on `source_url` / file path (youtube → `video`, substack → `newsletter`)

**Disposition** (see rubric in reference):

| Disposition | When |
|-------------|------|
| **FETCH** | Markdown body on disk under `docs/harvest/` |
| **LINK** | Media or article cataloged by URL only (YouTube, Spotify, stable third-party) |
| **TRANSCRIBE** | A/V primary content; transcript not ready yet |
| **SKIP** | Wrong person, duplicate, or **book** (defer to corpus-upload) |

**Never put books in the manifest.**

### Step 3 — Stable ids and paths

**Id format:** `{slug}-{type-short}-{NNN}` or reuse frontmatter `id` / filename stem.

Examples: `danielle-strickland-blog-094`, `jr-woodward-newsletter-003`, `hugh-halter-video-012`.

**harvested_path** (FETCH only): repo-relative POSIX path:

```
docs/harvest/{type-folder}/{id}.md
```

Type folder names (plural): `articles`, `newsletters`, `videos`, `podcasts`, `interviews`, `academic`, `talks`, `audio`.

**Frontmatter template** for new FETCH files — see [reference/frontmatter-template.md](reference/frontmatter-template.md).

### Step 4 — Merge LINK-only rows

Videos and podcast-host episodes often have **no markdown file**. Add them via:

- `--merge-existing` (keep prior LINK rows), and/or
- `--supplement` JSON:

```json
[
  {
    "id": "hugh-halter-video-001",
    "title": "Talk title",
    "type": "video",
    "disposition": "LINK",
    "canonical_url": "https://www.youtube.com/watch?v=abc123",
    "host": "YouTube",
    "date": "2021-06-01",
    "primary": true
  }
]
```

Dedupe by `id` first, then by normalized `canonical_url`.

### Step 5 — Write manifest

Output schema: [reference/manifest-schema.md](reference/manifest-schema.md).

```bash
pnpm harvest:build-manifest -- --slug {slug} --merge-existing
```

Also refresh `CONTENT_SOURCES.md` stub summary if the tenant already uses it (counts must match non-SKIP items).

### Step 6 — Validate

```bash
pnpm harvest:validate-manifest -- --slug {slug}
```

Gate checks:

- [ ] Every **FETCH** row has `harvested_path` pointing to an existing file
- [ ] Every **LINK** video/podcast row has `canonical_url`
- [ ] No duplicate `id` values
- [ ] `summary.total` == `items.length`
- [ ] Summary disposition counts match items
- [ ] No `type: book` in items
- [ ] `leader` field matches slug

**ZenWrite admin bundle:** run from zenwrite repo:

```bash
pnpm harvest:build-bundle -- --repo ../movement-leader-websites/{slug} --out {slug}-bundle.zip
```

Upload zip in Admin → Harvest import → Preview must show correct `targetTable` per row.

---

## Type → ingest target (downstream)

| Harvest `type` | Default disposition | Ingest table |
|----------------|--------------------|--------------|
| `article`, `newsletter`, `interview`, `academic`, `resource`, `course` | FETCH | `archive_items` (or `content_items`) |
| `video` | LINK | `videos` |
| `podcast-host`, `podcast` | LINK | `podcast_episodes` |
| `podcast-guest` | FETCH/LINK | `content_items` if body exists |
| `book-chapter` | FETCH | `book_chapters` (requires parent book id in `host`) |

Full mapping: [reference/type-taxonomy.md](reference/type-taxonomy.md).

---

## Agent execution rules

1. **Prefer the CLI** over hand-editing JSON — it keeps paths and summaries consistent.
2. **Read frontmatter before inferring** — harvested files often already contain full metadata.
3. **Do not invent URLs or dates** — use `unknown` for date when missing.
4. **Migration, not authoring** — manifest describes existing content only.
5. **Persist incrementally** — write manifest after each batch when fixing large tenants.
6. **No app code changes** unless adding manifest tooling under `scripts/harvest/`.

---

## Session report (print when done)

1. `{slug}` and manifest path
2. Items by type and disposition (FETCH / LINK / TRANSCRIBE / SKIP)
3. Validation: pass / fail with first 5 errors
4. `fetched_to_disk` count vs files found on disk
5. Suggested next step: `pnpm harvest:transcribe` → `pnpm harvest:ingest` or ZenWrite bundle upload

---

## Related skills

| Skill | Role |
|-------|------|
| **`movement-leader-content-harvest`** | Full 00–09 web sweep → manifest (upstream) |
| **`movement-leader-media-transcribe`** | YouTube captions + Whisper → transcripts |
| **`movement-leader-harvest-ingest`** | Manifest → Supabase draft rows |
| **`movemental-leader-corpus-upload`** | Books / dossier JSONB (parallel track) |

## Additional resources

- [reference/manifest-schema.md](reference/manifest-schema.md)
- [reference/type-taxonomy.md](reference/type-taxonomy.md)
- [reference/frontmatter-template.md](reference/frontmatter-template.md)
- Step 08 prompt: `docs/build/skills/content-gathering/08-write-inventory-and-manifest.md`
- ZenWrite ingest mapper: `zenwrite/server/services/admin/ingest/harvestMapper.ts`
