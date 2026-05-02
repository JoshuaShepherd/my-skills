
Export a platform feature as a product constitution and data reference: $ARGUMENTS

$ARGUMENTS should include:
- The feature or slice name (e.g., "course detail page", "article reader", "agent chat", "book listing")
- Optionally: scope constraints ("just the enrollment flow", "only the reading experience")
- Optionally: output path for the generated markdown
- Empty — ask the user which feature to export

## Purpose

This skill produces a **feature constitution** — a complete specification of *what* a feature is and *what data it works with*, without prescribing *how* it should look. The output is designed to be pasted into Google AI Studio Build mode (or any AI prototyping tool) so the tool can make its own design decisions while respecting the data contracts and product requirements.

**Include:** Data shapes, relationships, API contracts, business rules, user stories, acceptance criteria, example payloads.

**Exclude:** CSS variables, design tokens, color palettes, component hierarchies, animation specs, Tailwind classes, responsive breakpoints, typography scales.

## Before Starting

1. Identify the feature's data footprint:
   - **Schema tables** — `{{SCHEMA_PATH}}` (grep for relevant table names)
   - **Zod schemas** — `{{SCHEMAS_DIR}}/` (find matching schema files)
   - **Services** — `{{SERVICES_DIR}}/` and `src/lib/services/custom/`
   - **API routes** — `{{API_DIR}}/` and `src/app/api/custom/`
2. Read the page/component files in `src/app/(public)/` to understand the user-facing behavior
3. Read relevant `{{DOCS_DIR}}/` files for feature narrative context
4. Read `{{CONFIG_PATH}}` for domain context and feature flags

## Discovery Strategy

1. **Start from the page** — Find the page file(s) in `src/app/(public)/` that render this feature
2. **Understand the user flow** — Read the page and its components to understand what the user sees and does
3. **Find the routes** — Grep for API endpoints the feature calls
4. **Find the services** — Grep for service functions those routes use
5. **Find the schemas** — Grep for Zod schemas those services validate against
6. **Find the tables** — Grep for Drizzle tables those schemas derive from

## Document Structure

Generate a single markdown file with these sections. Use XML-style section tags for structured parsing.

### Section 1: Domain Context

```markdown
<domain-context>
# Platform: [tenant name from config]

This is a thought leader platform for [leader name]. The platform serves [audience description from config].

**Domain vocabulary:**
- [Term 1]: [Definition — e.g., "Pathway: A curated learning journey through multiple content types"]
- [Term 2]: [Definition]
- ...

**Active feature flags relevant to this feature:**
- [flag]: [enabled/disabled] — [what it controls]
</domain-context>
```

### Section 2: Feature Charter

Write this section yourself based on what you learn from reading the code and docs. This is the constitution — it defines what the feature *is* and *must do*.

```markdown
<feature-charter>
## Feature: [Name]

### Purpose
[2-3 sentences describing why this feature exists and what value it delivers to the user]

### User Stories
- As a [role], I want to [action] so that [outcome].
- As a [role], I want to [action] so that [outcome].
- ...

### Acceptance Criteria
- [ ] [Observable behavior 1 — written as a testable statement]
- [ ] [Observable behavior 2]
- [ ] [Observable behavior 3]
- [ ] ...

### User Flow
1. User [action] → sees [result]
2. User [action] → sees [result]
3. ...
[Describe the complete happy path and any key branching paths]

### Business Rules
- [Rule 1: e.g., "A user can only enroll in a course once"]
- [Rule 2: e.g., "Lessons must be completed in order within a week"]
- [Rule 3: e.g., "Free users see week 1 only; paid users see all weeks"]
- ...

### Edge Cases & Empty States
- **No data**: [What happens when there are no items to display]
- **Unauthorized**: [What happens for unauthenticated or unpermitted users]
- **Error state**: [What the user should understand if something goes wrong]
- [Any other edge cases discovered in the code]

### Content & Copy Requirements
- [Key content areas: e.g., "Hero section needs a headline, subheadline, and CTA"]
- [Tenant-driven copy: what comes from config vs what is static]
- [Tone guidance from tenant config if relevant]
</feature-charter>
```

### Section 3: Data Model

Extract the relevant Drizzle table definitions and convert to clean TypeScript interfaces.

```markdown
<data-model>
## Database Tables

### [table_name]
```typescript
interface TableName {
  id: string;              // UUID, auto-generated
  organization_id: string; // UUID, tenant scoping
  // ... all columns with types and constraints
  created_at: string;      // ISO timestamp
  updated_at: string;      // ISO timestamp
}
```

### Relationships
- `table_a.foreign_key` → `table_b.id` (one-to-many)
- ...

### Entity Relationship Summary
[Plain-English description of how the tables relate. E.g., "A Course has many Lessons. Each Lesson belongs to one Week. Users enroll in Courses, creating an Enrollment record that tracks progress."]

### Example Data
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  // ... realistic example payload
}
```
</data-model>
```

**Rules for this section:**
- Convert Drizzle column types to TypeScript primitives (text→string, integer→number, boolean→boolean, jsonb→Record<string,unknown>, uuid→string, timestamp→string)
- Include column constraints as comments (notNull, default values, references)
- Generate realistic JSON examples using domain-appropriate content (not lorem ipsum)
- Include ALL tables that participate in the feature, even junction/join tables
- Stop at 2 degrees of relationship separation from the core feature tables

### Section 4: API Contracts

```markdown
<api-contracts>
## Endpoints

### GET /api/simplified/[resource]
**Purpose:** [What this endpoint is for]

**Query params:**
- `organization_id` (required): string
- `limit` (optional): number (default: 20)
- `offset` (optional): number (default: 0)

**Response shape:**
```typescript
interface ListResponse {
  data: ResourceType[];
  total: number;
}
```

**Error responses:**
```typescript
{ success: false, error: string }
```

### POST /api/simplified/[resource]
**Purpose:** [What this endpoint is for]

**Request body:**
```typescript
interface CreateRequest {
  // ... Zod schema fields with required/optional annotations
}
```

**Validation rules:**
- [field]: [constraint — e.g., "min 1 character, max 500"]
- ...
</api-contracts>
```

**Rules:**
- Include the actual Zod validation shapes from `{{SCHEMAS_DIR}}/`
- Note which fields are required vs optional
- Include error response shapes (Result<T> pattern)
- Document any custom endpoints from `src/app/api/custom/`

### Section 5: State & Behavior

```markdown
<state-and-behavior>
## Key State

### Client State
- [What state the UI needs to track — e.g., "selected week index", "search query", "active tab"]
- [Loading/error states for each data fetch]

### Server State (via API)
- [What data is fetched and when — e.g., "Course detail fetched on page load", "Lessons fetched when week is selected"]
- [Caching expectations if any]

### User-Driven State Changes
- [Action] → [State change] → [What should update]
- [Action] → [State change] → [What should update]

### Authentication & Authorization
- [Who can access this feature — anonymous, authenticated, specific roles]
- [What changes based on auth state]
- [How tenant scoping works for this feature]
</state-and-behavior>
```

## Execution Steps

### Step 1 — Discover the Feature Footprint
Trace the feature through schema → services → routes → pages using the discovery strategy above. Read every relevant file.

### Step 2 — Read Domain Context
Read `tenant.config.ts` for domain vocabulary, feature flags, and content context.

### Step 3 — Draft the Document
Assemble all 5 sections into a single markdown file. Write the Feature Charter yourself — synthesize what you've learned into a clear product story.

### Step 4 — Generate Example Data
Create realistic JSON examples for each schema table. Use content that matches the platform's domain (from tenant config context).

### Step 5 — Save and Report

Save the document to: `{{DOCS_DIR}}/studio-exports/[feature-slug].md`

If the directory doesn't exist, create it.

## Output Format

```
## Studio Export: [Feature Name]

### Data Captured
- Schema tables: [count] ([table names])
- API endpoints: [count]
- Business rules: [count]
- User stories: [count]

### Document
Saved to: `{{DOCS_DIR}}/studio-exports/[feature-slug].md`
- Total sections: 5

### How to Use
1. Go to aistudio.google.com → Build mode (or any AI prototyping tool)
2. Paste the full document as context
3. Ask it to build the feature — it will make its own design decisions based on the data model and product requirements
4. Use the acceptance criteria to verify the output

### Next Steps
- Review the charter for accuracy before using
- Add screenshots if you want the prototype to match existing visual style
```

## Anti-Patterns

- **Don't dump raw source files** — Translate Drizzle `pgTable()` calls to clean TypeScript interfaces
- **Don't include implementation details** — Omit middleware internals, auth plumbing, service implementations. Focus on the *shape* of things.
- **Don't use lorem ipsum** — Always generate domain-appropriate example data
- **Don't include 148 tables** — Only include tables that participate in the feature. Stop at 2 degrees of separation.
- **Don't prescribe UI** — No CSS, no component hierarchies, no design tokens, no animation specs. Let the prototyping tool make those decisions.
- **Don't include styling guidance** — No color values, font stacks, spacing scales, or Tailwind classes. The constitution is about *what*, not *how it looks*.
