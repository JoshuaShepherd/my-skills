---
name: docs-type-safety
description: Audit and update the type safety documentation in _docs/type/ to match the actual codebase state. Ensures docs are the single source of truth without errors or gaps.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Type Safety Documentation Audit & Update

Audit every file in `_docs/type/` against the live codebase and fix any errors, gaps, or stale information so the docs are the authoritative single source of truth for the 7-layer type safety chain.

## Type Safety Chain: Error Check and Fix (reference)

When running or documenting validation, use this workflow. Full detail lives in `_docs/type/TYPE_SAFETY.md` (Error Fixing Protocol).

### Run error check

1. **Full chain:** `npx tsc --noEmit -p tsconfig.build.json` — checks all layers (server + client + shared schema).
2. **Client only:** `npx tsc --noEmit` (uses `tsconfig.json`, covers `src/` only).
3. Exit **0** = success (no type errors). Non-zero = failure with errors printed to stdout.

### Fix errors (until 0 errors)

1. Run `npx tsc --noEmit -p tsconfig.build.json`.
2. If errors appear, **trace each error to its source layer** (fix at the lowest layer possible — never change a lower layer to satisfy an upper one). See `_docs/type/TYPE_SAFETY.md` "Error Fixing Protocol" and the layer doc in `_docs/type/layers/` for guidance.
3. Re-run type check after fixes.
4. Repeat until exit 0.

### Layer-specific fix hints

| Layer | If it fails | Action |
|-------|-------------|--------|
| 1 — Schema | Column mismatch | Schema is auto-generated — regenerate from live DB; never edit manually. See `01-drizzle-schema.md`. |
| 2 — Routes | Missing/wrong column access | Update route to match schema column names; ensure `organization_id` filter present. See `02-server-routes.md`. |
| 3 — Mappers | Row interface out of sync | Update `*Row` interface and `toStudio*/fromStudio*` functions to match schema changes. See `03-mappers.md`. |
| 4 — Frontend Types | Type shape mismatch | Update `src/types.ts` or `src/types/video-editor.ts` to match what mappers now return. See `04-frontend-types.md`. |
| 5 — API Client | Fetch/auth issues | Update `apiFetch` signature or error handling in `src/api/client.ts`. See `05-api-client.md`. |
| 6 — Hooks | Return type mismatch | Update hook generic type parameter to match new frontend type. See `06-react-hooks.md`. |
| 7 — Components | Prop type errors | Update component props/usage to match new hook return or frontend type. See `07-ui-components.md`. |

## Before Starting

1. Read every file in `_docs/type/` (README.md, TYPE_SAFETY.md, all files in layers/).
2. Gather ground truth from the codebase for each layer — use the actual source files as the authority.

## Ground Truth Collection

For each layer, collect the following from the **actual codebase** (not from existing docs):

### Layer 1 — Drizzle Schema
- Read `shared/alan-hirsch/database/schema.ts` (structure, key table exports)
- Identify tables used by Content Studio: `contentItems`, `courseLessons`, `courses`, `courseModules`, `comments`, `mediaItems`
- Note helper functions: `id()`, `createdAt()`, `updatedAt()`

### Layer 2 — Server Routes
- List `server/routes/*.routes.ts` files
- For each route file, note: base path, HTTP methods, which DB tables are queried, which mappers are used
- Check for tenant isolation (`organization_id` filtering)
- Current files: `articles`, `courses`, `lessons`, `media`, `comments`, `video-projects`, `ai`, `auth`

### Layer 3 — Mappers
- List `server/mappers/*.mapper.ts` files
- For each mapper, note: Row interface, frontend type, `toStudio*`/`fromStudio*` exports, JSONB field handling
- Current files: `article`, `course`, `lesson`, `media`, `video-project`

### Layer 4 — Frontend Types
- Read `src/types.ts` for core types (ContentType, WorkflowStatus, Lesson, Module, Course, CourseMetadata, MediaAsset, etc.)
- Read `src/types/video-editor.ts` for video domain types (Scene, Track, VideoFormat, VideoCompositionProps, etc.)

### Layer 5 — API Client
- Read `src/api/client.ts` for `apiFetch<T>` signature, auth handling, error handling, 204 behavior

### Layer 6 — React Hooks
- List `src/hooks/*.ts` files
- For each hook file, note: query keys, endpoints, return types, invalidation patterns
- Note `useVideoProject` custom hook with debounced auto-save pattern
- Current files: `useArticles`, `useCourses`, `useLessons`, `useMedia`, `useComments`, `useVideoProject`, `useAuth`

### Layer 7 — UI Components
- Sample key components in `src/components/` and `src/components/video-editor/`
- Note which hooks and types each component imports
- Current key components: `Editor`, `CourseSettings`, `VideoStudio`, `MediaLibrary`, `AIAgent`, `Teleprompter`, `VideoEditorShell`, `SceneInspector`, `StoryboardView`

### Cross-Cutting
- Read `tsconfig.json`, `tsconfig.build.json`, `tsconfig.server.json` for include/exclude patterns
- Read `server/db.ts` for database connection pattern
- Verify `getTenantOrgId()` usage for tenant isolation

## Audit Checklist

Compare every claim in the docs against ground truth. Flag and fix:

1. **Incorrect counts** — table counts, entity counts, file counts
2. **Wrong patterns** — code examples that don't match actual generated code
3. **Missing information** — new files, types, or conventions not documented
4. **Stale references** — files, paths, or commands that no longer exist
5. **Naming convention errors** — incorrect camelCase/PascalCase/kebab-case mappings
6. **JSONB field contents** — verify what each JSONB column actually stores
7. **Type union values** — verify ContentType, WorkflowStatus, VideoFormat, etc. match actual code
8. **Commands** — ensure all pnpm/npx commands listed match what actually works
9. **Cross-references** — ensure layer docs reference each other correctly
10. **Video editor chain** — verify video-project.mapper.ts ↔ video-editor.ts ↔ useVideoProject ↔ VideoEditorShell chain is documented

## Update Rules

- Fix errors in place — do not create new files unless a section genuinely needs its own file
- Use actual code snippets from the codebase, not invented examples
- Keep the same document structure and voice — just make it accurate
- Update counts, paths, patterns, and examples to match reality
- If a doc file covers something that no longer exists, remove that section
- If the codebase has something undocumented, add it to the appropriate doc
- Update the README.md index if any files were added or removed

## After Updating

1. Review each updated file for internal consistency
2. Ensure no doc references a pattern that contradicts another doc
3. Verify all code examples are syntactically correct
4. Confirm the README.md index accurately lists all files in `_docs/type/`
5. Run `npx tsc --noEmit -p tsconfig.build.json` to confirm type safety passes
