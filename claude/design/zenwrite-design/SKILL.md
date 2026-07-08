---
name: zenwrite-design
description: Design and build new UI for ZenWrite — the light-primary, distraction-free scholarly-writing app — the best possible way within its own design chain (Tokens → Primitives → Components → Built → Patterns). Newsreader serif + Manrope, brand-violet content sphere, sky/emerald/rose community sphere, React 19 + Tailwind v4 (CSS-first). Use whenever CREATING or EXTENDING a ZenWrite component, panel, screen, tile, overlay, wizard, or page — including "build a component," "add a panel," "make a new screen," "design a tile," "make this in our style," or "extend the editor." For reviewing/aligning existing UI, use the zenwrite-ui-audit skill instead.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ZenWrite Design — Builder

Design UI that looks like it was **always** part of ZenWrite. ZenWrite is a **light-primary,
distraction-free scholarly writing sanctuary**: the manuscript is the hero, chrome fades while
typing, and the app is split into two color spheres. This skill is the *builder* — it produces
new UI that is correct on the first pass by reasoning **down the design chain** and reusing what
already exists. (To review or realign existing UI, use **zenwrite-ui-audit**.)

## First: load the chain (the contract)

Do this before writing any markup.

1. **In the ZenWrite repo** (`docs/design/` exists) — that folder is the **live source of truth**.
   Read `docs/design/README.md`, then the layer file(s) for what you're building
   (`01-tokens` … `05-patterns-and-layouts`, and `06-prompt-engineering` for templates). Also read
   the `@theme` block in `src/index.css` for the current token set before choosing colors.
2. **As a fast portable summary / outside the repo** — read
   [`references/tokens-and-chain.md`](references/tokens-and-chain.md).

Then keep two references open while you work:
- [`references/build-recipes.md`](references/build-recipes.md) — copy-paste, token-correct skeletons
  for every layer (tile, slide-in panel, wizard, modal, page header, catalog list, status usage,
  editor extension). **Start from these, don't invent markup.**
- [`references/static-html-docs.md`](references/static-html-docs.md) — token map for self-contained
  `docs/html/*` pages outside the Vite bundle.
- [`references/engineering.md`](references/engineering.md) — React 19 + Tailwind v4 + a11y standards
  the output must also satisfy.

## Non-negotiables (memorize)

- **Light-primary.** No global `prefers-color-scheme` dark mode. `dark:` only under an explicit
  `.dark` ancestor.
- **Two spheres, never crossed.** Content = **brand-violet** (Create / Edit / Organize).
  Community = **sky / emerald / rose** (Engage & Kairos → sky, Manage → emerald, Analyze → rose).
  Resolve community accents through `getViewAccent(view)` in `src/lib/viewAccents.ts` — never
  hand-roll `text-sky-700` strings.
- **Tokens, never hex.** `bg-brand-violet`, not `bg-[#14006a]`, not `bg-indigo-900`. Never build
  dynamic color strings (`bg-${c}-500`) — use static class maps.
- **The 70 / 20 / 10 rule.** ~70% shared chrome (cards, primary CTAs, focus rings) stays
  violet/neutral; ~20% sphere color; ~10% view accent on headers, active tabs, nav active states,
  stat highlights. **Primary CTAs stay `bg-brand-violet` on every view**, including community screens.
- **Deliberate type.** `font-serif` (Newsreader) for literary titles/body/empty-states;
  `font-manrope` for uppercase eyebrows, labels, chips, metrics; `font-mono` only for keys/scores.
- **Chrome fades.** In the editor, secondary chrome idle-fades at `duration-700`. Never add
  persistent editor chrome or anything that hides the manuscript while writing.

## Build workflow (reason down the chain)

1. **Place it in the chain.** Decide the layer, because that decides the recipe and the file:
   - pill / badge / state surface → **Primitive** (`src/components/`, reuse if it exists)
   - panel / wizard / toolbar / palette → **Component**
   - a full view / major surface → **Built component** (`*Screen.tsx`, `Editor`, `MediaSurface`)
   - a cross-cutting shell / overlay / nav / idle behavior → **Pattern** (lives in `App.tsx`)
2. **Determine the sphere.** Content (violet) or community (sky/emerald/rose)? If community, plan to
   pull accents from `getViewAccent(view)` and title via `ViewPageHeader`. Keep primary CTAs violet.
3. **Reuse before you create.** Grep `src/components/` first. Compose these before writing new markup:
   `StatusChip`, `VoiceFidelityChip`, `StateLayouts` (Loading/Empty/Error), `ViewPageHeader`,
   `BottomNav`, the slide-in-panel shell, the full-screen wizard shell, the home-tile pattern,
   the ⌘K palette. **Extract a new primitive only when a 2nd/3rd real consumer already exists** —
   avoid premature abstraction.
4. **Compose from the recipes.** Take the matching skeleton from
   [`references/build-recipes.md`](references/build-recipes.md) verbatim as your skeleton, then fill
   it in. This guarantees the right radii (`rounded-2xl`), borders (`border-brand-violet/10`), page
   shell (`max-w-7xl mx-auto px-6 py-8`), z-index stack, `animate-in` motion, and header typography
   (`font-serif text-lg font-light italic text-brand-violet`).
5. **Make it accessible by construction.** Every interactive element gets
   `focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none` and an
   accessible name (`aria-label` on icon-only buttons). Overlays: ESC + backdrop close, focus trap,
   restore focus on close. Semantic elements (`<button>` for actions, `<a>` for nav).
6. **Wire it up.** New screens/panels get state in `App.tsx` (a view-switch case or an overlay
   boolean), respect the idle-fade contract, and route by manuscript type where relevant
   (`article/book/lesson/newsletter` → `Editor`; `podcast/video` → `MediaSurface`).
7. **Self-check + validate.** Walk the build checklist below, then run
   `pnpm build:check` (and `RUN_BUILD_VALIDATION=true pnpm build:check` for the Vite bundle). Fix TS
   errors listed in `reports/tsc.txt` — typecheck is the repo's only lint gate.

## Build checklist (run on your own output before shipping)

- [ ] Correct layer + file location (`src/components/`, flat); named export matches file.
- [ ] Typed props interface, no `any`; local UI state only, domain data via props/hooks.
- [ ] Only `@theme` tokens — no `#`/`[#` in `className`, no raw hex in `style`, no dynamic color strings.
- [ ] Right sphere: content leads violet; community leads via `getViewAccent`; CTAs stay `bg-brand-violet`.
- [ ] Typography by layer: `font-serif` literary, `font-manrope` uppercase labels, `font-mono` keys only.
- [ ] Cards `rounded-2xl border-brand-violet/10`; page `max-w-7xl mx-auto px-6 py-8`; sections `space-y-8`.
- [ ] Reused `StatusChip` / `StateLayouts` / `ViewPageHeader` instead of re-implementing.
- [ ] `focus-visible` ring + accessible name on every control; ESC/backdrop/focus-trap on overlays.
- [ ] Hover `transition-all duration-200`; editor chrome respects `duration-700` idle-fade.
- [ ] Overlay z-index follows the stack (backdrop 40 · slide-in 50 · publish 60 · palette 70).
- [ ] `dark:` only under a `.dark` ancestor; no global dark hijack.
- [ ] Responsive: mobile single-column, `md+` layout, `max-w-7xl` wide cap; tap targets ≥ ~44px.
- [ ] Wired in `App.tsx` if it's a screen/panel; `pnpm build:check` passes.

## Output

The component/screen file(s) in `src/components/`, any `App.tsx` wiring, a one-line note on which
primitives/patterns you reused (and any new primitive you extracted + why), and confirmation the
build check passed — or the exact errors if it didn't.

## Guardrails

- **Enforce the existing system; don't invent a new one.** If the user wants a genuinely new visual
  direction, say so and get explicit agreement before diverging.
- **Don't cross spheres** (violet is not a community accent; sky/emerald/rose are not content accents),
  **don't add hex or dynamic color strings**, global dark mode, persistent editor chrome, or debug
  panels — these are the documented anti-patterns.
- **Prefer composition over abstraction.** Reuse primitives; extract only on real, existing repetition.
- When `docs/design/` disagrees with the bundled reference, **the repo wins** — it's the live source
  of truth and the reference may lag.
