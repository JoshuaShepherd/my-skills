---
name: responsive-audit
description: Audit pages for responsiveness across mobile, tablet, and desktop breakpoints. Check layout, typography, overflow, touch targets, and spacing.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Audit the target page or component for responsiveness across breakpoints.

Target: $ARGUMENTS

If no target is provided, audit all page-level components in `src/`.

## Breakpoints to Test

- **Mobile**: 375px (iPhone SE / small Android)
- **Tablet**: 768px (iPad portrait)
- **Desktop small**: 1024px (laptop)
- **Desktop large**: 1280px+ (monitor)

## Audit Dimensions

### 1. Mobile-First Architecture
- Verify base styles target mobile, with `sm:`, `md:`, `lg:` for larger screens
- Flag desktop-first patterns (e.g., `w-1/3 sm:w-full` instead of `w-full sm:w-1/3`)

### 2. Grid & Flexbox Collapse
- Multi-column grids must stack on mobile: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Flex containers must wrap: `flex-wrap` or switch to `flex-col` on small screens
- Sidebar layouts must collapse to single column on mobile

### 3. Typography Scaling
- Body text: minimum 16px on mobile
- Headings should scale down: use `text-2xl md:text-4xl` patterns
- Line length: max 65-75ch for readability

### 4. Overflow Prevention
- No horizontal scroll on any breakpoint
- Check for fixed-width elements that exceed viewport: `w-[600px]`, wide tables
- Images must be constrained: `max-w-full` or `w-full`

### 5. Touch Targets
- Interactive elements: minimum 44x44px tap area on mobile
- Adequate spacing between clickable items (minimum 8px gap)
- No hover-only interactions without mobile alternative

### 6. Spacing & Padding
- Container padding: minimum 16px (p-4) on mobile
- Section spacing should reduce on mobile: `py-16 md:py-24`
- No content touching screen edges

### 7. Navigation
- Navigation must be accessible on mobile (hamburger menu, bottom nav, etc.)
- No horizontal nav that overflows on small screens

### 8. Images & Media
- All images: `max-w-full h-auto` or equivalent
- Consider `aspect-ratio` for responsive containers
- Lazy loading for below-fold images

### 9. Forms & Inputs
- Full-width inputs on mobile
- Adequate font size (16px+) to prevent iOS zoom
- Touch-friendly select/dropdown components

### 10. Conditional Content
- Check for `hidden md:block` patterns — ensure mobile users aren't missing critical content
- Verify mobile alternatives exist for desktop-only features

## Output Format

```
## Responsive Audit: [target]

### Score: X/10

### Issues Found
| # | Dimension | Severity | File:Line | Issue | Fix |
|---|-----------|----------|-----------|-------|-----|

### Recommendations
- ...
```

Apply all Critical and High severity fixes automatically.
