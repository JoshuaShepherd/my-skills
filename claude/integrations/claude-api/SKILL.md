---
name: claude-api
description: Build, refine, and master agents using the Anthropic Claude API and @anthropic-ai/sdk. Covers messages API, tool use, extended thinking, prompt caching, streaming, and multi-agent patterns. Fetches live docs from docs.anthropic.com. Use when building or debugging anything on the Claude API.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

Build or refine a Claude API agent: $ARGUMENTS

$ARGUMENTS can include:
- What to build (e.g. `tool-use agent`, `streaming chatbot`, `multi-step reasoning agent`)
- A file path to existing code to refine
- A capability to add (e.g. `add caching`, `add extended thinking`, `add computer use`)
- A model preference (e.g. `--model opus`, `--model sonnet`, `--model haiku`)
- Empty — scaffold a starter agent with best-practice defaults

---

## Authoritative Sources

Always fetch fresh docs before generating or advising on code. These are the canonical Anthropic sources:

| Resource | URL |
|----------|-----|
| Model overview (current IDs) | `https://docs.anthropic.com/en/docs/about-claude/models/overview` |
| Messages API reference | `https://docs.anthropic.com/en/api/messages` |
| Tool use guide | `https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview` |
| Extended thinking | `https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking` |
| Prompt caching | `https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching` |
| Streaming | `https://docs.anthropic.com/en/docs/build-with-claude/streaming` |
| Computer use | `https://docs.anthropic.com/en/docs/build-with-claude/computer-use` |
| Batch API | `https://docs.anthropic.com/en/docs/build-with-claude/message-batches` |
| Errors & rate limits | `https://docs.anthropic.com/en/api/errors` |
| Pricing | `https://www.anthropic.com/pricing` |

**Fetch the model overview and the relevant API reference page before writing any code.** Model IDs change — never use memory alone.

---

## Environment Setup

```bash
pnpm add @anthropic-ai/sdk
```

```env
# .env.local
ANTHROPIC_API_KEY=sk-ant-...
```

```typescript
// src/lib/ai/anthropic.ts
import Anthropic from '@anthropic-ai/sdk';

export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

**Current model IDs (verify against live docs before using):**
- `claude-opus-4-6` — 1M context, 128k output, $5/$25 per 1M — highest capability
- `claude-sonnet-4-6` — 1M context, 64k output, $3/$15 per 1M — best balanced (Jan 2026 cutoff)
- `claude-haiku-4-5-20251001` — 200k context, 64k output, $1/$5 per 1M — fastest/cheapest

---

## Phase 1 — Load Context

1. Fetch the model overview page to confirm current model IDs
2. Read any existing code files specified in $ARGUMENTS
3. Read `_docs/ai-intelligence/` for latest pricing/capability snapshot if available
4. Identify the pattern needed: basic call / tool use / thinking / caching / streaming / computer use / multi-agent

---

## Phase 2 — Core Patterns

### Pattern 1: Basic Message

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 4096,
  system: 'You are a helpful assistant.',
  messages: [
    { role: 'user', content: 'Hello, world!' }
  ],
});

console.log(message.content[0].type === 'text' ? message.content[0].text : '');
```

### Pattern 2: Tool Use (Function Calling)

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: 'get_weather',
    description: 'Get current weather for a location.',
    input_schema: {
      type: 'object' as const,
      properties: {
        location: {
          type: 'string',
          description: 'City and state, e.g. "San Francisco, CA"',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          description: 'Temperature unit',
        },
      },
      required: ['location'],
    },
  },
];

async function runWithTools(userMessage: string) {
  const messages: Anthropic.MessageParam[] = [
    { role: 'user', content: userMessage }
  ];

  while (true) {
    const response = await client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      tools,
      messages,
    });

    // If no tool use, we're done
    if (response.stop_reason === 'end_turn') {
      const textBlock = response.content.find(b => b.type === 'text');
      return textBlock?.type === 'text' ? textBlock.text : '';
    }

    // Collect all tool_use blocks
    const toolUseBlocks = response.content.filter(
      (b): b is Anthropic.ToolUseBlock => b.type === 'tool_use'
    );

    if (toolUseBlocks.length === 0) break;

    // Add assistant turn
    messages.push({ role: 'assistant', content: response.content });

    // Execute tools and collect results
    const toolResults: Anthropic.ToolResultBlockParam[] = await Promise.all(
      toolUseBlocks.map(async (toolUse) => {
        const result = await executeTool(toolUse.name, toolUse.input);
        return {
          type: 'tool_result' as const,
          tool_use_id: toolUse.id,
          content: JSON.stringify(result),
        };
      })
    );

    // Add user turn with all tool results
    messages.push({ role: 'user', content: toolResults });
  }
}

async function executeTool(name: string, input: unknown): Promise<unknown> {
  // Dispatch to real tool implementations
  if (name === 'get_weather') {
    return { temperature: 72, unit: 'fahrenheit', condition: 'sunny' };
  }
  throw new Error(`Unknown tool: ${name}`);
}
```

### Pattern 3: Extended Thinking

```typescript
const response = await client.messages.create({
  model: 'claude-opus-4-6',    // or claude-sonnet-4-6
  max_tokens: 16000,
  thinking: {
    type: 'enabled',
    budget_tokens: 10000,       // how many tokens Claude can think with
  },
  messages: [{ role: 'user', content: 'Solve this step by step: ...' }],
});

// Thinking blocks come before text blocks
for (const block of response.content) {
  if (block.type === 'thinking') {
    console.log('Thinking:', block.thinking);
  } else if (block.type === 'text') {
    console.log('Answer:', block.text);
  }
}
```

**Adaptive Thinking (Opus 4.6 + Sonnet 4.6 only):**
```typescript
thinking: {
  type: 'auto',    // Claude allocates budget dynamically per task complexity
}
```

### Pattern 4: Prompt Caching

Cache large, reused content to save 90% on cached token costs.

```typescript
const response = await client.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 4096,
  system: [
    {
      type: 'text',
      text: LARGE_SYSTEM_PROMPT,          // e.g. 10k token brand voice instructions
      cache_control: { type: 'ephemeral' }, // cached for 5 minutes (default)
    },
  ],
  messages: [{ role: 'user', content: userQuery }],
});
```

**Cache durations:**
- `ephemeral` (default) — 5 minutes
- For 1-hour cache: check current docs — Anthropic extended cache TTL to 1 hour for some plans

**When to cache:**
- System prompts > 1,024 tokens that don't change between requests
- Large document context fed to every request
- Tool definitions (cache the full tools array)

**Cost with caching:**
- Write: $3.75/M (Sonnet) — slightly above standard on first write
- Read: $0.30/M (Sonnet) — 90% cheaper than standard $3.00

### Pattern 5: Streaming

```typescript
const stream = client.messages.stream({
  model: 'claude-sonnet-4-6',
  max_tokens: 4096,
  messages: [{ role: 'user', content: 'Write a long essay about...' }],
});

// Preferred: use the helper methods
const text = await stream.finalText();

// Or process events manually
for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text);
  }
}

const finalMessage = await stream.finalMessage();
console.log('Usage:', finalMessage.usage);
```

**Next.js streaming (App Router):**
```typescript
// app/api/chat/route.ts
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

export async function POST(req: Request) {
  const { messages } = await req.json();

  const stream = client.messages.stream({
    model: 'claude-sonnet-4-6',
    max_tokens: 4096,
    messages,
  });

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const event of stream) {
        if (
          event.type === 'content_block_delta' &&
          event.delta.type === 'text_delta'
        ) {
          controller.enqueue(encoder.encode(event.delta.text));
        }
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
```

### Pattern 6: Multi-Turn Conversation State

```typescript
class ClaudeConversation {
  private messages: Anthropic.MessageParam[] = [];
  private client = new Anthropic();

  async send(userContent: string): Promise<string> {
    this.messages.push({ role: 'user', content: userContent });

    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      system: this.systemPrompt,
      messages: this.messages,
    });

    const assistantText = response.content
      .filter((b): b is Anthropic.TextBlock => b.type === 'text')
      .map(b => b.text)
      .join('');

    this.messages.push({ role: 'assistant', content: response.content });
    return assistantText;
  }

  reset() {
    this.messages = [];
  }

  constructor(private systemPrompt: string) {}
}
```

### Pattern 7: Batch API (50% off, async)

```typescript
// Submit batch
const batch = await client.beta.messages.batches.create({
  requests: items.map((item, i) => ({
    custom_id: `item-${i}`,
    params: {
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 1024,
      messages: [{ role: 'user', content: item.prompt }],
    },
  })),
});

// Poll until complete
let result = await client.beta.messages.batches.retrieve(batch.id);
while (result.processing_status === 'in_progress') {
  await new Promise(r => setTimeout(r, 60000));
  result = await client.beta.messages.batches.retrieve(batch.id);
}

// Stream results
for await (const entry of client.beta.messages.batches.results(batch.id)) {
  if (entry.result.type === 'succeeded') {
    console.log(entry.custom_id, entry.result.message.content);
  }
}
```

---

## Phase 3 — Agent Patterns

### Autonomous Tool-Loop Agent

```typescript
async function runAgent(
  task: string,
  tools: Anthropic.Tool[],
  toolHandlers: Record<string, (input: unknown) => Promise<unknown>>,
  maxTurns = 10,
): Promise<string> {
  const client = new Anthropic();
  const messages: Anthropic.MessageParam[] = [
    { role: 'user', content: task }
  ];

  for (let turn = 0; turn < maxTurns; turn++) {
    const response = await client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 8192,
      tools,
      tool_choice: { type: 'auto' },
      messages,
    });

    messages.push({ role: 'assistant', content: response.content });

    if (response.stop_reason === 'end_turn') {
      return response.content
        .filter((b): b is Anthropic.TextBlock => b.type === 'text')
        .map(b => b.text)
        .join('');
    }

    if (response.stop_reason !== 'tool_use') break;

    const toolResults: Anthropic.ToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type !== 'tool_use') continue;
      const handler = toolHandlers[block.name];
      if (!handler) throw new Error(`No handler for tool: ${block.name}`);
      const output = await handler(block.input);
      toolResults.push({
        type: 'tool_result',
        tool_use_id: block.id,
        content: JSON.stringify(output),
      });
    }

    messages.push({ role: 'user', content: toolResults });
  }

  throw new Error('Agent exceeded max turns');
}
```

### Multi-Agent Orchestration (Claude-as-Orchestrator)

```typescript
// Orchestrator delegates to specialized subagents
const orchestratorTools: Anthropic.Tool[] = [
  {
    name: 'delegate_to_researcher',
    description: 'Delegate a research subtask to the researcher agent.',
    input_schema: {
      type: 'object' as const,
      properties: {
        task: { type: 'string', description: 'The research task' },
      },
      required: ['task'],
    },
  },
  {
    name: 'delegate_to_writer',
    description: 'Delegate a writing subtask to the writer agent.',
    input_schema: {
      type: 'object' as const,
      properties: {
        task: { type: 'string', description: 'The writing task' },
        context: { type: 'string', description: 'Background context from research' },
      },
      required: ['task', 'context'],
    },
  },
];

const subagentHandlers = {
  delegate_to_researcher: async ({ task }: { task: string }) => {
    return runAgent(task, researcherTools, researcherHandlers);
  },
  delegate_to_writer: async ({ task, context }: { task: string; context: string }) => {
    return runAgent(`${task}\n\nContext: ${context}`, writerTools, writerHandlers);
  },
};
```

---

## Phase 4 — Provider-Specific Optimizations

### 1M Context Usage (Opus/Sonnet 4.6)

```typescript
// Read entire codebase into context — no chunking needed
import fs from 'fs';
import path from 'path';

function readDirectory(dir: string): string {
  const files = fs.readdirSync(dir, { recursive: true }) as string[];
  return files
    .filter(f => f.endsWith('.ts') || f.endsWith('.tsx'))
    .map(f => {
      const fullPath = path.join(dir, f);
      const content = fs.readFileSync(fullPath, 'utf-8');
      return `\`\`\`typescript\n// ${f}\n${content}\n\`\`\``;
    })
    .join('\n\n');
}

const response = await client.messages.create({
  model: 'claude-opus-4-6',
  max_tokens: 8192,
  messages: [{
    role: 'user',
    content: `Here is the entire codebase:\n\n${readDirectory('./src')}\n\nNow refactor...`
  }],
});
```

### Computer Use (claude-opus-4-6 / claude-sonnet-4-6)

```typescript
const response = await client.beta.messages.create({
  model: 'claude-opus-4-6',
  max_tokens: 4096,
  betas: ['computer-use-2025-01-24'],   // check docs for latest beta string
  tools: [
    { type: 'computer_20250124', name: 'computer', display_width_px: 1280, display_height_px: 800 },
    { type: 'text_editor_20250429', name: 'str_replace_based_edit_tool' },
    { type: 'bash_20250124', name: 'bash' },
  ],
  messages: [{ role: 'user', content: 'Open the browser and navigate to docs.anthropic.com' }],
});
```

---

## Phase 5 — Error Handling & Rate Limits

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

async function callWithRetry(
  params: Anthropic.MessageCreateParamsNonStreaming,
  maxRetries = 3,
): Promise<Anthropic.Message> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await client.messages.create(params);
    } catch (error) {
      if (error instanceof Anthropic.RateLimitError) {
        const delay = Math.pow(2, attempt) * 1000;
        console.warn(`Rate limited. Waiting ${delay}ms...`);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      if (error instanceof Anthropic.APIError) {
        console.error(`API error ${error.status}: ${error.message}`);
        if (error.status >= 500 && attempt < maxRetries) continue;
        throw error;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

**HTTP status codes:**
- `400` — Bad request (invalid params)
- `401` — Invalid API key
- `403` — Permission denied
- `404` — Resource not found
- `429` — Rate limit (retry with backoff)
- `500/529` — Overloaded (retry with backoff)

---

## Phase 6 — Cost Reference (verify at anthropic.com/pricing)

| Model | Input | Cache Write | Cache Read | Output | Batch In | Batch Out |
|-------|-------|-------------|------------|--------|----------|-----------|
| Opus 4.6 | $5/M | $6.25/M | $0.50/M | $25/M | $2.50/M | $12.50/M |
| Sonnet 4.6 | $3/M | $3.75/M | $0.30/M | $15/M | $1.50/M | $7.50/M |
| Haiku 4.5 | $1/M | $1.25/M | $0.10/M | $5/M | $0.50/M | $2.50/M |

**Fast Mode (Opus 4.6, beta):** $30 input / $150 output — ~6× faster, does not stack with Batch.

**Cost formula:**
```
cost = (input_tokens / 1_000_000 × input_price)
     + (output_tokens / 1_000_000 × output_price)
     - (cached_tokens / 1_000_000 × (input_price - cache_read_price))
```

---

## Output

When building or scaffolding:
1. Fetch the model overview URL to confirm current model IDs
2. Read any existing code files before modifying
3. Generate TypeScript with strict types — no `any`
4. Include error handling and rate limit retry logic
5. Add a cost comment showing tokens × price for the chosen model
6. Write files to their appropriate path (e.g. `src/lib/ai/`, `src/agents/`, `src/app/api/`)

Always state which model ID you used and why.
