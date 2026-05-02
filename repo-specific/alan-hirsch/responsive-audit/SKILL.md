---
name: responsive-audit
description: Audit and fix responsiveness issues across any section or page — breakpoint coverage, layout collapse, touch targets, typography scaling, overflow, image sizing, and navigation behavior. Enforces mobile-first design for this Next.js + Tailwind + shadcn platform.
user-invocable: true
allowed-tools: Read, Edit, Grep, Glob, Bash, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__emulate, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__evaluate_script
---

Audit and fix responsiveness across the specified section or page(s).

Target: $ARGUMENTS

If no target is provided, audit `src/app/(public)/page.tsx` (homepage) and its constituent sections.

## Before Starting

1. Read the target file(s) — include any layout files wrapping the page (`layout.tsx`, `PublicLayoutClient.tsx`).
2. Read `src/components/navigation/SiteBar.tsx`, `PublicHeader.tsx`, and `BottomNav.tsx` — nav behavior drives the viewport offset at every breakpoint.
3. Read `src/app/globals.css` — note any custom responsive CSS, `--chat-viewport-offset`, container widths, and safe-area handling.
4. Read `tailwind.config.ts` — confirm the breakpoint scale in use.
5. Identify all component files rendered by the target — read them too.

## Breakpoint Reference

This platform uses **Tailwind's default breakpoint scale** (mobile-first):

| Breakpoint | Min-width | Device context |
|---|---|---|
| (base) | 0px | Phones portrait (320–479px) |
| `xs` | 475px | Large phones (if configured) |
| `sm` | 640px | Phones landscape / small tablets |
| `md` | 768px | Tablets portrait |
| `lg` | 1024px | Tablets landscape / small laptops |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Wide desktop |

**Primary test widths:** 375px (iPhone SE), 390px (iPhone 14), 430px (iPhone 14 Pro Max), 768px (iPad), 1024px (iPad landscape), 1280px (desktop), 1440px (wide desktop).

## Audit Checklist

Work through all 10 dimensions. For every issue record: file, line number, offending code, severity, and the concrete fix.

---

### 1. MOBILE-FIRST ARCHITECTURE

The single most common failure mode: desktop-first styles that override down instead of building up.

- [ ] **Mobile-first class order:** Base classes define the mobile layout; `sm:`, `md:`, `lg:`, `xl:` progressively enhance. No bare classes that only make sense on desktop (e.g., `grid-cols-3` without a mobile fallback like `grid-cols-1`).
- [ ] **No mobile overrides with `max-*` prefixes:** Avoid `max-sm:hidden`, `max-md:flex-col` patterns — these are desktop-first. Prefer `hidden sm:block`, `flex-col md:flex-row`.
- [ ] **Container max-width:** Sections use `max-w-screen-xl mx-auto` (or equivalent token) so content doesn't stretch to 2560px on ultra-wide.
- [ ] **Section padding scales correctly:** At minimum `px-4 sm:px-6 lg:px-8` — never raw `px-20` without mobile consideration.

---

### 2. GRID & FLEXBOX LAYOUT COLLAPSE

- [ ] **Grid column collapses:** Every `grid` with multiple columns has a mobile-safe base (e.g., `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`). Flag any `grid-cols-2+` without a base.
- [ ] **Flex wrap vs overflow:** Flex rows use `flex-wrap` OR have a `flex-col` mobile base. Check for flex rows that overflow at 375px.
- [ ] **Gap scaling:** Gaps scale with breakpoint — `gap-4 md:gap-6 lg:gap-8` not a fixed large gap.
- [ ] **Order / stacking sequence:** On mobile, the most important content (headline, CTA) stacks first — hero text before image, not after.
- [ ] **Sidebar patterns:** Any sidebar (course sidebar, nav drawer) is off-canvas or collapsed on mobile. No fixed-width sidebars that push content off screen.
- [ ] **Two-column → one-column:** Every two-column layout (`grid-cols-2`, `flex` row) collapses to single column on mobile.
- [ ] **Card grids:** Card grids have a sensible minimum card width (`min-w-0` to allow shrinking, or `grid-cols-1 sm:grid-cols-2`).

---

### 3. TYPOGRAPHY SCALING

- [ ] **Heading scale:** `h1` / hero headings use fluid or responsive sizing — `text-3xl sm:text-4xl lg:text-5xl xl:text-6xl`. Never a single large fixed size.
- [ ] **Body text minimum:** Body text is **minimum 16px** on mobile (maps to `text-base`). `text-sm` (14px) is acceptable for labels, metadata, captions only.
- [ ] **No iOS auto-zoom:** Any `<input>`, `<textarea>`, `<select>` inside forms has `text-base` (16px) minimum to prevent iOS Safari from zooming the page on focus.
- [ ] **Line length control:** Long-form prose (`<article>`, readers, book chapters) has `max-w-prose` or equivalent (~65ch) to prevent unreadable 1440px-wide lines.
- [ ] **Truncation without overflow:** Text truncation uses `truncate` (with parent `min-w-0`) not fixed widths that break at different sizes.
- [ ] **Responsive heading hierarchy:** `h2` is visually distinct from `h1` at every breakpoint — not the same size on mobile due to scaling.

---

### 4. OVERFLOW & SCROLL

- [ ] **No horizontal scroll on any breakpoint:** At 375px, 390px, 768px, 1024px — zero horizontal scrollbar or overflow. Check with `overflow-x: hidden` audit.
- [ ] **Overflow sources found:** Wide tables, long URLs, code blocks, image grids, fixed-width elements. Each should have: `overflow-x-auto` wrapper, `word-break: break-word`, or `min-w-0`.
- [ ] **Scroll containers declared:** Any element with `overflow-y-auto` or `overflow-y-scroll` has an explicit height (`h-full`, `max-h-[...]`, or `flex-1`) so it doesn't collapse.
- [ ] **`min-w-0` on flex children:** Flex children that contain text or grids have `min-w-0` to prevent flex blowout.
- [ ] **Code blocks:** Fenced code blocks in readers/courses have `overflow-x-auto` — long lines scroll horizontally inside the block, not the page.
- [ ] **Sticky elements don't cause overflow:** Sticky sidebars, nav bars, and CTAs do not cause horizontal overflow on mobile.

---

### 5. IMAGES & MEDIA

- [ ] **Next.js `<Image>` usage:** All images use `next/image` `<Image>` component, not raw `<img>` tags. This enforces responsive sizing automatically.
- [ ] **`sizes` prop set correctly:** `<Image>` has a `sizes` prop matching its responsive behavior (e.g., `sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"`). Missing `sizes` defaults to `100vw`, which wastes bandwidth on mobile.
- [ ] **No fixed-width images that overflow:** Images never have `w-[600px]` or similar fixed widths without `max-w-full`.
- [ ] **Aspect ratio preservation:** Images that need to preserve aspect ratio use `aspect-ratio` utilities (`aspect-video`, `aspect-square`) not fixed `h-[xxx]` that crop or distort.
- [ ] **Hero images fill correctly:** Hero/banner images use `object-cover` with `w-full` and an explicit height tier (`h-64 sm:h-80 md:h-[500px]`).
- [ ] **Video embeds are responsive:** Any `<iframe>` or video embed is wrapped in a responsive container (`aspect-video w-full`) — never fixed `width="560" height="315"`.
- [ ] **Avatar/icon images:** Small circular images use `rounded-full`, explicit `w-` and `h-`, never scale up beyond their intrinsic size.

---

### 6. NAVIGATION & HEADER

- [ ] **Mobile nav present:** The site has a mobile navigation mechanism — either a hamburger menu, bottom nav (`BottomNav`), or slide-out drawer. There is no desktop-only navigation.
- [ ] **Header height accounted for:** Page content top-padding or scroll offset accounts for the sticky header height at each breakpoint. No content hidden behind the nav.
- [ ] **Bottom nav safe area:** `BottomNav` applies `pb-[env(safe-area-inset-bottom)]` or equivalent for iPhone home-indicator clearance.
- [ ] **Nav items readable on mobile:** Nav links are readable at 375px, not truncated or overlapping.
- [ ] **Dropdown/mega-menus collapse on mobile:** Any mega-menu (like `NavPathwaysMega`) is off-canvas or a full-screen overlay on mobile, not a hover-dependent dropdown.
- [ ] **Logo scales correctly:** Header logo doesn't overflow on 320px devices. Uses `h-8` or fluid sizing.
- [ ] **CTA buttons in header:** "Sign in", "Get started" buttons in header collapse gracefully — either hidden on mobile (if bottom nav provides the CTA) or reduced to icon/short label.

---

### 7. TOUCH TARGETS & INTERACTION

- [ ] **Minimum tap target 44×44px:** Every button, link, icon button, and interactive element meets Apple/WCAG minimum of 44×44px. Common failures: icon-only buttons (`p-2` with 16px icon = 32px tap target), inline text links in dense lists.
- [ ] **Spacing between adjacent targets:** Minimum 8px between two adjacent interactive elements. Back-to-back small buttons with no gap cause mis-taps.
- [ ] **No hover-only interactions:** Tooltips, action menus, and reveal patterns that only appear on `:hover` must have a tap/long-press or always-visible equivalent on touch.
- [ ] **Swipe gestures are supplemental:** Any swipe gesture (carousel, drawer) also has a visible tap control (arrows, buttons). Swipe alone is not discoverable.
- [ ] **Carousels/sliders:** Carousel has visible prev/next buttons AND touch/swipe support. Auto-play is paused on hover/focus/touch.

---

### 8. SPACING & DENSITY

- [ ] **Consistent padding scale:** Sections use the project's spacing scale (`py-12 md:py-16 lg:py-24`) not arbitrary values. Mobile sections are not over-padded (wasting scarce vertical space) or under-padded (feeling cramped).
- [ ] **Card content density:** Cards have enough internal padding at all breakpoints (`p-4 md:p-6`). Content doesn't touch card edges on mobile.
- [ ] **No fixed heights that clip content:** `h-[xxx]` on text containers can clip content at smaller breakpoints or when text reflows. Prefer `min-h-[xxx]`.
- [ ] **Readable vertical rhythm:** On mobile, section headings, body copy, and CTAs have breathing room between them — minimum 16px gaps in the flow.

---

### 9. DARK/LIGHT MODE × RESPONSIVE

These two dimensions interact — a dark-mode fix can break layout if it uses `dark:block hidden` patterns incorrectly.

- [ ] **No `dark:` class that changes layout:** `dark:hidden`, `dark:block`, `dark:flex` should never be used to swap layout elements. Dark mode changes color, not structure.
- [ ] **Responsive visibility helpers use the right prefix order:** `hidden md:block` not `md:block hidden` (Tailwind applies classes left to right, but both work — just confirm intent matches output).
- [ ] **Responsive + dark combo classes:** Classes like `dark:md:flex` are valid but easy to misread. Confirm intent is correct for each breakpoint.

---

### 10. PLATFORM-SPECIFIC PATTERNS

Checks specific to this Next.js + shadcn platform's conventions:

- [ ] **`Sheet` for mobile drawers:** Mobile off-canvas patterns use shadcn `Sheet` not custom drawer implementations.
- [ ] **`Dialog` for mobile modals:** Modal overlays use shadcn `Dialog` which handles focus trap and scroll lock correctly across devices.
- [ ] **`ScrollArea` for bounded scroll regions:** Bounded scroll areas (sidebars, dropdowns) use shadcn `ScrollArea` for consistent cross-browser scroll behavior.
- [ ] **Server Component layout stability:** Server Component pages don't cause layout shift because client components below them haven't hydrated yet. Check for `min-h-[xxx]` skeletons on async content.
- [ ] **Next.js Image priority on LCP:** The above-the-fold hero image has `priority` on the `<Image>` component to avoid LCP regression on mobile.
- [ ] **No `useSearchParams` in layouts:** `useSearchParams` in layouts forces client-side rendering of the whole tree — check that params are read in leaf client components only.
- [ ] **`viewport` meta tag:** Confirm `<meta name="viewport" content="width=device-width, initial-scale=1">` is set in root layout. Without it, mobile browsers zoom out and breakpoints don't fire correctly.

---

## Audit Process

### Step 1 — Read
Read every file in scope (page, layout, all child components). Note any file you cannot access.

### Step 2 — Static Analysis
Work through all 10 dimensions against the source code. Record each issue with:
- Dimension number
- Severity: **CRITICAL** (broken/unusable at some breakpoint) | **HIGH** (significant UX degradation) | **MEDIUM** (best practice violation, not broken) | **LOW** (polish/optimization)
- File path and line number
- Offending code snippet
- Specific fix

### Step 3 — Visual Verification (if Chrome DevTools MCP available)
If the dev server is running, use the Chrome DevTools MCP to verify visually:

```
1. Navigate to the target page
2. Emulate iPhone SE (375×667)    → screenshot → check for overflow/overlap
3. Emulate iPhone 14 (390×844)   → screenshot → check key interactions
4. Emulate iPad (768×1024)        → screenshot → check column collapse
5. Emulate desktop (1280×800)     → screenshot → check full layout
6. Emulate iPhone 14 landscape (844×390) → screenshot → check vertical space
```

Check each screenshot for:
- Horizontal scrollbar present
- Content cut off by edges
- Text too small to read
- Overlapping elements
- Missing navigation
- Broken images

### Step 4 — Fix
Fix issues in order: CRITICAL → HIGH → MEDIUM → LOW.

**Fixing rules:**
1. Always read a file before editing it.
2. Fix at the correct layer — if a grid needs to change, fix the grid, not a parent's overflow.
3. Use Tailwind responsive prefixes, not arbitrary CSS in `globals.css`, unless the fix is structural and applies globally.
4. Never add `!important` to fix a responsive issue — trace the conflicting specificity and fix it properly.
5. Preserve both dark and light mode after every edit.
6. Do not refactor surrounding code — surgical fixes only.
7. After fixing a CRITICAL issue, re-screenshot that breakpoint to confirm.

### Step 5 — Report

Output the full audit report before fixing, then list files modified.

---

## Output Format

```
## Responsiveness Audit: [target]

### Summary
- Files audited: X
- Breakpoints tested: 375px, 768px, 1024px, 1280px
- Issues found: X (Critical: X, High: X, Medium: X, Low: X)
- Auto-fixed: X | Manual review needed: X

### Dimension Scores
| # | Dimension | Score | Issues |
|---|-----------|-------|--------|
| 1 | Mobile-First Architecture | PASS / PARTIAL / FAIL | X |
| 2 | Grid & Flexbox Collapse | PASS / PARTIAL / FAIL | X |
| 3 | Typography Scaling | PASS / PARTIAL / FAIL | X |
| 4 | Overflow & Scroll | PASS / PARTIAL / FAIL | X |
| 5 | Images & Media | PASS / PARTIAL / FAIL | X |
| 6 | Navigation & Header | PASS / PARTIAL / FAIL | X |
| 7 | Touch Targets & Interaction | PASS / PARTIAL / FAIL | X |
| 8 | Spacing & Density | PASS / PARTIAL / FAIL | X |
| 9 | Dark/Light Mode × Responsive | PASS / PARTIAL / FAIL | X |
| 10 | Platform-Specific Patterns | PASS / PARTIAL / FAIL | X |

### Issues Found

#### CRITICAL
1. [DIMENSION #] — description — [file:line](file:line)
   Evidence: `offending code`
   Fix: specific code change

#### HIGH
...

#### MEDIUM
...

#### LOW
...

### Passing Dimensions
- [#] DIMENSION — what's working well

### Files Modified
- path/to/file.tsx — X fixes applied
  - Fix 1: description (line N)
  - Fix 2: description (line N)
```

---

## Common Quick Fixes Reference

| Pattern | Problem | Fix |
|---|---|---|
| `grid-cols-3` | No mobile base | → `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3` |
| `flex` row with no wrap | Overflow at 375px | → `flex-col sm:flex-row` or add `flex-wrap` |
| `text-6xl` (bare) | Too large on mobile | → `text-3xl sm:text-4xl lg:text-6xl` |
| `px-20` (bare) | No mobile padding | → `px-4 sm:px-8 lg:px-20` |
| `w-[600px]` on image | Overflow on mobile | → `w-full max-w-[600px]` |
| `<img src=...>` | No responsive sizing | → `<Image ... sizes="..." fill />` |
| `h-[500px]` on text box | Clips content | → `min-h-[500px]` |
| `p-2` icon button | 32px tap target | → `p-3` (48px) or `size-11` |
| `gap-12` (bare) | Too wide gap on mobile | → `gap-6 md:gap-12` |
| `max-w-[1400px]` no mx-auto | Sticks to edge | → add `mx-auto` |
| `hidden sm:block` sibling `sm:hidden` | Correct pattern | ✓ no change |
| `max-sm:hidden` | Desktop-first | → `hidden sm:block` |
| `iframe width="560"` | Fixed-width video | → wrap with `<div class="aspect-video w-full"><iframe ... class="w-full h-full" /></div>` |
| `text-sm` on `<input>` | iOS zoom on focus | → `text-base` |
| missing `sizes` on `<Image>` | Downloads 1x image at full resolution | → `sizes="(max-width: 768px) 100vw, 50vw"` |
