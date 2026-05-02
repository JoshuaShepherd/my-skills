---
name: puck-visual-editor
description: Build, extend, and persist Puck visual editors with React/Next.js and Supabase. Use whenever the user mentions Puck, @puckeditor/core, visual editor, site pages, puck_data, drag-and-drop CMS, block registry, Render vs Puck, RSC, per-page component palettes, categories, slots, permissions, richtext, plugin rail, data migration, composition, or shared blocks in packages/blocks — even if they do not say "Puck" by name.
---

# Puck visual editor (movemental-visual-editor)

**Canonical documentation:** [https://puckeditor.com/docs](https://puckeditor.com/docs)

**Release note:** Puck **0.21** adds AI (beta), **`richtext`** fields, and the **Plugin Rail**. See the [0.21 announcement](https://puckeditor.com/blog/puck-021) for a concise feature summary.

**This repo:** Pin is `@puckeditor/core` in root `package.json`. Before relying on APIs, confirm the installed version in `pnpm-lock.yaml` and scan [Puck releases](https://github.com/puckeditor/puck/releases) for breaking changes.

---

## 1. Mental model (official docs)

- **[`Config`](https://puckeditor.com/docs/api-reference/configuration/config)** — Declares `components` (each with `fields`, `defaultProps`, `render`), optional `categories`, `root`, and per-component options (`permissions`, `resolveData`, etc.).
- **[`Data`](https://puckeditor.com/docs/api-reference/data-model/data)** — JSON: `content`, `root`, and legacy `zones`. Prefer **[`slot` fields](https://puckeditor.com/docs/api-reference/fields/slot)** over DropZones; see [DropZones → slots migration](https://puckeditor.com/docs/guides/migrations/dropzones-to-slots).
- **Editor vs render** — **`<Puck />`** is **client-only**. **`<Render />`** and [`resolveAllData`](https://puckeditor.com/docs/api-reference/functions/resolve-all-data) can run in **RSC** when the config is RSC-safe. See [Server Components](https://puckeditor.com/docs/integrating-puck/server-components).

**Persistence in this project:** `public.site_pages.puck_data` (jsonb) stores **Data**, not React source. Implementations live in **`packages/blocks`** (`@movemental/blocks`). Consumer sites must use the **same config keys** (`type` strings) as stored JSON.

---

## 2. Official documentation index (keep answers and PRs linked here)

### Getting started

| Topic | URL |
|--------|-----|
| Docs home / introduction | [Introduction](https://puckeditor.com/docs) |
| Install and minimal editor | [Getting Started](https://puckeditor.com/docs/getting-started) |

### Integrating Puck

| Topic | URL |
|--------|-----|
| Component config (`render`, `fields`, `defaultProps`) | [Component configuration](https://puckeditor.com/docs/integrating-puck/component-configuration) |
| Root wrapper and page metadata | [Root configuration](https://puckeditor.com/docs/integrating-puck/root-configuration) |
| Sidebar grouping | [Categories](https://puckeditor.com/docs/integrating-puck/categories) |
| Layouts and nesting | [Multi-column layouts](https://puckeditor.com/docs/integrating-puck/multi-column-layouts) |
| `resolveData`, read-only fields | [Dynamic props](https://puckeditor.com/docs/integrating-puck/dynamic-props) |
| Conditional field definitions | [Dynamic fields](https://puckeditor.com/docs/integrating-puck/dynamic-fields) |
| CMS-style picks and `resolveData` | [External data sources](https://puckeditor.com/docs/integrating-puck/external-data-sources) |
| RSC, `"use client"`, split configs | [Server components](https://puckeditor.com/docs/integrating-puck/server-components) |
| `migrate`, `transformProps`, prop compatibility | [Data migration](https://puckeditor.com/docs/integrating-puck/data-migration) |
| Preview iframe and breakpoints | [Viewports](https://puckeditor.com/docs/integrating-puck/viewports) |
| Global and per-component permissions | [Feature toggling](https://puckeditor.com/docs/integrating-puck/feature-toggling) |
| Rich text (TipTap, `richtext` field, inline edit) | [Rich text editing](https://puckeditor.com/docs/integrating-puck/rich-text-editing) |
| Interactive elements inside the preview | [Overlay portals](https://puckeditor.com/docs/integrating-puck/overlay-portals) |

### Extending Puck

| Topic | URL |
|--------|-----|
| Custom editor layouts (`Puck.Preview`, etc.) | [Composition](https://puckeditor.com/docs/extending-puck/composition) |
| Custom field editors | [Custom fields](https://puckeditor.com/docs/extending-puck/custom-fields) |
| Field transforms | [Field transforms](https://puckeditor.com/docs/extending-puck/field-transforms) |
| `usePuck`, app state | [Internal Puck API](https://puckeditor.com/docs/extending-puck/internal-puck-api) |
| Editor chrome styling | [Theming](https://puckeditor.com/docs/extending-puck/theming) |
| Plugins, Plugin Rail, core plugins | [Plugin API (guide)](https://puckeditor.com/docs/extending-puck/plugins) |
| Experimental UI hooks | [UI overrides](https://puckeditor.com/docs/extending-puck/ui-overrides) |

### Guides

| Topic | URL |
|--------|-----|
| Migrations index | [Guides / Migrations](https://puckeditor.com/docs/guides/migrations) |

### API reference (high-signal)

| Topic | URL |
|--------|-----|
| `Config` | [Configuration / Config](https://puckeditor.com/docs/api-reference/configuration/config) |
| `ComponentConfig` | [Component config](https://puckeditor.com/docs/api-reference/configuration/component-config) |
| `Data`, `content`, `root` | [Data model](https://puckeditor.com/docs/api-reference/data-model/data) |
| `<Puck />` | [Puck component](https://puckeditor.com/docs/api-reference/components/puck) |
| Compositional children (`Puck.Preview`, …) | [Puck subcomponents](https://puckeditor.com/docs/api-reference/components/puck-components) |
| `<Render />` | [Render component](https://puckeditor.com/docs/api-reference/components/render) |
| Permissions | [Permissions](https://puckeditor.com/docs/api-reference/permissions) |
| Fields index | [Fields](https://puckeditor.com/docs/api-reference/fields) |
| `slot` field (`allow` / `disallow`) | [Slot field](https://puckeditor.com/docs/api-reference/fields/slot) |
| `richtext` field | [Richtext field](https://puckeditor.com/docs/api-reference/fields/richtext) |
| `external` field | [External field](https://puckeditor.com/docs/api-reference/fields/external) |
| Rich text toolbar composition | [RichTextMenu](https://puckeditor.com/docs/api-reference/components/rich-text-menu) |
| `migrate` | [migrate()](https://puckeditor.com/docs/api-reference/functions/migrate) |
| `transformProps` | [transformProps()](https://puckeditor.com/docs/api-reference/functions/transform-props) |
| `resolveAllData` | [resolveAllData()](https://puckeditor.com/docs/api-reference/functions/resolve-all-data) |
| `registerOverlayPortal` | [registerOverlayPortal()](https://puckeditor.com/docs/api-reference/functions/register-overlay-portal) |
| Plugins (reference) | [Plugins API reference](https://puckeditor.com/docs/api-reference/plugins) |
| Blocks plugin | [blocks plugin](https://puckeditor.com/docs/api-reference/plugins/blocks-plugin) |
| Outline plugin | [outline plugin](https://puckeditor.com/docs/api-reference/plugins/outline-plugin) |
| Fields plugin | [fields plugin](https://puckeditor.com/docs/api-reference/plugins/fields-plugin) |
| Legacy sidebar plugin | [legacy-side-bar plugin](https://puckeditor.com/docs/api-reference/plugins/legacy-side-bar-plugin) |
| Overrides list | [Overrides](https://puckeditor.com/docs/api-reference/overrides) |
| FieldTransforms | [FieldTransforms](https://puckeditor.com/docs/api-reference/field-transforms) |

### Puck AI (cloud beta)

| Topic | URL |
|--------|-----|
| Overview | [Puck AI overview](https://puckeditor.com/docs/ai/overview) |
| AI plugin setup | [AI getting started](https://puckeditor.com/docs/ai/getting-started) |
| Constrain generation | [AI configuration](https://puckeditor.com/docs/ai/ai-configuration) |
| Business context | [Business context](https://puckeditor.com/docs/ai/business-context) |
| Agent tools | [AI tools](https://puckeditor.com/docs/ai/tools) |
| Programmatic generation | [Headless generation](https://puckeditor.com/docs/ai/headless-generation) |

---

## 3. Practices aligned with Puck docs

1. **Stable component keys** — Keys in `config.components` become persisted `type` strings. Renames require [Data migration](https://puckeditor.com/docs/integrating-puck/data-migration); prefer `transformProps` or backwards-compatible `render` functions.
2. **TypeScript** — Use `Config<Components>` and typed props per [Component configuration](https://puckeditor.com/docs/integrating-puck/component-configuration).
3. **RSC** — Next.js App Router: `import { Render, resolveAllData } from "@puckeditor/core/rsc"` where appropriate; keep **`<Puck />`** in a client boundary. Follow [Server components](https://puckeditor.com/docs/integrating-puck/server-components).
4. **Saving** — `onChange` receives latest [`Data`](https://puckeditor.com/docs/api-reference/data-model/data) for drafts; `onPublish` for explicit publish ([Puck component](https://puckeditor.com/docs/api-reference/components/puck)).
5. **Nested regions** — Use **`type: "slot"`** with [`allow` / `disallow`](https://puckeditor.com/docs/api-reference/fields/slot) to restrict blocks inside a layout region.
6. **Per-page palette** — Puck does not load the sidebar from Supabase. Derive **filtered `Config`** (`components` + `categories`) from DB metadata (e.g. `page_type`, `allowed_component_types`) before passing `config` to `<Puck />`.
7. **Styles** — `import "@puckeditor/core/puck.css"` ([Getting Started](https://puckeditor.com/docs/getting-started)).
8. **Rich text** — Use the [`richtext`](https://puckeditor.com/docs/api-reference/fields/richtext) field; sanitize or constrain output in `render` for public pages if content is user-authored ([Rich text editing](https://puckeditor.com/docs/integrating-puck/rich-text-editing)).
9. **Plugins** — Register via [`plugins` on `<Puck />`](https://puckeditor.com/docs/api-reference/components/puck#plugins). Core rail: blocks, outline, fields; optional `legacy-side-bar` ([Plugin API](https://puckeditor.com/docs/extending-puck/plugins)).
10. **Custom editor chrome** — Prefer [Composition](https://puckeditor.com/docs/extending-puck/composition); use [UI overrides](https://puckeditor.com/docs/extending-puck/ui-overrides) sparingly (experimental API).

---

## 4. Where this repo implements Puck

| Area | Path |
|------|------|
| Shared `puckConfig`, `EMPTY_PUCK_DATA`, blocks | `packages/blocks/` |
| Drizzle table | `sitePages` in `src/lib/database/schema.ts` |
| APIs | `src/app/api/site-pages/` |
| Hooks | `src/hooks/site-pages.hooks.ts` |
| Editor routes | `src/app/(editor)/` |
| Cursor rule | `.cursor/rules/10-puck-blocks-editor.mdc` |
| Implementation checklist | `_docs/_prompts/06-puck-implementation-prompts.md` |
| Per-page components + Supabase MCP | `_docs/_prompts/08-puck-per-page-components-supabase-setup.md` |

---

## 5. Related agent skills (Claude / Cursor)

Use these when automating migrations, APIs, or agentic features alongside Puck:

| Skill | Use when |
|--------|-----------|
| `.claude/skills/migrations-workflow/SKILL.md` | Drizzle ↔ Supabase migrations after schema changes |
| `.claude/skills/supabase-security-audit/SKILL.md` | RLS and policies on `site_pages` (or equivalent) |
| `.claude/skills/agent-tool/SKILL.md` | Defining tools for **Puck AI** [Tools](https://puckeditor.com/docs/ai/tools) or your own orchestration |
| `.claude/skills/agent-create/SKILL.md` | New agents that generate or validate Puck `Data` |
| `.claude/skills/agent-instructions/SKILL.md` | Prompt layers for AI that must only emit registered component keys |

---

## 6. When editing this skill

- Reconcile links with the sidebar at [puckeditor.com/docs](https://puckeditor.com/docs); Puck may add guides or rename paths.
- Bump the **version callout** when `@puckeditor/core` major or minor changes in `package.json` / lockfile.
