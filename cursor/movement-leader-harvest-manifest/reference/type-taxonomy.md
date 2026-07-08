# Harvest type taxonomy

## Directory → type mapping

Folder under `docs/harvest/` (singular aliases in parentheses):

| Folder | Harvest `type` | Ingest target |
|--------|----------------|---------------|
| `articles` | `article` | `archive_items` / `content_items` |
| `newsletters` | `newsletter` | `archive_items` / `content_items` |
| `interviews` | `interview` | `archive_items` / `content_items` |
| `academic` | `academic` | `archive_items` / `content_items` |
| `resources` | `resource` | `archive_items` / `content_items` |
| `courses` | `course` | `archive_items` / `content_items` |
| `videos` | `video` | `videos` |
| `podcasts` | `podcast-host` or `podcast` | `podcast_episodes` |
| `podcast-guest` | `podcast-guest` | `content_items` (if FETCH body) |
| `talks`, `audio`, `sermons` | `talk` / `audio` / `sermon` | Usually LINK → media tables |
| `books` | **out of scope** | Defer to corpus-upload |
| `book-chapters` | `book-chapter` | `book_chapters` |

## URL heuristics (when type missing)

| Signal | Infer type |
|--------|------------|
| `youtube.com`, `youtu.be`, `vimeo.com` | `video` |
| `substack.com`, `/p/` on Substack | `newsletter` |
| `spotify.com`, `podcasts.apple.com`, `.mp3` in alt_urls | `podcast-host` |
| `medium.com`, `/blog/`, owned domain blog path | `article` |
| DOI, `.edu`, journal domain | `academic` |

## Disposition defaults

| Type | Default disposition when… |
|------|---------------------------|
| Any | `.md` file on disk → **FETCH** |
| `video`, `podcast-host` | URL only, no body → **LINK** |
| `video`, `podcast-host` | URL + `TRANSCRIPT PENDING` stub → **TRANSCRIBE** |
| Guest appearance, syndicated | Often **LINK** unless full text fetched |
| Book | **SKIP** (log to books-seen.md) |

## Content-type mapping at ingest (articles)

| Harvest `type` | DB `content_type` | DB `format` |
|----------------|-------------------|-------------|
| `article`, `interview`, `academic` | `article` | `article` |
| `newsletter` | `newsletter` | `email` |
| `podcast-guest` | `podcast_guest` | `article` |

See `zenwrite/server/services/admin/ingest/harvestMapper.ts` → `mapContentType()`.
