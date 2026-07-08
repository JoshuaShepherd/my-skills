---
name: persisted-content-remediation
description: >-
  Safely audit and remediate persisted text/content fields in Supabase or Postgres when bodies
  are in the wrong format (HTML, Markdown, MDX, plain text, hybrid, JSON, empty). Use for content
  format drift, ingest bypass, wrong-field storage, leaked markup, or batch normalization — always
  audit-first, backup, dry-run, deterministic transforms, never AI-rewrite in place.
disable-model-invocation: true
---

# Persisted Content Remediation

Safe workflow for fixing **stored content bodies** (not UI code) when format, encoding, or structure is wrong. Applies to any table/column (`book_chapters.content`, `content_items.content`, `archive_items.content`, etc.) and any source/target format: **HTML, Markdown, MDX, plain text, hybrid, JSON**.

## When to use

- User asks to fix, normalize, convert, or clean up **persisted content** in a database
- Audit found format drift (e.g. Markdown stored where HTML is expected)
- Ingest pipeline skipped conversion or used a naive converter
- Hybrid bodies (HTML + leaked `##` / `**` / `[^n]`)
- Wrong-field writes, truncation, empty placeholders, test/E2E pollution
- **Not** for: live editor UX, rendering component changes, or greenfield ingest (use the ingest skill instead)

## Golden rules (non-negotiable)

1. **Audit before write.** Classify every affected row; know the canonical target format from code (reader + service layer), not assumptions.
2. **MCP/database reads OK; MCP bulk writes NOT OK.** Use Supabase MCP `execute_sql` for classification and spot checks only. Remediation writes go through a **local script** + service role client.
3. **Deterministic transforms only.** Libraries (`marked`, `remark`, `sanitize-html`) — never paraphrase or "clean up" prose with the LLM.
4. **Scope to bad rows.** UPDATE only IDs matching the audit query. Never "fix all rows in the table."
5. **Backup before apply.** Export affected `(id, content, word_count, updated_at, …)` to JSON or a backup table.
6. **Dry-run default.** Script must support `--dry-run`; write human-reviewable diffs before `--apply`.
7. **Re-audit after apply.** Re-run classification SQL; counts of bad buckets should drop to zero (or documented exceptions).
8. **One tier at a time.** Pure-format fixes before hybrid surgery before cosmetic cleanup.

## Phase 0 — Discover canonical format

Before auditing data, read the **code path** that owns the field:

| Question | Where to look |
|----------|---------------|
| What format does the reader expect? | Components using `dangerouslySetInnerHTML`, MDX renderer, `ReactMarkdown`, TipTap JSON |
| What format does write path produce? | Service `create*` / `update*`, ingest mappers, `cleanupContent()` |
| What metadata must stay in sync? | `word_count`, `estimated_reading_time`, `updated_at` |
| Is there a naive converter to avoid? | e.g. repo `markdownToHtml()` — headings only, leaks inline MD |

Document finding in the audit report: **target format**, **detection heuristics**, **forbidden double-conversion**.

## Phase 1 — Audit (read-only)

### 1a. Locate the authoritative table

```sql
-- Example: find populated content tables
SELECT table_name FROM information_schema.columns
WHERE table_schema = 'public' AND column_name = 'content'
ORDER BY table_name;
```

Confirm row counts; ignore empty duplicate/legacy tables.

### 1b. Classify formats in SQL

Use mutually exclusive buckets (top-down). Adapt patterns to the domain — see [reference/audit-patterns.md](reference/audit-patterns.md).

Minimum buckets:

| Bucket | Meaning |
|--------|---------|
| `target_format` | Matches canonical (e.g. HTML fragment) |
| `pure_source_format` | Entire body is wrong format (e.g. raw Markdown, no HTML) |
| `hybrid` | Target format + leaked source tokens |
| `empty_or_tiny` | Null, `''`, or placeholder (`<p></p>`) |
| `plain_text` | Neither target nor recognizable markup |
| `structured_other` | JSON, MDX/JSX, XML — rare but flag explicitly |

### 1c. Severity rank

Worst → mildest:

1. **Pure wrong format** — visible breakage (literal `##`, `**`)
2. **Hybrid structural leaks** — `##` headings inside HTML
3. **Inline artifacts** — footnotes `[^1]`, stray bold, EPUB links
4. **Cosmetic noise** — HTML comments (`<!-- page: N -->`), entities
5. **Empty/test rows** — delete or leave; not format conversion

### 1d. Write audit report

Path convention (ZenWrite): `docs/build/<domain>/<topic>-audit.md`

Include: TL;DR, canonical format evidence (code citations), distribution table, per-entity breakdown, severity, root-cause read, recommended tiers, SQL appendix.

**Stop here unless user explicitly approves remediation.**

## Phase 2 — Plan remediation tiers

| Tier | Typical action | Risk |
|------|----------------|------|
| T1 Pure source → target | Full doc conversion via library | Low (with backup) |
| T2 Hybrid structural | Re-ingest from source file OR HTML-aware partial convert | Medium |
| T3 Inline artifacts | Targeted rules (footnotes policy, bold, links) | Medium–high |
| T4 Cosmetic strip | Comment/whitespace normalization | Low |
| T5 Row delete | Test/E2E rows only | Low (confirm with user) |

**Do not combine tiers in one apply pass.**

## Phase 3 — Implement remediation script

Create under `scripts/remediate-<domain>.ts` (or repo convention). Required flags:

```
tsx scripts/remediate-<domain>.ts --dry-run [--bucket pure_markdown] [--book-id UUID] [--limit N]
tsx scripts/remediate-<domain>.ts --apply --backup ./backups/<timestamp>.json [--bucket ...]
```

### Script requirements

```typescript
// Pattern (adapt per repo)
import './load-local-env.js';
import { createClient } from '@supabase/supabase-js';
import { marked } from 'marked'; // or remark/unified — pin version, verify docs
import { createHash } from 'crypto';
import { writeFileSync, mkdirSync } from 'fs';

const dryRun = !process.argv.includes('--apply');
const backupPath = getArg('--backup');

// 1. SELECT only rows matching audit bucket (same SQL as Phase 1)
// 2. For each row: transform deterministically; NEVER call LLM
// 3. Validate: sha256 before/after, length ratio, format re-check
// 4. If validation fails → skip row, log to remediation-skipped.json
// 5. dry-run → write diff files; apply → UPDATE + sync word_count/reading_time
```

### Transform selection

| Source → Target | Tool | Caution |
|-----------------|------|---------|
| MD → HTML | `marked` / `remark` + `rehype-sanitize` | Configure allowed tags to match reader |
| MDX → HTML | MDX compile OR strip JSX if MDX not supported | MDX ≠ MD; needs separate pipeline |
| HTML → HTML (hybrid) | Parse DOM (`node-html-parser`, `cheerio`); convert text nodes only | Never regex whole document |
| HTML → MD | Only if target is MD (rare) | Lossy; document why |
| Plain → HTML | Wrap in `<p>`, escape entities | Minimal |
| Strip comments | DOM or targeted regex on known patterns | Low risk |

**Never run MD converter on already-HTML bodies** unless you've extracted markdown islands first.

### Validation gates (per row)

Skip and flag if any fail:

- [ ] `sha256(before)` recorded in backup
- [ ] Plain-text word count within ±15% (or policy threshold)
- [ ] `len(after) >= 0.85 * len(before)` for MD→HTML (HTML adds tags)
- [ ] Re-classification passes target bucket
- [ ] No `<script>`, event handlers, or disallowed tags (if sanitizing)
- [ ] Unicode/CJK/RTL preserved (spot-check non-Latin samples)

### Diff output

Write to `docs/build/<domain>/remediation-diffs/<id>.diff` or a single JSONL with `{ id, beforeHead, afterHead, warnings }`.

## Phase 4 — Review gate

Before `--apply`:

1. User reviews audit + sample diffs (minimum 3 rows: small, medium, large; include non-English if present)
2. Confirm tier scope and row count
3. Confirm backup path exists

**Agent must not run `--apply` without explicit user approval.**

## Phase 5 — Apply and verify

```bash
# Apply
tsx scripts/remediate-<domain>.ts --apply --backup ./backups/2026-07-08-book-chapters.json --bucket pure_markdown

# Re-audit (same SQL as Phase 1)
# Expect: pure_source_format count → 0 for applied bucket
```

Print session report:

- Rows selected / transformed / skipped / failed
- Backup path
- Before/after bucket counts
- Skipped row IDs + reasons
- Suggested manual follow-ups

## Tool choice matrix

| Task | Tool | Notes |
|------|------|-------|
| Schema discovery | Supabase MCP `list_tables`, `execute_sql` | Read-only |
| Format classification | Supabase MCP `execute_sql` | Read-only |
| Spot-check bodies | Supabase MCP or script SELECT | Prefer script for large bodies |
| Backup export | Local script → JSON | Full fidelity |
| Transform | Local script + library | Deterministic |
| Write | Local script UPDATE | Transactional per batch optional |
| Bulk write via MCP | **Forbidden** | Truncation, no rollback, no diff review |

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| LLM rewrites chapter/article in chat | Hallucination, truncation, tone drift |
| `UPDATE ... SET content = '...'` via MCP with inline body | Context limits; untested |
| Run naive `markdownToHtml()` on hybrid HTML | Double-wraps, breaks tags |
| Regex replace on 40k-char HTML | Eats closing tags, nested structures |
| Fix all rows "while we're at it" | Damages good content |
| Skip backup "it's just 56 rows" | Irreversible without PITR |
| Assume MDX when codebase uses HTML | Wrong target format |

## Repo integration (ZenWrite)

| Resource | Path |
|----------|------|
| Example audit | `docs/build/books/chapter-content-format-audit.md` |
| Naive converter (do not use for full remediation) | `server/services/admin/ingest/contentCleanup.ts` |
| Chapter write path | `server/services/books/bookChapters.service.ts` |
| Migration script pattern | `scripts/migrate-books-to-catalog.ts` |
| Markdown lib | `marked` in `package.json` |
| Supabase project | Movemental `vhaiiiykcukrlyvwlgip` |

## Invocation

```
/persisted-content-remediation audit book_chapters.content
/persisted-content-remediation plan --report docs/build/books/chapter-content-format-audit.md
/persisted-content-remediation script book-chapters --tier 1 --dry-run
```

## Related skills

- **`movement-leader-harvest-ingest`** — forward ingest (prevent recurrence)
- **`type-safety-chain`** — if remediation touches schema/contracts
- **`validate`** — post-change repo validation

## Additional resources

- SQL classification templates: [reference/audit-patterns.md](reference/audit-patterns.md)
- Worked example walkthrough: [reference/worked-example-book-chapters.md](reference/worked-example-book-chapters.md)
