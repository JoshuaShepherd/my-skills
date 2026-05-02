---
name: tailwind-cleanup
description: Scan and fix Tailwind anti-patterns — hardcoded colors, arbitrary values, inconsistent spacing, and dark/light mode issues.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Scan and fix Tailwind anti-patterns across the codebase.

Target: $ARGUMENTS

If no target is provided, scan `src/components/` and `src/`.

## Before Starting

1. Read the main CSS file (e.g., `src/index.css` or `src/app.css`) to understand existing CSS custom properties and tokens.
2. Read `vite.config.ts` and any Tailwind config to understand the current setup.

## Scan Checklist

Work through each category. For every violation, record the file, line number, the offending code, and a concrete fix.

### 1. HARDCODED COLORS (Critical)

Search for Tailwind palette colors used directly instead of semantic tokens:

```
bg-red-*, bg-blue-*, bg-green-*, text-red-*, text-blue-*, text-green-*, border-red-*, etc.
```

**Fix**: Replace with CSS custom property tokens or semantic class names. If no token exists, add one.

### 2. ARBITRARY VALUES (Warning)

Search for bracket notation that should be tokens:

```
w-[347px], h-[52px], text-[#hex], bg-[#hex], p-[13px], m-[7px]
```

**Fix**: Replace with nearest Tailwind spacing/sizing utility or create a token if reused.

Acceptable uses: one-off layout values, calc expressions, CSS variable references like `bg-[var(--color)]`.

### 3. INCONSISTENT SPACING

Search for spacing values that don't follow a consistent scale:

```
p-[13px], gap-[7px], m-[11px]
```

**Fix**: Round to nearest Tailwind spacing value (4px increments).

### 4. DARK/LIGHT MODE ISSUES

Search for color utilities missing dark mode counterparts:

```
bg-white (missing dark:bg-*)
text-black (missing dark:text-*)
border-gray-200 (missing dark:border-*)
```

**Fix**: Add `dark:` variants for all color utilities, or use CSS custom properties that handle both modes.

### 5. INLINE STYLES

Search for `style=` and `style={{` in JSX that could be Tailwind utilities:

```
style={{ color: '#xxx' }}
style={{ fontSize: '14px' }}
style={{ marginTop: '20px' }}
```

**Fix**: Replace with equivalent Tailwind class.

## Output Format

```
## Tailwind Cleanup Report

### Critical (must fix)
| File | Line | Issue | Fix |
|------|------|-------|-----|

### Warning (should fix)
| File | Line | Issue | Fix |
|------|------|-------|-----|

### Info (consider fixing)
| File | Line | Issue | Fix |
|------|------|-------|-----|
```

After reporting, apply all Critical and Warning fixes automatically.
