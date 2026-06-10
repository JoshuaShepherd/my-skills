---
name: openai-api
description: Build, refine, and master agents using the OpenAI API — Chat Completions, Responses API, and OpenAI Agents SDK. Covers function calling, structured output, streaming, multi-agent handoffs, and the full gpt-5.4 family. Fetches live docs from platform.openai.com and openai.github.io/openai-agents-python. Use when building or debugging anything on OpenAI.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

Build or refine an OpenAI agent: $ARGUMENTS

$ARGUMENTS can include:
- What to build (e.g. `function calling agent`, `streaming chatbot`, `multi-agent pipeline`, `structured output extractor`)
- A file path to existing code to refine
- A capability to add (e.g. `add structured output`, `add web search tool`, `add handoffs`)
- A model preference (e.g. `--model gpt-5.4`, `--model gpt-5.4-mini`, `--model o3`)
- SDK preference (e.g. `--sdk agents` for OpenAI Agents SDK, `--sdk chat` for Chat Completions)
- Empty — scaffold a starter agent with best-practice defaults

---

## Authoritative Sources

Always fetch fresh docs before generating or advising on code. These are the canonical OpenAI sources:

| Resource | URL |
|----------|-----|
| Model overview | `https://platform.openai.com/docs/models` |
| Chat Completions API | `https://platform.openai.com/docs/api-reference/chat` |
| Responses API (Agents SDK) | `https://platform.openai.com/docs/api-reference/responses` |
| Function calling | `https://platform.openai.com/docs/guides/function-calling` |
| Structured outputs | `https://platform.openai.com/docs/guides/structured-outputs` |
| Streaming | `https://platform.openai.com/docs/api-reference/streaming` |
| Batch API | `https://platform.openai.com/docs/guides/batch` |
| OpenAI Agents SDK (Python) | `https://openai.github.io/openai-agents-python/` |
| Agents SDK GitHub | `https://github.com/openai/openai-agents-python` |
| Pricing | `https://openai.com/api/pricing/` |
| Rate limits | `https://platform.openai.com/docs/guides/rate-limits` |

**Fetch the model page and the relevant guide before writing any code.** Model IDs and capabilities change frequently.

---

## Environment Setup

```bash
pnpm add openai
# For Agents SDK (TypeScript — community port or Python-first)
pnpm add @openai/agents   # if available; check npm for current package name
```

```env
# .env.local
OPENAI_API_KEY=sk-proj-...
```

```typescript
// src/lib/ai/openai.ts
import OpenAI from 'openai';

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});
```

**Current model IDs (verify against live docs before using):**
- `gpt-5.4` — 1.05M context, flagship, $2.50/$15 per 1M — most capable standard model
- `gpt-5.4-mini` — 1.05M context, balanced, $0.75/$4.50 per 1M — best value for most tasks
- `gpt-5.4-nano` — 1.05M context, fast/cheap, $0.20/$1.25 per 1M — high-volume simple tasks
- `gpt-5.4-pro` — 1.05M context, ultra, $30/$180 per 1M — highest-stakes tasks
- `o3` — 200k context, reasoning SOTA — coding/math/science
- `o4-mini` — 200k context, fast reasoning
- `o3-pro` — 200k context, extended compute reasoning

---

## Phase 1 — Load Context

1. Fetch the model overview to confirm current model IDs and capabilities
2. Read any existing code files specified in $ARGUMENTS
3. Determine the right SDK: Chat Completions API (simpler, universal) vs Responses API / Agents SDK (structured agent loops)
4. Read `_docs/ai-intelligence/` for latest pricing snapshot if available

**Decision rule:**
- Simple chatbot, RAG, extraction → Chat Completions
- Autonomous agents with tool loops, handoffs, tracing → Responses API / Agents SDK

---

## Phase 2 — Core Patterns

### Pattern 1: Basic Chat Completion

```typescript
import OpenAI from 'openai';

const client = new OpenAI();

const response = await client.chat.completions.create({
  model: 'gpt-5.4-mini',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});

console.log(response.choices[0].message.content);
console.log('Tokens used:', response.usage);
```

### Pattern 2: Function Calling

```typescript
import OpenAI from 'openai';

const client = new OpenAI();

const tools: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get current weather for a location.',
      parameters: {
        type: 'object',
        properties: {
          location: { type: 'string', description: 'City and state, e.g. "Austin, TX"' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['location'],
        additionalProperties: false,
      },
      strict: true,   // Enable strict mode for guaranteed schema adherence
    },
  },
];

async function runWithTools(userMessage: string) {
  const messages: OpenAI.ChatCompletionMessageParam[] = [
    { role: 'user', content: userMessage },
  ];

  while (true) {
    const response = await client.chat.completions.create({
      model: 'gpt-5.4-mini',
      tools,
      tool_choice: 'auto',
      messages,
    });

    const choice = response.choices[0];
    messages.push(choice.message);

    if (choice.finish_reason === 'stop') {
      return choice.message.content;
    }

    if (choice.finish_reason !== 'tool_calls') break;

    // Execute tool calls in parallel
    const toolResults = await Promise.all(
      (choice.message.tool_calls ?? []).map(async (toolCall) => {
        const args = JSON.parse(toolCall.function.arguments);
        const result = await executeTool(toolCall.function.name, args);
        return {
          role: 'tool' as const,
          tool_call_id: toolCall.id,
          content: JSON.stringify(result),
        };
      })
    );

    messages.push(...toolResults);
  }
}

async function executeTool(name: string, args: Record<string, unknown>): Promise<unknown> {
  if (name === 'get_weather') {
    return { temp: 72, unit: args.unit ?? 'fahrenheit', condition: 'sunny' };
  }
  throw new Error(`Unknown tool: ${name}`);
}
```

### Pattern 3: Structured Outputs (Guaranteed JSON Schema)

```typescript
import OpenAI from 'openai';
import { zodResponseFormat } from 'openai/helpers/zod';
import { z } from 'zod';

const client = new OpenAI();

const ArticleSchema = z.object({
  title: z.string(),
  summary: z.string(),
  topics: z.array(z.string()),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
  publishedAt: z.string(),
});

const response = await client.beta.chat.completions.parse({
  model: 'gpt-5.4-mini',
  messages: [
    { role: 'system', content: 'Extract article metadata accurately.' },
    { role: 'user', content: articleText },
  ],
  response_format: zodResponseFormat(ArticleSchema, 'article'),
});

const article = response.choices[0].message.parsed;
// article is typed as z.infer<typeof ArticleSchema>
```

**Without Zod (manual JSON schema):**
```typescript
const response = await client.chat.completions.create({
  model: 'gpt-5.4-mini',
  messages: [...],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'article',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          topics: { type: 'array', items: { type: 'string' } },
        },
        required: ['title', 'topics'],
        additionalProperties: false,
      },
    },
  },
});

const data = JSON.parse(response.choices[0].message.content ?? '{}');
```

### Pattern 4: Streaming

```typescript
const stream = await client.chat.completions.stream({
  model: 'gpt-5.4-mini',
  messages: [{ role: 'user', content: 'Write a long essay...' }],
});

for await (const chunk of stream) {
  const delta = chunk.choices[0]?.delta?.content;
  if (delta) process.stdout.write(delta);
}

const finalCompletion = await stream.finalChatCompletion();
console.log('Total tokens:', finalCompletion.usage?.total_tokens);
```

**Next.js streaming (App Router):**
```typescript
// app/api/chat/route.ts
import OpenAI from 'openai';

const client = new OpenAI();

export async function POST(req: Request) {
  const { messages } = await req.json();

  const stream = await client.chat.completions.stream({
    model: 'gpt-5.4-mini',
    messages,
  });

  return new Response(stream.toReadableStream(), {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
```

### Pattern 5: Reasoning Models (o3 / o4-mini)

```typescript
// o3 does not support system messages — use developer role
const response = await client.chat.completions.create({
  model: 'o3',
  reasoning_effort: 'high',   // 'low' | 'medium' | 'high'
  messages: [
    {
      role: 'developer',   // not 'system' for o-series
      content: 'You are a helpful coding assistant.',
    },
    { role: 'user', content: 'Write a Rust implementation of quicksort...' },
  ],
  // Note: temperature, top_p, and tools may be restricted on o-series
  // Always check docs for current o-model constraints
});
```

### Pattern 6: Batch API (50% off, async)

```typescript
import fs from 'fs';

// 1. Create JSONL file of requests
const requests = items.map((item, i) => ({
  custom_id: `item-${i}`,
  method: 'POST',
  url: '/v1/chat/completions',
  body: {
    model: 'gpt-5.4-nano',
    messages: [{ role: 'user', content: item.prompt }],
    max_tokens: 512,
  },
}));

fs.writeFileSync('batch_requests.jsonl', requests.map(r => JSON.stringify(r)).join('\n'));

// 2. Upload file
const file = await client.files.create({
  file: fs.createReadStream('batch_requests.jsonl'),
  purpose: 'batch',
});

// 3. Create batch
const batch = await client.batches.create({
  input_file_id: file.id,
  endpoint: '/v1/chat/completions',
  completion_window: '24h',
});

// 4. Poll until complete
let result = await client.batches.retrieve(batch.id);
while (result.status === 'in_progress' || result.status === 'validating') {
  await new Promise(r => setTimeout(r, 30000));
  result = await client.batches.retrieve(batch.id);
}

// 5. Download results
const output = await client.files.content(result.output_file_id!);
const lines = (await output.text()).split('\n').filter(Boolean);
const results = lines.map(line => JSON.parse(line));
```

---

## Phase 3 — Responses API & Agents SDK

The Responses API is the foundation of the OpenAI Agents SDK. It supports multi-turn agent loops with built-in tool execution, tracing, and handoffs.

### Responses API (Single Turn)

```typescript
const response = await client.responses.create({
  model: 'gpt-5.4',
  input: 'Summarize this document and extract action items.',
  tools: [
    { type: 'web_search_preview' },      // Built-in web search
    { type: 'file_search', vector_store_ids: ['vs_abc123'] }, // Built-in RAG
    { type: 'code_interpreter', container: { type: 'auto' } }, // Code execution
  ],
});

for (const output of response.output) {
  if (output.type === 'message') {
    console.log(output.content);
  }
}
```

### OpenAI Agents SDK (Python-first, TypeScript community port)

The official Agents SDK is Python-first. For TypeScript projects, use the Responses API directly or use a community port. Check npm for `@openai/agents`.

**Python pattern for reference (the authoritative API):**
```python
from agents import Agent, Runner, handoff, tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    return f"Sunny, 72°F in {location}"

researcher = Agent(
    name="Researcher",
    instructions="You research topics thoroughly.",
    tools=[get_weather],
)

writer = Agent(
    name="Writer",
    instructions="You write clear, compelling content.",
    handoffs=[researcher],
)

result = Runner.run_sync(writer, "Write a report on climate in Austin, TX")
print(result.final_output)
```

**TypeScript equivalent using Responses API directly:**
```typescript
type AgentConfig = {
  name: string;
  instructions: string;
  tools: OpenAI.ResponsesAPI.Tool[];
  model: string;
};

async function runAgent(
  agent: AgentConfig,
  input: string,
  previousResponseId?: string,
): Promise<{ output: string; responseId: string }> {
  const response = await client.responses.create({
    model: agent.model,
    instructions: agent.instructions,
    input,
    tools: agent.tools,
    previous_response_id: previousResponseId,   // Enables conversation state via API
  });

  const text = response.output
    .filter(o => o.type === 'message')
    .flatMap(o => o.content)
    .filter(c => c.type === 'output_text')
    .map(c => c.text)
    .join('');

  return { output: text, responseId: response.id };
}
```

### Configurable Reasoning Effort (gpt-5.4 family)

```typescript
const response = await client.chat.completions.create({
  model: 'gpt-5.4',
  reasoning_effort: 'medium',  // 'none' | 'low' | 'medium' | 'high' | 'extra-high'
  messages: [...],
});
```

---

## Phase 4 — Built-in Tools (Responses API)

### Web Search

```typescript
const response = await client.responses.create({
  model: 'gpt-5.4',
  tools: [{ type: 'web_search_preview' }],
  input: 'What are the latest AI model releases in 2026?',
});
```

### File Search (Vector Store RAG)

```typescript
// 1. Create and populate a vector store
const vs = await client.vectorStores.create({ name: 'my-docs' });
await client.vectorStores.fileBatches.uploadAndPoll(vs.id, {
  files: [fs.createReadStream('./docs/guide.pdf')],
});

// 2. Use in agent
const response = await client.responses.create({
  model: 'gpt-5.4',
  tools: [{ type: 'file_search', vector_store_ids: [vs.id] }],
  input: 'What does the guide say about authentication?',
});
```

### Code Interpreter

```typescript
const response = await client.responses.create({
  model: 'gpt-5.4',
  tools: [{ type: 'code_interpreter', container: { type: 'auto' } }],
  input: 'Calculate the compound interest on $10,000 at 5% for 10 years.',
});
```

---

## Phase 5 — Error Handling & Rate Limits

```typescript
import OpenAI from 'openai';

const client = new OpenAI();

async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof OpenAI.RateLimitError) {
        const retryAfter = parseInt(error.headers?.['retry-after'] ?? '5', 10);
        console.warn(`Rate limited. Retrying after ${retryAfter}s...`);
        await new Promise(r => setTimeout(r, retryAfter * 1000));
        continue;
      }
      if (error instanceof OpenAI.APIError && error.status >= 500 && attempt < maxRetries) {
        await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

**Key error types:** `RateLimitError` (429), `AuthenticationError` (401), `BadRequestError` (400), `InternalServerError` (500).

---

## Phase 6 — Cost Reference (verify at openai.com/api/pricing)

| Model | Input | Cached Input | Output | Batch In | Batch Out | Context |
|-------|-------|-------------|--------|----------|-----------|---------|
| gpt-5.4-nano | $0.20/M | $0.02/M | $1.25/M | $0.10/M | $0.625/M | 1.05M |
| gpt-5.4-mini | $0.75/M | $0.075/M | $4.50/M | $0.375/M | $2.25/M | 1.05M |
| gpt-5.4 | $2.50/M | $0.25/M | $15/M | $1.25/M | $7.50/M | 1.05M |
| gpt-5.4-pro | $30/M | — | $180/M | — | — | 1.05M |

**Long context uplift:** prompts >272K tokens incur 2× input + 1.5× output for the full session.

**Cost formula:**
```
cost = (input_tokens / 1_000_000 × input_price)
     + (output_tokens / 1_000_000 × output_price)
     - (cached_tokens / 1_000_000 × (input_price - cached_price))
```

---

## Output

When building or scaffolding:
1. Fetch the model overview URL to confirm current model IDs
2. Read any existing code files before modifying
3. Generate TypeScript with strict types — no `any`
4. Use Chat Completions for simple tasks; Responses API for agent loops
5. Include error handling with exponential backoff
6. Add a cost comment for the chosen model at the expected token volume
7. Write files to their appropriate path (e.g. `src/lib/ai/`, `src/agents/`, `src/app/api/`)

Always state which model ID and API surface you used and why.
