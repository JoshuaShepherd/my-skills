
Add, replace, or audit icons using Lucide React: $ARGUMENTS

$ARGUMENTS should include:
- What icons are needed (by name, description, or category)
- Optionally: target component or page path
- Optionally: size, color, stroke width preferences
- Optionally: "audit" to scan for icon inconsistencies
- Empty — ask the user what they need

## Authoritative Documentation

### Primary References
- Lucide Homepage: https://lucide.dev/
- What is Lucide?: https://lucide.dev/guide/
- React Package Guide: https://lucide.dev/guide/packages/lucide-react
- Installation: https://lucide.dev/guide/installation

### Icon Browser & Categories
- All Icons: https://lucide.dev/icons/
- Icons by Category: https://lucide.dev/icons/categories

### Customization Guides
- Sizing: https://lucide.dev/guide/basics/sizing
- Color: https://lucide.dev/guide/basics/color
- Stroke Width: https://lucide.dev/guide/basics/stroke-width
- Global Styling: https://lucide.dev/guide/advanced/global-styling
- Accessibility: https://lucide.dev/guide/advanced/accessibility
- Icon Design Guide: https://lucide.dev/guide/design/icon-design-guide

### Source & Package
- GitHub: https://github.com/lucide-icons/lucide
- npm: https://www.npmjs.com/package/lucide-react

## Before Starting

1. Confirm `lucide-react` is installed — if not: `pnpm add lucide-react`
2. Check existing icon usage patterns in the codebase for consistency
3. Browse https://lucide.dev/icons/ to find the right icon by name or category

## Icon Props API

Every Lucide icon component accepts these props plus all standard SVG attributes:

| Prop | Type | Default | Description |
|---|---|---|---|
| `size` | `number \| string` | `24` | Width and height in pixels |
| `color` | `string` | `"currentColor"` | Stroke color (inherits from parent text color) |
| `strokeWidth` | `number` | `2` | SVG stroke width |
| `absoluteStrokeWidth` | `boolean` | `false` | When true, stroke width stays constant regardless of icon size |
| `className` | `string` | `""` | CSS classes applied to the SVG (all icons also get `lucide` class) |

## Import Patterns

### Named Imports (always use this for static icons)
```tsx
import { Camera, Home, ArrowRight, Menu } from "lucide-react";

<Camera size={24} />
<Home className="w-5 h-5 text-muted-foreground" />
```

### Dynamic Import (only when icon name comes from data/CMS)
```tsx
import { DynamicIcon } from "lucide-react/dynamic";

// Icon name from database or CMS field
<DynamicIcon name={iconNameFromDB} size={24} color="currentColor" />
```

### Custom Icon Creation
```tsx
import { createLucideIcon } from "lucide-react";

const CustomIcon = createLucideIcon("CustomIcon", [
  ["circle", { cx: "12", cy: "12", r: "10", key: "circle" }],
  ["line", { x1: "12", y1: "8", x2: "12", y2: "16", key: "line1" }],
]);
```

### Lab Icons (experimental)
```tsx
import { Icon } from "lucide-react";
import { someExperimentalIcon } from "@lucide/lab";

<Icon iconNode={someExperimentalIcon} size={24} />
```

## Tailwind Integration

Lucide icons use `currentColor`, so they inherit text color from Tailwind utilities:

```tsx
// Color via text utilities (preferred with Tailwind)
<Home className="text-primary" />
<Home className="text-muted-foreground" />

// Size via width/height utilities
<Home className="w-5 h-5" />
<Home className="w-8 h-8" />

// Stroke width via arbitrary value
<Home className="stroke-[1.5]" />

// Combined styling
<Home className="w-5 h-5 text-primary stroke-[1.5]" />

// Animation
<Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />

// Dark mode
<Sun className="w-5 h-5 text-yellow-500 dark:text-yellow-300" />

// Hover states
<Heart className="w-5 h-5 text-muted-foreground hover:text-destructive transition-colors" />
```

**Important:** Don't mix Tailwind classes and Lucide props for the same property. Pick one approach:
- **Tailwind approach** (preferred in Tailwind projects): `className="w-5 h-5 text-primary"`
- **Props approach**: `size={20} color="var(--primary)"`

## Sizing Standards

Maintain consistent icon sizes across the application:

| Context | Size | Tailwind | Props |
|---|---|---|---|
| Inline with text (body) | 16px | `w-4 h-4` | `size={16}` |
| Buttons (small) | 16px | `w-4 h-4` | `size={16}` |
| Buttons (default) | 20px | `w-5 h-5` | `size={20}` |
| Navigation items | 20px | `w-5 h-5` | `size={20}` |
| Card headers | 24px | `w-6 h-6` | `size={24}` |
| Feature icons | 32px | `w-8 h-8` | `size={32}` |
| Hero/decorative | 48px | `w-12 h-12` | `size={48}` |
| Empty states | 48-64px | `w-12 h-12` to `w-16 h-16` | `size={48}` to `size={64}` |

## Accessibility Rules

| Scenario | Pattern |
|---|---|
| **Icon next to text** (decorative) | No label needed — icon is visual reinforcement |
| **Icon-only button** | Put `aria-label` on the **button**, NOT the icon |
| **Standalone meaningful icon** | Use visually-hidden text span alongside |
| **Interactive icon** | Always wrap in `<button>` with min 44x44px target |

```tsx
// Icon-only button — correct
<button aria-label="Close dialog" className="p-2">
  <X className="w-5 h-5" />
</button>

// Icon with visible text — no extra label needed
<button className="flex items-center gap-2">
  <Download className="w-4 h-4" />
  Download
</button>

// Standalone meaningful icon
<span className="inline-flex items-center gap-1">
  <Mail className="w-4 h-4" />
  <span className="sr-only">Email</span>
</span>
```

## Bundle Optimization

| Strategy | Impact |
|---|---|
| Named imports (`import { X } from "lucide-react"`) | ~1KB per icon, tree-shakes unused |
| Next.js | Pre-configured in `optimizePackageImports` — automatic |
| Vite dev mode | Can be slow with barrel imports; configure aliases if needed |
| DynamicIcon | Creates separate network requests — only for data-driven icons |

**Never do:**
```tsx
// This defeats tree-shaking — imports ALL 1700+ icons
import * as icons from "lucide-react";
```

## Global Styling

Target all Lucide icons with the `.lucide` class:

```css
/* In globals.css */
.lucide {
  width: 1em;
  height: 1em;
  stroke-width: 1.75;
}
```

## Common Icon Selections by Category

### Navigation
`Menu`, `X`, `ChevronDown`, `ChevronRight`, `ChevronLeft`, `ArrowLeft`, `ArrowRight`, `Home`, `Search`, `ExternalLink`

### Actions
`Plus`, `Minus`, `Edit`, `Trash2`, `Copy`, `Download`, `Upload`, `Share2`, `MoreHorizontal`, `MoreVertical`, `RefreshCw`

### Status & Feedback
`Check`, `CheckCircle`, `AlertTriangle`, `AlertCircle`, `Info`, `XCircle`, `Loader2`, `Clock`, `Ban`

### Content & Media
`FileText`, `Image`, `Video`, `Music`, `BookOpen`, `Bookmark`, `Link`, `Paperclip`, `Quote`

### Communication
`Mail`, `MessageSquare`, `MessageCircle`, `Phone`, `Send`, `Bell`, `BellRing`

### Users & Social
`User`, `Users`, `UserPlus`, `Heart`, `ThumbsUp`, `Star`, `Award`

### Layout & UI
`LayoutDashboard`, `Grid`, `List`, `Columns`, `SidebarOpen`, `PanelLeft`, `Maximize`, `Minimize`

### Settings & Tools
`Settings`, `Sliders`, `Filter`, `SlidersHorizontal`, `Wrench`, `Shield`, `Lock`, `Unlock`, `Key`, `Eye`, `EyeOff`

## Audit Checklist

When auditing icon usage, check for:

1. **Consistency** — Same concept uses the same icon everywhere (e.g., "edit" is always `Edit`, not sometimes `Pencil`)
2. **Size consistency** — Icons in the same context use the same size
3. **Color consistency** — Icons use semantic tokens (`text-muted-foreground`, `text-primary`), not hardcoded colors
4. **Stroke width consistency** — All icons use the same stroke width (default 2, or project standard)
5. **Accessibility** — Icon-only buttons have `aria-label` on the button
6. **Import style** — All using named imports, no `import *`
7. **No mixing** — Not mixing Lucide props and Tailwind classes for the same property
8. **Tap targets** — Interactive icons wrapped in buttons with min 44x44px target

## Output Format

```
## Icon Implementation Report

### Icons Added/Changed
| Location | Icon | Size | Notes |
|---|---|---|---|
| components/nav.tsx:12 | Menu → MenuIcon | w-5 h-5 | Renamed for clarity |

### Audit Findings (if auditing)
- ✅ Consistent sizing in navigation
- ⚠️ 3 icon-only buttons missing aria-label
- ❌ Hardcoded color on Settings icon in sidebar

### Changes Made
- path/to/file.tsx — replaced X with Y
```

## Rules

- Always use named imports — never `import *`
- Use Tailwind classes for sizing/color in Tailwind projects — don't mix with props
- Icon-only buttons must have `aria-label` on the `<button>`, not the icon
- Maintain consistent icon sizes per context (see sizing standards table)
- Use `Loader2` with `animate-spin` for loading states (not `Loader`)
- Icons are decorative when next to visible text — no extra labeling needed
- Use `DynamicIcon` only when icon names come from external data
- Browse https://lucide.dev/icons/ to verify icon names before using
