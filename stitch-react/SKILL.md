---
name: stitch-react
description: "Convert Stitch screens to React components — fetches and caches designs locally, extracts design tokens, decomposes HTML into shadcn/ui components, generates TypeScript types, wires Layer 5 hooks, and archives existing pages. Triggers on: Stitch React, component conversion, React conversion, HTML to React. NOT for: new React apps, API routes, services, or schema changes."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

Convert Stitch screen(s) to React components for: $ARGUMENTS

$ARGUMENTS should include:
- A Stitch project ID or screen ID, OR "list" to browse available projects
- The target page route (e.g., "homepage", "pathways", "content/books")
- Optionally: "tokens-only" to extract design tokens without building components
- Optionally: "fetch-only" to download designs without converting
- Optionally: "all" to convert all screens in a project sequentially
- Empty — list projects and ask the user what to convert

---

## Purpose

This skill takes a generated Stitch screen (HTML/CSS) and converts it into production React components that integrate with the project's six-layer type safety chain. It fetches and caches design assets locally for reliable access, archives existing page implementations before replacing them, and ensures no work is lost.

## Critical Rules

1. **NEVER overwrite existing components or pages.** Always archive first (see Archive Protocol).
2. **NEVER hand-edit generated Layer 1-5 files.** Use hooks from `src/hooks/simplified/` and `src/hooks/custom/` as-is.
3. **Components consume hooks (Layer 5), never call APIs or services directly.**
4. **Use semantic CSS classes only** — `bg-primary`, `text-muted-foreground`, etc. Never hardcode hex/rgb.
5. **Use shadcn/ui components** — `Card`, `Button`, `Input`, `Badge`, `Tabs`, etc. Never raw HTML with inline styles.
6. **Use `tenantConfig`** for any text that could vary per tenant. Never hardcode tenant strings.
7. **Push "use client" to leaf components only.** Keep page.tsx as a Server Component.
8. **Follow the design chain:** Tokens → Tailwind → Radix/shadcn → Domain components → Patterns → Pages.

---

## Phase 0 — Fetch & Cache Designs

Stitch assets live behind Google Cloud Storage signed URLs that expire and often fail with AI tool built-in fetch. **Always download to local cache first.**

### Cache structure
```
.stitch/designs/
  ├── {page-slug}.html          # Full HTML from Stitch
  ├── {page-slug}.png           # Screenshot at full width
  └── {page-slug}.meta.json     # Screen metadata (id, title, dimensions, deviceType)
```

The `{page-slug}` is derived from the screen title: lowercase, spaces→hyphens, strip parenthetical suffixes. Example: "Homepage: The Modern Archivist (Full)" → `homepage-the-modern-archivist`.

### Fetch workflow

1. **Get screen metadata** via `mcp__stitch__get_screen` to retrieve `htmlCode.downloadUrl`, `screenshot.downloadUrl`, `width`, `height`, `title`, and `deviceType`.

2. **Check local cache** — if `.stitch/designs/{page-slug}.html` and `.stitch/designs/{page-slug}.png` already exist:
   - Ask the user whether to **refresh** from Stitch or **reuse** existing files.
   - Only re-download if the user confirms.

3. **Download HTML:**
   ```bash
   bash scripts/fetch-stitch.sh "{htmlCode.downloadUrl}" ".stitch/designs/{page-slug}.html"
   ```

4. **Download screenshot** — append `=w{width}` to the screenshot URL first (Google CDN serves low-res thumbnails by default):
   ```bash
   bash scripts/fetch-stitch.sh "{screenshot.downloadUrl}=w{width}" ".stitch/designs/{page-slug}.png"
   ```

5. **Save metadata:**
   ```json
   {
     "screenId": "projects/{project}/screens/{screen}",
     "title": "Homepage: The Modern Archivist (Full)",
     "width": 2560,
     "height": 15320,
     "deviceType": "DESKTOP",
     "fetchedAt": "2026-03-21T14:00:00Z"
   }
   ```

6. **Visual audit** — read the downloaded `.png` to confirm design intent and layout details before proceeding with conversion.

### Fetch-only mode
If the user specified "fetch-only", stop after this phase. This is useful for bulk-downloading a project's screens for browsing/selection before deciding what to convert.

### Stitch API reference
- **htmlCode.downloadUrl**: Signed URL requiring `curl -L` (redirects + TLS/SNI). AI fetch tools often fail on these.
- **screenshot.downloadUrl**: Serves low-res thumbnail by default. Append `=w{width}` for full resolution.
- **deviceType**: Usually `DESKTOP` with 2560px base width. Components should be responsive from this base.
- **Element tracking**: Preserve `data-stitch-id` attributes as comments in TSX for future design sync.

---

## Phase 1 — Pre-Flight Checks

Before any conversion work:

1. **Read the cached HTML** from `.stitch/designs/{page-slug}.html`.
2. **Read the target page's current implementation** (if it exists) to understand what hooks, data sources, and patterns are already in use.
3. **Read `src/app/globals.css`** to understand current design tokens.
4. **Read `src/lib/config/tenant.config.ts`** to understand tenant theming and feature flags.
5. **Extract the Tailwind config from the Stitch HTML `<head>`** — this contains the design's color/font/spacing definitions. Compare with project's `tailwind.config.ts` to identify token gaps.
6. **Identify which database entities the page needs** (e.g., homepage needs pathways, content items, courses). Map each to its Layer 5 hook file in `src/hooks/simplified/` or `src/hooks/custom/`.

---

## Phase 2 — Archive Existing Page (Archive Protocol)

**This phase is MANDATORY when a page already exists at the target route.**

### For a page file (`page.tsx`):
```
src/app/(public)/page.tsx → src/app/(public)/page-old.tsx     (rename, remove default export)
```

The archived file should be renamed by appending `-old` before the extension. Remove or comment out the `export default` so Next.js doesn't conflict with the new page. Add a comment at the top:

```typescript
// ARCHIVED: [date] — replaced by stitch-react conversion from Stitch screen [screen-id]
// This file is preserved for reference. Delete when the new implementation is verified.
```

### For section components referenced by the page:
Do NOT archive individual section components (e.g., `src/components/hero.tsx`). The new page will import NEW components from a screen-specific directory. Old components remain untouched and available — they just won't be imported by the new page.

### For pages with `-old` suffix already existing:
If `page-old.tsx` already exists, use `page-old-2.tsx`, `page-old-3.tsx`, etc. Never overwrite an archive.

### What to record:
After archiving, note in your conversion report:
- What was archived and where
- Which hooks/data sources the old page used (carry forward to new implementation)
- Which section components the old page imported (for reference during conversion)

---

## Phase 3 — Token Extraction

Extract design tokens from the Stitch HTML/CSS and map them to the project's existing token system.

### Token source
The Stitch HTML `<head>` contains a localized `tailwind.config` with the screen's color/font/spacing definitions. Extract this first, then map to project tokens.

### What to extract:
| Stitch artifact | Maps to | Location |
|-----------------|---------|----------|
| Color palette (backgrounds, text, accents) | CSS custom properties | `src/app/globals.css` (`:root` and `.dark`) |
| Font families | Tailwind font config | `tailwind.config.ts` |
| Font sizes / weights / line heights | Tailwind type scale | `tailwind.config.ts` or `globals.css` |
| Spacing rhythm (padding, gap, margin patterns) | Tailwind spacing scale | Note patterns, don't add custom tokens unless necessary |
| Border radius values | `--radius` variable | `globals.css` |
| Shadow patterns | Tailwind shadow utilities | Note patterns |

### Rules for token updates:
- **Only update tokens if the Stitch design meaningfully differs from current tokens.** If the existing tokens are close enough, use them.
- **Prefer mapping Stitch values to existing semantic tokens** over adding new ones.
- **If adding new CSS variables, follow the existing naming convention** in globals.css (e.g., `--card`, `--popover`, `--accent`).
- **Support both light and dark mode.** If Stitch generated a dark-mode design, ensure light mode values also exist.
- **Ask the user before changing existing token values** — these affect the entire site.

### Token-only mode:
If the user specified "tokens-only", stop after this phase and report the token mapping. This is useful for the first screen conversion to establish the design foundation before converting components.

---

## Phase 4 — Component Decomposition Plan

Analyze the Stitch HTML and create a conversion plan BEFORE writing any code.

### Step 1 — Identify sections
Break the Stitch screen into logical sections. For a homepage this might be:
- Hero
- Social proof / logos
- Pathways grid
- Content sampler
- AI Lab teaser
- Course CTA
- Newsletter signup

### Step 2 — Map sections to components
For each section, determine:

| Section | New component path | shadcn/ui primitives used | Data source (hook) | Client or Server? |
|---------|-------------------|---------------------------|--------------------|--------------------|
| Hero | `src/components/home/hero.tsx` | Button | tenantConfig (static) | Server |
| Pathways | `src/components/home/pathways.tsx` | Card, Badge | `usePathwaysList` | Client |
| ... | ... | ... | ... | ... |

### Step 3 — Identify data requirements
For each component that needs data:
1. Check if a Layer 5 hook exists in `src/hooks/simplified/` or `src/hooks/custom/`
2. If the hook exists, note the import path and the data shape it returns
3. If NO hook exists, note what custom hook or data fetch is needed and flag it for the user

**NEVER create new hooks, services, or API routes.** If a hook doesn't exist, flag it and ask the user whether to:
- Use an existing hook with filtering
- Skip that section for now
- Run `/generate` to create the missing layers first

### Step 4 — Present the plan
Show the full conversion plan to the user and wait for approval before proceeding. The plan should include:
- Archive targets (what gets renamed)
- New component tree (file paths and hierarchy)
- Token changes (if any)
- Data source mapping (which hooks wire to which components)
- Anything that can't be converted (missing hooks, unsupported patterns)

---

## Phase 5 — Build Components

After the user approves the plan, build components bottom-up (leaf components first, page composition last).

### Component file structure:
```
src/components/[page-name]/
  ├── hero.tsx                    # Section component
  ├── pathways-grid.tsx           # Section component
  ├── content-sampler.tsx         # Section component
  └── ...
```

### JSX syntax rules (when converting from raw Stitch HTML)
- `class` → `className`
- `for` → `htmlFor`
- `style="color: red"` → `style={{ color: "red" }}`
- Self-closing tags: `<img>`, `<input>`, `<br>` → `<img />`, `<input />`, `<br />`
- Comments: `<!-- text -->` → `{/* text */}`
- Replace icon font text nodes with lucide-react imports:
  ```tsx
  // Bad: <span class="material-symbols-outlined">search</span>
  // Good:
  import { Search } from "lucide-react";
  <Search size={18} />
  ```

### State discipline
Only add `useState`/`useEffect` where behavior is actually needed. Static sections (hero, social proof, navigation) should be Server Components with no state. Never wire fake interactivity or invent business logic not present in the design.

### For each component:

1. **Start from the Stitch HTML structure** — preserve the semantic hierarchy (headings, sections, lists)
2. **Replace HTML elements with shadcn/ui equivalents:**
   - `<div class="card">` → `<Card>`, `<CardHeader>`, `<CardContent>`
   - `<button>` → `<Button variant="...">`
   - `<input>` → `<Input>`
   - Tabs → `<Tabs>`, `<TabsList>`, `<TabsTrigger>`, `<TabsContent>`
3. **Replace all colors with semantic tokens:**
   - Any background color → `bg-background`, `bg-card`, `bg-primary`, `bg-muted`
   - Any text color → `text-foreground`, `text-muted-foreground`, `text-primary`
   - Any border → `border-border`, `border-primary`
4. **Replace hardcoded text with `tenantConfig`** where appropriate
5. **Wire data from hooks:**
   ```tsx
   "use client";
   import { useContentItemsList } from "@/hooks/simplified/content-items.hooks";

   export function ContentSampler() {
     const { data, isLoading, error } = useContentItemsList({
       status: "published",
       limit: 6
     });
     // Handle loading, error, and data states
   }
   ```
6. **Handle all states** — loading (skeleton/spinner), error (message + retry), empty (message + action)
7. **Preserve GSAP animations** from the old components if they existed, or add subtle scroll reveals following the project's animation pattern
8. **Treat background images as dynamic data** — extract image URLs from Stitch HTML into tenant config or content hooks rather than hardcoding into styles

### TypeScript requirements:
- Type all props with `Readonly` interfaces: `interface HeroProps { readonly title: string; ... }`
- Use types from Layer 2 schemas when referencing entity shapes: `import type { ContentItems } from "@/lib/schemas"`
- Never use `any`

### Accessibility:
- Preserve heading hierarchy (h1 → h2 → h3, no skipping)
- All images need `alt` text
- Interactive elements need visible focus states (shadcn handles this)
- Tap targets minimum 44x44px

---

## Phase 6 — Compose the Page

Create the new `page.tsx` that imports and arranges all section components.

```tsx
// src/app/(public)/page.tsx
import { Hero } from "@/components/home/hero";
import { PathwaysGrid } from "@/components/home/pathways-grid";
import { ContentSampler } from "@/components/home/content-sampler";
// ... etc

export default function HomePage() {
  return (
    <>
      <Hero />
      <PathwaysGrid />
      <ContentSampler />
      {/* ... */}
    </>
  );
}
```

Rules:
- Page file is a **Server Component** (no "use client")
- Section components that need data are Client Components (they have "use client")
- Static sections (hero with tenant config only) can be Server Components
- Check feature flags: `{tenantConfig.features.chat && <AILabTeaser />}`

---

## Phase 7 — Verification Checklist

After building, verify:

- [ ] Designs cached in `.stitch/designs/` with HTML, PNG, and metadata
- [ ] Old page archived as `page-old.tsx` with archive comment
- [ ] No old component files were overwritten or modified
- [ ] New page.tsx is a Server Component (no "use client")
- [ ] All data comes from Layer 5 hooks, never direct API calls
- [ ] No hardcoded colors — only semantic Tailwind classes
- [ ] No hardcoded tenant strings — uses `tenantConfig`
- [ ] All components use shadcn/ui primitives
- [ ] Loading, error, and empty states handled in every data-consuming component
- [ ] TypeScript types imported from Layer 2 schemas where needed
- [ ] Heading hierarchy is correct (one h1 per page, proper nesting)
- [ ] No new hooks, services, or API routes were created
- [ ] Image URLs extracted to config/hooks, not hardcoded in styles

Report the checklist results to the user.

---

## Phase 8 — Conversion Report

```markdown
## Stitch → React Conversion Complete

### Screen
- **Stitch Project:** [project ID]
- **Stitch Screen:** [screen ID / title]
- **Local Cache:** `.stitch/designs/{page-slug}.html`
- **Target Route:** [e.g., / (homepage)]

### Archived
- `src/app/(public)/page.tsx` → `src/app/(public)/page-old.tsx`

### New Files Created
1. `src/app/(public)/page.tsx` — Page composition (Server Component)
2. `src/components/home/hero.tsx` — Hero section
3. `src/components/home/pathways-grid.tsx` — Pathways grid (Client)
4. ...

### Token Changes
- [List any globals.css or tailwind.config.ts changes, or "None"]

### Data Sources Wired
| Component | Hook | Entity |
|-----------|------|--------|
| PathwaysGrid | `usePathwaysList` | pathways |
| ContentSampler | `useContentItemsList` | content_items |

### Flagged Issues
- [Any missing hooks, unsupported patterns, or items needing manual attention]

### Next Steps
- Run `pnpm dev` and verify the page renders
- Compare visually with the Stitch screenshot at `.stitch/designs/{page-slug}.png`
- Run `/design-audit` to check visual quality
- Run `/responsive-audit` to check breakpoints
- Delete `page-old.tsx` once verified
```

---

## Multi-Screen Workflow

When converting multiple screens (e.g., "all"):

1. **Start with Homepage** — establishes tokens and shared patterns
2. **Convert in the build order** from the screen prompts doc (Homepage → Pathways Hub → Pathway Detail → Content Library → ...)
3. **Reuse shared components** — if the homepage conversion created a `PathwaysGrid` component, the Pathways Hub page should import and extend it, not duplicate it
4. **After each screen**, verify before proceeding to the next
5. **Token extraction only happens once** (first screen). Subsequent screens use the established tokens.

### Bulk fetch workflow
To download all screens for browsing before converting:
1. Call `mcp__stitch__list_screens` to get all screen metadata
2. For each screen, run the fetch workflow (Phase 0) to cache HTML + screenshot
3. Present a summary table of cached designs with titles and file paths
4. User selects which screens to convert

---

## Anti-Patterns

- **Never modify generated Layer 1-5 files** (schema, Zod, services, routes, hooks). If something is missing, use `/generate` or `/validate` first.
- **Never create a new API route or service** as part of a conversion. Flag the gap and let the user decide.
- **Never copy Stitch CSS verbatim.** Extract the design intent and express it through the project's token system.
- **Never put all sections in one giant component.** Decompose into focused section components.
- **Never skip the archive step.** Even if the current page "looks bad," it contains valuable context about data wiring and hooks.
- **Never use arbitrary Tailwind values** (`text-[#ff6b35]`, `p-[37px]`). Map to the token system.
- **Never create component files in `src/components/ui/`.** That's reserved for shadcn primitives. Use `src/components/[page-name]/` for page sections.
- **Never use AI built-in fetch for Stitch URLs.** Always use `scripts/fetch-stitch.sh` — Google Cloud Storage URLs require curl with redirect handling.
- **Never leave document-level HTML in component output.** Strip `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, and CDN `<script>` tags — these don't belong inside React components.
- **Never use icon font text nodes.** Replace `<span class="material-symbols-outlined">icon_name</span>` with the equivalent lucide-react import. Lucide is already in the project — use it.
