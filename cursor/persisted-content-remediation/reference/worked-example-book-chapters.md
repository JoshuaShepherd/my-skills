# Worked example: `book_chapters.content`

ZenWrite audit (2026-07-08). Full report: `docs/build/books/chapter-content-format-audit.md` in the zenwrite repo.

## Canonical format

**Sanitized HTML fragment** — not MDX, not Markdown.

Evidence:

- Reader: `dangerouslySetInnerHTML` + `prose`
- Write path: `cleanupContent()` → `markdownToHtml()` on ingest; default `'<p></p>'`
- Table: `book_chapters.content` (1,460 rows with body); `books_chapters` empty legacy duplicate

## Audit results (baseline)

| Bucket | Count | Action tier |
|--------|------:|-------------|
| HTML (target) | 1,323 | None |
| Hybrid HTML + MD | 64 | T2–T3 |
| Pure Markdown | 56 | **T1 first** |
| Empty/tiny | 17 | T5 (mostly test) |
| Plain text | 1 | Manual |
| MDX/JSON | 0 | — |

Top pure-Markdown books: *The Art of Missional Spirituality* (42), *Kingdom Contours* (10), *The Underground Church* (4).

## Recommended remediation order

1. **T1** — 56 pure Markdown → `marked` + sanitize → UPDATE; backup + dry-run
2. **T2** — 8 hybrid with structural `##` inside HTML
3. **T3** — 322 HTML rows with `[^n]` / stray `**` (needs footnote policy)
4. **T4** — optional strip `<!-- page: N -->` (797 rows, cosmetic)
5. **T5** — delete or ignore E2E/test rows

## What not to do

- Do not run repo `markdownToHtml()` for remediation — it misses inline MD and caused the footnote leak
- Do not MCP-UPDATE 45k-char bodies through chat
- Do not convert the 1,323 good HTML rows

## Script name (when built)

`scripts/remediate-book-chapter-content.ts` with `--bucket pure_markdown --dry-run`
