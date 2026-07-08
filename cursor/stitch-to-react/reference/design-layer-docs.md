# Design layer documentation (per Stitch screen)

Write **only what this screen introduces or uses** under:

```
docs/design/stitch-screens/{slug}/
  README.md           # stitch IDs, route, date, status
  L1_TOKENS.md
  L2_TAILWIND.md
  L3_PRIMITIVES.md
  L4_COMPONENTS.md
  L5_LAYOUTS.md
```

Do not overwrite `docs/design/layers/` global docs unless the user explicitly asks. Cross-link to global docs when reusing existing tokens.

---

## README.md

```markdown
# Stitch screen: {title}

| Field | Value |
|-------|-------|
| Screen ID | `projects/{projectId}/screens/{screenId}` |
| Cache slug | `{slug}` |
| Target route | `/path` |
| Converted | {ISO date} |
| Status | BUILT \| PARTIAL |
| Color mode | dark \| light \| dual |

## Cache
- `.stitch/designs/{slug}.html`
- `.stitch/designs/{slug}.png`

## Production files
- `src/app/(public)/…/page.tsx`
- `src/components/{area}/…`
```

---

## L1_TOKENS.md

Document **Stitch source → semantic CSS variable** mapping for this screen.

```markdown
# L1 — Tokens ({slug})

**Stitch source:** embedded tailwind.config in `.stitch/designs/{slug}.html`
**Applied in:** `src/app/globals.css` (list selectors changed)

## Color mapping

| Stitch / MD3 name | Hex/HSL in wireframe | Semantic var | Applied class |
|-------------------|----------------------|--------------|---------------|
| surface | #131313 | `--background` | `bg-background` |
| primary | … | `--primary` | `bg-primary` |

## Typography

| Stitch font key | Production var | Tailwind key |
|-----------------|----------------|--------------|
| headlineFont | `--font-display` | `font-display` |

## Layout / radius

| Stitch token | CSS var / value |
|--------------|-----------------|
| ROUND_FOUR | `--radius: 0.25rem` |

## Effect utilities (if any)

| Class | Purpose | Defined in |
|-------|---------|------------|
| `.text-gradient-gold` | hero emphasis | globals.css @layer utilities |

## Dual mode

Note light (`:root`) and dark (`.dark`) values if both exist.

## Net-new tokens

List any vars **added** by this screen (or "None — mapped to existing semantics").
```

---

## L2_TAILWIND.md

```markdown
# L2 — Tailwind ({slug})

**Changed files:** `tailwind.config.ts` (or "None")

## Font size extensions

| Key | Size/lh/weight | Stitch name | Used in |
|-----|----------------|-------------|---------|

## Spacing extensions

| Key | Value | Stitch source | Used in |

## Max width / container

| Key | Value |

## Plugins / animations

Note any tailwindcss-animate classes used (`animate-in`, etc.).

## Anti-patterns avoided

- No hex in config
- No MD3 color keys (`surface-container-high`)
```

---

## L3_PRIMITIVES.md

```markdown
# L3 — Primitives ({slug})

**Rule:** shadcn files in `src/components/ui/` are read-only. This doc records **how this screen composes them**.

## Primitive usage map

| Stitch element | shadcn primitive | Variant / class overrides |
|----------------|------------------|---------------------------|
| Primary CTA | Button | `rounded-none px-8 py-4 text-headline-md` |
| FAQ block | Accordion | default |
| Mobile menu | Sheet | — |

## Icon mapping

| Stitch icon font | lucide-react |
|------------------|--------------|
| search | `Search` |

## Patterns not in shadcn

Hand-rolled div modules → note whether production uses `<Card>` or custom div + tokens.
```

---

## L4_COMPONENTS.md

```markdown
# L4 — Components ({slug})

## Section map

| Order | Stitch section name | Component | Path | Status | Hook |
|-------|---------------------|-----------|------|--------|------|
| 1 | Hero Section | Hero | `src/components/home/hero.tsx` | BUILT | tenantConfig |

## Component notes

### Hero
- Server Component
- Props: …
- Key classes: …
- Stitch comment ids preserved: …

(repeat per section)

## Shared with other routes

List components reused from prior conversions.
```

---

## L5_LAYOUTS.md

```markdown
# L5 — Layout ({slug})

## Route

`src/app/(public)/{route}/page.tsx`

## Shell

Cinematic standard | Chat fullscreen | Immersive | Course hub

## Section stack (render order)

1. Hero
2. …

## Feature gates

| Section | Flag |
|---------|------|
| AILabTeaser | `features.chat` |

## Responsive behavior

| Breakpoint | Layout change |

## Archive

`page-old.tsx` — preserved until verified
```
