---
name: movemental-ink
description: >
  Front-end UI design expert for movemental-ai's "Ink Band" design system — the
  agent room. Use when building or restyling any screen, primitive, shell zone,
  or component on the .ink-band-surface to match the existing visual language.
  Anchors to the .ink-band-surface tokens in src/app/globals.css, the
  agent-room CSS module (src/components/agent-room/ink-band.module.css), the
  real component tree (shell/ · screen/ · ink/), and docs/design/INK_BAND_DESIGN_CHAIN.md.
  Keywords: Ink Band, agent room, warm paper, red margin rule, Playfair display,
  Inter body, Caveat hand, IBM Plex Mono labels, ink-blue #22409b pen, ink
  gestures, mast/screen/voice/composer, closed screen set, tonal stacking,
  hairline borders, staggered reveal, Tailwind v4, shadcn.
---

# Ink Band UI (movemental-ai)

Use this skill whenever you build or restyle front-end UI in this repo. As of
the 2026-06 pivot, **movemental-ai is agent-only and Ink Band is the sole live
design system.** Concept Modern (`DESIGN.md`) is archived reference for a future
marketing merge — do not implement it in `src/`.

## North Star

**Ink Band — the agent's hand.** The agent room is a **sheet of warm paper the
agent writes on by hand**: a cream page with a faint **red margin rule**,
headlines in literary serif, the agent's live voice in **handwriting** in
pen-ink blue, labels in **typewriter mono**, and gestures (underline, circle,
arrow) drawn as **rough ink strokes** over the page. It is a **manuscript the
org is shown back to itself** — not a chat window or a dashboard.

Pillars: *editorial, not app-like* (add space, never shrink type) · *the hand is
visible* (handwritten "say" lines, ink gestures; motion is choreography) · *one
pen, one accent* (a single ink-blue carries voice, links, active state, strokes)
· *paper depth, light borders* (tonal stacking **plus** hairline 1px borders and
12–20px radii) · *a closed screen set* · *restraint as honesty*.

## CRITICAL: scope to `.ink-band-surface`

The Ink Band ramp must **never leak** outside its scoped surface.

- **Live surface** is the `.ink-band-surface` wrapper applied by
  [src/app/agent/layout.tsx](src/app/agent/layout.tsx) (the room) and
  [src/components/ink-band/utility-shell.tsx](src/components/ink-band/utility-shell.tsx)
  (auth / staff admin — same ramp, no room chrome).
- The marketing nav/footer are suppressed for `/agent` via `proxy.ts`
  (`x-movemental-shell: room`).
- **Caveat (the hand face) is scoped, not global** — loaded via `next/font` in
  the agent layout + utility shell as `--font-ink-hand-face`, so utility/auth
  routes that don't render the room never fetch or paint it. The other three
  faces cascade from the root layout.
- **IGNORE / do not reintroduce:** Concept Modern `oat-*` tokens, the archived
  `(site)` marketing route group + `nav/`/`sections/` under
  `_archive/pre-marketing-migration-2026-06/`, the legacy "Digital Curator"
  `#0053db` blue.

## Source of truth (read these, in order)

1. [src/app/globals.css](src/app/globals.css) — **token SSOT.** The
   `.ink-band-surface` block (`--color-ink-band-*`, `--font-ink-*`) and the
   `:root` shadcn ramp mapped to the same hexes.
2. [docs/design/INK_BAND_DESIGN_CHAIN.md](docs/design/INK_BAND_DESIGN_CHAIN.md)
   — the design charter + layer-by-layer chain (canon). Index:
   [docs/design/README.md](docs/design/README.md).
3. [src/components/agent-room/ink-band.module.css](src/components/agent-room/ink-band.module.css)
   — the demonstrated recipes for every primitive/figure/shell zone. **All
   agent-room CSS lives here** — do not add Concept Modern or `oat-*` tokens.
4. Golden components — the real tree, composed down the chain:
   - `shell/` — `mast`, `screen-zone`, `voice-zone`, `agent-dock`, `ink-overlay`
   - `screen/` — the closed screen set (`opening-hero`, `reality-check-beat`,
     `readback`, `process-accordion`, `safety-plan-cards`, `audience`, …)
   - `ink/` — `ink-voice`, `gesture-paths`, `use-ink-gestures`, `use-ink-voice`

> ⚠️ The `INK_BAND_DESIGN_CHAIN.md` SSOT upstream is the
> `movemental-agentic-front-end` prototype (vanilla HTML/CSS). Use it for *how*
> the design behaves; the React **implementation** lives in this repo. Replace
> the prototype's scripted **data**, keep its **structure** and screen vocabulary.

## Stack

Next.js 16 App Router (RSC) · React 19 · Tailwind **v4** (CSS-first `@theme`, no
HSL) · shadcn "radix-nova" over Radix (utility pages) · CSS Modules for the room ·
`cn()` from `src/lib/utils.ts` · Lucide icons.

## Color — tokens only (raw hex in `globals.css` only)

The accent is **the pen (ink-blue), not a brand color.** Use the `--color-ink-band-*`
custom properties via the module CSS; never raw hex / `bg-white` / `bg-black` /
`bg-blue-600` in components.

| Role | Token | Hex |
|---|---|---|
| App background (warmest paper) | `--color-ink-band-bg` | `#fbfaf6` |
| Chrome surface (voice, composer, wells) | `--color-ink-band-surface` | `#f6f3ec` |
| AI dock band (cooler than stage) | `--color-ink-band-ai-surface` | mix(surface 90% / blue 10%) |
| Raised writing surface (cards, options, fields) | `--color-ink-band-paper` | `#fffdf7` |
| Primary text + ink-pill CTA / send | `--color-ink-band-ink` | `#1a1a1a` (never pure black) |
| Secondary text, metadata, body | `--color-ink-band-ink-muted` | `#5c5651` |
| Hairline borders, rails, node rings | `--color-ink-band-border` | `#e5dfd2` |
| Dark hero treatments (reserved) | `--color-ink-band-hero-dark` | `#0a0e1a` |
| **Margin rule / severity ticks / refusals** (reserved red) | `--color-ink-band-margin-red` | `#c08a7e` |
| **The pen** — voice, links, active borders, strokes, focus | `--color-ink-band-blue` | `#22409b` |
| **Highlighter** — exactly one lead chip (reserved) | `--color-ink-band-highlight` | `#eaff3a` |

**One pen, one accent.** Ink-blue is the only accent. Red stays in the margin
rule / severity ticks / refusals; highlighter-yellow marks exactly one chip.
Nothing else competes. Shadcn utility pages consume the same ramp via the
`:root` semantic tokens (`bg-background`, `text-foreground`, `border-border`, …).

## Typography — four voices, used correctly

- **Display + headlines:** Playfair Display → `--font-ink-display` (weight 600,
  `line-height 1.07`, `letter-spacing -0.025em`). All `h1–h6` on the surface
  auto-set this.
- **Body / UI / options / inputs:** Inter → `--font-ink-body`.
- **Agent voice ONLY:** Caveat → `--font-ink-hand` (the `.vline` handwriting and
  the readback "you are here" annotation). Never use it for chrome or body.
- **Eyebrows / section labels / metadata / prices / crumbs:** IBM Plex Mono →
  `--font-ink-mono`. The label idiom is mono, ~`.66–.7rem`,
  `letter-spacing .13–.18em`, `uppercase`, `--ink-muted`.
- Fluid sizing via `clamp()`: `h1` `clamp(1.85rem,4.3vw,2.85rem)`, `.q`
  `clamp(1.5rem,3.6vw,2.05rem)`, path numeral `clamp(3.4rem,11vw,5.25rem)`.
- Measure: body `max-width 68ch`, drawer/way `56–62ch`, question `40ch`,
  headline `22ch`. Sheet width `56rem` → `68rem` (≥62rem) → `76rem` (≥90rem).

## Spacing, radius, depth, motion

- **Radii:** `12px` (option/field/faq), `14–16px` (cards/way), `20px` (path
  stack card), `999px` (chips, field, send). Unlike Concept Modern, Ink Band
  **does** use generous radii as notebook/card vocabulary.
- **Borders:** always `1px solid var(--color-ink-band-border)`, going
  `var(--color-ink-band-ink)` (or ink-blue) on hover/active. Hairlines are part
  of the language here — not banned.
- **Depth:** tonal stacking `paper` on `surface` on `bg`, plus the hairline
  borders. No decorative drop shadows.
- **Motion (choreography, not decoration):** house easing
  `cubic-bezier(.2,.7,.2,1)`. Staggered entrances key off a `--i` index custom
  property (`animation-delay:calc(var(--i,0)*Nms + delay)`; options `70ms`,
  readback `95ms`, faces `32ms`). Named keyframes: `optIn`, `rbIn`, `faceIn`,
  `settle`, `fadein`, `beatGrow`, `cfDraw`, `cfShake`. The hand draws on via a
  `clip-path:inset(0 100% 0 0)→0` reveal under a moving `.nib`; gestures are SVG
  `.stroke`s through the `#rough` filter.
- **Reduced motion is mandatory.** `@media (prefers-reduced-motion: reduce)`
  disables the clip reveal, hides the nib, and turns off opt/readback/face/beat/
  form animations. A port **must** keep this.

## The chain — compose down, never reach around

Tokens → **Primitives** → **Components** → **Built layers (shell)** → **Pages**.

- **Primitives (Layer 2):** `eyebrow` · `sec-label`/`band-label` · sheet `h1` ·
  `.q` (posed question) · body · `chip` (`.chip.lead` = highlighter) · `opt`
  (answer button; `.locked`/`.chosen`) · `field`+`send` · `mast`/`logo`/`crumb`
  · `mail` · `refuse` (red-ruled "won't do") · `honest` (italic caveat) ·
  `stroke` (ink gesture).
- **Components (Layer 3):** beat progress · readback spine (`.rb-*`, "you are
  here" + severity ticks) · path drawers (stacked, `0fr→1fr`) · ways/pricing ·
  faq accordion (`<details>`) · faces band (duotone avatars) · team · leader
  head · contact form (`cfDraw` success, `cfShake` invalid) · layered list.
- **Built layers (Layer 4 — the shell):** `mast` → `#screen` (radial paper wash
  + `<svg #ink>` gesture overlay with `#rough`/`#marker` filters) → `voice`
  (handwritten lines) → `composer` (chips + `field`+`send`). Body is
  `100dvh` flex; only `#screen` scrolls. Static-page variant swaps voice/composer
  for a footer.
- **Pages (Layer 5 — the closed screen set):** one `.sheet` composition per
  `ScreenId`. The set is **closed**: `home`, `beat`, `readback`, `path`,
  `pricing`, `safety`, `confirm`, `leader`, `founders`, `about`, `contact`,
  `faq`. New surfaces are a deliberate vocabulary change, not an ad-hoc page,
  and map 1:1 to the engine `ComponentId` ↔ `ScreenId` contract.

## Avoid (drift — do not copy)

- Concept Modern / `oat-*` tokens, `DESIGN.md` patterns, or a second live token
  system anywhere in `src/`.
- Ink Band tokens **leaking** outside `.ink-band-surface`; loading Caveat globally.
- Raw hex / `bg-black` / `text-black` / `bg-blue-*` in TSX; bypassing the module
  CSS recipes.
- Using ink-blue for anything but the pen; using red or highlighter outside
  their reserved roles; a second competing accent.
- Pure-black text (`#000`) — primary ink is `#1a1a1a`.
- Adding screens outside the closed set; building a chat-UI or card-grid
  marketing layout; shrinking type to fit.
- Dropping the reduced-motion guard or the duotone portrait treatment — both are
  load-bearing for the feel.

## Workflow checklist

1. Confirm you're inside `.ink-band-surface`; open `globals.css` +
   `INK_BAND_DESIGN_CHAIN.md` for tokens/rules and `ink-band.module.css` for recipes.
2. Compose **down the chain**: primitives → figures → the shell zone → a closed-set
   screen. Reuse the real `shell/`·`screen/`·`ink/` components; don't hand-roll divs.
3. Four type voices in their lanes (Playfair display, Inter body, Caveat voice-only,
   IBM Plex Mono labels). `<em>`/`b` for in-line emphasis, never serif body.
4. Palette via `--color-ink-band-*` tokens only; ink-pill CTAs; one pen (ink-blue);
   red + highlighter stay reserved.
5. Depth = tonal stacking + 1px hairlines + 12–20px radii. No drop shadows.
6. Motion = house easing + `--i` stagger; gestures via `#rough`; voice via nib +
   clip reveal. Verify `prefers-reduced-motion` bails out.
7. Verify: no raw hex, no `oat-*`/Concept Modern, no token leak, no Caveat in
   chrome, no off-set screens, no second accent.
