# Frontmatter Template Reference

This document defines the complete frontmatter specification for corpus ingestion files.
Two variants are provided: Tier 2 (converted markdown) and Tier 3 (curated corpus).

---

## Tier 2 — Converted Markdown

Minimum required fields immediately after MarkItDown conversion.

```yaml
---
# === IDENTITY ===
title: ""                        # Full title of the source document
author: ""                       # Full name (e.g. "Alan Hirsch")
editor: ""                       # Editor name if applicable (optional)
translator: ""                   # Translator name for non-English sources (optional)

# === SOURCE PROVENANCE ===
source_type: ""                  # book | sermon | transcript | slides | article | web | audio | zip
source_file: ""                  # Relative path to Tier 1 raw file (e.g. corpus_ingest/raw/alan_hirsch/books/foo.pdf)
source_url: ""                   # Original URL if web/audio source (optional)
original_filename: ""            # Original filename before any renaming (optional)
publication_year: ""             # Year of publication (optional but recommended)
publisher: ""                    # Publisher name (optional)
isbn: ""                         # ISBN if book (optional)
edition: ""                      # Edition info (optional)

# === CONVERSION METADATA ===
conversion_tool: markitdown      # Always "markitdown" for this pipeline
conversion_date: ""              # ISO 8601 date (e.g. "2026-03-27")
conversion_version: ""           # markitdown version used (optional but useful)
ai_enhanced: false               # true if LLM was used for image/slide descriptions

# === PIPELINE STATE ===
tier: converted_markdown         # converted_markdown | curated_corpus
cleanup_status: raw_conversion   # raw_conversion | in_review | cleaned | promoted

# === QUALITY SIGNALS ===
confidence: ""                   # high | medium | low — overall extraction quality
conversion_notes: ""             # Free text: known issues, artifacts, caveats, what needs cleanup
---
```

---

## Tier 3 — Curated Corpus

Full frontmatter for a promoted, curated file. Includes all Tier 2 fields plus enrichment.

```yaml
---
# === IDENTITY ===
title: ""                        # Document or chapter title
author: ""                       # Full name
editor: ""                       # Optional
translator: ""                   # Optional

# === SOURCE PROVENANCE (carried forward from Tier 2) ===
source_type: ""
source_file: ""
source_url: ""
publication_year: ""
publisher: ""
isbn: ""
edition: ""

# === CONVERSION METADATA (carried forward) ===
conversion_tool: markitdown
conversion_date: ""
conversion_version: ""
ai_enhanced: false

# === PIPELINE STATE ===
tier: curated_corpus
cleanup_status: promoted         # promoted | needs_revision

# === CORPUS ORGANIZATION ===
series: ""                       # Book/series slug (e.g. "the-forgotten-ways")
chapter: ""                      # Chapter number or ID (e.g. "ch03")
chapter_title: ""                # Chapter title
part: ""                         # Part/section within book (optional)
sequence: 0                      # Numeric sort order within series

# === LANGUAGE ===
language: en                     # en | es | pt | pt-BR | de | fr
is_translation: false            # true for non-English versions
source_language: ""              # Original language if translated (e.g. "en")

# === THEMATIC ENRICHMENT ===
topics: []                       # Array of topic slugs (e.g. ["apostolic-imagination", "mDNA"])
themes: []                       # Free-form theme tags
concepts: []                     # Key theological/conceptual terms in this document
related_books: []                # Slugs of closely related books in corpus

# === RETRIEVAL HINTS ===
summary: ""                      # 1-2 sentence summary for retrieval context
retrieval_priority: ""           # high | normal | low — weight in RAG ranking
exclude_from_retrieval: false    # Set true for TOC pages, indexes, boilerplate

# === QUALITY SIGNALS ===
confidence: high                 # high | medium | low
conversion_notes: ""             # Remaining notes (e.g. "page 47 table was manually fixed")
reviewed_by: ""                  # Name/agent that reviewed this file
review_date: ""                  # ISO date of last review
---
```

---

## Field Notes

### `source_type`
| Value | Use for |
|-------|---------|
| `book` | Published books (any format) |
| `sermon` | Sermon manuscripts or audio |
| `transcript` | Recorded talks, interviews, Q&As |
| `slides` | PowerPoint, Keynote, PDF slide decks |
| `article` | Journal articles, essays, blog posts |
| `web` | Web pages, HTML pages |
| `audio` | Standalone audio with transcription |
| `zip` | Archive containing mixed content |

### `confidence`
| Value | Meaning |
|-------|---------|
| `high` | Clean text extraction, structure intact, verified against original |
| `medium` | Minor artifacts present, structure mostly intact, spot-checked |
| `low` | Known extraction issues (OCR noise, broken tables, truncation), needs careful review before use |

### `cleanup_status`
| Value | Meaning |
|-------|---------|
| `raw_conversion` | Direct MarkItDown output, not yet reviewed |
| `in_review` | Currently being inspected/cleaned |
| `cleaned` | Cleanup complete, ready for promotion review |
| `promoted` | Tier 3 version exists in `corpus/` — this Tier 2 file is archived |
| `needs_revision` | Was promoted but a problem was found; re-promotion required |

### `retrieval_priority`
Use sparingly. Most files should be `normal`. Use `high` for primary source texts (e.g., canonical book chapters). Use `low` for appendices, indexes, or supplemental material that clutters retrieval.

---

## Naming Convention for Promoted Files

When splitting a book into chapters for Tier 3:

```
corpus/alan_hirsch/<book-slug>/
├── book.json
├── ch01-<chapter-title-slug>.md
├── ch02-<chapter-title-slug>.md
└── ...
```

**book.json minimum shape:**
```json
{
  "slug": "the-forgotten-ways",
  "title": "The Forgotten Ways",
  "author": "Alan Hirsch",
  "publication_year": 2006,
  "language": "en",
  "source_file": "corpus_ingest/raw/alan_hirsch/books/the-forgotten-ways.pdf",
  "chapters": ["ch01-the-journey-begins", "ch02-the-apostolic-genius"],
  "topics": ["mDNA", "apostolic-imagination", "missional-church"],
  "tier": "curated_corpus"
}
```
