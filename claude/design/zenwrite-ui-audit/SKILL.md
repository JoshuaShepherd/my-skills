---
name: zenwrite-ui-audit
description: Audit and improve existing ZenWrite UI — React 19 + Tailwind v4 quality plus the ZenWrite design chain (light-primary, dual-sphere; Newsreader serif + Manrope; brand-violet content, sky/emerald/rose community). Finds and fixes design drift (hardcoded hex, dynamic color strings, wrong sphere accents, missing focus rings, ad-hoc badges, dark-mode hijacks, token misuse) AND React/Tailwind/a11y/perf issues, ranked by severity, then applies the fixes. Use whenever REVIEWING, ALIGNING, CLEANING UP, or IMPROVING existing ZenWrite components/screens — "audit this page," "flush drift," "make this match our style," "clean up the styling," "check design consistency," "improve this component's react/tailwind." For building NEW UI from scratch, use zenwrite-design instead.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ZenWrite UI Audit & Improve

Find drift and defects in existing ZenWrite UI, grade them, and fix them — **without inventing a new
design**. This skill covers two intertwined dimensions: **design-chain alignment** (tokens, spheres,
typography, patterns) and **React/Tailwind engineering quality** (correctness, a11y, performance,
Tailwind hygiene). It is an auditor *and* an improver. (To build new UI, use **zenwrite-design**.)

## First: load the contract

1. **In the ZenWrite repo** (`docs/design/` exists) — that folder + `src/index.css` `@theme` are the
   **live source of truth**. Skim `docs/design/README.md` and the layer file(s) relevant to the target.
2. Load the two references you'll grade against:
   - [`references/audit-checklist.md`](references/audit-checklist.md) — the design-chain 12-point
     checklist + severity ladder + WCAG/responsive gates.
   - [`references/react-tailwind-audit.md`](references/react-tailwind-audit.md) — the engineering
     audit dimensions (React correctness, hooks, a11y, Tailwind hygiene, performance).

## Workflow

1. **Scope.** Confirm the target: specific files, a route/screen, or a full `src/` sweep ("flush
   drift"). State what you're auditing before you start.
2. **Mechanical scan.** Run the scanner — it *locates*, you *judge*:
   ```bash
   bash <skill-dir>/scripts/audit-scan.sh src                 # or narrow: … src/components/EngageScreen.tsx
   ```
   It surfaces hardcoded hex, dynamic color strings, missing focus rings, dark-mode hijacks, ad-hoc
   status badges, font hygiene, and points to review each interactive element.
3. **Chain review (design).** For each file, walk the
   [12-point reconstruction checklist](references/audit-checklist.md) and assign severity
   (CRITICAL / HIGH / MEDIUM / LOW): sphere discipline, typography layer, token usage, focus/a11y,
   z-index, `StateLayouts`/`StatusChip` reuse, `dark:` scoping, responsive behavior.
4. **Engineering review (react/tailwind).** For each file, walk
   [`references/react-tailwind-audit.md`](references/react-tailwind-audit.md): effect misuse and
   missing cleanup, unstable keys, `any` types, dynamic color strings, class duplication that should
   be a primitive, uncontrolled inputs, missing memoization on hot paths, overlay focus management,
   layout-shift risks. Assign severity on the same ladder.
5. **Report.** List findings **most-severe first**, each as
   `file:line → what's wrong → concrete fix (exact token/class or code change)`. Group by file. Flag
   anything that is an intentional, documented exception (e.g. Editor/MediaSurface/PublishPanel are
   view-accent–exempt) rather than drift.
6. **Fix (when asked to improve/align, not just report).** Apply lowest-risk first — token swaps,
   focus rings, `StatusChip`/`StateLayouts` substitution, `aria-label`s — then structural: primitive
   extraction, z-index correction, sphere correction, effect/key/type fixes. **Never introduce a new
   hex or new token to fix a hit** — reuse existing tokens; only add to `@theme` for a genuinely new
   semantic color (rare — flag it and get agreement).
7. **Validate.** `pnpm build:check` (and `RUN_BUILD_VALIDATION=true pnpm build:check` for the Vite
   bundle). Resolve TS errors in `reports/tsc.txt`. Re-run the scanner to confirm hits are gone.

## Severity ladder (quick)

| Level | Meaning | Examples |
|-------|---------|----------|
| **CRITICAL** | Breaks the contract or a11y | hardcoded hex in shell/nav; dynamic color string (unstyled after purge); interactive element with no accessible name; contrast <3:1 on a control; effect leaking a timer/listener |
| **HIGH** | Visible inconsistency or real bug | wrong sphere accent; ad-hoc status span vs `StatusChip`; missing focus ring; panel title not `font-serif italic`; wrong z-index; unstable list key causing state bugs |
| **MEDIUM** | Drift that erodes coherence | `text-sky-700` where a `community-*` token exists; `rounded-xl` where cards use `rounded-2xl`; missing hover transition; needless `useEffect`; class-string duplication |
| **LOW / INFO** | Nits & future extraction | repeated Tailwind string → extract a primitive; Manrope vs Inter mixups; missing `useMemo` on a cheap path |

## Guardrails

- **Enforce the existing system; don't redesign.** If a finding implies a new visual direction, flag
  it as a proposal, don't apply it silently.
- **Don't cross spheres**, don't add hex/dynamic color strings, global dark mode, persistent editor
  chrome, or debug panels — those are the documented anti-patterns you're removing, not adding.
- **Prefer composition over new abstractions.** Extract a primitive only when a real 2nd/3rd consumer
  already exists.
- When the bundled reference disagrees with the repo's `docs/design/`, **the repo wins**.

## Output

A severity-ranked findings report (`file:line → problem → fix`), grouped by file, design and
engineering findings together. If fixing: the edits, a before/after summary, a passing
`pnpm build:check`, and a clean re-scan.
