---
name: pathway-builder
description: "Build type-safe React pathway pages from pathway_sections database content — generates types, hooks, section components, and page composition. Triggers on: pathway page, pathway builder, build pathway, pathway components. NOT for: pathway content editing, seed scripts, schema changes, or Stitch conversions."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Build pathway page components for: $ARGUMENTS

$ARGUMENTS should include:
- A pathway slug (e.g., "mdna", "discipleship", "metanoia") OR "all" for every pathway
- Optionally: "types-only" to generate types and hooks without building components
- Optionally: a specific section_type to build a single section (e.g., "hero", "faq")
- Empty — list available pathways from the database and ask what to build

---

## Purpose

This skill builds production React components for pathway detail pages using content stored in the `pathway_sections` database table. It generates the full type-safe chain: database types → hooks → section components → page composition. Every component consumes data through hooks (Layer 5), never direct API calls.

## Data Source: `pathway_sections` Table

Each pathway has 13 section rows in the `pathway_sections` table:

| order | section_type | What it stores |
|-------|-------------|----------------|
| 0 | `hero` | Title, subtitle, hero quote, hero image brief |
| 1 | `core_question` | The pathway's central question |
| 2 | `anchor_quote` | Primary Hirsch quote with citation |
| 3 | `overview` | Prose overview of the pathway |
| 4 | `model` | Framework/model with titled elements |
| 5 | `scripture` | Biblical foundations with verse references |
| 6 | `case_studies` | Real-world examples with narratives |
| 7 | `faq` | Question/answer pairs |
| 8 | `practices` | Formation exercises with steps |
| 9 | `reflection` | Guided reflection prompts |
| 10 | `courses` | Related course connections |
| 11 | `resources` | Books, articles, further reading |
| 12 | `glossary` | Key term definitions |

Each row has:
- `body` (text) — main markdown/prose content
- `structured` (JSONB) — typed metadata specific to the section_type

---

## Critical Rules

1. **Components consume hooks (Layer 5), never call APIs or services directly.**
2. **Use semantic CSS classes only** — `bg-primary`, `text-muted-foreground`, etc. Never hardcode hex/rgb.
3. **Use shadcn/ui components** — `Card`, `Button`, `Accordion`, `Badge`, `Tabs`, etc. Never raw HTML with inline styles.
4. **Use `tenantConfig`** for any text that could vary per tenant. Never hardcode tenant strings.
5. **Push "use client" to leaf components only.** Keep page.tsx as a Server Component where possible.
6. **Follow the design chain:** Tokens → Tailwind → Radix/shadcn → Domain components → Page.
7. **NEVER modify existing Layer 1–5 files** (schema, Zod, services, routes, hooks in `simplified/`). If something is missing in those layers, flag it.
8. **Archive before overwriting.** If a pathway page or component already exists, archive it first (see Phase 1).

---

## Phase 0 — Pre-Flight Checks

Before any build work:

1. **Read `src/types/pathway.ts`** to understand existing types (`StudioPathway`, `PathwaySections`, sub-types).
2. **Read `src/hooks/usePathways.ts`** to understand existing hooks.
3. **Read `src/app/globals.css`** and `src/lib/config/tenant.config.ts` for tokens and tenant config.
4. **Check if `src/types/pathway-section.ts` exists** — if not, it needs to be created (Phase 2).
5. **Check if `src/hooks/usePathwaySections.ts` exists** — if not, it needs to be created (Phase 2).
6. **Check if `server/routes/pathway-sections.routes.ts` exists** — if not, it needs to be created (Phase 2).
7. **Verify the target pathway exists** by checking the database or the pathway list. If building for a specific slug, confirm it has section rows.

---

## Phase 1 — Archive Existing Implementation

**MANDATORY when a pathway page or component already exists at the target path.**

### Archive protocol:
```
src/app/(public)/pathways/[slug]/page.tsx → page-old.tsx
src/components/pathway/[component].tsx → [component]-old.tsx
```

Add archive comment:
```typescript
// ARCHIVED: [date] — replaced by pathway-builder skill
// This file is preserved for reference. Delete when verified.
```

If `-old` already exists, use `-old-2`, `-old-3`, etc.

---

## Phase 2 — Types, Hook, and Route Generation

### Step 1 — Create `src/types/pathway-section.ts`

Define types for the `pathway_sections` table row and per-section structured data:

```typescript
// --- Section Types (matching pathway_sections.section_type CHECK constraint) ---
export type PathwaySectionType =
  | 'hero'
  | 'core_question'
  | 'anchor_quote'
  | 'overview'
  | 'model'
  | 'scripture'
  | 'case_studies'
  | 'faq'
  | 'practices'
  | 'reflection'
  | 'courses'
  | 'resources'
  | 'glossary';

// --- Per-section structured JSONB shapes ---

export interface HeroStructured {
  subtitle?: string;
  hero_quote?: string;
  hero_quote_source?: string;
  hero_image_brief?: string;
}

export interface CoreQuestionStructured {
  question?: string;
}

export interface AnchorQuoteStructured {
  quote?: string;
  source?: string;
  book?: string;
}

export interface OverviewStructured {
  summary?: string;
}

export interface ModelElement {
  title: string;
  body: string;
}

export interface ModelStructured {
  elements?: ModelElement[];
  intro?: string;
}

export interface ScriptureRef {
  reference: string;
  text: string;
  connection?: string;
}

export interface ScriptureStructured {
  refs?: ScriptureRef[];
}

export interface CaseStudy {
  title: string;
  description: string;
  context?: string;
  lessons?: string[];
}

export interface CaseStudiesStructured {
  studies?: CaseStudy[];
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface FaqStructured {
  items?: FaqItem[];
}

export interface PracticeStep {
  title: string;
  description: string;
  duration?: string;
}

export interface Practice {
  title: string;
  intro?: string;
  steps?: PracticeStep[];
}

export interface PracticesStructured {
  practices?: Practice[];
}

export interface ReflectionStructured {
  prompts?: string[];
}

export interface CourseLink {
  title: string;
  slug: string;
  description?: string;
}

export interface CoursesStructured {
  courses?: CourseLink[];
}

export interface Resource {
  title: string;
  author?: string;
  type?: 'book' | 'article' | 'video' | 'podcast';
  description?: string;
  url?: string;
}

export interface ResourcesStructured {
  resources?: Resource[];
}

export interface GlossaryTerm {
  term: string;
  definition: string;
}

export interface GlossaryStructured {
  terms?: GlossaryTerm[];
}

// --- Union of all structured types ---
export type SectionStructured =
  | HeroStructured
  | CoreQuestionStructured
  | AnchorQuoteStructured
  | OverviewStructured
  | ModelStructured
  | ScriptureStructured
  | CaseStudiesStructured
  | FaqStructured
  | PracticesStructured
  | ReflectionStructured
  | CoursesStructured
  | ResourcesStructured
  | GlossaryStructured;

// --- Database row shape ---
export interface PathwaySection {
  id: string;
  pathway_id: string;
  section_type: PathwaySectionType;
  title: string | null;
  slug: string;
  body: string | null;
  structured: SectionStructured;
  order_index: number;
  status: string;
  organization_id: string | null;
  created_at: string;
  updated_at: string;
}

// --- Typed section helpers ---
export type TypedSection<T extends PathwaySectionType, S extends SectionStructured> = PathwaySection & {
  section_type: T;
  structured: S;
};

export type HeroSection = TypedSection<'hero', HeroStructured>;
export type CoreQuestionSection = TypedSection<'core_question', CoreQuestionStructured>;
export type AnchorQuoteSection = TypedSection<'anchor_quote', AnchorQuoteStructured>;
export type OverviewSection = TypedSection<'overview', OverviewStructured>;
export type ModelSection = TypedSection<'model', ModelStructured>;
export type ScriptureSection = TypedSection<'scripture', ScriptureStructured>;
export type CaseStudiesSection = TypedSection<'case_studies', CaseStudiesStructured>;
export type FaqSection = TypedSection<'faq', FaqStructured>;
export type PracticesSection = TypedSection<'practices', PracticesStructured>;
export type ReflectionSection = TypedSection<'reflection', ReflectionStructured>;
export type CoursesSection = TypedSection<'courses', CoursesStructured>;
export type ResourcesSection = TypedSection<'resources', ResourcesStructured>;
export type GlossarySection = TypedSection<'glossary', GlossaryStructured>;
```

### Step 2 — Create `src/hooks/usePathwaySections.ts`

```typescript
import { useQuery } from '@tanstack/react-query';
import { apiFetch } from '../api/client';
import type { PathwaySection, PathwaySectionType } from '../types/pathway-section';

/** Fetch all sections for a pathway, ordered by order_index */
export function usePathwaySections(pathwayId: string | null) {
  return useQuery({
    queryKey: ['pathway-sections', pathwayId],
    queryFn: () => apiFetch<PathwaySection[]>(`/pathway-sections/${pathwayId}`),
    enabled: !!pathwayId,
  });
}

/** Fetch a single section by pathway + section_type */
export function usePathwaySection(pathwayId: string | null, sectionType: PathwaySectionType) {
  return useQuery({
    queryKey: ['pathway-sections', pathwayId, sectionType],
    queryFn: () => apiFetch<PathwaySection>(`/pathway-sections/${pathwayId}/${sectionType}`),
    enabled: !!pathwayId,
  });
}

/** Helper to extract a typed section from the full sections array */
export function findSection<T extends PathwaySectionType>(
  sections: PathwaySection[] | undefined,
  type: T
): PathwaySection | undefined {
  return sections?.find((s) => s.section_type === type);
}
```

### Step 3 — Create `server/routes/pathway-sections.routes.ts`

```typescript
import { Router } from 'express';
import { eq, and, asc } from 'drizzle-orm';
import { getDb, schema } from '../db';
import { getTenantOrgId } from '../tenant';

export const pathwaySectionsRouter = Router();

// Get all sections for a pathway (by pathway_id), ordered by order_index
pathwaySectionsRouter.get('/:pathwayId', async (req, res) => {
  try {
    const orgId = getTenantOrgId();
    const { pathwayId } = req.params;

    const rows = await getDb()
      .select()
      .from(schema.pathwaySections)
      .where(
        and(
          eq(schema.pathwaySections.pathway_id, pathwayId),
          eq(schema.pathwaySections.organization_id, orgId)
        )
      )
      .orderBy(asc(schema.pathwaySections.order_index));

    res.json(rows);
  } catch (err) {
    console.error('GET /api/pathway-sections/:pathwayId error:', err);
    res.status(500).json({ error: 'Failed to fetch pathway sections' });
  }
});

// Get single section by pathway_id + section_type
pathwaySectionsRouter.get('/:pathwayId/:sectionType', async (req, res) => {
  try {
    const orgId = getTenantOrgId();
    const { pathwayId, sectionType } = req.params;

    const [row] = await getDb()
      .select()
      .from(schema.pathwaySections)
      .where(
        and(
          eq(schema.pathwaySections.pathway_id, pathwayId),
          eq(schema.pathwaySections.section_type, sectionType),
          eq(schema.pathwaySections.organization_id, orgId)
        )
      );

    if (!row) {
      res.status(404).json({ error: 'Section not found' });
      return;
    }

    res.json(row);
  } catch (err) {
    console.error('GET /api/pathway-sections/:pathwayId/:sectionType error:', err);
    res.status(500).json({ error: 'Failed to fetch pathway section' });
  }
});
```

**Register the route** in the server's main router file alongside the existing `pathwaysRouter`:
```typescript
import { pathwaySectionsRouter } from './routes/pathway-sections.routes';
app.use('/api/pathway-sections', pathwaySectionsRouter);
```

### Types-only mode:
If the user specified "types-only", stop after this phase and report what was generated.

---

## Phase 3 — Component Decomposition Plan

### Section-to-component mapping:

| section_type | Component | shadcn/ui primitives | Client? | Key data fields |
|-------------|-----------|---------------------|---------|-----------------|
| `hero` | `PathwayHero` | — | Server | title, subtitle, hero_quote, hero_image_brief |
| `core_question` | `PathwayCoreQuestion` | Card | Server | question from structured |
| `anchor_quote` | `PathwayAnchorQuote` | Card | Server | quote, source, book |
| `overview` | `PathwayOverview` | — | Server | body (markdown prose) |
| `model` | `PathwayModel` | Card, Tabs | Client | elements[] with title/body |
| `scripture` | `PathwayScripture` | Accordion | Client | refs[] with reference/text |
| `case_studies` | `PathwayCaseStudies` | Card | Client | studies[] |
| `faq` | `PathwayFaq` | Accordion | Client | items[] Q&A |
| `practices` | `PathwayPractices` | Card, Badge | Client | practices[] with steps |
| `reflection` | `PathwayReflection` | Card | Server | prompts[] |
| `courses` | `PathwayCourses` | Card, Button | Client | courses[] links |
| `resources` | `PathwayResources` | Card, Badge | Server | resources[] |
| `glossary` | `PathwayGlossary` | Accordion | Client | terms[] |

### Component directory structure:
```
src/components/pathway/
  ├── pathway-hero.tsx
  ├── pathway-core-question.tsx
  ├── pathway-anchor-quote.tsx
  ├── pathway-overview.tsx
  ├── pathway-model.tsx
  ├── pathway-scripture.tsx
  ├── pathway-case-studies.tsx
  ├── pathway-faq.tsx
  ├── pathway-practices.tsx
  ├── pathway-reflection.tsx
  ├── pathway-courses.tsx
  ├── pathway-resources.tsx
  ├── pathway-glossary.tsx
  └── pathway-page-shell.tsx   # Client wrapper that fetches all sections
```

### Present the plan to the user and wait for approval before Phase 4.

---

## Phase 4 — Build Components

Build bottom-up: individual section components first, then the page shell.

### Component pattern:

Each section component receives its typed section data as a prop — it does NOT fetch data itself. The page shell fetches all sections via `usePathwaySections` and distributes them.

```tsx
// Example: src/components/pathway/pathway-faq.tsx
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import type { FaqSection } from "@/types/pathway-section";

interface PathwayFaqProps {
  section: FaqSection;
}

export function PathwayFaq({ section }: PathwayFaqProps) {
  const items = section.structured.items ?? [];

  if (items.length === 0) return null;

  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-bold text-foreground">
        {section.title ?? "Frequently Asked Questions"}
      </h2>
      <Accordion type="single" collapsible className="w-full">
        {items.map((item, i) => (
          <AccordionItem key={i} value={`faq-${i}`}>
            <AccordionTrigger>{item.question}</AccordionTrigger>
            <AccordionContent>{item.answer}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  );
}
```

### Page shell pattern:

```tsx
// src/components/pathway/pathway-page-shell.tsx
"use client";

import { usePathway } from "@/hooks/usePathways";
import { usePathwaySections, findSection } from "@/hooks/usePathwaySections";
import type { PathwaySection } from "@/types/pathway-section";

import { PathwayHero } from "./pathway-hero";
import { PathwayCoreQuestion } from "./pathway-core-question";
import { PathwayAnchorQuote } from "./pathway-anchor-quote";
import { PathwayOverview } from "./pathway-overview";
import { PathwayModel } from "./pathway-model";
import { PathwayScripture } from "./pathway-scripture";
import { PathwayCaseStudies } from "./pathway-case-studies";
import { PathwayFaq } from "./pathway-faq";
import { PathwayPractices } from "./pathway-practices";
import { PathwayReflection } from "./pathway-reflection";
import { PathwayCourses } from "./pathway-courses";
import { PathwayResources } from "./pathway-resources";
import { PathwayGlossary } from "./pathway-glossary";

interface PathwayPageShellProps {
  pathwayId: string;
}

export function PathwayPageShell({ pathwayId }: PathwayPageShellProps) {
  const { data: pathway, isLoading: pathwayLoading } = usePathway(pathwayId);
  const { data: sections, isLoading: sectionsLoading } = usePathwaySections(pathwayId);

  if (pathwayLoading || sectionsLoading) {
    return <PathwayPageSkeleton />;
  }

  if (!pathway || !sections) {
    return <div className="text-center py-12 text-muted-foreground">Pathway not found</div>;
  }

  const hero = findSection(sections, 'hero');
  const coreQuestion = findSection(sections, 'core_question');
  const anchorQuote = findSection(sections, 'anchor_quote');
  const overview = findSection(sections, 'overview');
  const model = findSection(sections, 'model');
  const scripture = findSection(sections, 'scripture');
  const caseStudies = findSection(sections, 'case_studies');
  const faq = findSection(sections, 'faq');
  const practices = findSection(sections, 'practices');
  const reflection = findSection(sections, 'reflection');
  const courses = findSection(sections, 'courses');
  const resources = findSection(sections, 'resources');
  const glossary = findSection(sections, 'glossary');

  return (
    <div className="space-y-16">
      {hero && <PathwayHero section={hero} />}
      {coreQuestion && <PathwayCoreQuestion section={coreQuestion} />}
      {anchorQuote && <PathwayAnchorQuote section={anchorQuote} />}
      {overview && <PathwayOverview section={overview} />}
      {model && <PathwayModel section={model} />}
      {scripture && <PathwayScripture section={scripture} />}
      {caseStudies && <PathwayCaseStudies section={caseStudies} />}
      {faq && <PathwayFaq section={faq} />}
      {practices && <PathwayPractices section={practices} />}
      {reflection && <PathwayReflection section={reflection} />}
      {courses && <PathwayCourses section={courses} />}
      {resources && <PathwayResources section={resources} />}
      {glossary && <PathwayGlossary section={glossary} />}
    </div>
  );
}

function PathwayPageSkeleton() {
  return (
    <div className="space-y-16 animate-pulse">
      <div className="h-64 bg-muted rounded-lg" />
      <div className="h-24 bg-muted rounded-lg max-w-2xl mx-auto" />
      <div className="space-y-4">
        <div className="h-6 bg-muted rounded w-1/3" />
        <div className="h-4 bg-muted rounded w-full" />
        <div className="h-4 bg-muted rounded w-5/6" />
      </div>
    </div>
  );
}
```

### Rules for every component:

1. **Props, not fetches** — section components receive their `PathwaySection` as a prop
2. **Null-safe** — always default structured fields (`section.structured.items ?? []`)
3. **Return null for empty** — if a section has no meaningful content, render nothing
4. **Semantic tokens** — `text-foreground`, `bg-card`, `border-border`, never hex values
5. **shadcn/ui** — Accordion for expandable lists, Card for contained content, Badge for labels, Tabs for multi-view
6. **Markdown rendering** — for `body` fields containing markdown, use the project's markdown renderer or `dangerouslySetInnerHTML` with sanitization. Check if `@/components/ui/markdown` or a similar utility exists first.
7. **Type assertions** — when passing to typed section components, assert the type: `section={hero as HeroSection}`

---

## Phase 5 — Compose the Page

Create the page route that renders the shell:

```tsx
// src/app/(public)/pathways/[slug]/page.tsx
import { PathwayPageShell } from "@/components/pathway/pathway-page-shell";

interface PathwayPageProps {
  params: { slug: string };
}

export default function PathwayPage({ params }: PathwayPageProps) {
  // The shell needs a pathway_id, but the route gives us a slug.
  // Option A: Pass slug and let shell resolve it via usePathways
  // Option B: Server-side lookup to get the ID
  // Use the approach that matches the project's existing pattern.
  return <PathwayPageShell pathwaySlug={params.slug} />;
}
```

If the page route already exists, the page shell must coexist or replace only the sections portion. Check the existing page before writing.

---

## Phase 6 — Verification Checklist

After building, verify:

- [ ] Types file `src/types/pathway-section.ts` exists with all 13 section structured types
- [ ] Hook file `src/hooks/usePathwaySections.ts` exists with `usePathwaySections` and `usePathwaySection`
- [ ] Server route `server/routes/pathway-sections.routes.ts` exists and is registered
- [ ] All 13 section components exist in `src/components/pathway/`
- [ ] Page shell fetches via hooks, never direct API calls
- [ ] No hardcoded colors — only semantic Tailwind classes
- [ ] No hardcoded tenant strings — uses `tenantConfig` where appropriate
- [ ] All components use shadcn/ui primitives
- [ ] Every section component handles empty/null data gracefully
- [ ] TypeScript compiles without errors (`pnpm tsc --noEmit`)
- [ ] No existing files were overwritten without archiving
- [ ] Drizzle schema includes `pathwaySections` table (in `shared/alan-hirsch/database/schema.ts`)

Report the checklist results to the user.

---

## Phase 7 — Build Report

```markdown
## Pathway Builder — Complete

### Pathway
- **Slug:** [pathway slug]
- **Sections built:** [count] / 13

### New Files Created
1. `src/types/pathway-section.ts` — Section types and structured JSONB shapes
2. `src/hooks/usePathwaySections.ts` — TanStack Query hooks
3. `server/routes/pathway-sections.routes.ts` — Express route
4. `src/components/pathway/pathway-hero.tsx` — Hero section
5. `src/components/pathway/pathway-core-question.tsx` — Core question
6. ... [list all]
13. `src/components/pathway/pathway-glossary.tsx` — Glossary
14. `src/components/pathway/pathway-page-shell.tsx` — Client shell
15. `src/app/(public)/pathways/[slug]/page.tsx` — Page route

### Archived
- [List any archived files, or "None — fresh build"]

### Data Flow
```
pathway_sections table
  → GET /api/pathway-sections/:pathwayId
    → usePathwaySections(pathwayId)
      → PathwayPageShell
        → findSection(sections, 'hero') → <PathwayHero section={...} />
        → findSection(sections, 'faq')  → <PathwayFaq section={...} />
        → ... (13 sections)
```

### Flagged Issues
- [Any missing dependencies, schema gaps, or items needing manual attention]

### Prerequisites
- [ ] Run migration `001_create_pathway_sections.sql` in Supabase
- [ ] Run seed `002_seed_pathway_sections.sql` to populate content
- [ ] Register route in server entry: `app.use('/api/pathway-sections', pathwaySectionsRouter)`

### Next Steps
- Run `pnpm dev` and navigate to `/pathways/[slug]`
- Verify all 13 sections render with database content
- Run `/design-audit` to check visual quality
- Run `/responsive-audit` to check breakpoints
```

---

## Anti-Patterns

- **Never create API routes or hooks that duplicate existing Layer 1-5 files.** Check first.
- **Never fetch data inside section components.** The shell fetches; sections receive props.
- **Never copy markdown content into component files.** All content comes from the database at runtime.
- **Never use the old `PathwaySections` type** (from `src/types/pathway.ts`) for new pathway pages. That type maps to the legacy `attachments` JSONB column. Use `PathwaySection` from `src/types/pathway-section.ts`.
- **Never hardcode section order.** Use `order_index` from the database.
- **Never skip the decomposition plan.** Present it to the user before building.
- **Never put all 13 sections in one giant component file.** One file per section type.
