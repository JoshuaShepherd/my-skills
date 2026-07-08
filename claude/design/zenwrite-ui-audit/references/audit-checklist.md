# ZenWrite Design-Chain Audit Checklist & Severity

Use this for the **design** dimension of an audit. Pair with `scripts/audit-scan.sh` (mechanical
hits) — this file adds judgment and severity. For the **engineering** dimension see
`react-tailwind-audit.md`. When this disagrees with the repo's `docs/design/`, the repo wins.

## Severity ladder

| Level | Meaning | Examples |
|-------|---------|----------|
| **CRITICAL** | Breaks the design contract or accessibility | Hardcoded hex in shell/nav; dynamic color string (renders unstyled after purge); interactive element with no accessible name; contrast < 3:1 on UI control |
| **HIGH** | Visible inconsistency users will notice | Wrong sphere accent; ad-hoc status span vs StatusChip; missing focus-visible ring; panel title not `font-serif italic`; wrong z-index causing overlap |
| **MEDIUM** | Drift that erodes coherence | `text-sky-700` where a `community-*` token exists; `rounded-xl` where cards use `rounded-2xl`; missing hover transition; inconsistent spacing scale |
| **LOW / INFO** | Nits & future extraction | Repeated Tailwind string that should become a primitive; Manrope vs Inter mixups on labels |

Report findings most-severe first. For each: **file:line → what's wrong → the fix (concrete class/token)**.

## The 12-point reconstruction checklist

- [ ] All colors use `@theme` tokens — no `#`/`[#` in `className`, no raw hex in `style`.
- [ ] Typography matches layer — `font-serif` literary titles/body; `font-manrope` uppercase eyebrows/labels; `font-mono` only for keys/scores.
- [ ] Cards use `rounded-2xl` + `border-brand-violet/10` (content) or sphere-appropriate border (community).
- [ ] Every interactive element has `focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none` and an accessible name.
- [ ] Hover uses `transition-all duration-200` (or `transition-colors`), never instant snaps.
- [ ] No dynamic Tailwind class concatenation for colors — static maps only.
- [ ] `dark:` variants appear only where a `.dark` ancestor exists; no global dark hijack.
- [ ] Loading / empty / error use `StateLayouts` primitives (violet loading/empty, rose error).
- [ ] Status badges use `StatusChip`, not ad-hoc spans.
- [ ] Sphere discipline — content screens lead with violet; community screens lead with sky/emerald/rose (via `getViewAccent`); neither borrows the other's primary accent; **primary CTAs stay `bg-brand-violet` on every view**.
- [ ] Panel z-index follows the stack (backdrop 40 · panel 50 · publish 60 · palette 70); slide-ins animate `slide-in-from-right duration-300`.
- [ ] New screens/panels wired into `App.tsx` view switch or overlay flags; NavigationAxis idle-fade respected in editor.

## Sphere & view-accent specifics

| View | Sphere | Accent | Header/title |
|------|--------|--------|--------------|
| home, create, organize | content | violet | `ViewPageHeader` / violet section header |
| engage, kairos | community | sky | `ViewPageHeader view="engage"` + `getViewAccent` |
| manage | community | emerald | `ViewPageHeader view="manage"` |
| analyze | community | rose | `ViewPageHeader view="analyze"` |

**70 / 20 / 10:** ~70% shared chrome (cards, CTAs, focus rings stay violet/neutral); ~20% sphere
color; ~10% view accent on headers, active tabs, nav active, stat highlights. **Exempt from
view-accent recolor:** Editor, MediaSurface, PublishPanel — do **not** file these as drift.

## Accessibility (WCAG 2.1 AA)

- Small text (<24px / <18.66px bold): **≥ 4.5:1** contrast. Large text & UI controls / focus rings: **≥ 3:1**.
- `brand-violet #14006a` on dark surfaces fails — swap to `dark:text-indigo-300` (or a lighter violet token).
- Every control reachable/operable by keyboard; visible focus ring on tab.
- Icon-only buttons need `aria-label`; decorative icons `aria-hidden`.
- Respect reduced motion where animations are non-essential.

## Responsive

- Verify mobile (single-column home, collapsed spine, bottom-nav-first), `md+` (dual-column, spine in
  book mode), and wide (`max-w-7xl` cap).
- Tap targets ≥ ~44px; no horizontal scroll at 320px; text reflows without clipping.

## Fix protocol

1. Run `scripts/audit-scan.sh <scope>` for mechanical hits.
2. Walk the 12-point checklist per file, assigning severity.
3. Apply fixes lowest-risk first (token swaps, focus rings, `StatusChip`/`StateLayouts` substitution,
   `aria-label`s) → structural (primitive extraction, z-index, sphere correction).
4. **Never introduce a new hex or new color token to fix a hit** — reuse existing tokens; only add to
   `@theme` if a genuinely new semantic color is required (rare; flag it).
5. Validate: `pnpm build:check` (and `RUN_BUILD_VALIDATION=true pnpm build:check`). Fix TS errors in
   `reports/tsc.txt`. Re-run the scanner to confirm the hits are gone.
