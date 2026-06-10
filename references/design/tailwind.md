
Build or style UI with Tailwind CSS v4: $ARGUMENTS

$ARGUMENTS should include:
- What to build or style (component, page, layout, design system)
- Optionally: target file path
- Optionally: design requirements (colors, typography, spacing, responsive behavior)
- Optionally: framework context (Next.js, Vite, React Router)
- Optionally: "audit" to scan for utility issues
- Empty — ask the user what they need

## Authoritative Documentation

### Primary References
- Tailwind CSS Docs: https://tailwindcss.com/docs
- Installation (Vite): https://tailwindcss.com/docs/installation/using-vite
- Installation (PostCSS): https://tailwindcss.com/docs/installation/using-postcss
- Installation (CLI): https://tailwindcss.com/docs/installation/tailwind-cli
- Framework Guides: https://tailwindcss.com/docs/installation/framework-guides

### Core Concepts
- Styling with Utility Classes: https://tailwindcss.com/docs/styling-with-utility-classes
- Hover, Focus & Other States: https://tailwindcss.com/docs/hover-focus-and-other-states
- Responsive Design: https://tailwindcss.com/docs/responsive-design
- Dark Mode: https://tailwindcss.com/docs/dark-mode
- Theme Variables: https://tailwindcss.com/docs/theme
- Adding Custom Styles: https://tailwindcss.com/docs/adding-custom-styles
- Detecting Classes in Source Files: https://tailwindcss.com/docs/detecting-classes-in-source-files
- Functions & Directives: https://tailwindcss.com/docs/functions-and-directives
- Browser Support: https://tailwindcss.com/docs/browser-support

### v4 Architecture
- v4 Upgrade Guide: https://tailwindcss.com/docs/upgrade-guide
- CSS-first Configuration: https://tailwindcss.com/blog/tailwindcss-v4
- Compatibility (v3 → v4): https://tailwindcss.com/docs/compatibility

### Utility Reference
- Layout: https://tailwindcss.com/docs/display
- Flexbox & Grid: https://tailwindcss.com/docs/flex-basis
- Spacing: https://tailwindcss.com/docs/padding
- Sizing: https://tailwindcss.com/docs/width
- Typography: https://tailwindcss.com/docs/font-family
- Backgrounds: https://tailwindcss.com/docs/background-color
- Borders: https://tailwindcss.com/docs/border-radius
- Effects: https://tailwindcss.com/docs/box-shadow
- Transitions & Animation: https://tailwindcss.com/docs/transition-property
- Transforms: https://tailwindcss.com/docs/scale

### Ecosystem
- Tailwind Plus (Components): https://tailwindcss.com/plus
- GitHub: https://github.com/tailwindlabs/tailwindcss
- npm: https://www.npmjs.com/package/tailwindcss
- Prettier Plugin: https://github.com/tailwindlabs/prettier-plugin-tailwindcss

## Before Starting

1. Determine the Tailwind version — this skill targets **v4** (CSS-first config)
2. Confirm `tailwindcss` is installed — if not: `pnpm add tailwindcss @tailwindcss/vite` (Vite) or `pnpm add tailwindcss @tailwindcss/postcss` (PostCSS)
3. Read the project's CSS entry file (usually `app/globals.css` or `src/index.css`) for existing theme tokens
4. Check for `tailwind.config.ts` — in v4 this is optional; prefer CSS-first `@theme` configuration

## Tailwind v4 — CSS-First Architecture

### Key Change from v3
v4 replaces `tailwind.config.js` with **CSS-first configuration** using `@theme`, `@import`, and `@custom-variant` directives.

### Entry Point (globals.css)

```css
@import "tailwindcss";

/* Custom theme variables */
@theme {
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.1 200);
  --color-accent: oklch(0.8 0.2 80);
  --color-background: oklch(0.98 0 0);
  --color-foreground: oklch(0.15 0 0);
  --color-muted: oklch(0.95 0 0);
  --color-muted-foreground: oklch(0.5 0 0);
  --color-border: oklch(0.9 0 0);
  --color-card: oklch(1 0 0);
  --color-destructive: oklch(0.65 0.2 25);
  --color-success: oklch(0.7 0.2 145);

  --font-sans: "Inter", "system-ui", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;

  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.07);
  --shadow-lg: 0 10px 15px oklch(0 0 0 / 0.1);

  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.4s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Dark Mode (v4)

```css
@import "tailwindcss";

/* Class-based dark mode (for manual toggle) */
@custom-variant dark (&:where(.dark, .dark *));

/* Or use default prefers-color-scheme (no config needed) */
```

Usage in HTML/JSX:
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <!-- Content adapts to theme -->
</div>
```

### Extending the Default Theme

```css
@theme {
  /* ADD to existing namespace (extends) */
  --color-brand: oklch(0.7 0.18 250);

  /* OVERRIDE defaults by redefining */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;

  /* CLEAR a namespace and replace entirely */
  --font-*: initial;
  --font-sans: "Inter", sans-serif;
  --font-display: "Cal Sans", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}
```

### v3 Compatibility (if needed)

```css
@import "tailwindcss";
@config "../../tailwind.config.ts";
```

## Utility-First Patterns

### Layout

```html
<!-- Flexbox centering -->
<div class="flex items-center justify-center min-h-screen">

<!-- CSS Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- Container with auto margins -->
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
```

### Responsive Design

Breakpoints are mobile-first — utilities apply at that breakpoint AND above:

| Prefix | Min Width | CSS |
|---|---|---|
| `sm:` | 640px | `@media (min-width: 640px)` |
| `md:` | 768px | `@media (min-width: 768px)` |
| `lg:` | 1024px | `@media (min-width: 1024px)` |
| `xl:` | 1280px | `@media (min-width: 1280px)` |
| `2xl:` | 1536px | `@media (min-width: 1536px)` |

```html
<!-- Stack on mobile, 2 cols on md, 3 cols on lg -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

<!-- Full width on mobile, max-width on desktop -->
<div class="w-full lg:max-w-2xl">

<!-- Hidden on mobile, visible on md+ -->
<nav class="hidden md:flex">
```

### Typography

```html
<!-- Heading -->
<h1 class="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">

<!-- Body text -->
<p class="text-base text-muted-foreground leading-relaxed">

<!-- Small/caption -->
<span class="text-sm text-muted-foreground">
```

### Spacing

The spacing scale uses a 4px base (1 unit = 0.25rem = 4px):

| Class | Value | Pixels |
|---|---|---|
| `p-1` | 0.25rem | 4px |
| `p-2` | 0.5rem | 8px |
| `p-3` | 0.75rem | 12px |
| `p-4` | 1rem | 16px |
| `p-6` | 1.5rem | 24px |
| `p-8` | 2rem | 32px |
| `p-12` | 3rem | 48px |
| `p-16` | 4rem | 64px |

### States & Interactivity

```html
<!-- Hover, focus, active -->
<button class="bg-primary text-white hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary active:scale-[0.98] transition-all">

<!-- Group hover (parent triggers child style) -->
<div class="group">
  <p class="text-muted-foreground group-hover:text-foreground transition-colors">

<!-- Focus-within (child focus triggers parent style) -->
<div class="focus-within:ring-2 focus-within:ring-primary">

<!-- Disabled state -->
<button class="disabled:opacity-50 disabled:pointer-events-none">
```

### Animations & Transitions

```html
<!-- Simple transition -->
<div class="transition-all duration-200 ease-in-out">

<!-- Transform on hover -->
<div class="hover:scale-105 hover:-translate-y-1 transition-transform duration-300">

<!-- Animate entrance -->
<div class="animate-fade-in">

<!-- Spin (built-in) -->
<svg class="animate-spin h-5 w-5">
```

## Component Patterns

### Card

```html
<div class="rounded-lg border border-border bg-card p-6 shadow-sm transition-shadow hover:shadow-md">
  <h3 class="text-lg font-semibold text-foreground">Title</h3>
  <p class="mt-2 text-sm text-muted-foreground">Description text here.</p>
</div>
```

### Button Variants

```html
<!-- Primary -->
<button class="inline-flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary active:scale-[0.98] transition-all disabled:opacity-50 disabled:pointer-events-none">

<!-- Secondary -->
<button class="inline-flex items-center justify-center gap-2 rounded-md border border-border bg-background px-4 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted transition-colors">

<!-- Ghost -->
<button class="inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium text-foreground hover:bg-muted transition-colors">

<!-- Destructive -->
<button class="inline-flex items-center justify-center gap-2 rounded-md bg-destructive px-4 py-2 text-sm font-medium text-white hover:bg-destructive/90 transition-colors">
```

### Input

```html
<input class="w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
```

### Navigation

```html
<nav class="flex items-center justify-between px-6 py-4 border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
  <div class="flex items-center gap-8">
    <a href="/" class="text-lg font-bold text-foreground">Logo</a>
    <div class="hidden md:flex items-center gap-6">
      <a class="text-sm text-muted-foreground hover:text-foreground transition-colors">
    </div>
  </div>
</nav>
```

### Modal / Dialog Overlay

```html
<!-- Backdrop -->
<div class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm">
  <!-- Content -->
  <div class="fixed left-1/2 top-1/2 z-50 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg rounded-lg border border-border bg-card p-6 shadow-lg animate-fade-in">
    <h2 class="text-lg font-semibold text-foreground">Dialog Title</h2>
    <p class="mt-2 text-sm text-muted-foreground">Body content.</p>
  </div>
</div>
```

## Semantic Color System

Always use semantic color tokens — never raw palette colors in components:

| Token | Use For | Tailwind Class |
|---|---|---|
| `background` | Page background | `bg-background` |
| `foreground` | Primary text | `text-foreground` |
| `card` | Card surfaces | `bg-card` |
| `muted` | Subtle backgrounds | `bg-muted` |
| `muted-foreground` | Secondary text | `text-muted-foreground` |
| `border` | Borders, dividers | `border-border` |
| `primary` | Brand/action color | `bg-primary`, `text-primary` |
| `destructive` | Danger actions | `bg-destructive` |
| `success` | Success states | `bg-success` |

### Opacity Modifiers

```html
<!-- Apply opacity to any color -->
<div class="bg-primary/10">   <!-- 10% opacity -->
<div class="bg-primary/50">   <!-- 50% opacity -->
<div class="text-foreground/70"> <!-- 70% opacity -->
```

## shadcn/ui Integration

Tailwind + shadcn/ui is the dominant React component pattern:

### Required CSS Variables (globals.css)

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark counterparts */
  }
}
```

### cn() Utility (class merging)

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Usage:
```tsx
<div className={cn(
  "rounded-lg border p-4",
  isActive && "border-primary bg-primary/5",
  className
)}>
```

## Advanced Patterns

### Container Queries (v4)

```html
<div class="@container">
  <div class="@sm:flex @md:grid @md:grid-cols-2">
    <!-- Responds to container width, not viewport -->
  </div>
</div>
```

### Arbitrary Values

```html
<!-- When the scale doesn't have what you need -->
<div class="top-[117px]">
<div class="grid grid-cols-[1fr_2fr_1fr]">
<div class="bg-[#1da1f2]">   <!-- Avoid — use theme tokens -->
<div class="bg-[--my-color]">  <!-- Better — reference CSS variable -->
```

### Arbitrary Variants

```html
<div class="[&>*]:mb-4">        <!-- Direct children spacing -->
<div class="[&_p]:text-sm">     <!-- All descendant paragraphs -->
<li class="[&:nth-child(3)]:underline">  <!-- Specific child -->
```

### Important Modifier

```html
<!-- Prefix with ! to add !important -->
<p class="!text-foreground">
```

### Peer & Group Modifiers

```html
<!-- Peer: sibling-based styling -->
<input class="peer" />
<p class="invisible peer-invalid:visible text-destructive text-sm">
  This field is required.
</p>

<!-- Group: parent-based styling -->
<a class="group">
  <span class="group-hover:underline">Link text</span>
  <svg class="group-hover:translate-x-1 transition-transform">
</a>
```

## Performance & Best Practices

1. **Use the design scale** — prefer `p-4` over `p-[16px]`
2. **Semantic tokens first** — `bg-primary` over `bg-blue-600`
3. **Mobile-first** — write base styles for mobile, add breakpoint variants for larger screens
4. **Reasonable className length** — if a className exceeds ~200 chars, extract to a component or CSS class
5. **cn() for conditionals** — never string-concatenate classNames; use `cn()` with `clsx` + `twMerge`
6. **Don't mix approaches** — either Tailwind classes or inline styles for a property, never both
7. **Consistent sizing** — use the same spacing scale throughout (4/8/12/16/24/32/48)
8. **Purging** — v4 auto-detects classes in source files; no purge config needed
9. **Prettier plugin** — install `prettier-plugin-tailwindcss` for consistent class ordering
10. **Tree-shaking** — v4 only includes utilities you actually use; no manual optimization needed

## Tailwind v4 vs v3 Key Differences

| Feature | v3 | v4 |
|---|---|---|
| Configuration | `tailwind.config.js` | `@theme` in CSS |
| Import | 3 directives | `@import "tailwindcss"` |
| Dark mode | `darkMode: 'class'` in config | `@custom-variant dark (...)` in CSS |
| Custom colors | `theme.extend.colors` in config | `--color-*` in `@theme` |
| Custom breakpoints | `theme.screens` in config | `--breakpoint-*` in `@theme` |
| Plugins | `plugins: [...]` in config | `@plugin "..."` in CSS |
| Content detection | `content: [...]` in config | Automatic (scans source files) |
| Color format | HSL (default) | oklch (recommended) |

## Output Format

```
## Tailwind Implementation Report

### Component: [name]
### File: [path]

### Design Tokens Used
- Colors: bg-primary, text-foreground, border-border
- Spacing: p-4, gap-6, mt-2
- Typography: text-sm, font-medium, tracking-tight

### Responsive Behavior
- Mobile: stacked single column
- md: 2-column grid
- lg: sidebar + content layout

### Dark Mode
- All colors use semantic tokens (auto dark mode)

### Next Steps
- Review styling in both light/dark modes
- Verify responsive breakpoints
```

## Rules

- Always use semantic color tokens — NEVER raw palette colors (`bg-blue-500`) in components
- Mobile-first responsive design — base styles for mobile, `md:` and `lg:` for larger screens
- Use `cn()` for conditional className merging — never string concatenation
- Prefer the spacing scale (4/8/12/16/24/32) — avoid arbitrary pixel values
- Always pair `bg-*` with appropriate `text-*` for contrast (e.g., `bg-primary text-primary-foreground`)
- Use `focus-visible:` instead of `focus:` for keyboard-only focus indicators
- Don't use `@apply` in v4 except in `globals.css` base styles — prefer utility classes in markup
- Use `transition-*` with explicit properties — avoid bare `transition` (animates everything)
- In Next.js App Router, Tailwind classes work in both server and client components
- Always add `disabled:opacity-50 disabled:pointer-events-none` to interactive elements
- Use `backdrop-blur-sm` for glassmorphism overlays — always with `bg-*/50` opacity
