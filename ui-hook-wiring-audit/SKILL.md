---
name: ui-hook-wiring-audit
description: "Audit and fix UI component data wiring — verifies every component renders the correct data by tracing rendered fields back to the type-safe hooks layer. Checks that book thumbnails, author profiles, course cards, video metadata, and all other domain data reach the correct UI locations through the right simplified or custom hooks. Reports status for each component, then fixes only incorrectly wired paths."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Audit and fix UI ↔ hook wiring for: $ARGUMENTS

$ARGUMENTS should include:
- A scope: a specific file, directory, route, or "full" for the entire `src/components/` tree
- Optionally: "audit-only" to report without making changes
- Optionally: a domain filter like "books", "courses", "videos", "agents" to limit to one domain
- Empty — ask the user for the target scope

---

## Purpose

This skill is the **Layer 6 ↔ Layer 5 verification** in the six-layer type safety chain:

```
Layer 5: React Hooks       src/hooks/simplified/       (data source)
                            src/hooks/custom/           (composite data)
         ──── this skill audits this boundary ────
Layer 6: UI Components     src/components/             (data consumer)
```

It answers: **"Is every piece of domain data in the UI sourced from the correct hook, and does every hook the UI needs actually get called?"**

A correctly wired component:
- Imports the right hook for the data it renders (e.g., `useBooks` for book title/thumbnail)
- Passes the right identifiers (e.g., `bookId`) to the hook
- Destructures the fields the template actually uses
- Uses mutations from the same domain hook for create/update/delete actions

An incorrectly wired component:
- Renders domain data from props that were never fetched (orphaned renders)
- Calls a hook for domain X but renders fields that belong to domain Y
- Hardcodes data that should come from a hook (mock/placeholder data left in)
- Missing a hook entirely — the UI shows empty or stale where live data should appear
- Uses the wrong hook for a relationship (e.g., `useContentItemsList` where `useBookChaptersList` is needed)
- Calls a hook but ignores its loading/error states in the render

---

## Phase 0 — Scope & Inventory

1. **Determine scope** from `$ARGUMENTS`. If empty, ask the user.

2. **Build the hook registry** — scan the available data sources:

   ```
   # All simplified hooks (one per DB table)
   src/hooks/simplified/*.hooks.ts

   # Custom composite hooks
   src/hooks/custom/*.ts

   # Agent-specific hooks (if present)
   src/hooks/agents/*.ts
   ```

   For each hook file, extract:
   - Hook names exported (e.g., `useBooks`, `useBooksList`, `useBooksCreate`, `useBooksUpdate`, `useBooksDelete`)
   - The entity/domain it serves (derived from filename: `books.hooks.ts` → `books`)
   - The Zod select schema fields it returns (look up in `src/lib/schemas/index.ts`)

   Store this as the **Hook Registry** — the source of truth for what data is available.

3. **Build the component inventory** — for each `.tsx` file in scope:
   - Record its path
   - Record all hook imports (from `@/hooks/simplified/` and `@/hooks/custom/`)
   - Record all hook call sites and the destructured return values
   - Record all JSX render expressions that reference data variables

---

## Phase 1 — Semantic Audit

For each component in the inventory, perform these checks:

### 1a. Intent Detection

Read the component and determine its **data intent** — what domain data does the UI want to display?

Indicators of intent:
- Component name: `BookThumbnail` → expects book data; `AuthorProfileCard` → expects author/user-profile data
- JSX content: renders `title`, `coverImageUrl`, `description` → book fields; renders `displayName`, `bio`, `avatarUrl` → profile fields
- Props interface: accepts `bookId`, `authorId`, `courseId`, `videoId` — these declare domain dependencies
- Route context: a component inside `src/app/(editor)/books/` is expected to deal with book data

### 1b. Hook Matching

For each detected intent, check:

1. **Is there a hook import that serves this domain?**
   - Book data → needs `useBooks` or `useBooksList` from `@/hooks/simplified/books.hooks`
   - Author profile → needs `useUserProfiles` from `@/hooks/simplified/user-profiles.hooks` or `useAuthorProfile` from `@/hooks/custom/use-author-profile`
   - Course lesson → needs `useCourseLessons` from `@/hooks/simplified/course-lessons.hooks`

2. **Is the hook called with the correct identifier?**
   - `useBooks(bookId)` — the `bookId` must come from props, route params, or a parent context
   - `useBookChaptersList({ bookId })` — the filter must include the scoping ID

3. **Do the destructured fields match what the JSX renders?**
   - If JSX uses `book.coverImageUrl` but the hook returns `data` and the component never accesses `data.coverImageUrl`, flag it
   - If JSX references `book.title` but the variable comes from a prop rather than a hook, trace whether the prop originates from a hook call in a parent — if so, mark as "wired via prop drilling" (valid but document it)

### 1c. Mutation Matching

For components with forms, buttons, or actions:
- Does the component import the correct mutation hook? (`useBooksUpdate` for editing a book, `useCommentsCreate` for adding a comment)
- Does the mutation call pass the correct payload shape matching the Zod update/insert schema?
- Does the mutation `onSuccess` invalidate the right query keys?

### 1d. Missing Hook Detection

Check for:
- **Hardcoded placeholder data** — strings like "Sample Book", "Author Name", `placeholder.jpg`, TODO comments, or empty arrays where hook data should be
- **Unused hook imports** — a hook is imported but never called (dead import)
- **Missing loading states** — hook is called but `isLoading` is never checked (UI will flash undefined data)
- **Missing error boundaries** — hook is called but `error` is never handled

---

## Phase 2 — Report

Generate a structured audit report. Group findings by component.

### Report Format

For each component file, output one of:

**PASS** — correctly wired:
```
PASS  src/components/book-editor/BookEditorClient.tsx
  hooks: useBooks(bookId), useBookChaptersList({bookId}), useBooksUpdate()
  renders: book.title, book.coverImageUrl, chapters list, publish action
  status: All data paths verified. Loading states handled. Mutations correct.
```

**WARN** — functional but has minor issues:
```
WARN  src/components/dashboard/ActivityFeed.tsx
  hooks: useContentItemsList()
  renders: item.title, item.updatedAt
  issues:
    - [WARN-01] No loading skeleton — shows nothing while fetching
    - [WARN-02] No error fallback — hook error silently swallowed
  status: Data wiring correct. UX gaps noted.
```

**FAIL** — incorrectly wired:
```
FAIL  src/components/some/BrokenComponent.tsx
  hooks: useContentItemsList()  <-- WRONG: renders book fields but fetches content-items
  expects: useBooksList() from @/hooks/simplified/books.hooks
  renders: item.title (ambiguous), item.coverImageUrl (NOT on content-items schema)
  issues:
    - [FAIL-01] Wrong hook: fetches content-items but renders book-specific fields
    - [FAIL-02] Field mismatch: coverImageUrl does not exist on ContentItems type
  fix: Replace useContentItemsList with useBooksList, update destructuring
```

**SKIP** — not a data-consuming component (pure UI primitive, layout wrapper, etc.):
```
SKIP  src/components/ui/Button.tsx — UI primitive, no domain data
```

### Summary Table

At the end of the report, output a summary:

```
UI ↔ Hook Wiring Audit Summary
═══════════════════════════════
Scope:    src/components/book-editor/
Date:     <today>

PASS:     12 components
WARN:      3 components (5 warnings)
FAIL:      2 components (4 failures)
SKIP:      8 components (UI primitives)
─────────────────────────────
Total:    25 components audited

Top issues:
  1. [FAIL-01] Wrong hook domain (2 occurrences)
  2. [WARN-01] Missing loading state (3 occurrences)
```

---

## Phase 3 — Fix (unless audit-only)

If not in `audit-only` mode, proceed to fix **only FAIL items**. Never modify PASS or WARN components.

For each FAIL:

1. **Read the component** fully (do not assume from the audit — re-read).
2. **Look up the correct hook** in the Hook Registry from Phase 0.
3. **Look up the correct schema fields** in `src/lib/schemas/index.ts` to ensure the replacement hook provides the fields the JSX needs.
4. **Apply the fix:**
   - Replace the incorrect hook import with the correct one
   - Update the hook call site (correct entity, correct filters/ID)
   - Update destructured fields to match the new hook's return type
   - If the component also needs mutation hooks, wire those from the same domain
   - Ensure `isLoading` and `error` are handled if the original code handled them
5. **Do NOT change:**
   - JSX structure or layout
   - Styling (classes, Tailwind)
   - Props interface (unless a new required prop like `bookId` is needed — add it minimally)
   - Any component marked PASS
   - Any component marked WARN (those are UX suggestions, not wiring bugs)

After each fix, note what changed:

```
FIXED src/components/some/BrokenComponent.tsx
  was:  useContentItemsList() → rendered book fields (type mismatch)
  now:  useBooksList({ limit: 20 }) → renders book.title, book.coverImageUrl
  changes:
    - Replaced import: content-items.hooks → books.hooks
    - Updated hook call: useContentItemsList() → useBooksList({ limit: 20 })
    - Updated destructuring: data → data (compatible, same shape access)
    - Added bookId prop to component interface
```

---

## Phase 4 — Verification

After all fixes:

1. **Re-run the audit** on fixed files only to confirm they now pass.
2. **Run TypeScript check** on modified files:
   ```bash
   npx tsc --noEmit --pretty <fixed-file-paths>
   ```
3. **Report final status** — the same summary table format, showing the delta.

---

## Critical Rules

1. **Never modify PASS components.** The audit documents them; it does not "improve" them.
2. **Never modify WARN components** unless the user explicitly asks to upgrade warnings to fixes.
3. **Trace through prop drilling.** If a component receives `book` as a prop, trace upward to find where the hook is called. The hook may be correctly wired in a parent — document the chain, don't re-fetch.
4. **Respect custom hooks.** `src/hooks/custom/` hooks often compose multiple simplified hooks. If a component uses `useAuthorProfile` instead of `useUserProfiles`, that's correct — the custom hook wraps the simplified one with additional logic.
5. **Schema is source of truth.** When checking if a field exists on a type, always verify against `src/lib/schemas/index.ts`, not from memory. Fields change as the DB evolves.
6. **One hook per concern.** A component should not call `useBooksList` AND manually fetch `/api/simplified/books` — flag dual-sourcing as FAIL.
7. **Filter by route context.** Components under `src/app/(editor)/books/` should primarily use book-domain hooks. A course hook in a book editor is suspicious unless it's a cross-reference feature.
8. **Preserve the type chain.** Fixes must maintain the downstream-only flow: hooks import from services/schemas, components import from hooks. Never introduce a direct service import into a component.

---

## Hook Domain Quick Reference

This is a non-exhaustive guide for common UI → hook mappings. Always verify against the actual hook registry.

| UI renders... | Expected hook source | Hook file |
|---|---|---|
| Book title, cover, description | `useBooks(id)` or `useBooksList()` | `books.hooks.ts` |
| Book chapters list | `useBookChaptersList({ bookId })` | `book-chapters.hooks.ts` |
| Reading progress | `useBookReadingProgressList()` | `book-reading-progress.hooks.ts` |
| Author name, bio, avatar | `useUserProfiles(id)` or `useAuthorProfile()` | `user-profiles.hooks.ts` / `use-author-profile.ts` |
| Course title, modules, weeks | `useCourses(id)`, `useCourseWeeksList()` | `courses.hooks.ts`, `course-weeks.hooks.ts` |
| Lesson content, script | `useCourseLessons(id)` | `course-lessons.hooks.ts` |
| Video metadata, thumbnail | `useVideos(id)` or `useVideosList()` | `videos.hooks.ts` |
| Video annotations | `useVideoAnnotationsList({ videoId })` | `video-annotations.hooks.ts` |
| Article/content body | `useContentItems(id)` | `content-items.hooks.ts` |
| Comments thread | `useCommentsList({ ... })` | `comments.hooks.ts` |
| Agent list, tools, metrics | `useAgentsList()`, `useAgentToolsList()` | `agents.hooks.ts`, `agent-tools.hooks.ts` |
| AI insights | `useAiInsightsList()` | `ai-insights.hooks.ts` |
| Voice identity | `useVoiceIdentitiesList()` | `voice-identities.hooks.ts` |
| Media items, uploads | `useMediaItemsList()` | `media-items.hooks.ts` |
| Podcast episodes | `usePodcastEpisodesList()` | `podcast-episodes.hooks.ts` |
| Organization settings | `useOrganizations(id)` | `organizations.hooks.ts` |
| Notifications | `useUserNotificationsList()` | `user-notifications.hooks.ts` |
| Assessment questions | `useAssessmentQuestionsList()` | `assessment-questions.hooks.ts` |
| Archive items | `useArchiveItemsList()` | `archive-items.hooks.ts` |

---

## Example Walkthrough

Suppose we audit `src/components/dashboard/BookShelf.tsx`:

```tsx
// BookShelf.tsx
import { useContentItemsList } from "@/hooks/simplified/content-items.hooks";

export function BookShelf() {
  const { data: books = [] } = useContentItemsList({ limit: 10 });
  return (
    <div className="grid grid-cols-4 gap-4">
      {books.map(book => (
        <div key={book.id}>
          <img src={book.coverImageUrl} alt={book.title} />  {/* coverImageUrl is NOT on content-items */}
          <p>{book.title}</p>
        </div>
      ))}
    </div>
  );
}
```

**Audit result:**
```
FAIL  src/components/dashboard/BookShelf.tsx
  hooks: useContentItemsList({ limit: 10 })
  intent: Renders book covers and titles (BookShelf name + coverImageUrl field)
  issues:
    - [FAIL-01] Wrong domain: useContentItemsList serves content-items, not books
    - [FAIL-02] Field mismatch: coverImageUrl does not exist on ContentItems schema
  fix: Replace with useBooksList({ limit: 10 }) from books.hooks.ts
```

**Fix applied:**
```tsx
// BookShelf.tsx — FIXED
import { useBooksList } from "@/hooks/simplified/books.hooks";

export function BookShelf() {
  const { data: books = [] } = useBooksList({ limit: 10 });
  return (
    <div className="grid grid-cols-4 gap-4">
      {books.map(book => (
        <div key={book.id}>
          <img src={book.coverImageUrl} alt={book.title} />
          <p>{book.title}</p>
        </div>
      ))}
    </div>
  );
}
```
