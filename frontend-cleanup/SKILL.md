---
name: frontend-cleanup
description: Audit a React/Next.js codebase for unused components, -v2 naming debt, and folder disorganization. Archives dead code and renames/restructures live components.
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
  - "Edit"
  - "Glob"
  - "Grep"
  - "Agent"
  - "TodoWrite"
---

# Frontend Component Cleanup

You are a frontend architect performing a safe, methodical cleanup of a React/Next.js component tree. Your job is to find unused components, resolve naming debt (like `-v2` suffixes), and organize everything into a clean, predictable folder structure — without breaking the app.

## Phase 1: Discovery & Inventory

### 1a. Map all components
Scan the `src/components/` directory recursively. For each component file (`.tsx`, `.ts`), record:
- File path
- Default and named exports
- Whether it's a page-level component, a shared/reusable component, or a UI primitive

### 1b. Build an import graph
For every file in the project (`src/`), find all imports that reference `src/components/`. Build a map:
- **Component → importers**: Which files import this component?
- **Component → zero importers**: These are candidates for archival.

Key search locations for imports:
- `src/app/` (pages, layouts, route handlers)
- `src/components/` (cross-component imports)
- `src/hooks/` (if any reference components)
- `src/lib/` (utilities that may reference components)
- Root config files (e.g., barrel exports)

### 1c. Check for dynamic/lazy imports
Search for `dynamic(`, `lazy(`, and string-based component references that static analysis might miss. Flag these as "potentially used" even if not in the static import graph.

### 1d. Check route usage
For Next.js App Router, check if components are used in:
- `page.tsx` files
- `layout.tsx` files
- `loading.tsx`, `error.tsx`, `not-found.tsx` files
- `template.tsx` files

## Phase 2: Classification

Sort every component into one of these categories:

| Category | Criteria | Action |
|----------|----------|--------|
| **Live** | Imported by at least one non-archived file | Keep, possibly rename/move |
| **Dead** | Zero imports anywhere in the project | Archive |
| **Shadowed** | A `-v2` version exists AND the original has zero imports | Archive the original |
| **Ambiguous** | Dynamically loaded or referenced by string | Flag for manual review |

### Naming debt detection
Find all directories and files with version suffixes: `-v2`, `-v3`, `-new`, `-old`, `-backup`, `-deprecated`, `-test`, `-temp`, `-wip`, `-draft`, `-copy`, `-legacy`, `-experimental`.

For each:
- If the non-suffixed version exists and is unused → the suffixed version is the canonical one
- If only the suffixed version exists → it IS the canonical version and should be renamed
- If both are actively used → flag for manual decision

## Phase 3: Generate Report

Before making ANY changes, produce a detailed report as a markdown file at `_docs/_build/frontend-cleanup-report.md`:

```markdown
# Frontend Component Cleanup Report
Generated: [date]

## Summary
- Total components scanned: X
- Live components: X
- Dead components (to archive): X
- Components to rename (remove -v2 etc.): X
- Ambiguous (manual review needed): X

## Dead Components (will archive)
| Component | Path | Last git commit | Reason |
|-----------|------|-----------------|--------|

## Rename Candidates (will remove version suffix)
| Current Path | New Path | Imports to update |
|-------------|----------|-------------------|

## Ambiguous (needs manual review)
| Component | Path | Reason |
|-----------|------|--------|

## Proposed Folder Structure
[Show the target directory tree for src/components/]
```

**STOP here and present the report to the user.** Do not proceed to Phase 4 until the user confirms the plan.

## Phase 4: Archive Dead Components

1. Create `src/components/_archive/` directory
2. Move dead components there, preserving their folder structure:
   - `src/components/old-thing/` → `src/components/_archive/old-thing/`
3. Add an `_archive/README.md` explaining what's in there and why
4. Verify the build still passes after archival: run `pnpm build` (or `pnpm typecheck` for speed)

## Phase 5: Rename & Restructure

For each `-v2` (or similar) component that is the canonical version:

1. Rename the file/folder to remove the suffix
2. Update ALL import paths across the codebase using find-and-replace
3. If the old (non-v2) version was archived in Phase 4, no conflict
4. If both exist and are used, flag for the user — do not auto-resolve

After each batch of renames, run `pnpm typecheck` to verify nothing broke.

## Phase 6: Folder Organization

Apply a clean folder convention. Suggest a structure based on what the project already has, but aim for:

```
src/components/
├── _archive/          # Dead components, preserved for reference
├── ui/                # Primitives (buttons, inputs, cards) — DO NOT MODIFY
├── shared/            # Reusable domain components (used across multiple pages)
├── [feature]/         # Feature-specific components (e.g., courses/, books/, ai-lab/)
├── layout/            # Layout components (navbar, footer, sidebar)
└── pages/             # Full page compositions (if used)
```

Move components to their correct folder, updating imports after each move.

## Safety Rules

1. **Never delete code** — only move to `_archive/`
2. **Always verify after changes** — run typecheck after each phase
3. **Present the plan before executing** — the report in Phase 3 is mandatory
4. **Preserve git history** — use `git mv` when possible for better blame tracking
5. **One phase at a time** — complete and verify each phase before moving to the next
6. **Don't touch `src/components/ui/`** — these are shadcn/ui primitives, leave them alone
7. **Check for CSS/style references** — some components may be referenced in CSS modules or Tailwind config
8. **Check for test references** — update test imports if tests reference moved components
