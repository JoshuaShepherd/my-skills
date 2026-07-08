# React 19 + Tailwind v4 Engineering Audit (ZenWrite)

The **engineering** dimension of a ZenWrite audit — correctness, hooks discipline, a11y, Tailwind
hygiene, and performance. Grade each finding on the same severity ladder as the design checklist.
Design chain wins on anything visual; this governs how the code behaves and holds up.

## React correctness & hooks

| Check | Severity if violated | Fix |
|-------|----------------------|-----|
| Effects only for real synchronization (subscriptions, timers, DOM measurement) — not for deriving state that could be computed in render | MEDIUM–HIGH | Derive during render; delete the effect |
| Every `useEffect` with a timer/listener/subscription **cleans up** in its return | CRITICAL (leak) | Return a cleanup that clears the timer / removes the listener |
| Effect dependency arrays are complete and correct (no stale closures, no missing deps) | HIGH | Add deps or restructure; don't silence the intent |
| List `key` is a stable id, never array index when items can reorder/insert/delete | HIGH (state bugs) | Use the item's id |
| No `any` (repo is `strict: true`); props are a typed interface | HIGH | Type the props / value |
| Domain data flows via props/hooks, not localStorage reads in presentation (editor settings + academic-mode flags are the only documented exceptions) | MEDIUM | Lift to hook/`App.tsx`, pass down |
| Inputs are controlled; autosave is debounced, not per-keystroke | MEDIUM | Controlled value + debounce |
| Memoization (`useMemo`/`useCallback`/`memo`) applied to genuinely expensive work / referential stability (recharts data), not sprinkled everywhere | LOW–MEDIUM | Add where hot, remove where cosmetic |
| Heavy surfaces (`AnalyticsView`/recharts, wizards) are `React.lazy` + `Suspense` so the editor path stays light | MEDIUM | Lazy-load |

## Accessibility (code-level)

| Check | Severity | Fix |
|-------|----------|-----|
| Actions are `<button>`, navigation is `<a>` — not clickable `<div>`/`<span>` | HIGH | Use the semantic element |
| Icon-only controls have `aria-label`; decorative icons `aria-hidden` | HIGH | Add the attribute |
| Every interactive element has `focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none` | HIGH | Add the ring |
| Overlays (panels, wizards, modals) trap focus, restore focus on close, close on ESC + backdrop | HIGH | Add focus management + ESC handler |
| `role`/`aria-modal` on dialogs; labelled by their title | MEDIUM | Add `role="dialog" aria-modal` + `aria-label` |
| Reduced motion respected for non-essential animation | LOW | `motion-reduce:` or guard |

## Tailwind v4 hygiene

| Check | Severity | Fix |
|-------|----------|-----|
| No `bg-[#hex]` / arbitrary color / raw palette (`bg-indigo-900`) — use `@theme` semantic tokens | CRITICAL–HIGH | Swap to `bg-brand-violet` etc. |
| No dynamic color strings (`bg-${c}-500`) — purge-unsafe | CRITICAL | Static class map keyed by variant |
| No `tailwind.config.js` reintroduced — tokens live in `src/index.css` `@theme` | HIGH | Move token to `@theme` |
| A class string repeated 3× → extract a primitive/component | LOW–MEDIUM | Extract (only with real repetition) |
| Arbitrary **values** (`text-[10px]`, `tracking-[0.25em]`) OK for the documented micro-type scale; arbitrary **colors** not | INFO / HIGH | Keep values, fix colors |
| Conditional classes via `cn()`/`clsx` or static maps, not deep nested ternaries in JSX | LOW | Refactor to helper/map |
| Motion via existing `animate-in`/`slide-in-*`/`zoom-in-*` utilities | LOW | Use the utility |

## Performance & correctness

| Check | Severity | Fix |
|-------|----------|-----|
| Editor path (`Editor`, `FloatingComposer`, `BottomNav`) stays lean — no whole-tree re-render on caret move | HIGH | Localize state; memoize boundaries |
| Idle-fade / hovers use CSS transitions, not JS-driven animation | MEDIUM | CSS `transition-*` |
| Async content reserves space (StateLayouts skeletons) to avoid layout shift | MEDIUM | Use `LoadingState` |
| No console noise / debug panels / port indicators left in production layouts | MEDIUM | Remove |

## Fix protocol (engineering)

1. Run `scripts/audit-scan.sh <scope>` for the mechanical hits (hex, dynamic strings, focus rings,
   dark hijack, ad-hoc badges).
2. Walk this table per file; combine with the design 12-point checklist. One ranked list.
3. Apply lowest-risk first (types, `aria-label`s, focus rings, token swaps) → structural (effect
   cleanup, key fixes, lazy-loading, primitive extraction).
4. Validate: `pnpm build:check`, then `RUN_BUILD_VALIDATION=true pnpm build:check`. Resolve
   `reports/tsc.txt` (typecheck is the only lint gate). Re-run the scanner.
