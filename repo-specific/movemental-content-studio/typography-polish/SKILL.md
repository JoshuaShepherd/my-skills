---
name: typography-polish
description: Audit typography for reading comfort, heading hierarchy, responsive scaling, and content rendering surfaces.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Audit typography across the project for readability and consistency.

Target: $ARGUMENTS (optional — specific component or page)

If no target is provided, audit all content-rendering surfaces.

## Audit Dimensions

### 1. Reading Comfort

- **Body text size**: 16-18px (text-base to text-lg)
- **Line height**: 1.6-1.8 for body text (leading-relaxed or leading-loose)
- **Line length**: max 65-75ch (`max-w-prose` or `max-w-[65ch]`)
- **Paragraph spacing**: adequate margin between paragraphs

### 2. Heading Hierarchy

- Clear visual progression: h1 > h2 > h3 > h4
- Consistent heading styles across pages
- No skipped heading levels in document structure
- Headings use appropriate font weight (bold/semibold for distinction)

### 3. Responsive Typography

- Text scales appropriately: `text-xl md:text-2xl lg:text-4xl`
- No text overflow on mobile (long words, URLs)
- Minimum 16px body text on mobile (prevents iOS zoom on inputs)

### 4. Font Loading

- Web fonts loaded with `font-display: swap` or `optional`
- System font fallback stack is appropriate
- No FOIT (Flash of Invisible Text) on slow connections

### 5. Content Typography

For rich text / article content:
- Lists (ul/ol) have proper indentation and markers
- Blockquotes are visually distinct
- Code blocks have monospace font and appropriate styling
- Links are visually distinct from surrounding text
- Bold and italic styles render correctly

### 6. Whitespace & Spacing

- Consistent spacing between sections
- Adequate padding in cards and containers
- No cramped text against edges

## Output Format

```
## Typography Audit: [target]

### Issues
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|

### Recommendations
- ...
```

Apply Critical and High severity fixes automatically.
