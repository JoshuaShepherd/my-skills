# ZenWrite Design Chain (portable reference)

This mirrors `docs/design/` in the ZenWrite repo. **When that folder exists in the
working repo, read it — it is the live source of truth.** This file is the fallback
so the skill works outside the repo and gives you the chain at a glance.

Chain order (always reason in this order): **Tokens → Primitives → Components → Built Components → Patterns**.

## Table of contents
- [Philosophy](#philosophy)
- [Layer 1 — Tokens](#layer-1--tokens)
- [Layer 2 — Primitives](#layer-2--primitives)
- [Layer 3 — Components](#layer-3--components)
- [Layer 4 — Built components](#layer-4--built-components)
- [Layer 5 — Patterns & layouts](#layer-5--patterns--layouts)
- [Anti-patterns](#anti-patterns)

---

## Philosophy

ZenWrite is a **light-primary, distraction-free scholarly writing sanctuary**. The
manuscript is the hero; chrome fades when the user types. Four load-bearing rules:

1. **Minimize cognitive load** — secondary chrome fades on typing (`duration-700` idle fade).
2. **Two spheres, kept separate** — Content Workspaces (violet) vs Scholarly Community (sky/emerald/rose).
3. **Deliberate type pairing** — Newsreader serif for literary body/titles; Inter/Manrope for functional UI.
4. **Never let OS dark mode hijack the UI** — `dark:` applies only under an explicit `.dark` ancestor.

**Stack:** React 19 · Vite 6 · Tailwind CSS v4 (CSS-first `@theme`, no `tailwind.config`) ·
`lucide-react` (line icons) + Material Symbols Outlined (filled) · `recharts` · `motion`.
All UI lives flat in `src/components/`.

---

## Layer 1 — Tokens

Source of truth: `src/index.css` `@theme` block. **Never** hardcode hex in components
(`bg-[#14006a]` is a violation → `bg-brand-violet`).

### Typography
| Utility | Font | Usage |
|---------|------|-------|
| `font-serif` | Newsreader | Body, titles, literary headings, empty states |
| `font-sans` | Inter | General UI, editor chrome labels |
| `font-manrope` | Manrope | Eyebrows, uppercase labels, chips, metrics |

Cadence idioms:
- Literary headings: `font-serif font-light italic tracking-tight`
- Functional eyebrows: `font-manrope text-[10px] font-extrabold uppercase tracking-[0.25em]`
- Chip labels: `text-[9px] font-manrope font-bold uppercase tracking-wider`

### Color tokens
```css
@theme {
  --font-serif: "Newsreader", serif;
  --font-sans: "Inter", sans-serif;
  --font-manrope: "Manrope", sans-serif;

  --color-brand-violet: #14006a;   /* primary content accent, borders, focus rings */
  --color-brand-sand: #fed488;     /* warm highlight, sparingly */
  --color-brand-lavender: #f0edff; /* soft violet wash backgrounds, scheduled chips */

  --color-workspace-bg-paper: #f4f4f1;  --color-workspace-text-paper: #1a1a1a;
  --color-workspace-bg-sepia: #eae8e3;  --color-workspace-text-sepia: #2c2b29;
  --color-workspace-bg-ink:   #14141b;  --color-workspace-text-ink:   #e2e2e8;

  --color-community-sky: #0ea5e9;      /* Engage */
  --color-community-emerald: #10b981;  /* Manage */
  --color-community-rose: #f43f5e;     /* Analyze */
}
```

**Dual spheres:**
| Sphere | Views | Accent | Token classes |
|--------|-------|--------|---------------|
| Content | Create, Edit, Organize | Brand violet | `text-brand-violet`, `bg-brand-lavender`, `border-brand-violet/10` |
| Community | Engage / Manage / Analyze | Sky / Emerald / Rose | `text-community-sky` / `-emerald` / `-rose` (or `text-sky-700` etc.) |

**Editor themes** (from `EditorSettings.theme`): `paper | sepia | ink` map to
`bg-workspace-bg-* text-workspace-text-*`. Caret: ink → light `#ECECF0`; paper/sepia → violet; prefer `caret-current`.

**Dark mode:** `@custom-variant dark (&:where(.dark, .dark *))`. Use `dark:text-indigo-300`
when brand-violet fails contrast on dark surfaces. No global `prefers-color-scheme`.

### Token hygiene
1. Add tokens to `@theme` only, with semantic prefixes (`brand-`, `workspace-`, `community-`).
2. Never assemble dynamic color strings (`bg-${c}-500`) — Tailwind purges them. Use static maps.
3. Verify WCAG: 4.5:1 small text, 3:1 UI controls / large text.

---

## Layer 2 — Primitives

Smallest reusable atoms. Rule: **copy a Tailwind string three times → extract a primitive first.**

| File | Export | Role |
|------|--------|------|
| `StatusChip.tsx` | default | Color-coded status pill (static color map, purge-safe) |
| `VoiceFidelityChip.tsx` | default | AI voice score chip |
| `StateLayouts.tsx` | `LoadingState`, `EmptyState`, `ErrorState` | Async UI states |
| `BottomNav.tsx` | default | Fixed editor bottom chrome |

- **StatusChip** shape: `inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-manrope font-bold uppercase tracking-wider border` + a static status→classes map (published=emerald, draft=stone, in-review=amber, scheduled=brand-lavender/brand-violet).
- **StateLayouts**: containers `rounded-2xl p-16`, violet family for loading/empty, **rose** family for error. Titles `font-serif`.
- Primitive rules: tokens only (no hex); no data fetching (props + local UI state only);
  `focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none`; `dark:` only under `.dark`.

Missing primitives (extract only on 2nd–3rd consumer — avoid premature abstraction):
Button variant map, IconButton, SlideInPanel, Modal, SearchField, ActionTile.

---

## Layer 3 — Components

Focused composed UI (panels, palettes, wizards). Import primitives; props down / events up.
Panel titles are **always** `font-serif text-lg font-light italic text-brand-violet`.

**Slide-in right panel shell** (shared by MetadataPanel, AcademicPanel, RevisionPanel, TeleprompterPanel):
```tsx
<div className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40" onClick={onClose} />
<aside className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white border-l border-brand-violet/10 shadow-2xl z-50 flex flex-col animate-in slide-in-from-right duration-300">
  <header className="flex items-center justify-between px-6 py-4 border-b border-brand-violet/5">
    <h2 className="font-serif text-lg font-light italic text-brand-violet">Panel Title</h2>
    <button className="… focus-visible:ring-2 focus-visible:ring-brand-violet">Close</button>
  </header>
  <div className="flex-1 overflow-y-auto p-6">{/* content */}</div>
</aside>
```

**Full-screen wizard** (CourseCreateWizard, SettingsModal): centered
`fixed inset-0 z-50 flex items-center justify-center` + `bg-black/50 backdrop-blur-sm` backdrop +
`bg-white rounded-2xl shadow-2xl max-w-lg border border-brand-violet/10 animate-in zoom-in-95`.

**Command palette (⌘K):** backdrop `bg-black/40 backdrop-blur-sm`; panel `rounded-2xl shadow-2xl border border-brand-violet/10`; active result `bg-brand-lavender text-brand-violet`; key hints `font-mono text-[10px] bg-stone-100 rounded px-1.5`.

---

## Layer 4 — Built components

Full screens (orchestrate components + hooks + app state). One screen, one file. Wired in `App.tsx`.

| File | View | Sphere |
|------|------|--------|
| `HomeScreen.tsx` | home | both (dual-sphere tiles) |
| `Editor.tsx` | create/edit | content (hero canvas) |
| `MediaSurface.tsx` | create (video/podcast) | content |
| `OrganizeScreen.tsx` | organize | content |
| `EngageScreen.tsx` | engage | community (sky) |
| `ManageScreen.tsx` | manage | community (emerald) |
| `AnalyzeScreen.tsx` / `AnalyticsView.tsx` | analyze | community (rose) |
| `PublishPanel.tsx` | overlay | content |

**Home tile pattern:**
```tsx
<button className="group w-full flex items-center gap-4 p-5 bg-white border border-brand-violet/10 rounded-2xl shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md focus-visible:ring-2 focus-visible:ring-brand-violet {sphereHover}">
  <span className="p-3 rounded-xl bg-brand-violet/5 {accent}">{icon}</span>
  <div>
    <h4 className="font-serif text-lg font-light">{label}</h4>
    <p className="text-xs text-stone-500 font-serif">{desc}</p>
  </div>
  <ChevronRight className="ml-auto opacity-0 group-hover:opacity-100" />
</button>
```
Sphere accent/hover map: content → `text-brand-violet` / `hover:bg-brand-violet/[0.04] hover:border-brand-violet/25`;
engage → `text-sky-700` / `hover:bg-sky-500/[0.06]`; manage → emerald; analyze → rose.

**Built rules:** respect sphere separation (don't merge Engage/Manage); keep slide-ins as
separate components (built screens only toggle visibility); lazy-load heavy charts.

---

## Layer 5 — Patterns & layouts

**App shell:** `min-h-screen bg-white flex flex-col` → conditional NavigationAxis →
`<main className="flex-1 relative">` → overlays.

**Centered page:** `max-w-7xl mx-auto px-6 py-8`; `space-y-8` between sections, `space-y-3` in lists.
Section header: `font-serif text-2xl font-light italic text-brand-violet tracking-tight`.

**Idle fade:** on typing, `App.tsx` sets idle → NavigationAxis wrapper gets
`opacity-0 select-none pointer-events-none -translate-y-2` at `duration-700`. NavigationAxis is hidden on `home`.

**Z-index stack:** backdrop `z-40` · slide-in panel `z-50` · PublishPanel `z-[60]` · CommandPalette `z-[70]`.

**Async state pattern:**
```tsx
{loading && <LoadingState />}
{error && <ErrorState message={error} />}
{!loading && !error && items.length === 0 && <EmptyState />}
{!loading && items.map(…)}
```

**Card taxonomy** (every manuscript/list card): pencil (inline title edit) · trash (two-step
confirm) · dropdown (format/status selector).

**Motion tokens:** enter `animate-in fade-in duration-300`; slide `slide-in-from-right`;
zoom `zoom-in-95`; hover lift `hover:-translate-y-0.5 hover:shadow-md`; transitions `duration-200`
(hover) / `duration-700` (idle fade).

**Responsive:** mobile → single-column home, spine collapses, bottom nav primary;
`md+` → dual-column home, spine visible in book mode; wide → `max-w-7xl` cap.

**Radius/spacing conventions:** cards `rounded-2xl`; icon wells `rounded-xl`; default content
border `border-brand-violet/10`; page pad `px-6 py-8`, tiles `p-5`, states `p-16`.

---

## Anti-patterns

- Global `prefers-color-scheme` dark mode (use scoped `.dark` only).
- Arbitrary hex in `className` (`bg-[#14006a]`) — use tokens.
- Dynamic Tailwind color concatenation (purged at build).
- Dense paragraph descriptions on home tiles (short `desc` + icon).
- Debug panels / port indicators / telemetry on production layouts.
- Navigation that hides the manuscript during editing.
- Ad-hoc status `<span>`s instead of `StatusChip`; ad-hoc loading/empty spinners instead of `StateLayouts`.
- Content-sphere violet used as the *primary* accent on community screens (and vice-versa).
