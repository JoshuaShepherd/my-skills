---
name: zenwrite-design-chain
description: Build new UI or audit/align existing UI for the ZenWrite scholarly-writing app — its light-primary, dual-sphere design system (Newsreader serif + Manrope, brand-violet content sphere, sky/emerald/rose community sphere) plus React 19 + Tailwind v4 and general web/a11y/responsive best practice. Use whenever creating, editing, reviewing, or "bringing into alignment" any ZenWrite component, panel, screen, or page — even when the user only says "build a component," "make this match our style," "audit this page," "clean up the styling," "check design consistency," or "flush drift." Both an auditor and a builder for the ZenWrite design chain (Tokens → Primitives → Components → Built → Patterns).
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ZenWrite Design Chain — Auditor & Builder

Build UI that looks like it was always part of ZenWrite, or pull existing UI back into
alignment. ZenWrite is a **light-primary, distraction-free scholarly writing sanctuary**:
the manuscript is the hero, chrome fades when typing, and the app is split into two
color spheres. Everything you produce must honor the chain **Tokens → Primitives →
Components → Built Components → Patterns** and hold to React 19 + Tailwind v4 + web best practice.

## First: load the design chain

The chain is the contract. Load it before building or auditing:

1. **If the repo has `docs/design/`** (ZenWrite repo) — that is the **live source of truth**.
   Read `docs/design/README.md` and the layer files (`01-tokens.md` … `06-prompt-engineering.md`)
   for whatever you're touching. Also read `src/index.css` `@theme` for current tokens.
2. **Otherwise (or as a fast summary)** — read [`references/design-chain.md`](references/design-chain.md),
   a portable mirror of the same chain.

Keep [`references/react-tailwind-best-practices.md`](references/react-tailwind-best-practices.md)
in mind for engineering/a11y/perf, and [`references/audit-checklist.md`](references/audit-checklist.md)
for review severity.

Non-negotiables (from the philosophy):
- **Light-primary.** No global `prefers-color-scheme` dark mode; `dark:` only under an explicit `.dark` ancestor.
- **Two spheres, kept separate.** Content = brand-violet (Create/Edit/Organize). Community = sky/emerald/rose (Engage/Manage/Analyze). Don't cross primary accents.
- **Tokens, never hex.** `bg-brand-violet`, not `bg-[#14006a]`. No dynamic color strings.
- **Deliberate type.** `font-serif` (Newsreader) for literary titles/body; `font-manrope` for uppercase eyebrows/labels.
- **Chrome fades.** In the editor, secondary chrome idle-fades at `duration-700`; never add persistent editor chrome.

## Pick the mode

- **Build mode** — user wants a new component, panel, screen, tile, or page → [Build workflow](#build-workflow).
- **Audit mode** — user wants a review, alignment pass, consistency/design check, or "flush drift" on existing UI → [Audit workflow](#audit-workflow).

If the ask is ambiguous ("work on the newsletter UI"), state which mode you're taking and why, then proceed.

---

## Build workflow

Reason **down the chain**, reusing what exists before creating anything new.

1. **Locate in the chain.** What layer is this? A pill/badge → primitive. A panel/wizard →
   component. A full view → built component. A cross-cutting shell/overlay behavior → pattern.
2. **Determine the sphere.** Content (violet) or community (sky/emerald/rose)? Resolve accent classes via `getViewAccent(view)` from `src/lib/viewAccents.ts` — headers, tabs, nav active states only; primary CTAs stay brand-violet.
3. **Reuse first.** Before writing markup, check for an existing primitive/pattern to compose:
   `StatusChip`, `VoiceFidelityChip`, `StateLayouts` (Loading/Empty/Error), the slide-in panel
   shell, the full-screen wizard shell, the home-tile pattern, the ⌘K palette. Grep `src/components/`.
   Extract a new primitive only when a 2nd/3rd consumer already exists — avoid premature abstraction.
4. **Compose with tokens.** Use the canonical patterns from `references/design-chain.md`
   (Layers 3–5) verbatim as your skeleton — panel titles `font-serif text-lg font-light italic
   text-brand-violet`, cards `rounded-2xl border-brand-violet/10`, page shell `max-w-7xl mx-auto
   px-6 py-8`, correct z-index and `animate-in` motion. Every interactive element gets
   `focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none` and an
   accessible name.
5. **Wire it up.** New screens/panels get state in `App.tsx` (view switch or overlay boolean),
   respect the idle-fade contract, and route by manuscript type where relevant
   (article/book/lesson/newsletter → Editor; podcast/video → MediaSurface).
6. **Engineer it well.** Typed props, no `any`, local UI state only, keyboard + SR accessible,
   ESC/backdrop close for overlays, static color maps (never `bg-${c}-500`), responsive across
   mobile / `md+` / wide. See `references/react-tailwind-best-practices.md`.
7. **Self-check + validate.** Run the [12-point checklist](references/audit-checklist.md) on your
   own output, then `pnpm build:check` (and `RUN_BUILD_VALIDATION=true pnpm build:check`). Fix TS
   errors in `reports/tsc.txt`.

**Output:** the component/screen file(s) in `src/components/`, any `App.tsx` wiring, a note on
which primitives/patterns you reused, and confirmation the build check passed (or the errors if not).

---

## Audit workflow

Find drift, grade it, fix it — without inventing a new design.

1. **Scope.** Confirm target: specific files, a route/screen, or a full `src/` sweep ("flush drift").
2. **Mechanical scan.** Run the scanner:
   ```bash
   bash <skill-dir>/scripts/audit-scan.sh src           # or narrow: ... src/components/EngageScreen.tsx
   ```
   It surfaces hardcoded hex, dynamic color strings, missing focus rings, dark-mode hijacks,
   ad-hoc status badges, and font hygiene. It **locates**; you **judge** each hit.
3. **Chain review.** For each file, walk the [12-point reconstruction checklist](references/audit-checklist.md)
   and assign severity (CRITICAL / HIGH / MEDIUM / LOW). Check sphere discipline, typography layer,
   token usage, focus/a11y, z-index, StateLayouts/StatusChip reuse, and responsive behavior.
4. **Report.** List findings **most-severe first**, each as
   `file:line → what's wrong → concrete fix (exact token/class)`. Group by file. Note anything
   that's an intentional, documented exception rather than drift.
5. **Fix (when asked to align, not just report).** Apply lowest-risk fixes first (token swaps,
   focus rings, StatusChip/StateLayouts substitution) → then structural (primitive extraction,
   z-index, sphere correction). **Never introduce a new hex or new token to fix a hit** — reuse
   existing tokens; only add to `@theme` for a genuinely new semantic color (rare — flag it).
6. **Validate.** `pnpm build:check` (+ Vite bundle variant). Resolve `reports/tsc.txt` errors.
   Re-run the scanner to confirm the hits are gone.

**Output:** a severity-ranked findings report; if fixing, the edits plus a before/after summary
and passing build check.

---

## Guardrails

- **Don't redesign.** This skill enforces *the existing* ZenWrite system; it does not invent new
  visual language. If the user wants a new direction, say so and get explicit agreement first.
- **Don't cross spheres.** Violet is not a community accent; sky/emerald/rose are not content accents.
- **Don't add hex or dynamic color strings**, global dark mode, persistent editor chrome, or debug
  panels — these are the documented anti-patterns.
- **Prefer composition over new abstractions.** Reuse primitives; extract only on real repetition.
- When the repo's `docs/design/` disagrees with `references/design-chain.md`, **the repo wins** —
  it's the live source of truth and this reference may lag.
