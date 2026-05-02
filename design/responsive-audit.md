
Audit and fix responsiveness across the specified section or page(s).

Target: $ARGUMENTS

If no target is provided, audit the homepage and its constituent sections.

## Before Starting

1. Read the target file(s) — include any layout files wrapping the page.
2. Read navigation components — nav behavior drives the viewport offset at every breakpoint.
3. Read the global CSS file — note any custom responsive CSS, viewport offsets, container widths, and safe-area handling.
4. Read the Tailwind config — confirm the breakpoint scale in use.
5. Identify all component files rendered by the target — read them too.

## Breakpoint Reference

Standard **Tailwind default breakpoint scale** (mobile-first):

| Breakpoint | Min-width | Device context |
|---|---|---|
| (base) | 0px | Phones portrait (320-479px) |
| `xs` | 475px | Large phones (if configured) |
| `sm` | 640px | Phones landscape / small tablets |
| `md` | 768px | Tablets portrait |
| `lg` | 1024px | Tablets landscape / small laptops |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Wide desktop |

**Primary test widths:** 375px (iPhone SE), 390px (iPhone 14), 430px (iPhone 14 Pro Max), 768px (iPad), 1024px (iPad landscape), 1280px (desktop), 1440px (wide desktop).

## Audit Checklist

Work through all 13 dimensions. For every issue record: file, line number, offending code, severity, and the concrete fix.

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
- [ ] **Sidebar patterns:** Any sidebar (nav drawer, filter panel) is off-canvas or collapsed on mobile. No fixed-width sidebars that push content off screen.
- [ ] **Two-column to one-column:** Every two-column layout (`grid-cols-2`, `flex` row) collapses to single column on mobile.
- [ ] **Card grids:** Card grids have a sensible minimum card width (`min-w-0` to allow shrinking, or `grid-cols-1 sm:grid-cols-2`).
- [ ] **`min-w-0` on flex children:** Flex children that contain text, truncated labels, or nested grids must have `min-w-0` to prevent flex blowout. This is the #1 cause of "it looks fine at 768px but breaks at 375px" bugs.

---

### 3. TYPOGRAPHY SCALING

- [ ] **Heading scale uses 3+ breakpoints:** `h1` / hero headings use at least a three-step scale — `text-3xl sm:text-4xl lg:text-5xl xl:text-6xl`. Two-step jumps (e.g., `text-lg sm:text-2xl`) are too aggressive when the breakpoint gap is wide.
- [ ] **Body text minimum 16px:** Body text is **minimum 16px** on mobile (maps to `text-base`). `text-sm` (14px) is acceptable for labels, metadata, captions only.
- [ ] **No iOS auto-zoom on form controls:** Any `<input>`, `<textarea>`, `<select>`, or custom dropdown trigger has `text-base` (16px) minimum font size. iOS Safari auto-zooms the page on focus for anything below 16px — this is the single most common mobile form bug.
- [ ] **Line length control:** Long-form prose has `max-w-prose` or equivalent (~65ch) to prevent unreadable 1440px-wide lines.
- [ ] **Truncation without overflow:** Text truncation uses `truncate` (with parent `min-w-0`) not fixed widths that break at different sizes.
- [ ] **Responsive heading hierarchy:** `h2` is visually distinct from `h1` at every breakpoint — not the same size on mobile due to scaling.
- [ ] **`text-wrap: balance` on headings:** Short headings (1–3 lines) benefit from `text-wrap: balance` to prevent orphan words. Supported in all modern browsers.

---

### 4. OVERFLOW & SCROLL

- [ ] **No horizontal scroll on any breakpoint:** At 375px, 390px, 768px, 1024px — zero horizontal scrollbar or overflow. Check with `overflow-x: hidden` audit.
- [ ] **Overflow sources found:** Wide tables, long URLs, code blocks, image grids, fixed-width elements. Each should have: `overflow-x-auto` wrapper, `word-break: break-word`, or `min-w-0`.
- [ ] **Scroll containers declared:** Any element with `overflow-y-auto` or `overflow-y-scroll` has an explicit height (`h-full`, `max-h-[...]`, or `flex-1`) so it doesn't collapse to zero.
- [ ] **Code blocks:** Fenced code blocks have `overflow-x-auto` — long lines scroll horizontally inside the block, not the page.
- [ ] **Sticky elements don't cause overflow:** Sticky sidebars, nav bars, and CTAs do not cause horizontal overflow on mobile.
- [ ] **`overscroll-contain` on nested scroll regions:** Dropdowns, modals, sidebars, and any scroll container nested inside the page must use `overscroll-behavior: contain` (Tailwind: `overscroll-contain`) to prevent scroll chaining — where scrolling to the bottom of a dropdown also scrolls the page behind it.

---

### 5. IMAGES & MEDIA

- [ ] **Responsive image component usage:** All images use the framework's optimized image component (e.g., `next/image`), not raw `<img>` tags.
- [ ] **`sizes` prop set correctly:** Image components have a `sizes` prop matching their responsive behavior (e.g., `sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"`).
- [ ] **No fixed-width images that overflow:** Images never have `w-[600px]` or similar fixed widths without `max-w-full`.
- [ ] **Aspect ratio preservation:** Images that need to preserve aspect ratio use `aspect-ratio` utilities (`aspect-video`, `aspect-square`) not fixed `h-[xxx]` that crop or distort.
- [ ] **Hero images fill correctly:** Hero/banner images use `object-cover` with `w-full` and an explicit height tier (`h-64 sm:h-80 md:h-[500px]`).
- [ ] **Video embeds are responsive:** Any `<iframe>` or video embed is wrapped in a responsive container (`aspect-video w-full`) — never fixed `width="560" height="315"`.
- [ ] **Avatar/icon images:** Small circular images use `rounded-full`, explicit `w-` and `h-`, never scale up beyond their intrinsic size.

---

### 6. NAVIGATION & HEADER

- [ ] **Mobile nav present:** The site has a mobile navigation mechanism — either a hamburger menu, bottom nav, or slide-out drawer. There is no desktop-only navigation.
- [ ] **Header height accounted for:** Page content top-padding or scroll offset accounts for the sticky header height at each breakpoint. No content hidden behind the nav.
- [ ] **Safe area insets on fixed bars:** Any fixed bottom element applies `pb-[env(safe-area-inset-bottom)]` for iPhone home-indicator clearance. Top elements account for `env(safe-area-inset-top)` on notched devices in landscape.
- [ ] **Nav items readable on mobile:** Nav links are readable at 375px, not truncated or overlapping.
- [ ] **Dropdown/mega-menus collapse on mobile:** Any mega-menu is off-canvas or a full-screen overlay on mobile, not a hover-dependent dropdown.
- [ ] **Logo scales correctly:** Header logo doesn't overflow on 320px devices. Uses fluid sizing that respects the header height constraint.
- [ ] **CTA buttons in header:** Action buttons in header collapse gracefully — either hidden on mobile (if bottom nav provides the CTA) or reduced to icon/short label.

---

### 7. TOUCH TARGETS & INTERACTION

- [ ] **Minimum tap target 44×44px:** Every button, link, icon button, and interactive element meets Apple/WCAG minimum of 44×44px. Common failures: icon-only buttons (`p-2` with 16px icon = 32px tap target), inline text links in dense lists. Use `min-h-11 min-w-11` (44px) as the floor.
- [ ] **Spacing between adjacent targets:** Minimum 8px between two adjacent interactive elements. Back-to-back small buttons with no gap cause mis-taps.
- [ ] **No hover-only interactions:** Tooltips, action menus, and reveal patterns that only appear on `:hover` must have a tap/long-press or always-visible equivalent on touch.
- [ ] **Touch feedback on mobile:** Interactive elements have `active:` states (e.g., `active:bg-secondary/70`) for immediate touch feedback. Desktop `:hover` states are invisible on touch devices.
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

- [ ] **No `dark:` class that changes layout:** `dark:hidden`, `dark:block`, `dark:flex` should never be used to swap layout elements. Dark mode changes color, not structure. Exception: swapping light/dark logo images with `dark:hidden` / `hidden dark:block` is correct.
- [ ] **Responsive visibility helpers use the right prefix order:** `hidden md:block` not `md:block hidden` (Tailwind applies classes left to right, but both work — just confirm intent matches output).
- [ ] **Responsive + dark combo classes:** Classes like `dark:md:flex` are valid but easy to misread. Confirm intent is correct for each breakpoint.

---

### 10. VIEWPORT UNITS & FIXED POSITIONING

Modern mobile browsers have dynamic toolbars that change the viewport height. This dimension catches the most common "works on desktop, broken on phone" bugs.

- [ ] **No raw `h-screen` for full-height layouts:** `h-screen` uses `100vh` which does NOT account for the mobile browser's URL bar. Use `h-dvh` (dynamic viewport height) or `min-h-dvh` instead.
- [ ] **Fixed bottom elements + virtual keyboard:** When a `position: fixed; bottom: 0` element contains an `<input>` or `<textarea>`, the virtual keyboard on iOS/Android pushes it up. If the element is tall, it can cover the entire viewport. Solutions: use `position: sticky` instead, use `visualViewport` API to detect keyboard, or restructure so inputs are in the scrollable flow rather than a fixed bar.
- [ ] **Dropdown direction on fixed bottom bars:** Dropdowns/selects inside fixed bottom bars must open **upward** (`bottom-full`) not downward, or they'll render off-screen below the viewport.
- [ ] **Viewport-relative max-heights:** Dropdown menus and popovers should use `max-h-[min(16rem,50vh)]` or similar viewport-capped values instead of fixed `max-h-64` — a fixed max-height that fits on desktop can exceed the visible area on a 667px phone.

---

### 11. PERFORMANCE ON MOBILE

Mobile devices have less GPU/CPU. Some CSS patterns that render smoothly on desktop cause jank on phones.

- [ ] **`backdrop-filter` used sparingly:** `backdrop-blur-xl`, `backdrop-blur-2xl` cause GPU strain on low-end Android. If used on large areas (full-width nav, modals), test on a mid-range device. Consider falling back to a solid `bg-background/95` on mobile if performance is an issue.
- [ ] **No `will-change` without cleanup:** `will-change: transform` on many elements simultaneously consumes GPU memory. Only add it to elements that are actively animating.
- [ ] **Animations pause off-screen:** Scroll-triggered animations should not run when the section is off-screen. Use Intersection Observer or equivalent scroll-trigger with toggle/cleanup.
- [ ] **`prefers-reduced-motion` respected:** Users who set "Reduce Motion" in OS settings should see reduced or no animations. Check that animations and CSS transitions have a `prefers-reduced-motion: reduce` fallback — at minimum, `motion-safe:` prefix on Tailwind animation classes.

---

### 12. LANDSCAPE ORIENTATION

Phone landscape (844×390 or shorter) is the most neglected breakpoint. Users rotate phones for video, forms, and reading.

- [ ] **Fixed bars don't consume >30% of landscape height:** A fixed header (56px) + fixed bottom bar (80px+) on a 390px-tall viewport leaves <250px for content. Check that fixed elements are compact or auto-hide in landscape.
- [ ] **Full-height sections don't force scroll:** A section with `min-h-screen` or `h-dvh` in landscape forces the user to scroll past a mostly-empty section. Use `min-h-[50vh]` or content-driven height for non-hero sections.
- [ ] **Forms are usable in landscape:** Form inputs + virtual keyboard in landscape leave almost no visible content. Long forms should scroll naturally, not be in fixed/sticky containers.

---

### 13. PLATFORM-SPECIFIC PATTERNS

Checks specific to the project's framework and component library conventions:

- [ ] **Sheet for mobile drawers:** Mobile off-canvas patterns use the component library's sheet/drawer component, not custom implementations.
- [ ] **Dialog for mobile modals:** Modal overlays use the component library's dialog which handles focus trap and scroll lock correctly across devices.
- [ ] **ScrollArea for bounded scroll regions:** Bounded scroll areas (sidebars, dropdowns) use a dedicated scroll area component for consistent cross-browser behavior.
- [ ] **Server Component layout stability:** Server Component pages don't cause layout shift because client components below them haven't hydrated yet. Check for `min-h-[xxx]` skeletons on async content.
- [ ] **Priority on LCP images:** The above-the-fold hero image has `priority` on the image component to avoid LCP regression on mobile.
- [ ] **`viewport` meta tag:** Confirm `<meta name="viewport" content="width=device-width, initial-scale=1">` is set in root layout. Without it, mobile browsers zoom out and breakpoints don't fire correctly.

---

## Audit Process

### Step 1 — Read
Read every file in scope (page, layout, all child components). Note any file you cannot access.

### Step 2 — Static Analysis
Work through all 13 dimensions against the source code. Record each issue with:
- Dimension number
- Severity: **CRITICAL** (broken/unusable at some breakpoint) | **HIGH** (significant UX degradation) | **MEDIUM** (best practice violation, not broken) | **LOW** (polish/optimization)
- File path and line number
- Offending code snippet
- Specific fix

### Step 3 — Visual Verification (if browser DevTools available)
If the dev server is running, use browser DevTools to verify visually:

```
1. Navigate to the target page
2. Emulate iPhone SE (375×667)    → screenshot → check for overflow/overlap
3. Emulate iPhone 14 (390×844)   → screenshot → check key interactions
4. Emulate iPad (768×1024)        → screenshot → check column collapse
5. Emulate desktop (1280×800)     → screenshot → check full layout
6. Emulate iPhone 14 landscape (844×390) → screenshot → check vertical space
7. Emulate Galaxy S21 (360×800)   → screenshot → check narrow Android
```

Check each screenshot for:
- Horizontal scrollbar present
- Content cut off by edges
- Text too small to read
- Overlapping elements
- Missing navigation
- Broken images
- Fixed elements consuming too much vertical space

### Step 4 — Fix
Fix issues in order: CRITICAL → HIGH → MEDIUM → LOW.

**Fixing rules:**
1. Always read a file before editing it.
2. Fix at the correct layer — if a grid needs to change, fix the grid, not a parent's overflow.
3. Use Tailwind responsive prefixes, not arbitrary CSS in global stylesheets, unless the fix is structural and applies globally.
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
| 10 | Viewport Units & Fixed Positioning | PASS / PARTIAL / FAIL | X |
| 11 | Performance on Mobile | PASS / PARTIAL / FAIL | X |
| 12 | Landscape Orientation | PASS / PARTIAL / FAIL | X |
| 13 | Platform-Specific Patterns | PASS / PARTIAL / FAIL | X |

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
| `text-lg sm:text-2xl` | Two-step jump too aggressive | → `text-base sm:text-lg md:text-2xl` |
| `px-20` (bare) | No mobile padding | → `px-4 sm:px-8 lg:px-20` |
| `w-[600px]` on image | Overflow on mobile | → `w-full max-w-[600px]` |
| `<img src=...>` | No responsive sizing | → Use framework image component with `sizes` prop |
| `h-[500px]` on text box | Clips content | → `min-h-[500px]` |
| `p-2` icon button | 32px tap target | → `p-3` (48px) or `min-h-11 min-w-11` |
| `gap-12` (bare) | Too wide gap on mobile | → `gap-6 md:gap-12` |
| `max-w-[1400px]` no mx-auto | Sticks to edge | → add `mx-auto` |
| `max-sm:hidden` | Desktop-first | → `hidden sm:block` |
| `iframe width="560"` | Fixed-width video | → wrap with `aspect-video w-full` container |
| `text-sm` on `<input>` | iOS zoom on focus | → `text-base` (also `<select>`, `<textarea>`) |
| `text-sm` on `<select>` | iOS zoom on focus | → `text-base` (most-missed variant) |
| missing `sizes` on image | Downloads full-res | → `sizes="(max-width: 768px) 100vw, 50vw"` |
| `h-screen` | Ignores mobile URL bar | → `h-dvh` or `min-h-dvh` |
| `h-[100vh]` | Same issue as `h-screen` | → `h-dvh` |
| `max-h-64` on dropdown | Exceeds small viewport | → `max-h-[min(16rem,50vh)]` |
| No `overscroll-contain` | Scroll chaining in dropdowns | → add `overscroll-contain` to scroll container |
| No `active:` state | No touch feedback on mobile | → add `active:bg-secondary/70` or similar |
| `bottom-0` fixed + input | Keyboard pushes bar up | → use `sticky` or move input to scroll flow |
| No `min-w-0` on flex child | Text overflows flex parent | → add `min-w-0` to the flex child |
