# harvest-manifest.json schema

Canonical path: `{slug}/docs/movement_leader_research/content/harvest-manifest.json`

## Top-level shape

```json
{
  "leader": "danielle-strickland",
  "generated": "2026-07-06",
  "summary": {
    "total": 120,
    "fetch": 85,
    "link": 30,
    "transcribe": 2,
    "skip": 3,
    "fetched_to_disk": 85
  },
  "items": []
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `leader` | yes | Must equal tenant slug |
| `generated` | yes | ISO date `YYYY-MM-DD` |
| `summary.total` | yes | Must equal `items.length` |
| `summary.fetch/link/transcribe/skip` | yes | Count by disposition |
| `summary.fetched_to_disk` | recommended | FETCH rows with existing `harvested_path` |

## Item shape

```json
{
  "id": "danielle-strickland-blog-094",
  "title": "Working at contentment.",
  "type": "article",
  "date": "2007-04-12",
  "disposition": "FETCH",
  "canonical_url": "https://www.daniellestrickland.com/blog/2007/04/12/working-at-contentment",
  "alt_urls": [],
  "host": "daniellestrickland.com",
  "primary": true,
  "harvested_path": "docs/harvest/articles/danielle-strickland-blog-094.md",
  "notes": "optional curator note"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Stable, unique within tenant; used for slug namespacing at ingest |
| `title` | yes | Display title |
| `type` | yes | See type-taxonomy.md |
| `date` | yes | `YYYY-MM-DD` or `unknown` |
| `disposition` | yes | `FETCH` \| `LINK` \| `TRANSCRIBE` \| `SKIP` |
| `canonical_url` | yes* | *Required for LINK; strongly recommended for FETCH |
| `alt_urls` | no | Wayback mirrors, syndication copies |
| `host` | yes | Outlet or platform label |
| `primary` | yes | Boolean — leader-authored primary vs guest/secondary |
| `harvested_path` | FETCH | Repo-relative path; `null` for LINK |
| `notes` | no | Free text |
| `audio_url` | no | Podcast mp3 when not in `canonical_url` |
| `transcript_status` | no | `missing` \| `auto-caption` \| `whisper` \| `pending` \| `approved` |

## ZenWrite bundle alias map

When packing for ZenWrite Admin → Harvest import, the ingest parser accepts these aliases:

| Manifest (MLW) | ZenWrite ingest |
|----------------|-----------------|
| `leader` | `leader_slug` (wrapper object) |
| `canonical_url` | `source_url` |
| `harvested_path` | `file_path` (relative to zip root) |
| `date` | `published` |

Zip layout for upload:

```
harvest-manifest.json
harvest/{type}/{id}.md
```

Use `pnpm harvest:build-bundle` (zenwrite) or ensure paths match `resolveHarvestFile()` candidates in `zenwrite/server/services/admin/ingest/harvestBundleParser.ts`.

## Validation rules

1. `items.length === summary.total`
2. Disposition counts in summary match item tallies
3. FETCH → non-null `harvested_path` → file exists on disk
4. LINK → non-empty `canonical_url`
5. SKIP and book types excluded from ingest but may appear in summary.skip
6. No duplicate `id`
7. No duplicate normalized `canonical_url` (warn if found)
