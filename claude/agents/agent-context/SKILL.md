---
name: agent-context
description: Build or modify user context systems — profile assembly, RunContract payloads, context schemas, catalog validation. Use when working on how user data flows into agents.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Work on agent context: $ARGUMENTS

## Before Starting

1. Read the context system across repos:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/instructions/context.ts` — dynamic context section built per run
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/lib/chat/build-user-context-instructions.ts` — renders human-readable blocks from user profile
   - `src/lib/ai-lab/build-user-context-blocks.ts` — `buildUserContextBlocksNew()` for template-aligned context
   - `src/lib/ai-lab/assemble-user-context.ts` — draft → agent context mapping
   - `src/lib/ai-lab/context-schema-template.ts` — `AILabNewContextDraft` schema
   - `src/lib/ai-lab/context-schema.ts` — legacy `AILabContextDraft` schema
2. Read the catalog for validation:
   - `src/lib/ai-lab/catalog.ts` — book slugs, topic slugs, `validateBookSlugs()`, `validateTopicSlugs()`
3. Read the RunContract type:
   - Search for `RunContract` in ai-lab-agent: booksFocus, booksRead, topicsSelected, conversationType, language, experienceLevel, ministryContext, vocational, kairosTags, lifeEvents

## Context Architecture

```
UI Drawer (client)
    │
    ▼
AILabNewContextDraft (Zod-validated)
    │  name, location, vocational, personality,
    │  neighborhood, kairos, engagement,
    │  booksFocus[], topicsSelected[]
    │
    ▼
buildRunContractPayload() — validates slugs against catalog
    │
    ▼
RunContract (sent to agent)
    │  booksFocus, booksRead, topicsSelected,
    │  conversationType, language, experienceLevel,
    │  ministryContext, vocational, kairosTags, lifeEvents
    │
    ▼
buildUserContextInstructions(contract) — renders markdown blocks
    │
    ▼
Dynamic Instructions (injected into agent prompt per run)
```

## Context Schema (Template-Aligned)

```typescript
// AILabNewContextDraft — what the UI drawer collects
export const aiLabNewContextDraftSchema = z.object({
  name: z.string().optional(),
  location: z.string().optional(),
  vocational: z.object({
    role: z.string().optional(),
    context: z.string().optional(),
  }).optional(),
  personality: z.object({
    type: z.string().optional(),     // e.g., MBTI, Enneagram
    details: z.string().optional(),
  }).optional(),
  neighborhood: z.object({
    description: z.string().optional(),
    challenges: z.string().optional(),
  }).optional(),
  kairos: z.object({
    worldEvents: z.string().optional(),
    lifeEvents: z.string().optional(),
  }).optional(),
  engagement: z.enum(['exploring', 'learning', 'applying', 'leading']).optional(),
  booksFocus: z.array(z.string()).optional(),
  topicsSelected: z.array(z.string()).optional(),
  language: z.string().default('en'),
});
```

## Building Context Blocks

Convert structured context into human-readable markdown for the agent:

```typescript
export function buildUserContextBlocks(context: RunContract): string {
  const blocks: string[] = [];

  if (context.userName) {
    blocks.push(`## User\nYou are speaking with **${context.userName}**.`);
  }

  if (context.vocational?.role) {
    blocks.push(`## Vocational Context\nRole: ${context.vocational.role}\nContext: ${context.vocational.context || 'Not specified'}`);
  }

  if (context.booksFocus?.length) {
    const bookTitles = context.booksFocus.map(slug => catalogLookup(slug)?.title).filter(Boolean);
    blocks.push(`## Book Focus\nThe user is particularly interested in: ${bookTitles.join(', ')}`);
  }

  if (context.kairos?.worldEvents) {
    blocks.push(`## Kairos Moment\nWorld events on the user's mind: ${context.kairos.worldEvents}`);
  }

  if (context.engagement) {
    blocks.push(`## Engagement Level\nThe user is currently in the **${context.engagement}** phase.`);
  }

  return blocks.join('\n\n');
}
```

## Catalog Validation

Book and topic slugs from the UI must be validated against the catalog before being sent to the agent:

```typescript
import { validateBookSlugs, validateTopicSlugs } from '@/lib/ai-lab/catalog';

function buildRunContractPayload(draft: AILabNewContextDraft): RunContract {
  return {
    booksFocus: validateBookSlugs(draft.booksFocus || []),     // filters to known slugs
    topicsSelected: validateTopicSlugs(draft.topicsSelected || []),
    language: draft.language || 'en',
    // ... map remaining fields
  };
}
```

The catalog is the SSoT:
- 14 books (5Q, Reframation, The Forgotten Ways, etc.)
- 13 topics (APEST, Missional, mDNA, etc.)
- Unknown slugs are silently dropped (not errors)

## Adding New Context Fields

1. Add to the Zod schema (`context-schema-template.ts`)
2. Add UI collection in the context drawer (`ContextDrawerNew.tsx`)
3. Map to RunContract in `assemble-user-context.ts`
4. Render as a context block in `build-user-context-blocks.ts`
5. Use in dynamic instructions (`context.ts` in ai-lab-agent)

## Multi-Tenant Context

For movemental-dashboard, context also includes org-specific data:

```typescript
// Organization-specific user context
const orgContext = await getAgentPromptContent(organizationId);
// Includes: voice identity, content form templates, writing examples
// These shape the agent's voice, not the user's context
```

User context (who the user IS) and agent content (how the agent SPEAKS) are separate concerns.

## Rules

- Context schemas must be Zod-validated — never trust raw client input
- Validate book/topic slugs against the catalog — drop unknowns silently
- Context blocks should be human-readable markdown (the LLM parses it)
- Dynamic context is NEVER cached — it changes per run
- Keep context blocks concise — each block should be 1-3 lines
- Never include sensitive user data (email, payment info) in context blocks
- User context shapes the conversation; agent content shapes the voice — keep them separate
- Test context building with unit tests that verify block generation for various input shapes
