# Static HTML docs (`docs/html/*`)

For self-contained reference pages outside the Vite bundle, mirror the live app tokens
from `src/index.css` `@theme` as CSS custom properties — **light-primary only** (no
`prefers-color-scheme` dark hijack).

## Token map

| App token | Hex | CSS variable |
|-----------|-----|--------------|
| `brand-violet` | `#14006a` | `--brand-violet` |
| `brand-lavender` | `#f0edff` | `--brand-lavender` |
| `workspace-bg-paper` | `#f4f4f1` | `--workspace-bg-paper` |
| `chrome-surface` | `#fafaf9` | `--chrome-surface` |
| `chrome-border` | `#e7e5e4` | `--border` |
| `chrome-muted` | `#78716c` | `--muted` |
| `community-sky` | `#0ea5e9` | `--sky` |
| `community-emerald` | `#10b981` | `--emerald` |
| `community-rose` | `#f43f5e` | `--rose` |

## Typography

Load via Google Fonts: Newsreader, Inter, Manrope (same as `src/index.css`).

| Role | Font | Pattern |
|------|------|---------|
| Literary titles | Newsreader | `font-weight: 300; font-style: italic; color: var(--brand-violet)` |
| Eyebrows / labels | Manrope | `font-size: 0.625rem; font-weight: 800; uppercase; letter-spacing: 0.2em` |
| Body | Inter | default sans |

## Surfaces (match HomeScreen)

- Page background: `--workspace-bg-paper` with a subtle violet radial wash
- Cards: white, `border: 1px solid rgba(20, 0, 106, 0.1)`, `border-radius: 1rem`, light shadow
- Sidebar TOC: white panel, `border-right: 1px solid var(--chrome-border)`
- Code blocks: dark panel (`#1c1917`) on light page — intentional contrast
- Focus: `outline: 2px solid var(--brand-violet); outline-offset: 2px`

## Reference implementation

`docs/html/orchestration/orchestration.css` — full styled companion to Trigger.dev docs.
