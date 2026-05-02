
Audit and fix typography for all database-rendered content (articles, documentation, courses, chat responses, or any component rendering HTML/markdown).

Target: $ARGUMENTS

If no target is provided, audit all content rendering surfaces.

## Before Starting

1. Read the global CSS file to load any existing prose/content typography classes.
2. Read the Tailwind config to confirm `@tailwindcss/typography` plugin presence and configuration.
3. Read any typography or font documentation for the project's canonical font pairing.
4. Read any design charter or design tokens documentation for typography intent.

## Content Rendering Surfaces

All database content typically passes through one of these rendering paths. Identify and catalog the specific surfaces used in this project:

| Surface | Component | CSS Class | Method |
|---------|-----------|-----------|--------|
| **Articles / Blog** | Article renderer | `.content-prose` or equivalent | `dangerouslySetInnerHTML` |
| **Documentation** | Doc renderer | `.content-prose` or equivalent | `dangerouslySetInnerHTML` |
| **Courses / Lessons** | Lesson content component | Course content class | HTML or ReactMarkdown |
| **Chat / AI responses** | Chat message component | Chat prose class | ReactMarkdown |

## Typography Best Practices Checklist

### 1. READING COMFORT (Critical)
- [ ] Body text is 17-18px (1.0625-1.125rem) — never raw 16px for long-form
- [ ] Line height is 1.7-1.8 for body text (generous for readability)
- [ ] Letter-spacing is -0.005em to -0.01em for body (tightens at reading sizes)
- [ ] Paragraph spacing is 1.25-1.5rem between `<p>` elements
- [ ] Max line length is capped at 65ch for comfortable reading
- [ ] First paragraph after a heading has no extra top margin

### 2. HEADING HIERARCHY (Critical)
- [ ] h2: ~1.5rem (24px), font-weight 700, heading font family, margin-top 2.5rem, margin-bottom 0.75rem
- [ ] h3: ~1.25rem (20px), font-weight 600, heading font family, margin-top 2rem, margin-bottom 0.5rem
- [ ] h4: ~1.125rem (18px), font-weight 600, margin-top 1.5rem, margin-bottom 0.5rem
- [ ] First heading in content has margin-top: 0
- [ ] Headings use foreground color, not muted

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
- [ ] `<code>` (inline) uses mono font, 0.875em size, muted background, small padding, 0.25rem radius

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
   Search for: dangerouslySetInnerHTML, ReactMarkdown, prose, content-prose, or equivalent content rendering patterns
   ```

2. **Check each surface** against the checklist above.

3. **Verify CSS class exists** — The primary content prose class in the global CSS should cover articles and general content. Additional surface-specific classes should share the same typographic foundation.

4. **Report** findings with file, line, issue, and fix.

## Fixing Protocol

1. **Never modify Tailwind prose plugin config for content typography** — use custom CSS classes for full control.
2. **Fix at the CSS layer first** — Update content prose classes in the global CSS rather than adding inline Tailwind classes.
3. **Keep surfaces consistent** — All long-form reading surfaces should feel like the same reading experience.
4. **Test dark mode** — All typography must work in both themes.
5. **Preserve interactive functionality** — Heading ID injection, IntersectionObserver for TOCs, and similar features must still work.

## Output Format

```
## Typography Polish Report

### Summary
- Surfaces audited: X
- Issues found: X (Critical: X, High: X, Medium: X, Low: X)
- Fixed: X

### Issues by Surface

#### [Surface Name] (component.tsx)
| Issue | Severity | Fix |
|-------|----------|-----|
| No prose styles applied | Critical | Use content prose CSS class |

#### [Surface Name] (component.tsx)
...

### Files Modified
- path/to/file — description of changes
```

## Rules

- Always scan before fixing. Present findings first.
- The primary content prose class is the canonical long-form typography class for articles and documentation.
- Additional surface classes (for courses, chat, etc.) should be optimized for their context (e.g., tighter spacing for chat).
- All surfaces share the same typographic DNA: same fonts, same base sizing, same element styles.
- Prefer hand-crafted CSS classes over the `@tailwindcss/typography` plugin for full control and consistency.
