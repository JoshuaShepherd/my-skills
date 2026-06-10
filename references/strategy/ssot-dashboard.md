# SSOT Dashboard

Design and structure a living Single Source of Truth dashboard (HTML/CSS/JS). Creates a navigable, well-designed dashboard that aligns project documentation into one canonical view for both humans and AI agents.

## Configuration

| Variable | Description |
|----------|-------------|
| `{{PROJECT_NAME}}` | Name of the project/platform |
| `{{DOCS_ROOT}}` | Path to project documentation (e.g. `_docs/`) |
| `{{DASHBOARD_ROOT}}` | Path to dashboard output files (e.g. `ssot-dashboard/`) |
| `{{BRAND_PRIMARY}}` | Primary brand color (CSS variable or hex) |
| `{{BRAND_SECONDARY}}` | Secondary brand color |
| `{{FONT_HEADING}}` | Heading font family |
| `{{FONT_BODY}}` | Body font family |

---

## When to Use

- User asks to design or refine the "SSOT dashboard," "living source of truth," or "documentation dashboard."
- User wants to align scattered `_docs` content into one navigable, well-designed dashboard.
- User needs a docs-first, token-based, agent-friendly documentation hub.

---

## Instructions

### 1. Ground in Project Docs

Read or reference the project's key documentation:
- Purpose and mission docs
- Site map / information architecture
- Platform architecture overview
- AI/product vision docs
- Design system and token definitions
- Business/foundation docs

### 2. Propose or Refine Dashboard Structure

Sidebar sections should map to the project's documentation taxonomy. Common categories:

- **Foundation** — Why the project exists, scope, governance
- **Core Story** — Anchor narrative, vision, mission, values
- **Information Architecture** — Site map, page hierarchy, navigation order
- **Platform & Architecture** — Tech stack, type safety, data model
- **AI/Product Vision** — Intelligence features, automation, agent systems
- **Design System & Tokens** — Typography, color, component tokens
- **Value Proposition** — Primary and segment value props
- **Audience** — Who you serve, personas, segments
- **Principles** — Non-negotiables, guardrails, ranked values
- **Voice & Tone** — Brand voice, what to avoid, leader-specific references
- **Content Types** — Articles, courses, books, videos, podcasts; creation rules

Main area shows one section at a time as the living doc.

### 3. Apply Docs-First Design

- Use typography and spacing for hierarchy
- Token-based components (cards, sections)
- Layout that is scannable and reading-optimized
- Keep semantic HTML and clear headings/IDs
- Responsive — works on desktop and tablet

### 4. Ensure Dual Audience

Output must be usable by both:
- **Humans** — readable, clear navigation, scannable
- **AI Agents** — semantic structure, stable landmarks, optional metadata like "Last updated"

---

## Output Conventions

- Edit or add files under `{{DASHBOARD_ROOT}}/`: `index.html`, `css/*.css`, `js/main.js`, `content/*.html`
- Preserve token-based styling; do not hardcode colors or type sizes
- For new content sections, add a corresponding sidebar entry and a `content/<section>.html` (or inlined section in `index.html`)
- Use CSS custom properties for all colors, spacing, and typography values

---

## Suggested File Structure

```
{{DASHBOARD_ROOT}}/
├── index.html              # Main shell with sidebar + content area
├── css/
│   ├── tokens.css          # Design tokens (colors, spacing, type)
│   ├── layout.css          # Grid, sidebar, content area
│   └── components.css      # Cards, badges, section styles
├── js/
│   └── main.js             # Navigation, section switching, search
└── content/
    ├── foundation.html     # Each section as a standalone partial
    ├── architecture.html
    ├── design-system.html
    └── ...
```

---

## Design Principles

1. **Docs as the product** — The dashboard IS the documentation, not a wrapper around it
2. **Token-first** — Every visual decision flows from design tokens, not ad-hoc styles
3. **Scan then read** — Hierarchy, whitespace, and typography enable quick scanning before deep reading
4. **Agent-parseable** — Semantic HTML, stable IDs, clear landmarks enable AI agents to navigate and extract
5. **Living** — Content sections link to source docs; "Last updated" timestamps enable freshness tracking
