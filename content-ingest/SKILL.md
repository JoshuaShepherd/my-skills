---
name: content-ingest
description: Ingest, organize, and structure raw content (book chapters, transcripts, articles, research notes) into the repository's canonical format. Use when bringing new source material into the content library.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Ingest content: $ARGUMENTS

$ARGUMENTS should specify: the source material (file path, URL, or pasted content) and the target location (corpus, course, article, pathway, research). If incomplete, ask the user.

## Content Types and Destinations

| Source | Destination | Format |
|--------|-------------|--------|
| Book chapters | `courses/corpus/[book-slug]/` | Markdown with frontmatter |
| Transcripts (audio/video) | `research/transcripts/` | Markdown with speaker tags |
| Articles | `articles/` | Markdown with frontmatter |
| Research papers/notes | `research/` | Markdown |
| Course drafts | `courses/courses/[slug]/` | Markdown per section |
| Pathway content | `pathways/` | Markdown with frontmatter |

## Ingestion Process

### 1. Assess the Source
- What type of content is this?
- What's the quality level? (raw transcript, edited draft, published)
- What frameworks or concepts does it contain?
- How does it relate to existing content in the repo?

### 2. Clean and Structure
- Remove artifacts (page numbers, headers/footers, OCR noise)
- Add frontmatter (title, author, source, date, tags, related frameworks)
- Structure with headings that reflect the content's logic
- Preserve Alan's exact language where possible — do not paraphrase theological claims

### 3. Tag and Cross-Reference
- Tag with relevant frameworks: mDNA elements, APEST types, key concepts
- Note connections to existing courses or pathways
- Flag quotable passages for use in course content

### 4. Place in Repository
- Write to the correct directory
- Update any index files if they exist
- Note what was ingested and where in the output

## Quality Checks
- Source attribution preserved
- No theological claims altered or softened
- Framework terminology used consistently (mDNA not "missional DNA", APEST not "fivefold gifts")
- Markdown formatting clean and consistent
