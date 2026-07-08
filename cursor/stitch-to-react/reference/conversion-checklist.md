# Conversion verification checklist

## Fetch & cache
- [ ] `.stitch/designs/{slug}.html` exists and is valid markup
- [ ] `.stitch/designs/{slug}.png` exists (full width via `=w{width}`)
- [ ] `.stitch/designs/{slug}.meta.json` has screenId, title, dimensions, fetchedAt

## Archive
- [ ] `page-old.tsx` exists with archive comment; default export removed/disabled
- [ ] No section component files overwritten

## Design chain docs (this screen only)
- [ ] `docs/design/stitch-screens/{slug}/README.md`
- [ ] `L1_TOKENS.md` — every Stitch color/font mapped to semantic var or marked net-new
- [ ] `L2_TAILWIND.md` — tailwind extensions documented
- [ ] `L3_PRIMITIVES.md` — shadcn composition map
- [ ] `L4_COMPONENTS.md` — section → file → hook table
- [ ] `L5_LAYOUTS.md` — route, shell, section order, feature gates

## Code quality
- [ ] `page.tsx` is Server Component (no `"use client"`)
- [ ] Data from Layer-5 hooks only; loading/empty/error handled
- [ ] No hardcoded hex or MD3 token names in TSX
- [ ] No hardcoded tenant strings — `tenantConfig`
- [ ] shadcn primitives used; `src/components/ui/*` untouched
- [ ] Lucide icons; no Material Symbols text nodes
- [ ] One `h1`; heading hierarchy correct
- [ ] Static color maps (no dynamic Tailwind class assembly)
- [ ] `pnpm typecheck` passes

## Visual
- [ ] Compared to cached PNG — layout, type scale, spacing rhythm match
- [ ] Dark mode OK (and light if tenant supports dual mode)

## Tracking
- [ ] `COMPONENT_CHECKLIST.md` updated to BUILT or PARTIAL
- [ ] Session report emitted
