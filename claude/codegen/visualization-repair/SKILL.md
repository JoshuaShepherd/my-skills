---
name: visualization-repair
description: >
  Audit React/Next.js components for broken charts and diagrams (Stitch exports,
  invalid SVG, collapsed Recharts, wrong motion.svg props). Propose a replacement
  using Recharts, Mermaid, D3, GSAP, or plain React/SVG, then implement. Use when
  visualizations are missing, clipped, zero-height, off-center, or non-interactive
  when they should work; keywords: broken chart, stitch visualization, ResponsiveContainer,
  radar, network graph, SVG motion.
user-invocable: true
---

# Visualization repair (broken-first)

Use this skill when charts or diagrams **fail visibly** (not for pixel-polish on working graphics).

## 1. Triage: “broken” vs “fine”

Treat as **broken** (fix):

- Chart area has **zero or collapsed height** (Recharts `ResponsiveContainer` with `height="100%"` inside a flex parent with no resolved height).
- SVG **`motion.*` with invalid attributes** (e.g. `motion.circle` missing `cx`/`cy`, or `r` as string where a number is required).
- **`transform="translate(50%, 50%)"` (or similar)** on SVG `<g>` where percentages are unsupported or inconsistent across browsers—use `viewBox` + numeric `translate(cx, cy)`.
- **`motion.line`** using `pathLength` / dash animation in ways that Framer does not apply reliably to `<line>`—prefer `<path d="M...L...">` or opacity/scale, or plain SVG + GSAP `strokeDashoffset`.
- **Rotation** of SVG primitives without moving the transform origin to the shape center—wrap in `<g transform="translate(cx,cy)">` and draw at `(0,0)`, or use a non-SVG layer (e.g. bordered `div` with `animate-spin` and token colors).

Treat as **out of scope** unless requested:

- Subtle animation timing, exact chart junk removal, or redesign for aesthetics only.

## 2. Choose implementation (preference order)

1. **Recharts** — time series, bars, scatters, areas when data is tabular; always give the chart wrapper an explicit **`min-height` in px** (or fixed `height`) so `ResponsiveContainer` measures correctly.
2. **Plain React + SVG** — custom polygons, radars, simple networks; use **`viewBox`** and user coordinates; semantic CSS variables (`var(--primary)`), no hardcoded hex.
3. **GSAP** — scroll-driven or complex path reveals; keep `"use client"` at the leaf that uses `useGSAP`.
4. **Mermaid** — static flow/diagrams in MD or server-rendered docs; avoid heavy client bundles unless the page already needs it.
5. **D3** — only when layout math is non-trivial and Recharts cannot express it; isolate in a small hook/component.

Respect project rules: **design tokens only**, **no `src/components/ui/*` edits for styling**, **`"use client"` as deep as possible**.

## 3. Verification

- Resize the viewport: chart must not disappear or collapse.
- Keyboard/focus: interactive SVG nodes need visible focus or dialog patterns if clickable.
- Run `pnpm lint` and `pnpm typecheck` on touched files.

## 4. Repo sweep checklist (when asked to “run everywhere”)

- Grep: `ResponsiveContainer`, `<svg`, `motion.circle`, `motion.line`, `motion.path`, `preserveAspectRatio="none"` on prose charts, `translate(50%`.
- Grep: `hsl(var(--` in `*.tsx` — this repo’s `:root` tokens are **hex** (`--primary: #…`); `hsl(var(--primary))` is invalid. Use `var(--primary)` in SVG/CSS, or Tailwind semantic classes (`bg-primary-container`, `text-on-primary`, `shadow-[…_color-mix(…)]`) instead of `bg-[hsl(var(--…))]`.
- Open files that mix **flex + `h-full` + Recharts** first—highest failure rate.

## 5. Full inventory sweep (this codebase)

**`<svg` in `src/**/*.tsx` (12 files):** `impact/page`, `model/page`, `transformation/page`, `analytics/page`, `DigitalFootprintVisualizer`, `SceniusVisualization`, `intake-form` (spinner only), `reader-sidebar` (progress ring → use `FormationRing`), `FormationRing` + `ui/formation-ring`, `PodcastHero` (decorative bars), `sentry-example-page`.

**Recharts:** only `DigitalFootprintVisualizer.tsx` (must keep explicit `min-h-*` on chart parents).

**GSAP / ScrollTrigger:** `SceniusVisualization.tsx` only.

**No** canvas, Chart.js, Visx, Nivo in `src/`.

## Related skills

- `visualization-expert` — chart type selection when data shape is unclear.
- `tailwind-cleanup` — token violations next to chart styling.
- `animation` — GSAP polish after correctness is fixed.
