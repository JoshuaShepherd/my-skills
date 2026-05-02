---
name: tailwind-cleanup
description: Scan and fix Tailwind anti-patterns for movemental — hardcoded colors, arbitrary values, raw HTML bypassing shadcn/primitives, border violations, and non-semantic tokens. Enforces DESIGN.md token-first design.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Scan and fix Tailwind anti-patterns across the movemental codebase, enforcing DESIGN.md token-first design.

Target: $ARGUMENTS

If no target is provided, scan `src/components/` and `src/app/(site)/`.

## Before Starting

1. Read `src/app/globals.css` — load the token inventory (`@theme inline` + `:root`).
2. Read `docs/design/DESIGN.md` — the authoritative design spec.
3. Read `docs/build/prompts/stitch-to-react-migration.md` §7 — the Stitch→DESIGN.md translation table.

## Scan Checklist

### 1. HARDCODED COLORS (Critical)

Search for Tailwind color utilities that bypass semantic tokens:

**Banned patterns:**
- `bg-white`, `bg-black` → `bg-card` / `bg-inverse-surface`
- `text-white` → `text-inverse-foreground` (only in midnight sections) or `text-primary-foreground`
- `text-black` → `text-foreground`
- `bg-blue-*`, `text-blue-*` → `bg-primary` / `text-primary`
- `bg-gray-*`, `text-gray-*`, `bg-slate-*`, `text-slate-*` → semantic tokens
- Arbitrary hex: `bg-[#...]`, `text-[#...]`, `border-[#...]`
- Inline rgb/hsl in className or style props

**Movemental translation table (from migration prompt §7):**

| Anti-pattern | Replace with |
|---|---|
| `bg-white`, `bg-[#ffffff]` | `bg-card` (on cards) or `bg-popover` |
| `bg-[#f7f9fb]` | `bg-background` |
| `bg-[#f0f4f7]` | `bg-section` or `bg-muted` |
| `bg-[#e1e9ee]` | `bg-elevated` or `bg-secondary` |
| `bg-[#0053db]`, `bg-blue-600` | `bg-primary` |
| `bg-[#101820]`, `bg-black` | `bg-inverse-surface` |
| `text-[#2a3439]` | `text-foreground` |
| `text-[#566166]`, `text-gray-500` | `text-muted-foreground` |
| `text-white` (on dark sections) | `text-inverse-foreground` |

**Allowed exceptions:**
- `src/components/ui/*` (shadcn primitives — do not touch)
- `src/app/globals.css` (token definitions)
- SVG `fill`/`stroke` using `currentColor`
- Opacity modifiers on semantic tokens: `bg-primary/10`, `text-inverse-foreground/55`

### 2. BORDER VIOLATIONS (Critical — DESIGN.md §3.1)

Search for decorative borders used for section separation:
- `border-b`, `border-t`, `divide-y`, `divide-x` between sections → **remove** and use tonal stacking
- Allowed: `border-border` on form inputs, `border-primary` for accent on quotes/callouts

### 3. SHADOW VIOLATIONS (High)

- `shadow-sm`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl` → **remove** or replace with `shadow-ambient`
- Only `shadow-ambient` (defined in globals.css) or tonal stacking (Ghost Lift)

### 4. ARBITRARY VALUES (High)

- `w-[`, `h-[`, `p-[`, `m-[`, `gap-[` with pixel/rem values → use Tailwind spacing scale
- `rounded-[` → use `rounded-md` (matches `--radius: 0.375rem`)
- `text-[` with size values → use standard Tailwind scale or Display/Eyebrow primitives
- `shadow-[` → use `shadow-ambient` token

**Allowed:** `clamp()` for responsive type, `calc()` for layout math, values in `globals.css`.

### 5. RAW HTML INSTEAD OF PRIMITIVES (Medium)

Search for patterns that should use movemental primitives:
- `<section` with manual bg/padding → `<Section variant="...">` primitive
- `<div` with `max-w-*` + `mx-auto` + `px-*` → `<Container>` primitive
- Large bold headings with manual tracking → `<Display size="...">` primitive
- Uppercase small labels → `<Eyebrow>` primitive
- Long-form text blocks → `<Prose>` primitive
- Cards with shadow + rounded → `<SurfaceCard tone="...">` primitive
- Raw `<button` → `<Button>` from shadcn

### 6. DARK MODE VIOLATIONS (Medium)

- No `dark:` prefixes should exist — movemental is light-primary only
- `class="dark"` on any element → remove (midnight is via Section variant, not class toggle)
- `text-white` outside a `variant="midnight"` context → `text-inverse-foreground` inside midnight, or `text-primary-foreground` on primary backgrounds

### 7. TAILWIND V4 BEST PRACTICES (Low)

- `aspect-[4/5]` → `aspect-4/5` (canonical Tailwind v4)
- `bg-gradient-to-*` → `bg-linear-to-*` (Tailwind v4)
- Duplicate utility classes
- Conflicting utilities (`p-4 p-6`, `flex block`)
- `className` concatenation without `cn()` utility

## Fixing Protocol

1. **Fix at the source layer** — If a needed token doesn't exist, add it to `globals.css` `@theme inline` first.
2. **Never modify `src/components/ui/*`** — These are shadcn primitives.
3. **Batch similar fixes** — If the same anti-pattern appears in multiple files, fix all instances.
4. **Verify after fixing** — Run `pnpm typecheck` after changes.

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

#### 2. BORDER VIOLATIONS — X violations
...

[Continue for all categories]

### Files Modified
- path/to/file.tsx — X fixes applied
```

## Rules

- Always scan before fixing. Present the full report first, then apply fixes.
- Group fixes by file to minimize edits.
- Do not touch `src/components/ui/*`, `globals.css` definitions, or Stitch source files in `docs/build/stitch/`.
- This is a light-primary site. There is NO global dark mode. Midnight is regional via `<Section variant="midnight">`.
