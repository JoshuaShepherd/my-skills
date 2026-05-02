---
name: design-section
description: Design a new UI section or component for movemental using DESIGN.md conventions — tonal stacking, primitives, semantic tokens, and the Stitch-informed editorial style.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Design and implement a UI section using movemental's Digital Curator design system.

Section request: $ARGUMENTS

## Before Starting

1. Read `docs/design/DESIGN.md` — the canonical design spec.
2. Read `src/components/primitives/index.ts` — available primitives.
3. Read `src/app/globals.css` — token inventory.
4. If the section has a Stitch source, read the relevant HTML in `docs/build/stitch/`.

## Design Dimensions

### 1. TONAL LAYER
Choose the section's background variant:
- `variant="default"` — `bg-background` (#f7f9fb) — the airy base
- `variant="section"` — `bg-section` (#f0f4f7) — tonal shift for alternating sections
- `variant="elevated"` — `bg-elevated` (#e1e9ee) — accent band for testimonials, callouts
- `variant="midnight"` — `bg-inverse-surface` (#101820) — dark hero/proof sections

### 2. STRUCTURE
Every section follows the pattern:
```tsx
<Section variant="..." spacing="sm|lg">
  <Container>
    <Eyebrow>Section label</Eyebrow>
    <Display size="md" as="h2">Heading</Display>
    <Prose>Body text</Prose>
    {/* Content: cards, grids, splits */}
  </Container>
</Section>
```

### 3. CONTENT PATTERNS
- **Feature Split:** `<FeatureSplit intro={...}>{content}</FeatureSplit>` — narrow intro + wide content
- **Card Grid:** `<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">` with `<SurfaceCard>`
- **Stat Callout:** Large number + label in a `bg-primary/5` rounded container
- **Before/After:** Two `<SurfaceCard>` side by side with contrasting content
- **Numbered Steps:** Data array mapped with `<SurfaceCard>` and step numbers

### 4. CARD TONES
Match card tone to parent section:
- On `variant="default"` → `<SurfaceCard tone="on-background">`
- On `variant="section"` → `<SurfaceCard tone="on-section">`
- On `variant="midnight"` → `<SurfaceCard tone="midnight">`

### 5. STYLE RULES
- **No borders for sectioning** — use tonal stacking
- **No decorative shadows** — only `shadow-ambient` or Ghost Lift (tonal)
- **Primary is a light-switch** — `#0053db` for CTAs and highlights only
- **Never pure black** — use `text-foreground` or `bg-inverse-surface`
- **Inter only** — no other fonts
- **Breathing layout** — if crowded, increase padding, never shrink type

## Implementation

1. Outline the component tree in a comment at the top of the file
2. Write the JSX using primitives and semantic tokens
3. Extract data into `const` arrays at the top of the file
4. Run `pnpm typecheck` after implementation

## Output

A complete, production-ready React Server Component using movemental primitives and DESIGN.md tokens. No `"use client"` unless the section genuinely requires interactivity.
