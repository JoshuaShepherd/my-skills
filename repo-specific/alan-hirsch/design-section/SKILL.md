---
name: design-section
description: Design a new UI section or component using the 5-dimension AntiGravity framework (pattern, style, color, typography, animation). Use when building a new visual section, hero, feature grid, or page layout.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Design and implement a UI section using the AntiGravity 5-dimension framework.

Section request: $ARGUMENTS

## Before Starting

1. Read `src/app/globals.css` to understand the current design tokens (CSS variables)
2. Read `src/lib/config/tenant.config.ts` to understand tenant theming
3. Read 1-2 existing pages in `src/app/(public)/` that are similar to what's being requested

## The 5 Dimensions

For each section you build, explicitly decide on all 5 dimensions:

### 1. PATTERN & LAYOUT (The Skeleton)
Choose a functional pattern based on the content type:
- **Content Hub**: Hero + Featured Grid + Category Filters + Load More
- **Detail Page**: Hero + Content Body + Related Items + CTA
- **Landing/Sales**: Hero + Features + Social Proof + Pricing + CTA
- **Dashboard/Bento**: Modular card grid, varying sizes, consistent gaps (16-24px)
- **Course/Learning**: Sidebar nav + Content area + Progress indicators
- **Listing**: Filter bar + Card grid + Pagination

### 2. STYLE & AESTHETIC (The Skin)
This project uses a warm, scholarly aesthetic. Apply these principles:
- Subtle depth through shadow layers, not heavy borders
- Rounded corners (use design token `--radius` from globals.css)
- Clean card-based layouts using shadcn Card component
- Generous whitespace — let content breathe
- Never glassmorphism or brutalism — this is a thought leader platform

### 3. COLOR & THEME (The Palette)
STRICT RULES — never hardcode colors:
- Use semantic Tailwind classes only: `bg-primary`, `text-muted-foreground`, `border-border`
- All color values come from CSS variables in `globals.css`
- Support both light and dark mode via the existing token system
- Follow 60-30-10 rule: 60% background, 30% surface/card, 10% accent/CTA
- Ensure WCAG AA compliance (4.5:1 contrast for text)

### 4. TYPOGRAPHY (The Voice)
Use the project's existing type scale (defined in globals.css and Tailwind config):
- Headings: Use Tailwind prose classes or explicit sizes from the scale
- Body: `text-base` or `text-sm` with `text-foreground` or `text-muted-foreground`
- Never import new fonts without explicit approval
- Maximum 3 font sizes per section for visual clarity

### 5. ANIMATIONS & INTERACTIONS (The Soul)
Use GSAP (already in the project) for scroll animations. Follow these rules:
- Micro-interactions: 150-300ms duration, `ease-out` easing
- Scroll reveals: Fade up (opacity 0->1, translateY 20px->0), stagger 100ms
- Card hovers: translateY(-2px) + shadow increase via Tailwind `hover:` utilities
- ALWAYS include `prefers-reduced-motion` support
- Never animate width/height/position — use transform and opacity only
- No animations longer than 500ms for user interactions
- Parallax: Subtle only, max 20-30px movement

## Implementation Rules

- Use shadcn/ui components (Card, Button, Badge, etc.) — never raw HTML with inline styles
- Use `tenantConfig` for any text that could vary per tenant
- Check feature flags before rendering optional sections
- Keep the page/layout as a Server Component; push "use client" to leaf interactive components
- Images: Use Next.js `<Image>` with WebP, lazy loading, proper width/height to avoid CLS

## Anti-Patterns to Avoid

- No more than 3 primary colors visible at once
- No more than 2 font families
- No light grey text on white backgrounds
- No hover-only interactions (must work on touch)
- No auto-playing media
- Tap targets minimum 44x44px
- No layout shifts — always set explicit dimensions on media
