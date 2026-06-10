---
name: workspace-organize
description: "Audit and fix workspace doc organization — frontmatter hygiene, section placement, sidebar rendering, and frontend-safe content. Ensures docs/workspace/ files render cleanly with no metadata leaking into the reader view. Use when adding docs, reorganizing sections, or before deploying."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---

Audit and organize workspace documents: $ARGUMENTS

$ARGUMENTS should be one of:
- "audit" — Full audit of all docs in docs/workspace/
- "fix" — Audit and auto-fix all issues found
- A specific section (e.g., "articles") — Audit that section only
- A specific file path — Audit that single file
- Empty — Run full audit

## What This Skill Does

The workspace at `/workspace` reads markdown from `docs/workspace/` and renders it in the browser. This skill ensures:

1. **Frontmatter is clean** — Only the right fields, correctly formatted
2. **No metadata leaks** — Status fields, editorial notes, and raw frontmatter never show in the reader
3. **Sections match directories** — Every subdirectory is a sidebar section
4. **Ordering is intentional** — `order` field controls sort within each section
5. **Filenames follow conventions** — Lowercase kebab-case, no prefixes, `.md` extension
6. **Content renders correctly** — Headings, lists, blockquotes, code, and task lists all work in `workspace-prose`

## Phase 1: Scan

Read all files in `docs/workspace/` recursively:

```bash
find docs/workspace -name "*.md" -not -name "README.md" | sort
```

For each file, extract and check:

### Frontmatter Checks

| Field | Required | Rules |
|-------|----------|-------|
| `title` | Yes | Non-empty string. Sentence case or title case. No quotes needed unless special chars. |
| `description` | Yes | 1 sentence, under 120 chars. Shown in sidebar/listing. |
| `order` | Yes | Integer. Controls sort within section. |
| `themes` | Articles only | Array of valid EEAT theme slugs |
| `status` | Articles only | One of: `draft`, `review`, `published` |
| `audience` | Articles only | One of: `collaborators`, `internal`, `public` |
| `author` | Articles only | Should be "Brad Brisco" |
| `updated` | Articles only | ISO date YYYY-MM-DD |

**Fields that must NOT appear in non-article docs:**
- `source`, `url`, `published_at`, `content_type`, `slug` — these are article-specific
- Any field not in the table above for the doc type

### Content Checks

| Issue | Detection | Fix |
|-------|-----------|-----|
| Frontmatter visible in body | Body starts with `---` after the closing `---` | Remove duplicate frontmatter |
| Raw YAML in body | Lines like `status: draft` or `themes:` in body text | Move to frontmatter or remove |
| Broken frontmatter | Missing closing `---` | Add closing delimiter |
| Double frontmatter | Two `---..---` blocks | Merge into one |
| H1 duplicates title | First heading matches `title` field exactly | Remove the H1 (title is rendered by the viewer) |
| Empty description | `description: ""` or missing | Generate from first paragraph |
| Missing order | No `order` field | Assign based on alphabetical position |
| Invalid theme slug | Theme not in EEAT taxonomy | Flag for user review |

### Filename Checks

| Issue | Detection | Fix |
|-------|-----------|-----|
| Uppercase letters | `[A-Z]` in filename | Rename to lowercase |
| Spaces in filename | ` ` in filename | Replace with `-` |
| Underscores | `_` in filename | Replace with `-` |
| Prefix `brad-brisco-` | Starts with `brad-brisco-` | Strip prefix |
| Non-.md extension | `.mdx`, `.markdown`, etc. | Rename to `.md` |

### Section Checks

| Issue | Detection | Fix |
|-------|-----------|-----|
| Orphan file | `.md` in `docs/workspace/` root (not in a subdirectory) | Move to appropriate section or flag |
| Empty section | Directory with no `.md` files | Flag for removal or content |
| Unknown section | Directory not in expected set | Flag for user review |

**Expected sections** (see `docs/workspace/README.md` and `WORKSPACE_SECTION_ORDER` in `src/lib/workspace/docs.ts`):
- `articles` — Covocational articles
- `author` — Voice identity, writing prompts, digital profile
- `books` — Published books and e-book manuscripts
- `ideas` — Notes and brainstorms
- `insights` — Content pipeline, EEAT, gap analysis, playbooks
- `meta` — Conventions, templates, article index (sidebar: Editorial)
- `podcasts` — Podcast notes
- `projects` — Active project documents
- `research` — Research notes and bibliography
- `videos` — Video scripts and outlines

## Phase 2: Report

Present findings as a table:

```
## Audit Results

### Issues Found: N

| File | Issue | Severity | Auto-fixable |
|------|-------|----------|-------------|
| ... | ... | error/warn | yes/no |

### Section Summary

| Section | Docs | All Clean | Issues |
|---------|------|-----------|--------|
| articles | 15 | ✓ | 0 |
| ... | ... | ... | ... |
```

Severity levels:
- **error** — Will break rendering or leak metadata (auto-fix if possible)
- **warn** — Should be fixed but won't break anything
- **info** — Suggestion for improvement

## Phase 3: Fix (if requested)

For each auto-fixable issue:
1. Show the proposed change
2. Apply with Edit tool
3. Mark as fixed in the report

For non-auto-fixable issues, explain what the user needs to decide.

## Phase 4: Verify Sidebar Rendering

After fixes, verify the API returns clean data:

1. Read `src/lib/workspace/docs.ts` to understand how the scanner works
2. Confirm every section directory is scanned
3. Confirm every file has valid frontmatter that the scanner can parse
4. Confirm `title` and `description` are the ONLY fields surfaced in the sidebar listing
5. Confirm no raw content or metadata appears in the sidebar (only title + description)

## Frontend-Safe Content Rules

These rules ensure clean rendering in the `workspace-prose` class:

1. **No frontmatter in body** — The viewer strips frontmatter via `gray-matter`. If there's a second `---` block, it renders as an `<hr>` and raw YAML text.

2. **No editorial metadata in prose** — Lines like `Status: draft`, `Audience: internal`, or `Updated: 2026-04-07` must ONLY live in frontmatter, never in the body.

3. **H1 is optional in body** — The doc viewer renders the `title` field as the page heading. If the body also has an `# H1`, it creates a duplicate. Prefer starting body content with H2 or a lead paragraph.

4. **Task lists render** — `- [ ]` and `- [x]` are styled by `workspace-prose`. Use them freely.

5. **Tables render** — Standard GFM tables work. `workspace-prose` styles them with Inter label font.

6. **Blockquotes render** — `>` blockquotes are styled. Use `> **Practice:**` for callouts.

7. **Code blocks render** — Fenced code blocks with language tags work. Inline `code` is styled.

8. **Images need relative paths** — Use `![alt](./image.png)` or absolute URLs. No broken image refs.

9. **Internal links** — Use relative paths from the file's location. e.g., `[Voice Guide](../author/voice-identity.md)`

## Quick Commands

### Audit everything
```
/workspace-organize audit
```

### Fix a specific section
```
/workspace-organize fix articles
```

### Check a single file before committing
```
/workspace-organize docs/workspace/articles/new-article.md
```
