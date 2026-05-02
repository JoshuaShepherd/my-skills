---
name: typography-polish
description: Audit and fix prose/content typography across all rendering surfaces — articles, books, courses, chat responses, and any component rendering HTML or markdown from the database. Ensures beautiful, consistent long-form reading experiences.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

Audit and fix typography for all database-rendered content (articles, books, courses, chat responses).

Target: $ARGUMENTS

If no target is provided, audit all content rendering surfaces.

## Before Starting

1. Read `src/app/globals.css` to load the current `.content-prose`, `.course-content-html`, `.chat-response-prose`, and any `prose` usage.
2. Read `tailwind.config.ts` to confirm `@tailwindcss/typography` plugin presence and configuration.
3. Read `_docs/guides/typography-and-fonts.md` for the canonical font pairing (Montserrat headings + Inter body).
4. Read `_docs/design/DESIGN_CHARTER.md` for design tokens and typography intent.

## Content Rendering Surfaces

All database content passes through one of these rendering paths:

| Surface | Component | CSS Class | Method |
|---------|-----------|-----------|--------|
| **Articles** | `ArticleReader.tsx` | `.content-prose` | `dangerouslySetInnerHTML` |
| **Books** | `ChapterContent.tsx` | `.content-prose` | `dangerouslySetInnerHTML` |
| **Courses** | `MarkdownProse.tsx` / `ReadingSection.tsx` | `.course-content-html` | HTML or ReactMarkdown |
| **Chat** | AI Lab components | `.chat-response-prose` | ReactMarkdown |

## Typography Best Practices Checklist

### 1. READING COMFORT (Critical)
- [ ] Body text is 17–18px (1.0625–1.125rem) — never raw 16px for long-form
- [ ] Line height is 1.7–1.8 for body text (generous for readability)
- [ ] Letter-spacing is -0.005em to -0.01em for body (tightens at reading sizes)
- [ ] Paragraph spacing is 1.25–1.5rem between `<p>` elements
- [ ] Max line length is capped at 65ch (`--measure`) for comfortable reading
- [ ] First paragraph after a heading has no extra top margin

### 2. HEADING HIERARCHY (Critical)
- [ ] h2: 1.5rem (24px), font-weight 700, font-heading (Montserrat), margin-top 2.5rem, margin-bottom 0.75rem
- [ ] h3: 1.25rem (20px), font-weight 600, font-heading (Montserrat), margin-top 2rem, margin-bottom 0.5rem
- [ ] h4: 1.125rem (18px), font-weight 600, margin-top 1.5rem, margin-bottom 0.5rem
- [ ] First heading in content has margin-top: 0
- [ ] Headings use `--foreground` color, not muted

### 3. LISTS (High)
- [ ] Unordered lists use `disc` markers
- [ ] Ordered lists use `decimal` markers
- [ ] List markers are tinted with primary color at 60% opacity
- [ ] Left padding is 1.75rem
- [ ] Li spacing is 0.5rem between items
- [ ] Li line-height is 1.7

### 4. BLOCKQUOTES (High)
- [ ] Left border: 3px solid primary at 40% opacity
- [ ] Background: primary at 4% opacity
- [ ] Border-radius: 0 0.5rem 0.5rem 0 (right side only)
- [ ] Padding: 1rem 1.25rem
- [ ] Font-style: italic
- [ ] Color: muted-foreground
- [ ] Last paragraph inside has margin-bottom: 0

### 5. INLINE ELEMENTS (Medium)
- [ ] `<strong>` uses font-weight 600 and foreground color
- [ ] `<em>` uses italic style
- [ ] `<a>` uses primary color, underline, 2px underline-offset, hover at 80% opacity
- [ ] `<code>` (inline) uses mono font, 0.875em size, muted background, 0.125rem 0.375rem padding, 0.25rem radius

### 6. CODE BLOCKS (Medium)
- [ ] `<pre>` has muted background, border, border-radius, 1rem padding
- [ ] Horizontal overflow scrolls (overflow-x: auto)
- [ ] Margin: 1.5rem 0

### 7. HORIZONTAL RULES (Low)
- [ ] `<hr>` uses border-top only, border color, 2rem vertical margin

### 8. IMAGES IN CONTENT (Low)
- [ ] Max-width: 100%, height: auto
- [ ] Border-radius from design tokens
- [ ] Margin: 1.5rem 0

### 9. TABLES IN CONTENT (Low)
- [ ] Full width, border-collapse
- [ ] Header row has border-bottom, font-weight 600
- [ ] Cells have padding 0.5rem 0.75rem
- [ ] Alternating row backgrounds (optional)

## Audit Process

1. **Scan** — Find all components that render HTML/markdown content from the database:
   ```
   Grep for: dangerouslySetInnerHTML, ReactMarkdown, course-content-html, prose, content-prose
   ```

2. **Check each surface** against the checklist above.

3. **Verify CSS class exists** — The `.content-prose` class in `globals.css` should cover articles, books, and any general content. `.course-content-html` and `.chat-response-prose` are separate but should share the same typographic foundation.

4. **Report** findings with file, line, issue, and fix.

## Fixing Protocol

1. **Never modify Tailwind prose plugin config for content typography** — use `.content-prose` CSS class for full control.
2. **Fix at the CSS layer first** — Update `.content-prose` / `.course-content-html` in `globals.css` rather than adding inline Tailwind classes.
3. **Keep surfaces consistent** — Articles, books, and courses should feel like the same reading experience.
4. **Test dark mode** — All typography must work in both themes.
5. **Preserve TOC functionality** — Heading ID injection and IntersectionObserver must still work.

## Output Format

```
## Typography Polish Report

### Summary
- Surfaces audited: X
- Issues found: X (Critical: X, High: X, Medium: X, Low: X)
- Fixed: X

### Issues by Surface

#### Articles (ArticleReader.tsx)
| Issue | Severity | Fix |
|-------|----------|-----|
| No prose styles applied (plugin missing) | Critical | Use .content-prose CSS class |

#### Books (ChapterContent.tsx)
...

#### Courses (MarkdownProse.tsx)
...

### Files Modified
- path/to/file — description of changes
```

## Rules

- Always scan before fixing. Present findings first.
- The `.content-prose` class is the canonical long-form typography class for articles and books.
- The `.course-content-html` class is the canonical class for course lesson content.
- The `.chat-response-prose` class is optimized for chat UX (tighter spacing).
- All three share the same typographic DNA: same fonts, same base sizing, same element styles.
- Do not add `@tailwindcss/typography` as a dependency — we use hand-crafted CSS classes for full control and consistency.
