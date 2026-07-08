# Harvest markdown frontmatter template

Every FETCH file under `docs/harvest/` should start with YAML frontmatter. The manifest builder reads these fields first.

## Article / newsletter (FETCH)

```markdown
---
id: danielle-strickland-blog-094
title: "Working at contentment."
type: article
author: Danielle Strickland
source_url: https://www.daniellestrickland.com/blog/2007/04/12/working-at-contentment
alt_urls: []
published: 2007-04-12
retrieved: 2026-07-06
host: daniellestrickland.com
primary: true
disposition: FETCH
license_note: owned blog
---

Body starts here…
```

## Video / podcast (LINK catalog stub — optional)

When keeping a placeholder md for TRANSCRIBE queue:

```markdown
---
id: hugh-halter-video-012
title: "Session at Exponential 2019"
type: video
source_url: https://www.youtube.com/watch?v=XXXXXXXXXXX
published: 2019-03-01
host: YouTube
primary: true
disposition: TRANSCRIBE
---

TRANSCRIPT PENDING
```

## Field aliases accepted by build-manifest

| Frontmatter key | Manifest field |
|-----------------|----------------|
| `id` | `id` |
| `title` | `title` |
| `type` | `type` |
| `source_url`, `canonical_url`, `url` | `canonical_url` |
| `published`, `date` | `date` |
| `host`, `outlet` | `host` |
| `primary` | `primary` (boolean) |
| `disposition` | `disposition` |
| `alt_urls` | `alt_urls` (array) |
| `notes`, `license_note` | `notes` (concatenated) |

Filename stem is used as `id` when frontmatter omits `id`.
