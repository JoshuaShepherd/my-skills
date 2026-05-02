---
name: write-tests
description: Write agent tests — use when asked to add unit tests, smoke tests, or E2E tests for agents, including tool tests, instruction composition tests, retrieval router tests, citation tests, and guardrail tests.
---

Write agent tests: $ARGUMENTS

## Before Starting

1. Read existing test examples:
   - `{{PROJECT_ROOT}}/tests/` — unit tests for catalog, router, citations, tools, context
   - `{{PROJECT_ROOT}}/e2e/` — Playwright endpoint specs
   - `src/lib/ai-lab/catalog.test.ts` — catalog validation tests (local)
2. Read the smoke test patterns:
   - `{{PROJECT_ROOT}}/smoke-test-chat.ts` — tool-triggering prompts
   - `{{PROJECT_ROOT}}/smoke-test-context.ts` — context propagation
   - `{{PROJECT_ROOT}}/smoke-test-fidelity.ts` — book fidelity (file_search + citations)
3. Check test infrastructure:
   - Run `pnpm test:run` for Vitest (unit tests in `tests/unit/`)
   - Run `pnpm test:e2e` for Playwright (e2e tests in `tests/e2e/`)

## Test Types

### 1. Unit Tests (Vitest)

Location: `tests/unit/agents/`

**Tool tests** — verify tool execution and output shape:
```typescript
import { describe, it, expect, vi } from 'vitest';
import { myTool } from '@/agents/my-agent/tools';

describe('myTool', () => {
  it('returns structured results for valid input', async () => {
    const result = await myTool.execute({ query: 'test query' });
    expect(result).toHaveProperty('data');
    expect(Array.isArray(result.data)).toBe(true);
  });

  it('returns empty results when service is unavailable', async () => {
    vi.stubEnv('EXTERNAL_API_URL', '');
    const result = await myTool.execute({ query: 'test' });
    expect(result.data).toEqual([]);
  });

  it('respects maxResults parameter', async () => {
    const result = await myTool.execute({ query: 'test', maxResults: 3 });
    expect(result.data.length).toBeLessThanOrEqual(3);
  });
});
```

**Instruction tests** — verify prompt composition:
```typescript
import { describe, it, expect } from 'vitest';
import { generateInstructions } from '@/agents/my-agent/instructions';

describe('generateInstructions', () => {
  it('includes core identity section', () => {
    const instructions = generateInstructions({ theme: 'metanoia', mode: 'teacher', style: 'conversation' });
    expect(instructions).toContain('You are');
    expect(instructions).toContain('voice markers');
  });

  it('adapts to theme', () => {
    const metanoia = generateInstructions({ theme: 'metanoia', mode: 'teacher', style: 'conversation' });
    const movemental = generateInstructions({ theme: 'movemental', mode: 'teacher', style: 'conversation' });
    expect(metanoia).not.toEqual(movemental);
  });

  it('includes dynamic context when provided', () => {
    const instructions = generateInstructions(
      { theme: 'metanoia', mode: 'teacher', style: 'conversation' },
      { userName: 'Alice' }
    );
    expect(instructions).toContain('Alice');
  });
});
```

**Router tests** — verify intent classification:
```typescript
import { describe, it, expect } from 'vitest';
import { routeRetrieval } from '@/agents/my-agent/retrieval/router';

describe('routeRetrieval', () => {
  it('classifies quote requests', () => {
    const result = routeRetrieval('What does Alan say about missional ecclesiology?', {});
    expect(result.intent).toBe('QUOTE_REQUEST');
  });

  it('classifies book-specific queries', () => {
    const result = routeRetrieval('Summarize chapter 3 of {{COURSE_NAME}}', { booksFocus: ['{{course-slug}}'] });
    expect(result.intent).toBe('BOOK_SPECIFIC');
    expect(result.temperatureOverride).toBeLessThanOrEqual(0.3);
  });

  it('returns GENERAL for casual conversation', () => {
    const result = routeRetrieval('How are you today?', {});
    expect(result.intent).toBe('GENERAL_CONVERSATION');
  });
});
```

**Citation tests** — verify parsing and rendering:
```typescript
describe('parseSource', () => {
  it('extracts book slug and chapter from file path', () => {
    const source = parseSource('books/{{course-slug}}/ch03-apostolic-environment.md');
    expect(source.bookSlug).toBe('{{course-slug}}');
    expect(source.chapter).toBe(3);
  });
});
```

**Guardrail tests** — verify pass/reject behavior:
```typescript
describe('contentFilter', () => {
  it('blocks script tags', async () => {
    const guardrail = contentFilter();
    const result = await guardrail.validate('<script>alert("xss")</script>');
    expect(result.passed).toBe(false);
  });

  it('passes normal text', async () => {
    const guardrail = contentFilter();
    const result = await guardrail.validate('Tell me about missional leadership');
    expect(result.passed).toBe(true);
  });
});
```

### 2. Smoke Tests (CLI scripts)

Location: `{{SCRIPTS_DIR}}/smoke-tests/` or project root

Smoke tests hit the running agent endpoint and assert behavior:

```typescript
// smoke-test-tool-trigger.ts
const response = await fetch(`${BASE_URL}/api/agents/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${API_KEY}` },
  body: JSON.stringify({
    message: 'What does {{AUTHOR_NAME}} write about APEST in The Permanent Revolution?',
    context: { booksFocus: ['permanent-revolution'] },
  }),
});

const events = await parseSSEStream(response);
const toolCalls = events.filter(e => e.type === 'tool_call');
const doneEvent = events.find(e => e.type === 'done');

assert(toolCalls.length > 0, 'Expected at least one tool call for book query');
assert(toolCalls.some(t => t.name === 'file_search' || t.name === 'search_books'), 'Expected retrieval tool');
assert(doneEvent?.finalOutput?.includes('Source'), 'Expected citations in output');
```

### 3. E2E Tests (Playwright)

Location: `tests/e2e/`

```typescript
import { test, expect } from '@playwright/test';

test('chat endpoint returns valid SSE stream', async ({ request }) => {
  const response = await request.post('/api/agents/chat', {
    data: { message: 'Hello' },
    headers: { Authorization: `Bearer ${process.env.API_KEY}` },
  });
  expect(response.status()).toBe(200);
  expect(response.headers()['content-type']).toContain('text/event-stream');

  const body = await response.text();
  expect(body).toContain('"type":"text_delta"');
  expect(body).toContain('"type":"done"');
});
```

## Running Tests

```bash
# Unit tests
pnpm test:run -- agents           # Run all agent tests
pnpm test:run -- router           # Run router tests
pnpm test:run -- guardrails       # Run guardrail tests

# E2E tests
pnpm test:e2e -- agents           # Run agent e2e specs

# Smoke tests (requires running server)
npx tsx {{SCRIPTS_DIR}}/smoke-tests/smoke-test-tool-trigger.ts
```

## Rules

- Unit tests must not call external APIs — mock external services
- Smoke tests require a running server — document the setup in the test file
- E2E tests use Playwright and run against the dev server
- Test both happy paths and error cases (missing API keys, invalid input, service unavailable)
- For retrieval tests, assert that the correct tools are invoked AND that citations appear in output
- Guardrail tests should cover both pass and reject cases
- Keep test files focused — one test file per concern (tools, router, guardrails, etc.)
