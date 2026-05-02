---
name: tailwind-cleanup
description: Scan and fix Tailwind anti-patterns — hardcoded colors, arbitrary values, raw HTML bypassing shadcn, layer violations, and dark/light mode issues. Enforces the D1→D6 token-first design chain.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Scan and fix Tailwind anti-patterns across the codebase, enforcing the token-first design chain (D1→D2→D3→D4→D5).

Target: $ARGUMENTS

If no target is provided, scan `src/components/` and `src/app/(public)/`.

## Before Starting

1. Read `src/app/globals.css` to load the current token inventory (`:root` + `.light` blocks).
2. Read `tailwind.config.ts` to load the semantic color map, spacing, and shadow tokens.
3. Read `_docs/design/DESIGN_CHAIN.md` for the authoritative layer rules.

## Scan Checklist

Work through each category. For every violation, record the file, line number, the offending code, and a concrete fix.

### 1. HARDCODED COLORS (Critical)

Search for Tailwind color utilities that bypass semantic tokens:

```
# Tailwind palette colors used directly (should be semantic tokens instead)
bg-red-*, bg-blue-*, bg-green-*, bg-yellow-*, bg-orange-*, bg-gray-*, bg-slate-*, bg-zinc-*, bg-neutral-*, bg-stone-*, bg-amber-*, bg-emerald-*, bg-teal-*, bg-cyan-*, bg-sky-*, bg-indigo-*, bg-violet-*, bg-purple-*, bg-fuchsia-*, bg-pink-*, bg-rose-*, bg-lime-*
text-red-*, text-blue-*, text-green-*, text-yellow-*, text-orange-*, text-gray-*, text-slate-*, text-zinc-*, text-neutral-*, text-stone-*, text-amber-*, text-emerald-*, text-teal-*, text-cyan-*, text-sky-*, text-indigo-*, text-violet-*, text-purple-*, text-fuchsia-*, text-pink-*, text-rose-*, text-lime-*
border-red-*, border-blue-*, border-green-*, border-yellow-*, border-orange-*, border-gray-*, border-slate-*, border-zinc-*, border-neutral-*, border-stone-*
from-*, via-*, to-* (gradient stops using palette colors)
```

Also search for:
- Inline hex values: `#[0-9a-fA-F]{3,8}` in className strings or style props
- Inline rgb/hsl: `rgb(`, `rgba(`, `hsl(`, `hsla(` in JSX (not globals.css)
- Arbitrary Tailwind values: `bg-[#`, `text-[#`, `border-[#`, `bg-[rgb`, `text-[hsl`

**Allowed exceptions:**
- `src/components/ui/*` (shadcn primitives — do not touch)
- `src/app/globals.css` (token definitions live here)
- `tailwind.config.ts` (theme mapping)
- SVG `fill`/`stroke` attributes using `currentColor`
- `bg-black`, `bg-white` ONLY when used with opacity modifiers for overlays (e.g. `bg-black/50`)
- Gradient stops using semantic tokens (`from-background`, `to-primary/10`)

**Semantic replacements:**
| Anti-pattern | Replace with |
|---|---|
| `bg-gray-900`, `bg-zinc-950`, `bg-neutral-900` | `bg-background` |
| `bg-gray-800`, `bg-zinc-900` | `bg-card` or `bg-secondary` |
| `bg-gray-100`, `bg-slate-50` | `bg-muted` or `bg-surface-light` |
| `text-gray-500`, `text-zinc-400` | `text-muted-foreground` |
| `text-gray-900`, `text-zinc-100` | `text-foreground` |
| `border-gray-200`, `border-zinc-800` | `border-border` |
| `bg-amber-*`, `bg-orange-*` (gold/brand) | `bg-primary` |
| `text-amber-*`, `text-orange-*` (gold/brand) | `text-primary` |
| `bg-red-*` (error) | `bg-destructive` |
| `bg-green-*` (success) | `bg-success` |

### 2. ARBITRARY VALUES (High)

Search for arbitrary Tailwind values that should be tokens:
- `w-[`, `h-[`, `p-[`, `m-[`, `gap-[`, `space-[` with pixel/rem values (should use spacing scale)
- `rounded-[` (should use `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-button`)
- `text-[` with size values (should use `text-body`, `text-small`, `text-h1`, etc.)
- `shadow-[` (should use `shadow-primary-glow*` or token-based shadows)
- `duration-[` (should use `duration-fast`, `duration-normal`, `duration-slow`)
- `z-[` with values > 50 (check if needed)

**Allowed:** Arbitrary values in `globals.css`, `clamp()` for responsive type, `calc()` for layout math.

### 3. RAW HTML INSTEAD OF SHADCN (Medium)

Search for raw HTML elements that should use shadcn components:
- `<button` without wrapping shadcn `Button` → use `<Button>` from `@/components/ui/button`
- `<input` without wrapping shadcn `Input` → use `<Input>` from `@/components/ui/input`
- `<select` → use `<Select>` from `@/components/ui/select`
- `<dialog` → use `<Dialog>` from `@/components/ui/dialog`
- `<table` → evaluate if `<Table>` from `@/components/ui/table` is appropriate
- Raw `<div>` acting as a card (with shadow + border + rounded) → use `<Card>` from `@/components/ui/card`

**Exceptions:**
- Form elements inside shadcn wrappers (e.g. Radix's internal `<button>`)
- `<button` in `src/components/ui/*` (shadcn internals)
- Semantic HTML elements used correctly (`<nav>`, `<header>`, `<main>`, `<section>`, `<article>`)

### 4. DESIGN CHAIN LAYER VIOLATIONS (Medium)

- **D3 importing from D5+:** Components importing from page files
- **D3 using raw fetch():** Components making API calls directly (should use hooks from D5)
- **Inline styles:** `style={{` in components (should use Tailwind classes or tokens)
- **!important in className:** Never use `!` prefix in Tailwind unless overriding a third-party library
- **Mixed spacing systems:** Same component using both Tailwind spacing (`p-4`) and raw CSS (`padding: 1rem`)
- **`border-l-4` content accents:** Should be `border-t-2 border-b-2 border-primary` (cinematic quote pattern per design charter). `border-l border-border` for structural dividers is fine.

### 5. DARK/LIGHT MODE ISSUES (Medium)

- Classes that only work in one theme: `dark:` prefixes without a light counterpart (or vice versa)
- Hardcoded `text-white` or `text-black` (should be `text-foreground` or `text-primary-foreground`)
- Background/text pairs that don't use matching semantic tokens (e.g. `bg-primary` without `text-primary-foreground`)
- Components missing dark mode consideration (no semantic tokens used at all)

### 6. TAILWIND BEST PRACTICES (Low)

- Duplicate utility classes in the same className
- Conflicting utilities (e.g. `p-4 p-6`, `flex block`)
- Overly long className strings (>200 chars) — consider extracting to a CSS class in globals.css or using `cn()` with conditionals
- `className` string concatenation without `cn()` utility (risk of duplicate/conflicting classes)

## Fixing Protocol

1. **Identify the correct layer** — Is this a token problem (D1), a primitive problem (D2), or a component problem (D3+)?
2. **Fix at the source layer** — If a needed semantic class doesn't exist, add the token to `globals.css` and map in `tailwind.config.ts` first.
3. **Never modify `src/components/ui/*`** — These are shadcn primitives. Fix via tokens or D3 wrappers.
4. **Test both themes** — After fixing, verify the component works in both dark and light mode.
5. **Batch similar fixes** — If the same anti-pattern appears in multiple files, fix all instances.

## Output Format

```
## Tailwind Cleanup Report

### Summary
- Files scanned: X
- Violations found: X (Critical: X, High: X, Medium: X, Low: X)
- Auto-fixed: X
- Manual review needed: X

### Violations by Category

#### 1. HARDCODED COLORS — X violations
| File | Line | Violation | Fix |
|------|------|-----------|-----|
| path/to/file.tsx | 42 | `bg-gray-900` | → `bg-background` |

#### 2. ARBITRARY VALUES — X violations
...

#### 3. RAW HTML — X violations
...

#### 4. LAYER VIOLATIONS — X violations
...

#### 5. DARK/LIGHT MODE — X violations
...

#### 6. BEST PRACTICES — X violations
...

### Files Modified
- path/to/file.tsx — X fixes applied
```

## Rules

- Always scan before fixing. Present the full report first, then apply fixes.
- Group fixes by file to minimize edits.
- If a fix requires a new token, document what token is needed and where to add it.
- Do not touch `src/components/ui/*`, `globals.css` token definitions, or `tailwind.config.ts` theme mappings unless adding new tokens.
- Preserve all existing functionality — these are cosmetic/token fixes only.
