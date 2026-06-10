---
name: puck-visual-editor
description: Build, extend, and persist Puck visual editors with React/Next.js and Supabase. Use whenever the user mentions Puck, @puckeditor/core, visual editor, site pages, puck_data, drag-and-drop CMS, block registry, Render vs Puck, RSC, per-page component palettes, richtext, plugin rail, slots, permissions, or data migration — even if they do not say "Puck" by name.
---

# Puck visual editor

**Canonical documentation:** [https://puckeditor.com/docs](https://puckeditor.com/docs)

**Release note:** Puck **0.21** adds AI (beta), **`richtext`** fields, and the **Plugin Rail**. Summary: [Puck 0.21 blog](https://puckeditor.com/blog/puck-021).

**Reference implementation (blocks + editor + `site_pages`):** sibling repo **`movemental-visual-editor`** — keep `.claude/skills/puck-visual-editor/SKILL.md` there in sync with this file for the full repo path table.

---

## 1. Mental model

- **[`Config`](https://puckeditor.com/docs/api-reference/configuration/config)** — `components`, `fields`, `defaultProps`, `render`, `categories`, `root`, `resolveData`, `permissions`, …
- **[`Data`](https://puckeditor.com/docs/api-reference/data-model/data)** — `content`, `root`, legacy `zones`. Prefer **[slots](https://puckeditor.com/docs/api-reference/fields/slot)** over DropZones ([migration guide](https://puckeditor.com/docs/guides/migrations/dropzones-to-slots)).
- **`<Puck />`** = client editor; **`<Render />`** + [`resolveAllData`](https://puckeditor.com/docs/api-reference/functions/resolve-all-data) = RSC-friendly when config is server-safe ([Server components](https://puckeditor.com/docs/integrating-puck/server-components)).

---

## 2. Official documentation index

### Getting started

| Topic | URL |
|--------|-----|
| Introduction | [Introduction](https://puckeditor.com/docs) |
| Install and minimal editor | [Getting Started](https://puckeditor.com/docs/getting-started) |

### Integrating Puck

| Topic | URL |
|--------|-----|
| Component configuration | [Component configuration](https://puckeditor.com/docs/integrating-puck/component-configuration) |
| Root configuration | [Root configuration](https://puckeditor.com/docs/integrating-puck/root-configuration) |
| Categories | [Categories](https://puckeditor.com/docs/integrating-puck/categories) |
| Multi-column layouts | [Multi-column layouts](https://puckeditor.com/docs/integrating-puck/multi-column-layouts) |
| Dynamic props | [Dynamic props](https://puckeditor.com/docs/integrating-puck/dynamic-props) |
| Dynamic fields | [Dynamic fields](https://puckeditor.com/docs/integrating-puck/dynamic-fields) |
| External data sources | [External data sources](https://puckeditor.com/docs/integrating-puck/external-data-sources) |
| Server components | [Server components](https://puckeditor.com/docs/integrating-puck/server-components) |
| Data migration | [Data migration](https://puckeditor.com/docs/integrating-puck/data-migration) |
| Viewports | [Viewports](https://puckeditor.com/docs/integrating-puck/viewports) |
| Feature toggling / permissions | [Feature toggling](https://puckeditor.com/docs/integrating-puck/feature-toggling) |
| Rich text editing | [Rich text editing](https://puckeditor.com/docs/integrating-puck/rich-text-editing) |
| Overlay portals | [Overlay portals](https://puckeditor.com/docs/integrating-puck/overlay-portals) |

### Extending Puck

| Topic | URL |
|--------|-----|
| Composition | [Composition](https://puckeditor.com/docs/extending-puck/composition) |
| Custom fields | [Custom fields](https://puckeditor.com/docs/extending-puck/custom-fields) |
| Field transforms | [Field transforms](https://puckeditor.com/docs/extending-puck/field-transforms) |
| Internal Puck API | [Internal Puck API](https://puckeditor.com/docs/extending-puck/internal-puck-api) |
| Theming | [Theming](https://puckeditor.com/docs/extending-puck/theming) |
| Plugins (Plugin Rail) | [Plugin API](https://puckeditor.com/docs/extending-puck/plugins) |
| UI overrides | [UI overrides](https://puckeditor.com/docs/extending-puck/ui-overrides) |

### API reference (frequently used)

| Topic | URL |
|--------|-----|
| `Config` | [Config](https://puckeditor.com/docs/api-reference/configuration/config) |
| `ComponentConfig` | [Component config](https://puckeditor.com/docs/api-reference/configuration/component-config) |
| `Data` model | [Data model](https://puckeditor.com/docs/api-reference/data-model/data) |
| `<Puck />` | [Puck](https://puckeditor.com/docs/api-reference/components/puck) |
| Puck subcomponents | [Puck components](https://puckeditor.com/docs/api-reference/components/puck-components) |
| `<Render />` | [Render](https://puckeditor.com/docs/api-reference/components/render) |
| Permissions | [Permissions](https://puckeditor.com/docs/api-reference/permissions) |
| `slot` field | [Slot field](https://puckeditor.com/docs/api-reference/fields/slot) |
| `richtext` field | [Richtext field](https://puckeditor.com/docs/api-reference/fields/richtext) |
| RichTextMenu | [RichTextMenu](https://puckeditor.com/docs/api-reference/components/rich-text-menu) |
| `migrate()` | [migrate](https://puckeditor.com/docs/api-reference/functions/migrate) |
| `transformProps()` | [transformProps](https://puckeditor.com/docs/api-reference/functions/transform-props) |
| `resolveAllData()` | [resolveAllData](https://puckeditor.com/docs/api-reference/functions/resolve-all-data) |
| `registerOverlayPortal` | [registerOverlayPortal](https://puckeditor.com/docs/api-reference/functions/register-overlay-portal) |
| Plugins API | [Plugins](https://puckeditor.com/docs/api-reference/plugins) |

### Puck AI (cloud beta)

| Topic | URL |
|--------|-----|
| Overview | [AI overview](https://puckeditor.com/docs/ai/overview) |
| Getting started | [AI getting started](https://puckeditor.com/docs/ai/getting-started) |
| AI configuration | [AI configuration](https://puckeditor.com/docs/ai/ai-configuration) |
| Business context | [Business context](https://puckeditor.com/docs/ai/business-context) |
| Tools | [AI tools](https://puckeditor.com/docs/ai/tools) |
| Headless generation | [Headless generation](https://puckeditor.com/docs/ai/headless-generation) |

---

## 3. Practices (short)

1. Stable `type` keys in JSON; use [Data migration](https://puckeditor.com/docs/integrating-puck/data-migration) when renaming.
2. Per-page palettes: **filter `Config.components` and `categories`** from DB-driven allowlists — not stored inside `puck_data` alone.
3. Slot **`allow` / `disallow`** for nested regions vs global palette ([Slot field](https://puckeditor.com/docs/api-reference/fields/slot)).
4. `import "@puckeditor/core/puck.css"`.
5. Rich text: follow [Rich text editing](https://puckeditor.com/docs/integrating-puck/rich-text-editing); treat public HTML carefully.

---

## 4. This monorepo (`non-profit-dashboard`)

There is **no** embedded Puck editor package here today. Use this skill when:

- Planning a **Supabase-backed** page builder that must align with **movemental-visual-editor**, or
- Authoring prompts and specs (see `_docs/_prompts/09-puck-per-page-components-supabase-setup.md`).

**Executable checklist and `packages/blocks` paths:** `../movemental-visual-editor/.claude/skills/puck-visual-editor/SKILL.md` and `_docs/_prompts/08-puck-per-page-components-supabase-setup.md` in that repo.

---

## 5. Related agent skills

| Skill | Use when |
|--------|-----------|
| `.claude/skills/migrations-workflow/SKILL.md` | Schema changes for `site_pages` / `puck_data` |
| `.claude/skills/supabase-security-audit/SKILL.md` | RLS on content tables |
| `.claude/skills/agent-tool/SKILL.md` | Puck AI [Tools](https://puckeditor.com/docs/ai/tools) or custom orchestration |
| `.claude/skills/agent-create/SKILL.md` | Agents that emit or validate Puck JSON |
| `.claude/skills/agent-instructions/SKILL.md` | Constraining models to registered component keys |
