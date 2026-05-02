---
name: react-audit
description: Audit React 19 configuration and usage patterns for correctness and optimization — hooks, components, error boundaries, routing, state management, performance, and best practices. Use to check React health before shipping.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Audit the React 19 configuration and usage patterns for this Vite SPA project. Check for correctness, performance, and modern best practices.

Target: $ARGUMENTS (default: full audit — scan all `src/**/*.{tsx,ts}`)

## Pre-flight

1. Read `src/main.tsx`, `src/App.tsx`, `package.json`, and `tsconfig.json`.
2. Glob `src/**/*.tsx` to inventory all components.
3. Grep for key patterns: `useEffect`, `useState`, `createContext`, `React.lazy`, `Suspense`, `ErrorBoundary`.
4. Check React and React DOM versions in `package.json`.

## Audit Checklist

### 1. ENTRY POINT & ROOT SETUP
- [ ] `createRoot` used (not deprecated `ReactDOM.render`)
- [ ] `<StrictMode>` wrapping the app (catches bugs in development)
- [ ] Root element exists in `index.html` with matching ID
- [ ] No synchronous heavy work in `main.tsx` (defer to lazy loading)
- [ ] Error boundary wraps the root or top-level routes
- [ ] If using Sentry: `Sentry.init()` called before `createRoot`

### 2. ROUTING (react-router-dom v7)
- [ ] Using `createBrowserRouter` or `<BrowserRouter>` (not `<HashRouter>` for Vercel deployment)
- [ ] Routes use lazy loading via `React.lazy()` for code splitting
- [ ] 404/catch-all route defined
- [ ] Route layout components avoid unnecessary re-renders
- [ ] `useNavigate` used instead of `<Navigate>` for programmatic navigation
- [ ] No `window.location` for in-app navigation (breaks SPA)
- [ ] Vercel SPA rewrite in place to support direct URL access

### 3. STATE MANAGEMENT
- [ ] `useState` for simple local state (not over-engineered with reducers)
- [ ] `useReducer` only for complex state with multiple sub-values or next-state-depends-on-previous
- [ ] Context not overused as global state (causes unnecessary re-renders)
- [ ] If using Context: value is memoized with `useMemo` to prevent re-renders
- [ ] No prop drilling deeper than 3 levels without Context or composition
- [ ] State lifted to lowest common ancestor, not to root
- [ ] No derived state stored in `useState` — compute inline or `useMemo`

### 4. EFFECTS & DATA FETCHING
- [ ] `useEffect` not used for data that can be computed from props/state
- [ ] `useEffect` cleanup functions present for subscriptions, timers, AbortControllers
- [ ] No `useEffect` with empty deps just to run code once — consider event handlers instead
- [ ] Data fetching uses AbortController for race condition prevention
- [ ] No `useEffect` → `setState` patterns that cause render waterfalls
- [ ] `useLayoutEffect` only for DOM measurement (not general side effects)
- [ ] Fetch calls go through hooks (not raw `fetch()` in components)

### 5. PERFORMANCE PATTERNS
- [ ] `React.lazy()` + `<Suspense>` for route-level code splitting
- [ ] Heavy components wrapped in `Suspense` with meaningful fallbacks
- [ ] `useMemo` for expensive computations (not for simple values)
- [ ] `useCallback` for functions passed to memoized children
- [ ] No premature optimization (don't memo everything — profile first)
- [ ] Lists use stable `key` props (not array index for dynamic lists)
- [ ] Large lists use virtualization (`react-window` or similar) if > 100 items
- [ ] Images use `loading="lazy"` for below-fold content
- [ ] `useTransition` for non-urgent state updates (search, filtering)
- [ ] `useDeferredValue` for expensive re-renders triggered by fast-changing values
- [ ] React Compiler considered (auto-memoization) — check if `babel-plugin-react-compiler` is beneficial

### 6. COMPONENT PATTERNS
- [ ] Function components only (no class components in new code)
- [ ] Components are single-responsibility (not doing too many things)
- [ ] Custom hooks extract reusable logic from components
- [ ] No inline function definitions in JSX that create new references each render (when passed to memoized children)
- [ ] Conditional rendering uses early returns, not nested ternaries
- [ ] `children` prop used for composition over configuration
- [ ] `forwardRef` used when exposing DOM refs (or React 19's ref-as-prop)
- [ ] No `dangerouslySetInnerHTML` without sanitization

### 7. ERROR HANDLING
- [ ] Error boundary component exists and wraps routes/major sections
- [ ] Error boundaries show user-friendly fallback UI (not blank screen)
- [ ] Error boundaries report to Sentry or logging service
- [ ] Async errors caught in data fetching hooks (not just render errors)
- [ ] Network errors handled with retry/fallback UI
- [ ] Loading states shown during data fetching (`<Suspense>` or conditional)

### 8. TYPESCRIPT & TYPES
- [ ] Components typed with explicit props interfaces (not `any`)
- [ ] Event handlers properly typed (`React.MouseEvent`, `React.ChangeEvent`, etc.)
- [ ] `useState<Type>()` generic used when type can't be inferred
- [ ] No `@ts-ignore` or `@ts-expect-error` without explanation
- [ ] Custom hooks return properly typed values
- [ ] No `as` type assertions where type guards would be safer

### 9. REACT 19 FEATURES
- [ ] Using React 19+ (check `package.json` version)
- [ ] `use()` hook considered for reading promises/context in render
- [ ] `useActionState` considered for form actions with pending state
- [ ] `useOptimistic` considered for optimistic UI updates
- [ ] `ref` as prop works without `forwardRef` in React 19 — check if `forwardRef` can be removed
- [ ] `<form action={}>` considered for progressive enhancement
- [ ] Document metadata (`<title>`, `<meta>`) can be rendered directly in components (React 19)

### 10. ACCESSIBILITY (a11y)
- [ ] Interactive elements use semantic HTML (`<button>`, `<a>`, `<input>`)
- [ ] No `<div onClick>` without `role="button"`, `tabIndex`, and keyboard handler
- [ ] Form inputs have associated `<label>` elements
- [ ] `aria-label` on icon-only buttons
- [ ] Focus management after route changes
- [ ] `useId()` for generating unique IDs for accessibility attributes
- [ ] Skip-to-content link present
- [ ] Color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text)

## Output Format

```
## React Audit Report

### Score: X/10 dimensions passing

### Critical Issues
1. [DIMENSION] — [severity: CRITICAL/HIGH/MEDIUM/LOW] — description — file:line
   Current: `current code`
   Fix: specific fix with code

### Warnings
1. [DIMENSION] — description — file:line
   Recommendation: what to change

### Optimizations
1. [DIMENSION] — description — file:line
   Benefit: expected improvement

### Passing
- [DIMENSION] — what's working well

### Key Recommendations
(Top 3 highest-impact changes to make)
```
