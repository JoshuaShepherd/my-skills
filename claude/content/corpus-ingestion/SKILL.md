---
name: corpus-ingestion
description: >
  Convert heterogeneous source files (PDFs, EPUBs, DOCX, PPTX, HTML, audio, images, ZIPs,
  web pages) into normalized markdown using MarkItDown, then prepare them for Movemental-style
  corpus pipelines. Use this skill whenever ingesting an author's books, sermons, transcripts,
  slide decks, or archive materials for downstream theme/voice/concept analysis, RAG pipeline
  preparation, course content generation, or vector store upload. Also trigger on: "ingest this
  book", "convert and add to corpus", "prepare source material", "add to the knowledge base",
  "batch convert documents for analysis", or any time raw heterogeneous files need to become
  clean, curated markdown assets.
allowed-tools: Read Write Edit Bash
---

# Corpus Ingestion — MarkItDown Pipeline

## Purpose

This skill governs how raw source materials are converted into markdown and promoted into a curated corpus. MarkItDown is the **conversion layer**, not the intelligence layer. It normalizes heterogeneous formats into a common markdown baseline so that later skills can clean, annotate, split, analyze, and retrieve from that content.

**Use this skill when:**
- Ingesting an author's books, essays, or published works
- Adding sermon transcripts, lecture recordings, or audio content
- Processing slide decks, workbooks, or PDF handouts
- Pulling web pages, articles, or archive materials into a corpus
- Preparing any source material for theme/voice analysis, RAG, or course generation

**Do not skip this skill** when adding new source material — raw files should always pass through the ingestion pipeline before entering curated storage. Skipping tiers creates data provenance problems.

---

## Three-Tier Pipeline Architecture

Every source file travels through three distinct tiers. Each tier has a different purpose, and they must not be conflated.

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: Raw Source                                          │
│  PDFs, EPUBs, DOCX, PPTX, HTML, audio, images, ZIPs, URLs  │
│  • Original, unmodified files                               │
│  • Preserved for provenance                                 │
│  • Never renamed or edited                                  │
│  Location: corpus_ingest/raw/<author>/<source-type>/        │
└────────────────────────────┬────────────────────────────────┘
                             │  MarkItDown conversion
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  TIER 2: Converted Markdown                                  │
│  Direct MarkItDown output, lightly wrapped with metadata    │
│  • Not yet canonical or curated                             │
│  • May contain extraction artifacts, bad tables, OCR noise  │
│  • Requires human/agent inspection before promotion         │
│  Location: corpus_ingest/converted_markdown/<author>/       │
└────────────────────────────┬────────────────────────────────┘
                             │  Cleaning, normalization, review
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  TIER 3: Curated Corpus                                      │
│  Cleaned, normalized, split/chunked, metadata-enriched      │
│  • Canonical — safe for downstream analysis                 │
│  • Frontmatter complete and validated                       │
│  • Ready for vector store, RAG, theme analysis, etc.        │
│  Location: corpus/<author>/<book-slug>/                     │
└─────────────────────────────────────────────────────────────┘
```

**The critical distinction:** Tier 2 is what MarkItDown produced. Tier 3 is what a human or agent curated. Never treat Tier 2 as ready for production retrieval. Never modify Tier 3 files as a shortcut — always trace changes back to Tier 2 and re-promote.

---

## Directory Conventions

```
project-root/
├── corpus_ingest/
│   ├── raw/
│   │   └── <author>/
│   │       ├── books/
│   │       ├── sermons/
│   │       ├── transcripts/
│   │       ├── slides/
│   │       └── web/
│   └── converted_markdown/
│       └── <author>/
│           ├── books/
│           ├── sermons/
│           ├── transcripts/
│           ├── slides/
│           └── web/
└── corpus/
    └── <author>/
        └── <book-or-series-slug>/
            ├── book.json          ← book/series metadata
            └── *.md               ← curated chapter/section files
```

For Movemental/Alan Hirsch work, the existing layout is:
```
corpus/alan_hirsch/<book-slug>/*.md     ← Tier 3 (curated, read-only once promoted)
corpus_ingest/raw/alan_hirsch/          ← Tier 1
corpus_ingest/converted_markdown/alan_hirsch/  ← Tier 2
```

---

## Workflow

### Step 1: Collect Raw Source Files

Gather source files into `corpus_ingest/raw/<author>/<source-type>/`. Preserve original filenames. Add a simple manifest if the batch is large.

```bash
# Example: place files
corpus_ingest/raw/alan_hirsch/books/the-forgotten-ways.pdf
corpus_ingest/raw/alan_hirsch/sermons/lausanne-2024-transcript.docx
corpus_ingest/raw/alan_hirsch/slides/apostolic-genius-workshop.pptx
```

### Step 2: Run MarkItDown Conversion

Use the batch script or run manually per file. See `scripts/batch_ingest.py` for automated batch processing.

```bash
# Single file
markitdown corpus_ingest/raw/alan_hirsch/books/the-forgotten-ways.pdf \
  -o corpus_ingest/converted_markdown/alan_hirsch/books/the-forgotten-ways.md

# Batch conversion (uses scripts/batch_ingest.py)
python scripts/batch_ingest.py \
  --input corpus_ingest/raw/alan_hirsch/ \
  --output corpus_ingest/converted_markdown/alan_hirsch/ \
  --author "Alan Hirsch"
```

For AI-enhanced conversions (slides with images, visual-heavy PDFs):
```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe this image in detail, focusing on theological concepts, diagrams, and key text visible in the slide."
)
result = md.convert("slides/workshop.pptx")
```

### Step 3: Add Frontmatter to Tier 2 Files

Every converted file must receive a frontmatter block immediately after conversion. This is the provenance record. See `references/frontmatter-template.md` for the full template and field definitions.

**Minimum required at Tier 2:**
```markdown
---
title: "The Forgotten Ways"
author: "Alan Hirsch"
source_type: book
source_file: "corpus_ingest/raw/alan_hirsch/books/the-forgotten-ways.pdf"
conversion_tool: markitdown
conversion_date: "2026-03-27"
tier: converted_markdown
cleanup_status: raw_conversion
---
```

### Step 4: Inspect and Validate

Before promotion, a human or agent must review each Tier 2 file. Key things to check:

- [ ] Did the conversion complete? (no truncation)
- [ ] Are tables legible, or garbled?
- [ ] Is heading structure preserved?
- [ ] Are there OCR artifacts or encoding errors?
- [ ] Is the structure coherent for this source type?
- [ ] Are footnotes / citations intact?
- [ ] For audio/video transcripts: is speaker attribution correct?

Document findings in the `conversion_notes` frontmatter field.

### Step 5: Clean and Normalize

Apply cleanup to the Tier 2 file before promotion. Do not do this in place — write cleaned output to a staging area, then promote. Common cleanup operations:

- Remove repeated headers, footers, page numbers from PDF extraction
- Normalize heading levels (some PDFs flatten all headings to H1)
- Clean broken table rows
- Fix character encoding issues (smart quotes, em-dashes)
- Remove publisher boilerplate / TOC noise from book conversions
- For sermons/transcripts: add speaker breaks, clean filler words if appropriate
- For slides: merge slide bodies into coherent prose sections

### Step 6: Add Tier 3 Frontmatter and Split if Needed

When ready for promotion:
1. Update frontmatter: set `tier: curated_corpus`, update `cleanup_status`
2. Add enrichment metadata: `topics`, `themes`, `series`, `language`
3. Split into chapter/section files if the source is a full book
4. Follow the existing corpus naming convention: `ch01-introduction.md`, etc.
5. Create or update `book.json` for the series

See `references/frontmatter-template.md` for the full Tier 3 frontmatter spec.

### Step 7: Promote to Curated Corpus

Move promoted files to `corpus/<author>/<book-slug>/`. Mark the Tier 2 file with `cleanup_status: promoted` so you know it has a canonical version.

### Step 8: Hand Off to Downstream Skills

Once files are in Tier 3, they are ready for:
- `build-rag` — vector store upload, retrieval pipeline setup
- Theme and voice analysis (topic guides, concept maps)
- Quote extraction and citation building
- Course/article generation pipelines
- Glossary and FAQ extraction

---

## Frontmatter Reference

See `references/frontmatter-template.md` for the complete template with all fields, descriptions, and allowed values. Key fields at a glance:

| Field | Required | Notes |
|-------|----------|-------|
| `title` | Yes | Book/document title |
| `author` | Yes | Full name |
| `source_type` | Yes | `book`, `sermon`, `transcript`, `slides`, `article`, `web`, `audio` |
| `source_file` | Yes | Relative path to Tier 1 file |
| `conversion_tool` | Yes | Always `markitdown` for this pipeline |
| `conversion_date` | Yes | ISO date of conversion |
| `tier` | Yes | `converted_markdown` or `curated_corpus` |
| `cleanup_status` | Yes | `raw_conversion`, `in_review`, `cleaned`, `promoted` |
| `language` | Tier 3 | `en`, `es`, `pt`, `pt-BR`, `de`, `fr` |
| `topics` | Tier 3 | Array of topic slugs |
| `series` | Tier 3 | Series/book slug for corpus grouping |
| `source_url` | If applicable | For web/audio sources |
| `conversion_notes` | Recommended | Human/agent notes about extraction quality |
| `confidence` | Recommended | `high`, `medium`, `low` — quality of extraction |

---

## Failure Modes and Warnings

Be explicit about these. Do not quietly pass bad output downstream.

### PDF Extraction
- **Scanned PDFs** produce garbled or empty output without OCR. Check if the PDF is text-based first.
- **Multi-column layouts** (common in academic papers) often produce mixed-up reading order.
- **Headers/footers** repeat on every extracted "page" — remove them during cleanup.
- **Footnotes** may be extracted out of context or attached to wrong paragraphs.
- **Image-heavy slides embedded as PDFs** may produce little usable text.

### Tables
- Complex nested tables often break. Check all tables in Tier 2 manually.
- Excel/PPTX tables generally convert better than PDF tables.

### OCR
- Low-resolution scans (below 300 DPI) produce unreliable OCR.
- Handwritten notes are not reliably extractable.
- Foreign language OCR requires appropriate language packs.

### Audio/Video Transcripts
- Auto-transcription does not add speaker attribution — add it manually or via a dedicated transcript tool.
- Filler words, false starts, and repetitions are preserved — normalize during cleanup if needed.

### Structure Collapse
- Some DOCX files lose heading hierarchy if styles were not used properly.
- PowerPoint notes may be mixed with slide body text.
- EPUB chapter breaks may not survive extraction cleanly.

### Duplicate Material
- Translations and editions of the same book will produce overlapping content.
- Track source files carefully in frontmatter to avoid duplicating corpus entries.

### False Confidence
- A clean Tier 2 file does not mean accurate extraction. Always validate against the original.
- "Looks fine" is not sufficient for theological/academic material where exact wording matters.

---

## Supported Source Types

| Source Type | Format(s) | Notes |
|-------------|-----------|-------|
| Books | PDF, EPUB, DOCX | Split into chapters before promoting |
| Sermons | DOCX, PDF, audio (MP3/WAV) | Audio requires transcription step |
| Transcripts | DOCX, TXT, PDF | Check speaker attribution |
| Slides/Workbooks | PPTX, PDF | Consider AI enhancement for diagrams |
| Articles/Essays | HTML, DOCX, PDF | Web pages via URL or saved HTML |
| Archives/ZIPs | ZIP | MarkItDown iterates contents automatically |
| Web pages | URL, HTML | Use `markitdown <url>` for live pages |

---

## Relationship to Downstream Skills

This skill is the **entry point** of the corpus pipeline. It must run before any of the following:

- **build-rag** — requires clean Tier 3 files for reliable retrieval
- **author-content** — requires corpus to have accurate, verified source material
- **course-authoring** — depends on curated corpus for grounded content generation
- Theme/concept extraction — garbage-in, garbage-out if Tier 2 isn't cleaned
- Voice analysis — requires clean prose, not PDF extraction artifacts
- Quote banking — requires verbatim accuracy; Tier 2 should never be used as quote source without verification
- Glossary/FAQ extraction — requires coherent, well-structured Tier 3 content
- Vector store upload (e.g., `npm run vector-store:upload`) — only Tier 3 files should be uploaded

**Never feed Tier 2 files directly into retrieval systems.** The pipeline exists precisely to prevent this.

---

## Quick Reference

```bash
# Install MarkItDown
pip install 'markitdown[all]'

# Convert single file
markitdown <file> -o <output.md>

# Batch convert a directory
python scripts/batch_ingest.py --input <raw-dir> --output <converted-dir> --author "<Author Name>"

# Convert a web page
markitdown https://example.com/article -o article.md

# Convert with AI image enhancement (for slides/visual PDFs)
# See scripts/batch_ingest.py --ai-enhance flag
```

---

## Notes for Future Agents

1. **Check `tier` and `cleanup_status` in frontmatter** before using any file. Do not analyze or retrieve from `tier: converted_markdown` files as if they were authoritative.
2. **Trace every Tier 3 file back to its Tier 1 source** before modifying. The `source_file` field is the provenance chain.
3. **Never modify files under `corpus/<author>/<book-slug>/` directly.** These are read-only once promoted. Re-run the ingestion pipeline for updates.
4. **The existing alan-books repo treats `corpus/alan_hirsch/` as Tier 3.** Do not ingest directly into this directory. Use the ingestion pipeline and then promote.
5. **When in doubt about extraction quality, mark `confidence: low`** and flag for human review before using the content downstream.
