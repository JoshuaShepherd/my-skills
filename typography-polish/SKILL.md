---
name: typography-polish
description: Audit and fix typography across movemental — heading hierarchy, Inter font compliance, display tracking, eyebrow conventions, prose width, and content readability across all page surfaces.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Audit and fix typography for all rendered content across movemental pages and components.

Target: $ARGUMENTS

If no target is provided, audit `src/app/(site)/` pages and `src/components/sections/`.

## Before Starting

1. Read `docs/design/DESIGN.md` §5 — Typography rules.
2. Read `src/app/globals.css` — font setup and `@layer base` heading defaults.
3. Read `src/app/layout.tsx` — Inter font loading via `next/font/google`.
4. Read `src/components/primitives/display.tsx` — Display heading component.
5. Read `src/components/primitives/eyebrow.tsx` — Eyebrow label component.
6. Read `src/components/primitives/prose.tsx` — Prose body text wrapper.

## Typography Rules (DESIGN.md §5)

| Element | Font | Weight | Tracking | Size | Notes |
|---------|------|--------|----------|------|-------|
| Display (h1 hero) | Inter | 600 (semibold) | -0.02em | fluid clamp | Via `<Display size="lg">` |
| Section heading (h2) | Inter | 600 | -0.02em | fluid | Via `<Display size="md" as="h2">` |
| Sub-heading (h3) | Inter | 600 | tight | 1.125-1.25rem | Standard Tailwind |
| Eyebrow / label | Inter | 500-700 | +0.05em | 0.75rem | Uppercase, via `<Eyebrow>` |
| Body text | Inter | 400 | normal | 1rem-1.125rem | Via `<Prose>` or standard |
| Body large | Inter | 400 | normal | 1.125rem | `text-lg` |

## Audit Checklist

### 1. FONT COMPLIANCE
- [ ] **Inter only** — no other fonts loaded or referenced
- [ ] No `font-serif`, `font-mono` in content areas (allowed in code blocks)
- [ ] No Google Fonts CDN links (must use `next/font/google`)
- [ ] Font loaded with `display: "swap"` for performance

### 2. HEADING HIERARCHY
- [ ] Single `h1` per page (via `<Display>` in hero section)
- [ ] Sequential heading order: h1 → h2 → h3 (no skipping levels)
- [ ] Display headings use `<Display>` primitive with `tracking-[-0.02em]`
- [ ] No orphaned headings (heading always followed by body content)
- [ ] Section headings use `<Display as="h2">`, not raw `<h2>` with manual styling

### 3. EYEBROW LABELS
- [ ] All section labels use `<Eyebrow>` primitive
- [ ] Uppercase with `tracking-[0.05em]`
- [ ] Size `0.75rem` (12px)
- [ ] Color: `text-muted-foreground` (default) or `text-primary` (when emphasized)
- [ ] No manual uppercase labels that bypass the Eyebrow component

### 4. BODY TEXT
- [ ] Minimum 16px (1rem) on all breakpoints
- [ ] Long-form content wrapped in `<Prose>` (caps width at `--prose-max: 680px`)
- [ ] Line height: 1.5-1.75 for body text (readable)
- [ ] No text smaller than 12px anywhere except fine print / legal
- [ ] Muted text uses `text-muted-foreground`, not opacity hacks

### 5. LINE LENGTH & READABILITY
- [ ] Prose blocks capped at ~680px (`--prose-max`) or max-w-2xl/max-w-3xl
- [ ] No full-width paragraphs at desktop (unreadable at 1200px+)
- [ ] Card text has appropriate max-width or container constraint

### 6. RESPONSIVE SCALING
- [ ] Display headings use responsive classes or `clamp()` for fluid sizing
- [ ] No fixed font sizes that are too large on mobile or too small on desktop
- [ ] Text doesn't overflow containers at 375px mobile width

## Fixing Protocol

1. Replace manual heading styling with `<Display>` / `<Eyebrow>` primitives.
2. Wrap long-form text in `<Prose>` to enforce max-width and readable line-height.
3. Never change the font family — Inter is the only font for movemental.
4. Fix heading hierarchy before fixing styling (semantic structure first).

## Output Format

```markdown
## Typography Audit: [target]

### Summary
- Pages/components scanned: X
- Violations found: X

### Issues
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|

### Fixes Applied
- file.tsx — description
```

## Rules

- Inter is the ONLY font. No exceptions.
- Use primitives (`Display`, `Eyebrow`, `Prose`) instead of manual styling.
- Heading hierarchy is semantic, not visual — fix structure before aesthetics.
- Present the full audit before applying fixes.
