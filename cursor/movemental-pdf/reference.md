# Movemental PDF — Reference

## CSS defaults (embedded in script)

- Page: `@page { size: letter; margin: 1in; }`
- Body: Georgia, 11pt, line-height 1.6, color `#1a1a1a`
- H1–H3: system sans-serif, `#2c3e50`
- Tables: bordered, header background `#f5f5f5`
- Page breaks: before each Part H1; `page-break-inside: avoid` on tables, blockquotes, pre

## Cover page fields

| Field | Source |
|-------|--------|
| Title | Leader display name from voice/themes H1 |
| Subtitle | `Voice & Themes` |
| Footer line | `Movemental · Generated {YYYY-MM-DD}` |

## Filename convention

`{Display Name} — Voice & Themes.pdf` on Desktop unless `--output` overrides.

## Related skills

- `pdf-ebook` — generic markdown→PDF (my-skills `claude/assets/pdf-ebook`)
- `movement-leader-voice` — authors `docs/voice/`
- `movement-leader-themes` — authors `docs/themes/`
