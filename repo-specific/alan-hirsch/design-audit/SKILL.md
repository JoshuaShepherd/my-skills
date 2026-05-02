---
name: design-audit
description: Audit a page or component against the AntiGravity 5-dimension design framework and project conventions. Use to check visual quality, accessibility, and consistency before shipping.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit the specified file(s) against design quality standards.

Target: $ARGUMENTS

## Audit Checklist

Read the target file(s) and evaluate across all 5 dimensions:

### 1. PATTERN & LAYOUT
- [ ] Clear visual hierarchy (heading -> subheading -> body -> CTA)
- [ ] Consistent spacing using Tailwind spacing scale (not arbitrary values)
- [ ] Responsive: works at mobile (375px), tablet (768px), desktop (1280px)
- [ ] No horizontal scroll on any breakpoint
- [ ] Content sections have logical grouping

### 2. STYLE & AESTHETIC
- [ ] Uses shadcn/ui components, not raw HTML with custom styles
- [ ] Consistent border radius (uses `rounded-*` from design tokens)
- [ ] Shadow usage is subtle and consistent
- [ ] No competing visual styles within the same view

### 3. COLOR & THEME
- [ ] NO hardcoded colors (no `bg-blue-600`, no hex values, no rgb())
- [ ] All colors use semantic tokens (`bg-primary`, `text-muted-foreground`, etc.)
- [ ] Works in both light and dark mode
- [ ] WCAG AA contrast compliance (4.5:1 for normal text, 3:1 for large text)
- [ ] Follows 60-30-10 color distribution

### 4. TYPOGRAPHY
- [ ] No more than 2 font families used
- [ ] No more than 5 font size variations in a single view
- [ ] Text is readable (minimum 16px body text on mobile)
- [ ] Line length capped at ~75 characters for readability
- [ ] No orphaned headings (heading always followed by content)

### 5. ANIMATIONS & INTERACTIONS
- [ ] All interactive elements have visible hover/focus states
- [ ] Focus indicators are at least 3px and high contrast
- [ ] `prefers-reduced-motion` is respected
- [ ] No animations block user interaction
- [ ] No transitions longer than 300ms for micro-interactions
- [ ] Scroll animations use transform/opacity only (GPU accelerated)

### ACCESSIBILITY
- [ ] All images have meaningful alt text
- [ ] No color-only information conveyance
- [ ] Keyboard navigation works (no traps)
- [ ] Tap targets are minimum 44x44px
- [ ] ARIA labels on icon-only buttons
- [ ] No auto-focus on page load (except search pages)

### TENANT ISOLATION
- [ ] No hardcoded tenant-specific strings (use tenantConfig)
- [ ] Feature flags checked before optional sections
- [ ] No direct fetch() calls (uses hooks)

## Output Format

Report as:
```
## Design Audit: [filename]

### Score: X/5 dimensions passing

### Issues Found
1. [DIMENSION] — [severity: HIGH/MEDIUM/LOW] — description — file:line
   Fix: specific suggestion

### Passing
- [DIMENSION] — what's working well
```
