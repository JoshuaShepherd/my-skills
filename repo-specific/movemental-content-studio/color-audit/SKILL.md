---
name: color-audit
description: Audit color palette for light/dark mode alignment, WCAG contrast compliance, and consistent token usage.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Audit the project's color system for accessibility and consistency.

Target: $ARGUMENTS (optional — specific component or page to audit)

## Before Starting

1. Read the main CSS file to inventory all color tokens and custom properties.
2. Read Tailwind config (if customized) for extended colors.

## Audit Dimensions

### 1. WCAG Contrast Compliance

Check all text/background combinations meet minimum contrast ratios:
- **Normal text** (< 18px): 4.5:1 ratio (WCAG AA)
- **Large text** (>= 18px bold or >= 24px): 3:1 ratio (WCAG AA)
- **UI components** (borders, icons, focus rings): 3:1 ratio

### 2. Light/Dark Mode Parity

- Every color token used in light mode has a dark mode counterpart
- Dark mode isn't just "invert" — check readability and contrast in both modes
- Backgrounds, text, borders, and interactive states all have dark variants

### 3. Color Consistency

- No raw hex/rgb values in components — all colors via tokens or Tailwind utilities
- Consistent use of semantic color names (primary, secondary, muted, destructive, etc.)
- No conflicting color assignments (same color used for success and error states)

### 4. Color Distribution

- **60-30-10 rule**: dominant background (60%), secondary surfaces (30%), accent (10%)
- Accent colors are used sparingly for CTAs and highlights
- Backgrounds provide sufficient visual hierarchy

### 5. Interactive State Colors

- Hover, focus, active, and disabled states are visually distinct
- Focus rings are visible against all backgrounds
- Disabled states have sufficient contrast to be readable but clearly muted

## Output Format

```
## Color Audit Report

### Token Inventory
| Token | Light Value | Dark Value | Usage Count |
|-------|-------------|------------|-------------|

### Contrast Issues
| # | Severity | Elements | Ratio | Required | Fix |
|---|----------|----------|-------|----------|-----|

### Missing Dark Mode
| # | File:Line | Class | Missing Dark Variant |
|---|-----------|-------|---------------------|

### Recommendations
- ...
```
