---
name: movement-leader-harvest-ingest
description: >-
  Ingest harvest-manifest.json items into Supabase content tables for a movement leader tenant —
  archive_items or content_items for FETCH articles, videos and podcast_episodes for LINK media,
  draft-by-default with namespaced slugs. Uses leaders.manifest.json for org/author IDs. Run after
  content-harvest (and media-transcribe for A/V). Distinct from movemental-leader-corpus-upload
  (dossier JSONB) and demo-pack ingest (synthetic seed).
disable-model-invocation: true
---

# Movement Leader Harvest Ingest

Load harvested content from a leader repo into the **shared Supabase** content tables (`archive_items`, `content_items`, `videos`, `podcast_episodes`, series tables). Default: **draft**, not published.

## Invocation

```
/movement-leader-harvest-ingest {leader-slug}
/movement-leader-harvest-ingest danielle-strickland --types video,podcast-host --dry-run
/movement-leader-harvest-ingest david-docusen --types article --layer archive
```

Run from **monorepo root**.

### CLI (preferred)

```bash
pnpm harvest:ingest -- --slug {leader-slug} --dry-run
pnpm harvest:ingest -- --slug danielle-strickland --types video,podcast-host
pnpm harvest:ingest -- --slug david-docusen --types article --layer archive --skip-existing
pnpm harvest:verify -- --slug danielle-strickland
```

| Flag | Effect |
|------|--------|
| `--slug` | Required leader slug |
| `--types` | Filter harvest `type` values (comma-separated) |
| `--layer archive` | FETCH articles → `archive_items` (default for bulk) |
| `--layer content` | FETCH articles → `content_items` draft |
| `--dry-run` | Log actions only |
| `--skip-existing` | Skip rows whose namespaced slug already exists |
| `--max N` | Limit items |

## Prerequisites

1. `harvest-manifest.json` at `{slug}/docs/movement_leader_research/content/`
2. Leader row in `leaders.manifest.json` with `orgId`, `authUserId`, `orgReady: true`
3. `DATABASE_URL` in tenant `.env.local` (service role / direct Postgres)
4. For articles: FETCH files exist under `docs/harvest/`
5. For video/podcast transcripts: run **`movement-leader-media-transcribe`** first (optional but recommended)

## Harvest type → table mapping

| Harvest `type` | Disposition | Target table | Notes |
|----------------|-------------|--------------|-------|
| `article`, `newsletter`, … | FETCH | `archive_items` or `content_items` | Body from `docs/harvest/` file |
| `video` | LINK | `videos` + `video_series` | `hosting_provider`, `external_id` from YouTube URL |
| `podcast-host`, `podcast` | LINK | `podcast_episodes` + `podcast_series` | `audio_url` from mp3 in `alt_urls` |
| `podcast-guest`, `interview` | FETCH/LINK | `content_items` if body exists | else warn |

## Slug namespacing

All slugs: `{tenant-slug}--{harvest-id}` — globally unique across tenants (`content_items.slug`, `videos.slug` are global unique).

`original_source` / metadata: `'harvest'`.

## Schema reference

- Column map: `docs/build/skills/demo-pack-seed/SCHEMA_FIELD_MAP.md`
- Drizzle schema: `_template-full/src/lib/database/schema.ts`
- Ingest implementation: `scripts/harvest/ingest-harvest.ts`
- Design doc: `docs/build/notes/admin-content-upload-dashboard-design-2026-07-05.md`

## Publishing

Ingest creates **draft** rows (`status: draft`, `published_at: null`). Publishing is a separate curator action with visibility gates.

## Related skills

- **`movement-leader-harvest-manifest`** — build/reconcile manifest from existing files (upstream when not sweeping)
- **`movement-leader-content-harvest`** — builds manifest (full web sweep)
- **`movement-leader-media-transcribe`** — transcripts for A/V (recommended before ingest)
- **`movemental-leader-corpus-upload`** — dossier `movement_leader_corpus_data` (parallel track)
- **`movement-leader-demo-pack`** — synthetic seed (not harvest)

## Session report

Print: slug, counts by type ingested/skipped/failed, dry-run vs live, suggest `pnpm harvest:verify`.
