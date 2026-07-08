# React 19 + Tailwind v4 Best Practices (ZenWrite stack)

General engineering standards that ride *alongside* the ZenWrite design chain. When these
conflict with the design chain, the design chain wins for anything visual; these govern
correctness, performance, and maintainability.

## React 19

- **Function components + hooks only.** No class components. Co-locate local UI state with `useState`; lift shared state to `App.tsx` or a context/hook.
- **Props down, events up.** Components receive data + callbacks; they don't reach into localStorage for domain data (editor settings/academic-mode flags are the documented exceptions).
- **Keys** on lists must be stable ids, never array index when items reorder.
- **Effects are a last resort.** Derive during render where possible; use `useEffect` only for real synchronization (subscriptions, timers, DOM measurement like idle-fade). Always clean up timers/listeners.
- **Memoize deliberately** — `useMemo`/`useCallback`/`memo` for genuinely expensive work or referential-stability needs (e.g. recharts data), not by default.
- **Lazy-load heavy surfaces** (`AnalyticsView`/recharts, wizards) with `React.lazy` + `Suspense` to keep the editor path light.
- **Controlled inputs** for form fields; debounce autosave rather than writing on every keystroke.
- **Accessibility is code, not polish:** semantic elements (`<button>` for actions, `<a>` for navigation), `aria-label` on icon buttons, focus management when opening/closing overlays (trap focus in modals, restore on close, ESC to dismiss).

## Tailwind CSS v4 (CSS-first)

- **No `tailwind.config.js`.** Tokens live in `src/index.css` `@theme`. Add semantic tokens there; consume as utilities.
- **Semantic tokens over raw palette / hex.** `bg-brand-violet`, not `bg-[#14006a]` and not `bg-indigo-900`. Community `sky/emerald/rose-700` are tolerated but prefer `community-*` tokens in new work.
- **Static class maps for variants** (purge safety):
  ```tsx
  const sphere = {
    content:   'text-brand-violet border-brand-violet/10 hover:bg-brand-violet/[0.04]',
    community: 'text-community-emerald border-emerald-100 hover:bg-emerald-500/[0.06]',
  } as const;
  className={sphere[kind]}
  ```
  Never `bg-${color}-500`.
- **Compose, don't duplicate.** Three repeats of a class string → extract a primitive/component (see design chain Layer 2).
- **Ordering & readability:** group by layout → box → color → typography → state. Consider a `cn()`/`clsx` helper for conditional classes rather than nested ternaries in JSX.
- **Arbitrary values** (`text-[10px]`, `tracking-[0.25em]`) are fine for the documented micro-type scale; arbitrary *colors* are not.
- **Motion:** use the `animate-in` / `slide-in-*` / `zoom-in-*` utilities already in use; reserve the `motion` library for complex sequenced animation, not simple hovers.

## Performance & correctness

- Keep the **editor path** (Editor, FloatingComposer, BottomNav) lean — it's the hero and runs on every keystroke. Avoid re-rendering the whole tree on caret moves.
- Prefer CSS transitions over JS-driven animation for idle-fade and hovers.
- Guard against layout shift: reserve space for async content; use the `StateLayouts` skeletons.
- Validate before shipping: `pnpm build:check`, then `RUN_BUILD_VALIDATION=true pnpm build:check`. Resolve TS errors (`reports/tsc.txt`) — the repo treats typecheck as the lint gate.

## New-component checklist (engineering side)

- [ ] One responsibility; named export matching file; placed in `src/components/`.
- [ ] Typed props interface; no `any`.
- [ ] Local UI state only; domain data via props/hooks.
- [ ] Keyboard + screen-reader accessible; focus-visible ring; ESC/backdrop close for overlays.
- [ ] No new hex; static color maps; tokens from `@theme`.
- [ ] Wired into `App.tsx` (view switch or overlay flag) if it's a screen/panel.
- [ ] `pnpm build:check` passes.
