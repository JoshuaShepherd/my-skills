# ZenWrite Tokens & Design Chain — portable summary

A condensed mirror of `docs/design/` (layers 01–05). **When the ZenWrite repo is present, its
`docs/design/` + `src/index.css` `@theme` block are the live source of truth and win over this file.**

## The chain

```
Tokens → Primitives → Components → Built Components → Patterns & Layouts
```

| Layer | What | Source of truth |
|-------|------|-----------------|
| Tokens | colors, type, spacing, motion, surfaces | `src/index.css` `@theme` |
| Primitives | chips, states, nav chrome, page header | `src/components/` (StatusChip, VoiceFidelityChip, StateLayouts, BottomNav, ViewPageHeader) |
| Components | panels, palettes, wizards, toolbars | `src/components/*Panel.tsx`, `CommandPalette`, `*Wizard.tsx` |
| Built | full screens & major surfaces | `*Screen.tsx`, `Editor`, `MediaSurface`, `PublishPanel` |
| Patterns | shells, overlays, nav, idle-fade | `src/App.tsx` conventions |

## Philosophy

Light-primary, distraction-free scholarly sanctuary. (1) Minimize cognitive load — chrome fades
while writing, the manuscript is the hero. (2) Separate two spheres — content (violet) vs community
(sky/emerald/rose). (3) Pair type deliberately — Newsreader serif for literary, Inter/Manrope for
functional UI. (4) Never let OS dark mode hijack — `dark:` scoped to `.dark` ancestors only.

## Typography tokens

| Utility | Font | Use |
|---------|------|-----|
| `font-serif` | Newsreader | body, titles, literary headings, empty states |
| `font-sans` | Inter | general UI, editor chrome labels |
| `font-manrope` | Manrope | eyebrows, uppercase labels, chips, metrics |

Cadence patterns:
- Literary heading: `font-serif font-light italic tracking-tight`
- Panel/section title: `font-serif text-lg font-light italic text-brand-violet` (panels) /
  `font-serif text-2xl font-light italic text-brand-violet tracking-tight` (sections)
- Functional eyebrow: `font-manrope text-[10px] font-extrabold uppercase tracking-[0.25em]`
- Chip label: `text-[9px] font-manrope font-bold uppercase tracking-wider`

## Color tokens (semantic — use these, never raw hex)

**Brand / content sphere**
| Token | Hex | Role |
|-------|-----|------|
| `brand-violet` | `#14006a` | primary content accent, borders, focus rings, CTAs |
| `brand-sand` | `#fed488` | warm highlight (sparingly) |
| `brand-lavender` | `#f0edff` | soft violet wash backgrounds, scheduled chips |
| `brand-violet-muted` | `#37285e` | secondary violet body text |
| `brand-plum` | `#37203b` | deep plum panel/publish titles |
| `brand-lavender-line` | `#b5a8c4` | lavender-gray dividers / hairlines |
| `brand-lavender-bright` | `#c9beff` | inline-edit highlight, dots |
| `brand-lavender-hover` | `#e0dbff` | lavender button hover fill |

**App chrome surfaces**
| Token | Hex | Role |
|-------|-----|------|
| `surface-warm` | `#fcf9f8` | warm paper panel / context-bar bg |
| `surface-warm-sunk` | `#fbf9f4` | recessed cream — cards, inputs, row hovers |
| `surface-ink` | `#111118` | elevated dark panel (scoped `dark:` only) |

**Editor theme surfaces** (from `EditorSettings.theme`)
| Theme | bg / text utilities |
|-------|---------------------|
| `paper` | `bg-workspace-bg-paper text-workspace-text-paper` (`#f4f4f1` / `#1a1a1a`) |
| `sepia` | `bg-workspace-bg-sepia text-workspace-text-sepia` (`#eae8e3` / `#2c2b29`) |
| `ink` | `bg-workspace-bg-ink text-workspace-text-ink` (`#14141b` / `#e2e2e8`) |

**Community sphere**
| Token | Hex | View |
|-------|-----|------|
| `community-sky` | `#0ea5e9` | Engage, Kairos |
| `community-emerald` | `#10b981` | Manage |
| `community-rose` | `#f43f5e` | Analyze |

All tokens accept opacity modifiers: `border-brand-violet/10`, `bg-sky-500/[0.06]`, etc.

## Dual spheres & view accents

| View | Sphere | Accent |
|------|--------|--------|
| `home`, `create`, `organize` | content | violet |
| `engage`, `kairos` | community | sky |
| `manage` | community | emerald |
| `analyze` | community | rose |

Resolve community accents at runtime from `src/lib/viewAccents.ts`:
`getViewAccent(view)` returns a profile (`icon`, `title`, `eyebrow`, `headerBorder`, `tabActive`,
`navActive`, `tileHover`, `statValue`, `pageWash`, …); `navItemClasses(view, isActive)` for nav.
Use `ViewPageHeader view="..."` for screen titles. **Exempt from view-accent recolor:** Editor,
MediaSurface, PublishPanel (they keep their own treatment).

**70 / 20 / 10:** accent-bearing = page headers, active nav items, active tab pills, home-tile
icons/hovers, decorative stat highlights. Shared (violet/neutral) = card shells, table bodies,
primary CTAs (`bg-brand-violet`), focus rings.

## Motion / spacing conventions

| Pattern | Classes |
|---------|---------|
| Enter | `animate-in fade-in duration-300` |
| Slide-in panel | `animate-in slide-in-from-right duration-300` |
| Modal/palette | `animate-in zoom-in-95` |
| Hover lift | `hover:-translate-y-0.5 hover:shadow-md` |
| Transition | `transition-all duration-200` |
| Idle fade (editor chrome) | `transition-all duration-700 opacity-0` |

| Convention | Value |
|------------|-------|
| Page width | `max-w-7xl mx-auto` |
| Page padding | `px-6 py-8` (or `py-12` on home) |
| Section gap | `space-y-8`; list gap `space-y-3` |
| Card radius | `rounded-2xl` |
| Default card border | `border-brand-violet/10` |
| Slide-in width | `w-full max-w-md`; wizard `max-w-lg` |

## Overlay z-index stack

| Layer | z |
|-------|---|
| slide-in backdrop | `z-40` |
| slide-in panel | `z-50` |
| PublishPanel | `z-[60]` |
| CommandPalette | `z-[70]` |

## Token hygiene rules

1. New tokens go in `@theme` in `src/index.css` only, named `brand-` / `workspace-` /
   `community-` / `surface-`.
2. Never assemble dynamic Tailwind color strings — static maps only.
3. Verify WCAG contrast (`docs/build/prompts/color_audit_checklist.md`): ≥4.5:1 small text,
   ≥3:1 UI controls / focus rings. `brand-violet` on dark surfaces fails → `dark:text-indigo-300`.
