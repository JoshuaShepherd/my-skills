---
name: movement-leader-media-transcribe
description: >-
  Transcribe YouTube and podcast items from a movement leader's harvest-manifest.json — yt-dlp
  auto-captions for video, Whisper for podcast RSS/mp3 URLs. Writes verbatim transcripts to
  docs/harvest/transcripts/ and updates the manifest. Run after movement-leader-content-harvest
  and before movement-leader-harvest-ingest when LINK/TRANSCRIBE media needs text.
disable-model-invocation: true
---

# Movement Leader Media Transcribe

Process **primary** video and podcast items from `harvest-manifest.json` into searchable transcript files. This skill closes the transcribe queue left by content-harvest step 07.

## Invocation

```
/movement-leader-media-transcribe {leader-slug}
/movement-leader-media-transcribe danielle-strickland --types video,podcast-host
/movement-leader-media-transcribe deb-hirsch --max 10 --dry-run
/movement-leader-media-transcribe hugh-halter --refresh
```

Run from **monorepo root** (`movement-leader-websites/`).

### CLI (preferred for batch)

```bash
pnpm harvest:transcribe -- --slug {leader-slug}
pnpm harvest:transcribe -- --slug danielle-strickland --types video,podcast-host --dry-run
pnpm harvest:transcribe -- --slug deb-hirsch --max 20 --refresh
pnpm harvest:transcribe -- --slug deb-hirsch --skip-whisper   # YouTube only
```

| Flag | Effect |
|------|--------|
| `--slug` | Required leader slug |
| `--types` | Filter: `video`, `podcast-host`, `podcast`, `audio` (comma-separated) |
| `--dry-run` | Report what would run; no files written |
| `--max N` | Limit items (cost control for Whisper) |
| `--refresh` | Re-transcribe even when a transcript file exists |
| `--skip-whisper` | YouTube yt-dlp only; skip podcast Whisper |

## Prerequisites

1. `harvest-manifest.json` exists for the tenant (`docs/movement_leader_research/content/`)
2. **YouTube:** `yt-dlp` installed (`pip install yt-dlp`)
3. **Podcast Whisper:** `OPENAI_API_KEY` in tenant `.env.local` or environment
4. **Large audio (>25MB):** `ffmpeg` recommended

## What gets transcribed

Items where `primary: true` and type is media (`video`, `podcast-host`, `podcast`, `audio`, …) and:

- `disposition` is `TRANSCRIBE`, `LINK`, or FETCH video
- No clean transcript file yet (unless `--refresh`)

**Skip:** guest-only items marked `primary: false`, articles, SKIP disposition.

## Pipeline

| Source | Method | Output |
|--------|--------|--------|
| YouTube URL | yt-dlp EN subs → VTT parse | `docs/harvest/transcripts/{id}.md` |
| Podcast mp3 in `alt_urls` | curl download → Whisper | same |
| Already pending stub | Overwrite when successful | updates `transcript_method` in front-matter |

Each file uses harvest front-matter + **verbatim** transcript body (no summarization).

## After transcribe

1. Update `harvest-manifest.json` `harvested_path` + `transcript_status`
2. Run **`movement-leader-harvest-ingest`** to push transcripts into Supabase `videos.transcript` / `podcast_episodes.transcript`

## Related skills

- **`movement-leader-content-harvest`** — discovery + manifest (upstream)
- **`movement-leader-harvest-ingest`** — manifest → Supabase (downstream)
- **`youtube-transcript`** — ad-hoc single-video extraction (not manifest-driven)

## Session report

Print: slug, items attempted, transcribed / failed / skipped, word counts, Whisper cost note if applicable.
