---
name: grok-api
description: Build, refine, and master agents using the xAI Grok API — OpenAI-compatible endpoint with grok-4.20 and grok-4-1-fast model families. Covers function calling, 2M context, multi-agent model, structured output, streaming, and cached inputs. Uses the OpenAI SDK with a base URL override. Fetches live docs from docs.x.ai. Use when building or debugging anything on xAI Grok.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

Build or refine a Grok API agent: $ARGUMENTS

$ARGUMENTS can include:
- What to build (e.g. `function calling agent`, `2M context RAG`, `streaming chatbot`, `multi-agent pipeline`)
- A file path to existing code to refine
- A capability to add (e.g. `add function calling`, `add structured output`, `maximize context`, `add reasoning`)
- A model preference (e.g. `--model grok-4.20`, `--model grok-4-1-fast`, `--model grok-4.20-multi-agent`)
- A mode preference (e.g. `--mode reasoning`, `--mode non-reasoning`)
- Empty — scaffold a starter agent with best-practice defaults

---

## Authoritative Sources

Always fetch fresh docs before generating or advising on code. These are the canonical xAI sources:

| Resource | URL |
|----------|-----|
| Model overview + pricing | `https://docs.x.ai/docs/models` |
| Developer docs (entry) | `https://docs.x.ai/docs` |
| Function calling | `https://docs.x.ai/docs/guides/function-calling` |
| Structured outputs | `https://docs.x.ai/docs/guides/structured-outputs` |
| xAI blog (announcements) | `https://x.ai/blog` |

> Note: fetch `https://docs.x.ai/docs` first to discover current guide URLs — xAI's docs structure evolves frequently.

**Fetch the model overview before writing any code.** xAI is releasing models frequently and pricing/IDs change.

---

## Environment Setup

```bash
# Reuse the OpenAI SDK — Grok is fully OpenAI-compatible
pnpm add openai
```

```env
# .env.local
XAI_API_KEY=xai-...
```

```typescript
// src/lib/ai/grok.ts
import OpenAI from 'openai';

export const grok = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});
```

**Current model IDs (verify against live docs before using):**

| Model ID | Context | Input $/M | Cached $/M | Output $/M | Notes |
|----------|---------|-----------|-----------|------------|-------|
| `grok-4.20-0309-reasoning` | 2M | $2.00 | $0.20 | $6.00 | Functions, structured, reasoning |
| `grok-4.20-0309-non-reasoning` | 2M | $2.00 | $0.20 | $6.00 | Functions, structured — faster |
| `grok-4.20-multi-agent-0309` | 2M | $2.00 | $0.20 | $6.00 | Multi-agent variant — only one on market |
| `grok-4-1-fast-reasoning` | 2M | $0.20 | $0.05 | $0.50 | **Best value** — #1 LMArena |
| `grok-4-1-fast-non-reasoning` | 2M | $0.20 | $0.05 | $0.50 | Fastest/cheapest of the family |

**Key facts:**
- #1 LMArena Text Arena (1483 Elo) — grok-4-1-fast-reasoning
- All models: 2M token context window (largest available)
- OpenAI-compatible: swap `baseURL`, reuse OpenAI SDK — no migration cost
- Cached input: 90% off (from $2.00 → $0.20 on grok-4.20, from $0.20 → $0.05 on grok-4-1-fast)
- Batch API available at 50% off (confirmed on models page)
- `logprobs` not supported on grok-4.20 models

---

## Phase 1 — Load Context

1. Fetch the model overview to confirm current model IDs and pricing
2. Read any existing code files specified in $ARGUMENTS
3. Read `_docs/ai-intelligence/` for latest snapshot if available
4. Determine model tier:
   - **grok-4-1-fast** → high-volume tasks, chatbots, RAG, content generation at commodity price
   - **grok-4.20** → complex reasoning, multi-step agents, high-accuracy tasks
   - **grok-4.20-multi-agent** → orchestrator role in multi-agent systems (only dedicated multi-agent model on market)
5. Determine reasoning mode:
   - `reasoning` → better accuracy, slower, slightly more tokens
   - `non-reasoning` → fastest output, use for latency-sensitive tasks

---

## Phase 2 — Core Patterns

### Pattern 1: Basic Completion

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'grok-4-1-fast-reasoning',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});

console.log(response.choices[0].message.content);
console.log('Tokens:', response.usage);
```

### Pattern 2: Function Calling

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});

const tools: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'search_knowledge_base',
      description: 'Search the internal knowledge base for relevant information.',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query',
          },
          top_k: {
            type: 'number',
            description: 'Number of results to return (default: 5)',
          },
        },
        required: ['query'],
        additionalProperties: false,
      },
      strict: true,
    },
  },
];

async function runWithTools(userMessage: string) {
  const messages: OpenAI.ChatCompletionMessageParam[] = [
    { role: 'user', content: userMessage },
  ];

  while (true) {
    const response = await client.chat.completions.create({
      model: 'grok-4-1-fast-reasoning',
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

    // Execute all tool calls in parallel
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

async function executeTool(
  name: string,
  args: Record<string, unknown>,
): Promise<unknown> {
  if (name === 'search_knowledge_base') {
    // Replace with real search implementation
    return { results: [], query: args.query };
  }
  throw new Error(`Unknown tool: ${name}`);
}
```

### Pattern 3: Structured Output (JSON Schema)

```typescript
import { z } from 'zod';
import { zodResponseFormat } from 'openai/helpers/zod';

const ArticleSchema = z.object({
  title: z.string(),
  summary: z.string(),
  topics: z.array(z.string()),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
});

const response = await client.beta.chat.completions.parse({
  model: 'grok-4-1-fast-non-reasoning',
  messages: [
    { role: 'system', content: 'Extract article metadata accurately.' },
    { role: 'user', content: articleText },
  ],
  response_format: zodResponseFormat(ArticleSchema, 'article'),
});

const article = response.choices[0].message.parsed;
// Typed as z.infer<typeof ArticleSchema>
```

**Manual JSON schema (without Zod):**
```typescript
const response = await client.chat.completions.create({
  model: 'grok-4-1-fast-non-reasoning',
  messages: [...],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'extraction',
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
  model: 'grok-4-1-fast-reasoning',
  messages: [{ role: 'user', content: 'Write a detailed analysis...' }],
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

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});

export async function POST(req: Request) {
  const { messages } = await req.json();

  const stream = await client.chat.completions.stream({
    model: 'grok-4-1-fast-reasoning',
    messages,
  });

  return new Response(stream.toReadableStream(), {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
```

### Pattern 5: 2M Context — Direct Document Injection

Grok's 2M context makes traditional RAG chunking optional for most document sets.

```typescript
import fs from 'fs';

// Load entire document corpus directly into context
function loadDocuments(paths: string[]): string {
  return paths
    .map(p => {
      const content = fs.readFileSync(p, 'utf-8');
      return `<document path="${p}">\n${content}\n</document>`;
    })
    .join('\n\n');
}

const documents = loadDocuments([
  './docs/guide.md',
  './docs/api-reference.md',
  './docs/changelog.md',
  // Add more — up to ~2M tokens total
]);

const response = await client.chat.completions.create({
  model: 'grok-4-1-fast-reasoning',
  messages: [
    {
      role: 'system',
      content: `You have access to the following documentation:\n\n${documents}`,
    },
    { role: 'user', content: 'How do I configure authentication?' },
  ],
});
```

**When to use direct injection vs RAG:**
- Direct injection: document set < 1.5M tokens, need cross-document reasoning, simpler architecture
- RAG: document set > 1.5M tokens, need citation precision, updates frequently

### Pattern 6: Prompt Caching (90% off cached tokens)

Cache reused system prompts and context to dramatically reduce costs on repeated requests.

```typescript
// Grok supports prompt caching — cached tokens cost $0.05/M vs $0.20/M on grok-4-1-fast
// Cache is automatic when the same prefix is reused across requests

// Pattern: put the large, stable content at the START of the system message
// Grok caches the longest common prefix automatically
const largeSystemPrompt = `
You are an expert assistant with deep knowledge of the following documentation:

${LARGE_DOCUMENT_CONTEXT}  // This prefix will be cached after first request

Always cite specific sections when answering questions.
`;

// First request — cache miss, full price
const response1 = await client.chat.completions.create({
  model: 'grok-4-1-fast-reasoning',
  messages: [
    { role: 'system', content: largeSystemPrompt },
    { role: 'user', content: 'Question 1' },
  ],
});

// Subsequent requests — cache hit on the shared prefix, 90% cheaper
const response2 = await client.chat.completions.create({
  model: 'grok-4-1-fast-reasoning',
  messages: [
    { role: 'system', content: largeSystemPrompt },  // Same prefix → cache hit
    { role: 'user', content: 'Question 2' },
  ],
});

// Check cache usage
console.log('Cache hit tokens:', response2.usage?.prompt_tokens_details?.cached_tokens);
```

### Pattern 7: Multi-Turn Conversation

```typescript
class GrokConversation {
  private messages: OpenAI.ChatCompletionMessageParam[] = [];

  constructor(
    private client: OpenAI,
    private systemPrompt: string,
    private model = 'grok-4-1-fast-reasoning',
  ) {}

  async send(userContent: string): Promise<string> {
    this.messages.push({ role: 'user', content: userContent });

    const response = await this.client.chat.completions.create({
      model: this.model,
      messages: [
        { role: 'system', content: this.systemPrompt },
        ...this.messages,
      ],
    });

    const assistantMessage = response.choices[0].message;
    this.messages.push(assistantMessage);
    return assistantMessage.content ?? '';
  }

  reset() {
    this.messages = [];
  }
}
```

---

## Phase 3 — Agent Patterns

### Autonomous Tool-Loop Agent

```typescript
async function runGrokAgent(
  task: string,
  tools: OpenAI.ChatCompletionTool[],
  toolHandlers: Record<string, (args: Record<string, unknown>) => Promise<unknown>>,
  model = 'grok-4.20-0309-reasoning',
  maxTurns = 15,
): Promise<string> {
  const messages: OpenAI.ChatCompletionMessageParam[] = [
    { role: 'user', content: task },
  ];

  for (let turn = 0; turn < maxTurns; turn++) {
    const response = await client.chat.completions.create({
      model,
      tools,
      tool_choice: 'auto',
      messages,
    });

    const choice = response.choices[0];
    messages.push(choice.message);

    if (choice.finish_reason === 'stop') {
      return choice.message.content ?? '';
    }

    if (choice.finish_reason !== 'tool_calls') break;

    const toolResults = await Promise.all(
      (choice.message.tool_calls ?? []).map(async (tc) => {
        const handler = toolHandlers[tc.function.name];
        if (!handler) throw new Error(`No handler for: ${tc.function.name}`);
        const output = await handler(JSON.parse(tc.function.arguments));
        return {
          role: 'tool' as const,
          tool_call_id: tc.id,
          content: JSON.stringify(output),
        };
      })
    );

    messages.push(...toolResults);
  }

  throw new Error('Agent exceeded max turns');
}
```

### Multi-Agent Orchestration (grok-4.20-multi-agent)

The `grok-4.20-multi-agent` model is the only dedicated multi-agent model variant on the market. Use it as the orchestrator.

```typescript
const orchestratorTools: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'run_researcher',
      description: 'Delegate a research task to the researcher subagent.',
      parameters: {
        type: 'object',
        properties: {
          task: { type: 'string', description: 'The research task to perform' },
        },
        required: ['task'],
        additionalProperties: false,
      },
      strict: true,
    },
  },
  {
    type: 'function',
    function: {
      name: 'run_writer',
      description: 'Delegate a writing task to the writer subagent, with research context.',
      parameters: {
        type: 'object',
        properties: {
          task: { type: 'string' },
          context: { type: 'string', description: 'Research findings to incorporate' },
        },
        required: ['task', 'context'],
        additionalProperties: false,
      },
      strict: true,
    },
  },
];

const orchestratorHandlers = {
  run_researcher: async ({ task }: { task: string }) =>
    runGrokAgent(task, researcherTools, researcherHandlers, 'grok-4-1-fast-reasoning'),
  run_writer: async ({ task, context }: { task: string; context: string }) =>
    runGrokAgent(
      `${task}\n\nResearch context:\n${context}`,
      writerTools,
      writerHandlers,
      'grok-4-1-fast-reasoning',
    ),
};

// Use the multi-agent model as orchestrator
const result = await runGrokAgent(
  'Research recent AI developments and write a 1000-word summary.',
  orchestratorTools,
  orchestratorHandlers,
  'grok-4.20-multi-agent-0309',  // dedicated orchestrator model
);
```

### RAG with 2M Context (Simplified Architecture)

```typescript
// With 2M context, you can skip chunking for most use cases
class GrokRAG {
  private client: OpenAI;
  private documents: Map<string, string> = new Map();

  constructor() {
    this.client = new OpenAI({
      apiKey: process.env.XAI_API_KEY,
      baseURL: 'https://api.x.ai/v1',
    });
  }

  addDocument(name: string, content: string) {
    this.documents.set(name, content);
  }

  buildContext(): string {
    return Array.from(this.documents.entries())
      .map(([name, content]) => `<document name="${name}">\n${content}\n</document>`)
      .join('\n\n');
  }

  async query(question: string): Promise<string> {
    const context = this.buildContext();
    // Estimate tokens: ~0.75 tokens per word, or use tiktoken
    const estimatedTokens = context.split(' ').length * 0.75;
    if (estimatedTokens > 1_800_000) {
      throw new Error('Document set exceeds safe 2M context limit. Implement chunking.');
    }

    const response = await this.client.chat.completions.create({
      model: 'grok-4-1-fast-reasoning',
      messages: [
        {
          role: 'system',
          content: `You are a helpful assistant. Answer questions based on the provided documents.\n\n${context}`,
        },
        { role: 'user', content: question },
      ],
    });

    return response.choices[0].message.content ?? '';
  }
}
```

---

## Phase 4 — Migrating from OpenAI

Since Grok uses the OpenAI-compatible API, migration is a 2-line change:

```typescript
// BEFORE (OpenAI)
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const model = 'gpt-5.4-mini';

// AFTER (Grok)
const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});
const model = 'grok-4-1-fast-reasoning';
```

**Known differences from OpenAI:**
- `logprobs` not supported on grok-4.20 models
- No Batch API (use real-time only)
- No DALL-E or image generation in the text API (separate `grok-imagine-image` endpoint)
- No Assistants API / Threads API
- No fine-tuning (as of last research — verify at docs.x.ai)

---

## Phase 5 — Error Handling & Rate Limits

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});

async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof OpenAI.RateLimitError) {
        const delay = Math.pow(2, attempt) * 1000;
        console.warn(`Rate limited. Retrying in ${delay}ms...`);
        await new Promise(r => setTimeout(r, delay));
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

---

## Phase 6 — Image Generation (Separate API)

Grok has a dedicated image generation API separate from the text models.

```typescript
// Image generation — NOT OpenAI-compatible, use fetch directly
const response = await fetch('https://api.x.ai/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.XAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'grok-imagine-image',    // or 'grok-imagine-image-pro'
    prompt: 'A futuristic city at sunset',
    n: 1,
  }),
});

const data = await response.json();
console.log(data.data[0].url);
```

**Image pricing:** `grok-imagine-image` = $0.02/image (300 RPM), `grok-imagine-image-pro` = $0.07/image (30 RPM).

---

## Phase 7 — Cost Reference (verify at docs.x.ai)

| Model | Input $/M | Cached $/M | Output $/M | Context |
|-------|-----------|-----------|------------|---------|
| grok-4-1-fast-reasoning | $0.20 | $0.05 | $0.50 | 2M |
| grok-4-1-fast-non-reasoning | $0.20 | $0.05 | $0.50 | 2M |
| grok-4.20-0309-reasoning | $2.00 | $0.20 | $6.00 | 2M |
| grok-4.20-0309-non-reasoning | $2.00 | $0.20 | $6.00 | 2M |
| grok-4.20-multi-agent-0309 | $2.00 | $0.20 | $6.00 | 2M |

**No Batch API** — all requests real-time.

**Cost formula:**
```
cost = (input_tokens / 1_000_000 × input_price)
     + (output_tokens / 1_000_000 × output_price)
     - (cached_tokens / 1_000_000 × (input_price - cached_price))
```

**Strategic note:** grok-4-1-fast at $0.20/$0.50 per 1M is the most disruptive value in the market as of Q1 2026. At 93% cheaper than Claude Sonnet / GPT-5.4-mini on input, any task currently on a mid-tier model should be evaluated on grok-4-1-fast first.

---

## Output

When building or scaffolding:
1. Fetch the model overview URL to confirm current model IDs
2. Read any existing code files before modifying
3. Default to `grok-4-1-fast-reasoning` for most tasks — only upgrade to grok-4.20 for complex multi-step reasoning
4. Use `grok-4.20-multi-agent-0309` when building multi-agent orchestrators
5. Always use OpenAI SDK with `baseURL` override — no new SDK needed
6. Include caching pattern when the system prompt is large and reused
7. Note any OpenAI features that are NOT supported (logprobs, Batch API, Assistants API)
8. Write files to their appropriate path (e.g. `src/lib/ai/`, `src/agents/`, `src/app/api/`)

Always state which model ID you used, reasoning vs non-reasoning mode, and why.
