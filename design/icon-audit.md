
Audit and fix icon and illustration anti-patterns across the codebase.

Target: $ARGUMENTS

If no target is provided, scan `src/components/` and `src/app/`.

## Before Starting

1. Read the global CSS file to confirm the current semantic color token inventory.
2. Read `{{ICON_WRAPPER_PATH}}` (e.g., `src/components/ui/icon.tsx`) if it exists — this is the canonical Icon wrapper. If it doesn't exist, note it as a critical gap.
3. Check which icon libraries are installed by searching `package.json`.

## Scan Checklist

### 1. MIXED ICON LIBRARIES (Critical)

The project should use **one icon library only** (e.g., Lucide React). Any other icon library is a violation.

Search for:
- `from '@heroicons/react'`
- `from 'react-icons'`
- `from 'phosphor-react'`
- `from '@radix-ui/react-icons'` — allowed ONLY inside `src/components/ui/*` (component library internals)
- `from 'feather-icons'`
- Any `<svg>` with inline path data that duplicates an icon from the primary library

**Fix:** Replace with the equivalent icon from the project's primary library.

### 2. RAW ICON USAGE (High)

Icons should always be used via the canonical `<Icon>` wrapper, not imported and rendered directly. Raw usage bypasses the size scale, accessibility defaults, and flex-compression guard.

Search for patterns like:
```
import { ArrowRight, Check, X } from 'lucide-react'
// then used as: <ArrowRight className="w-4 h-4" />
```

**Allowed exception:** Inside `src/components/ui/*` (component library primitives) and the Icon wrapper itself.

**Fix:** Replace `<IconName className="w-N h-N" />` with `<Icon icon={IconName} size="sm" />`.

### 3. ARBITRARY ICON SIZES (High)

Icons must use the canonical size token scale, not arbitrary pixel values:

| Token | Size | Use case |
|-------|------|----------|
| `xs`  | 12px | Captions, badges, inline metadata |
| `sm`  | 16px | Inline text, form labels, table cells |
| `md`  | 20px | Default UI, buttons, nav items |
| `lg`  | 24px | Section headers, card actions, prominent UI |
| `xl`  | 32px | Empty states, feature highlights |
| `2xl` | 48px | Hero sections, marketing, onboarding |

Search for:
- `w-[` or `h-[` with pixel values applied to icon elements
- `w-3 h-3`, `w-5 h-5`, `w-6 h-6`, `w-7 h-7`, `w-8 h-8`, `w-10 h-10` — these bypass the token scale
- `size={` with numeric values other than 12, 16, 20, 24, 32, 48

**Fix:** Replace with the `<Icon size="md">` pattern.

### 4. HARDCODED ICON COLORS (High)

Icons must inherit their color from the surrounding text context via `currentColor`. Never set a specific color on an icon.

Search for:
- `text-blue-*`, `text-gray-*`, `text-red-*` etc. on icon elements (should be semantic: `text-muted-foreground`, `text-primary`, `text-destructive`)
- `fill="` or `stroke="` with hex values or named colors (not `currentColor`) in inline SVGs
- `color=` prop on icon components

**Fix:** Remove the color class from the icon; apply it to the parent container using semantic tokens instead. Or, if only the icon needs color, use `text-primary`, `text-muted-foreground`, `text-destructive`.

### 5. MISSING FLEX-COMPRESSION GUARD (Medium)

Icons inside flex or grid containers will compress if `shrink-0` is missing.

Search for icon elements (or `<Icon>` wrapper usages) inside:
- `flex` containers without `shrink-0` on the icon
- `items-center` rows where the icon is a sibling of text

**Fix:** Add `shrink-0` to the icon's className (the `<Icon>` wrapper applies this automatically when used correctly).

### 6. ACCESSIBILITY VIOLATIONS (High)

**Pattern 1 — Decorative icons (no meaning without adjacent text):**
```tsx
// Correct
<Icon icon={Check} size="md" aria-hidden />
<span>Saved</span>

// Wrong — icon has no label, no aria-hidden
<CheckIcon className="w-5 h-5" />
<span>Saved</span>
```

**Pattern 2 — Icon-only buttons (icon IS the only affordance):**
```tsx
// Correct
<Button variant="ghost" size="icon" aria-label="Close dialog">
  <Icon icon={X} size="md" aria-hidden />
</Button>

// Wrong — no label, screen reader reads nothing useful
<button onClick={onClose}>
  <XIcon className="w-5 h-5" />
</button>
```

**Pattern 3 — Standalone meaningful icons (rare — chart markers, status indicators):**
```tsx
// Correct
<Icon icon={AlertTriangle} size="md" label="Warning" />

// Or for SVG illustrations:
<svg role="img" aria-label="Empty inbox illustration">
  <title>Empty inbox illustration</title>
  ...
</svg>
```

Search for:
- Icon-only `<button>` elements without `aria-label`
- `<Button size="icon">` without `aria-label`
- Icon elements that are the sole content of a clickable element, with no accessible label

### 7. ILLUSTRATION ANTI-PATTERNS (Medium)

Illustrations are larger SVGs used for empty states, onboarding, marketing sections, and feature highlights. They follow different rules from icons.

Search for:
- `<img src="*.png">` or `<img src="*.jpg">` used for illustrations (should be SVG)
- Inline SVG without `role="img"` and `<title>` (if it conveys meaning)
- SVG files that embed hardcoded hex colors (should use CSS custom properties to inherit theme)
- Illustrations that don't have a dark-mode variant or don't use `currentColor`/CSS vars
- `<img>` elements with empty or missing `alt` attribute
- Raster PNGs in illustration directories that could be SVG

**Fix per case:**
- Replace PNG illustrations with SVG equivalents
- Add `role="img"` + `<title>` to meaningful inline SVGs
- For decorative illustrations: `aria-hidden="true"` or `alt=""`
- Refactor hardcoded SVG colors to use `currentColor` or CSS custom properties

### 8. STROKE WEIGHT CONSISTENCY (Low)

Icons that default to `strokeWidth={2}` look best at UI sizes. At `xl` / `2xl` sizes used in marketing sections, `strokeWidth={1.5}` looks more refined. Never mix stroke weights in the same UI region.

Search for `strokeWidth=` props on icons and verify they follow the pattern:
- `xs`-`lg` sizes: `strokeWidth={2}` (default, can omit)
- `xl`-`2xl` sizes: `strokeWidth={1.5}` preferred

## Fixing Protocol

1. **Read each file first** before editing.
2. **Fix critical issues first** (mixed libraries, a11y), then high, then medium, then low.
3. **Never modify component library internals** (e.g., `src/components/ui/*` shadcn files).
4. **Batch edits per file** — fix all issues in a file in one edit.
5. **If `<Icon>` wrapper doesn't exist**, note it for `/icon-system` to create — don't create it inline here.

## Output Format

```
## Icon & Illustration Audit Report

### Summary
- Files scanned: X
- Violations found: X (Critical: X, High: X, Medium: X, Low: X)
- Auto-fixed: X
- Manual review needed: X

### Critical: Icon Wrapper Missing
[ ] {{ICON_WRAPPER_PATH}} does not exist -> Run /icon-system to create it

### Violations by Category

#### 1. MIXED LIBRARIES — X violations
| File | Line | Violation | Fix |
|------|------|-----------|-----|

#### 2. RAW ICON USAGE — X violations
| File | Line | Violation | Fix |
|------|------|-----------|-----|

#### 3. ARBITRARY SIZES — X violations
...

#### 4. HARDCODED COLORS — X violations
...

#### 5. FLEX COMPRESSION — X violations
...

#### 6. ACCESSIBILITY — X violations
...

#### 7. ILLUSTRATIONS — X violations
...

#### 8. STROKE WEIGHT — X violations
...

### Files Modified
- path/to/file.tsx — X fixes applied

### Remaining Manual Work
- Items that require design decisions or new assets
```
