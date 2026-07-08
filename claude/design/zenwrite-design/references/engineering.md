# React 19 + Tailwind v4 engineering standards (ZenWrite)

These ride *alongside* the design chain. When they conflict, the design chain wins for anything
visual; these govern correctness, performance, and maintainability.

## React 19

- **Function components + hooks only.** No classes. Co-locate local UI state with `useState`; lift
  shared state to `App.tsx` or a context/hook. Domain data comes via props/hooks, not localStorage
  (editor settings + academic-mode flags are the documented localStorage exceptions).
- **Props down, events up.** Components receive data + callbacks.
- **Keys** are stable ids, never array index when items can reorder.
- **Effects are a last resort.** Derive during render where possible; use `useEffect` only for real
  synchronization (subscriptions, timers, DOM measurement like idle-fade). Always clean up
  timers/listeners in the return.
- **Memoize deliberately** — `useMemo`/`useCallback`/`memo` for genuinely expensive work or
  referential stability (recharts data), not by default.
- **Lazy-load heavy surfaces** (`AnalyticsView`/recharts, wizards) with `React.lazy` + `Suspense` so
  the editor path stays light.
- **Controlled inputs** for forms; **debounce autosave** rather than writing every keystroke.
- **Accessibility is code:** semantic elements (`<button>` actions, `<a>` navigation), `aria-label`
  on icon-only buttons, `aria-hidden` on decorative icons, focus management on overlay open/close
  (trap focus, restore on close, ESC to dismiss), respect reduced motion for non-essential animation.

## Tailwind v4 (CSS-first)

- **No `tailwind.config.js`.** Tokens live in `src/index.css` `@theme`; consume as utilities.
- **Semantic tokens over raw palette / hex.** `bg-brand-violet`, not `bg-[#14006a]` and not
  `bg-indigo-900`. Community `sky/emerald/rose-700` are tolerated but prefer `community-*` /
  `getViewAccent` in new work.
- **Static class maps for variants** (purge safety) — never `bg-${color}-500`:
  ```tsx
  const sphere = {
    content:   'text-brand-violet border-brand-violet/10 hover:bg-brand-violet/[0.04]',
    community: 'text-community-emerald border-emerald-100 hover:bg-emerald-500/[0.06]',
  } as const;
  className={sphere[kind]}
  ```
- **Compose, don't duplicate.** Three repeats of a class string → extract a primitive/component.
- **Ordering:** layout → box → color → typography → state. Use a `cn()`/`clsx` helper for
  conditional classes rather than nested ternaries in JSX.
- **Arbitrary *values*** (`text-[10px]`, `tracking-[0.25em]`) are fine for the documented micro-type
  scale; arbitrary *colors* are not.
- **Motion:** use the `animate-in` / `slide-in-*` / `zoom-in-*` utilities already in use; reserve a
  motion library for complex sequenced animation, not simple hovers.

## Performance & correctness

- Keep the **editor path** (`Editor`, `FloatingComposer`, `BottomNav`) lean — it runs on every
  keystroke. Don't re-render the whole tree on caret moves.
- Prefer CSS transitions over JS-driven animation for idle-fade and hovers.
- Guard against layout shift: reserve space for async content; use `StateLayouts` skeletons.
- Validate before shipping: `pnpm build:check`, then `RUN_BUILD_VALIDATION=true pnpm build:check`.
  Resolve TS errors in `reports/tsc.txt` — typecheck (`strict: true`) is the repo's only lint gate.
