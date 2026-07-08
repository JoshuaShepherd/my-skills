# Audit SQL patterns

Reusable classification fragments for persisted `text` content fields. Adapt table/column names and bucket labels to the domain.

## Base CTE — per-row signals

```sql
WITH c AS (
  SELECT
    id,
    /* join keys, e.g. book_id, organization_id */
    content,
    length(content) AS len,
    -- HTML block/inline tags
    (content ~* '<(h[1-6]|p|div|blockquote|ul|ol|li|img|table|figure|section|hr|br|em|strong|span|a)(\s|>|/)') AS has_html,
    -- Markdown structural
    (content ~ '(^|\n)#{1,6}[ \t]') AS has_md_heading,
    (content ~ '\*\*[^*\n]+\*\*') AS has_md_bold,
    (content ~ '\][ ]?\([^)\n]+\)') AS has_md_link,
    (content ~ '(^|\n)[*-][ \t]+\S') AS has_md_bullet,
    (content ~ '\[\^[0-9]+\]') AS has_md_footnote,
    -- MDX / JSX
    (content ~ '(^|\n)(import |export )') AS has_mdx_kw,
    (content ~ '<[A-Z][A-Za-z0-9]+') AS has_jsx_comp,
    -- Other
    (btrim(content) ~ '^[\[{]') AS looks_json,
    (content ~ '<!--[ ]?page') AS has_page_comment,
    (content IS NULL OR btrim(content) = '' OR length(content) < 20) AS is_empty_or_tiny
  FROM your_table
  WHERE content IS NOT NULL OR /* include nulls if auditing empties */
)
SELECT /* ... */;
```

## Mutually exclusive bucket (top-down)

```sql
CASE
  WHEN is_empty_or_tiny THEN 'empty_or_tiny'
  WHEN looks_json THEN 'json'
  WHEN has_mdx_kw OR has_jsx_comp THEN 'mdx_or_jsx'
  WHEN has_html AND (has_md_heading OR has_md_bold OR has_md_bullet) THEN 'hybrid'
  WHEN has_html THEN 'html'                    -- rename to target_format if HTML is canonical
  WHEN has_md_heading OR has_md_bold OR has_md_link OR has_md_bullet THEN 'markdown'
  ELSE 'plain_text'
END AS format_bucket
```

## Distribution summary

```sql
SELECT format_bucket, count(*) AS rows, round(avg(len)) AS avg_len
FROM classified
GROUP BY 1 ORDER BY rows DESC;
```

## Per-parent breakdown (e.g. per book)

```sql
SELECT parent_title, format_bucket, count(*) AS chapters
FROM classified
GROUP BY 1, 2
ORDER BY 1, 2;
```

## Severity sub-counts

```sql
SELECT
  count(*) FILTER (WHERE NOT has_html AND has_md_heading) AS pure_md_structural,
  count(*) FILTER (WHERE has_html AND has_md_heading) AS hybrid_structural,
  count(*) FILTER (WHERE has_html AND NOT has_md_heading AND (has_md_bold OR has_md_footnote)) AS hybrid_inline_only,
  count(*) FILTER (WHERE has_md_footnote) AS any_footnotes
FROM classified
WHERE NOT is_empty_or_tiny;
```

## Export affected IDs for script

```sql
SELECT id, /* metadata for logging */
FROM classified
WHERE format_bucket IN ('markdown', 'hybrid')  -- tier scope
ORDER BY id;
```

## Post-remediation verification

Re-run distribution query; compare to baseline saved in audit report. Document any intentional exceptions (e.g. EPUB links pending slug map).

## Format-specific notes

| Format | Detection tip | Common false positive |
|--------|---------------|----------------------|
| HTML | Tag openers | `<` in math or comparisons (rare in prose) |
| Markdown | Line-start `#`, list markers | `#` mid-sentence |
| MDX | `import`/`export`, PascalCase components | HTML `<Section>` vs JSX |
| JSON | Starts with `{` or `[` | Unlikely in prose fields |
| Plain text | No signals | Short blurbs, titles stored as body |

Adjust thresholds (`length < 20`) per domain — section dividers may be intentionally tiny but valid HTML.
