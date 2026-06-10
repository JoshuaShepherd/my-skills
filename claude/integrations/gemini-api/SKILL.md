---
name: gemini-api
description: Build, refine, and master agents using the Google Gemini API and @google/generative-ai SDK. Covers generateContent, function calling, Google Search grounding, multimodal input (text/image/audio/video), streaming, context caching, and the Gemini 2.5 and 3.x model families. Fetches live docs from ai.google.dev. Use when building or debugging anything on Google Gemini.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

Build or refine a Gemini API agent: $ARGUMENTS

$ARGUMENTS can include:
- What to build (e.g. `multimodal agent`, `grounded chatbot`, `function calling pipeline`, `streaming assistant`)
- A file path to existing code to refine
- A capability to add (e.g. `add Google Search grounding`, `add audio input`, `add video analysis`, `add caching`)
- A model preference (e.g. `--model 2.5-pro`, `--model 2.5-flash`, `--model 2.5-flash-lite`)
- API surface preference (e.g. `--api gemini` for ai.google.dev, `--api vertex` for Vertex AI)
- Empty — scaffold a starter agent with best-practice defaults

---

## Authoritative Sources

Always fetch fresh docs before generating or advising on code. These are the canonical Google sources:

| Resource | URL |
|----------|-----|
| Model overview (current IDs) | `https://ai.google.dev/gemini-api/docs/models` |
| Quickstart | `https://ai.google.dev/gemini-api/docs/quickstart` |
| Function calling guide | `https://ai.google.dev/gemini-api/docs/function-calling` |
| Grounding with Google Search | `https://ai.google.dev/gemini-api/docs/grounding` |
| Multimodal input | `https://ai.google.dev/gemini-api/docs/vision` |
| Audio input | `https://ai.google.dev/gemini-api/docs/audio` |
| Video input | `https://ai.google.dev/gemini-api/docs/video` |
| Context caching | `https://ai.google.dev/gemini-api/docs/caching` |
| Streaming | `https://ai.google.dev/gemini-api/docs/text-generation#streaming` |
| Live API (audio/video realtime) | `https://ai.google.dev/gemini-api/docs/live` |
| Pricing | `https://ai.google.dev/gemini-api/docs/pricing` |
| Vertex AI pricing | `https://cloud.google.com/vertex-ai/generative-ai/pricing` |

**Fetch the model overview and the relevant guide before writing any code.** Gemini model IDs and feature availability evolve rapidly.

---

## Environment Setup

```bash
# Gemini API (ai.google.dev — recommended for prototyping + production)
pnpm add @google/generative-ai

# Vertex AI (Google Cloud — recommended for enterprise/compliance)
pnpm add @google-cloud/vertexai
```

```env
# .env.local — Gemini API
GOOGLE_API_KEY=AIza...

# Vertex AI (alternative)
GOOGLE_CLOUD_PROJECT=my-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

```typescript
// src/lib/ai/gemini.ts — Gemini API
import { GoogleGenerativeAI } from '@google/generative-ai';

export const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
```

**Current model IDs (verify against live docs before using):**

*Stable / GA — use for production:*
- `gemini-2.5-pro` — complex tasks, long reasoning, $1.25–$2.50/$10–$15 per 1M (tiered by context)
- `gemini-2.5-flash` — balanced production workloads, $0.30/$2.50 per 1M
- `gemini-2.5-flash-lite` — cheapest quality option, $0.10/$0.40 per 1M

*Preview — do not use in production:*
- `gemini-3.1-pro-preview` — next generation, $2–$4/$12–$18 per 1M
- `gemini-3-flash-preview` — fast preview, $0.50/$3.00 per 1M

**Free tier:** All major models — rate-limited, content may improve Google products.

---

## Phase 1 — Load Context

1. Fetch the model overview to confirm current model IDs and capabilities
2. Read any existing code files specified in $ARGUMENTS
3. Determine: Gemini API (simpler, free tier) vs Vertex AI (enterprise, data residency)
4. Identify modalities needed: text-only vs image/audio/video input
5. Read `_docs/ai-intelligence/` for latest pricing snapshot if available

**Decision rule:**
- Prototyping / startup → Gemini API with free tier
- Enterprise / HIPAA / data residency → Vertex AI
- Audio/video input → Gemini API (only provider with native audio + video in text models)

---

## Phase 2 — Core Patterns

### Pattern 1: Basic Text Generation

```typescript
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);

const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-flash',
  systemInstruction: 'You are a helpful assistant.',
});

const result = await model.generateContent('What is the capital of France?');
console.log(result.response.text());
console.log('Token count:', result.response.usageMetadata);
```

### Pattern 2: Function Calling

```typescript
import {
  GoogleGenerativeAI,
  FunctionDeclaration,
  Tool,
  FunctionCallingMode,
} from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);

const tools: Tool[] = [
  {
    functionDeclarations: [
      {
        name: 'get_weather',
        description: 'Get current weather for a location.',
        parameters: {
          type: 'OBJECT',
          properties: {
            location: {
              type: 'STRING',
              description: 'City and state, e.g. "Austin, TX"',
            },
            unit: {
              type: 'STRING',
              enum: ['celsius', 'fahrenheit'],
              description: 'Temperature unit',
            },
          },
          required: ['location'],
        },
      } satisfies FunctionDeclaration,
    ],
  },
];

const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-flash',
  tools,
  toolConfig: { functionCallingConfig: { mode: FunctionCallingMode.AUTO } },
});

async function runWithTools(userMessage: string) {
  const chat = model.startChat();
  let result = await chat.sendMessage(userMessage);

  while (true) {
    const response = result.response;
    const calls = response.functionCalls();

    if (!calls || calls.length === 0) {
      return response.text();
    }

    // Execute all function calls in parallel
    const functionResults = await Promise.all(
      calls.map(async (call) => {
        const output = await executeTool(call.name, call.args);
        return {
          functionResponse: {
            name: call.name,
            response: output,
          },
        };
      })
    );

    result = await chat.sendMessage(functionResults);
  }
}

async function executeTool(
  name: string,
  args: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  if (name === 'get_weather') {
    return { temperature: 72, unit: args.unit ?? 'fahrenheit', condition: 'sunny' };
  }
  throw new Error(`Unknown tool: ${name}`);
}
```

### Pattern 3: Google Search Grounding

Grounds responses in live Google Search results — no RAG pipeline needed for knowledge-current tasks.

```typescript
import { GoogleGenerativeAI, DynamicRetrievalMode } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);

const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-flash',
  tools: [
    {
      googleSearchRetrieval: {
        dynamicRetrievalConfig: {
          mode: DynamicRetrievalMode.MODE_DYNAMIC,
          dynamicThreshold: 0.3,  // Triggers search when model confidence < 30%
        },
      },
    },
  ],
});

const result = await model.generateContent(
  'What AI models were released in the last 3 months?'
);

// Access grounding metadata (sources used)
const groundingMetadata = result.response.candidates?.[0]?.groundingMetadata;
console.log('Search queries used:', groundingMetadata?.webSearchQueries);
console.log('Sources:', groundingMetadata?.groundingChunks);
console.log('Answer:', result.response.text());
```

**Pricing:** 5,000 free queries/month, then $14/1,000 queries.

### Pattern 4: Multimodal — Image Input

```typescript
import { GoogleGenerativeAI } from '@google/generative-ai';
import fs from 'fs';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

// Inline image (base64)
const imageData = fs.readFileSync('./diagram.png');
const result = await model.generateContent([
  {
    inlineData: {
      mimeType: 'image/png',
      data: imageData.toString('base64'),
    },
  },
  'Describe what you see in this diagram and identify any architectural issues.',
]);

console.log(result.response.text());
```

```typescript
// Image from URL (via File API for large files)
import { GoogleAIFileManager } from '@google/generative-ai/server';

const fileManager = new GoogleAIFileManager(process.env.GOOGLE_API_KEY!);
const uploadedFile = await fileManager.uploadFile('./large-diagram.png', {
  mimeType: 'image/png',
  displayName: 'Architecture Diagram',
});

const result = await model.generateContent([
  { fileData: { mimeType: 'image/png', fileUri: uploadedFile.file.uri } },
  'What does this architecture diagram show?',
]);
```

### Pattern 5: Audio Input (Unique to Gemini)

```typescript
import { GoogleGenerativeAI } from '@google/generative-ai';
import { GoogleAIFileManager } from '@google/generative-ai/server';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
const fileManager = new GoogleAIFileManager(process.env.GOOGLE_API_KEY!);

// Upload audio file
const audio = await fileManager.uploadFile('./interview.mp3', {
  mimeType: 'audio/mpeg',
  displayName: 'Interview Recording',
});

const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });
const result = await model.generateContent([
  { fileData: { mimeType: 'audio/mpeg', fileUri: audio.file.uri } },
  'Transcribe this interview and summarize the key points discussed.',
]);

console.log(result.response.text());
```

**Supported audio formats:** MP3, WAV, FLAC, AAC, OGG, OPUS, WEBM.

### Pattern 6: Video Input (Unique to Gemini)

```typescript
// Upload and analyze video
const video = await fileManager.uploadFile('./demo.mp4', {
  mimeType: 'video/mp4',
  displayName: 'Product Demo',
});

// Wait for processing
let videoFile = await fileManager.getFile(video.file.name);
while (videoFile.state === 'PROCESSING') {
  await new Promise(r => setTimeout(r, 5000));
  videoFile = await fileManager.getFile(video.file.name);
}

if (videoFile.state !== 'ACTIVE') throw new Error('Video processing failed');

const result = await model.generateContent([
  { fileData: { mimeType: 'video/mp4', fileUri: videoFile.uri } },
  'Describe what happens in this video and identify the key moments.',
]);
```

### Pattern 7: Streaming

```typescript
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

const streamResult = await model.generateContentStream('Write a detailed essay about...');

for await (const chunk of streamResult.stream) {
  const text = chunk.text();
  process.stdout.write(text);
}

const finalResponse = await streamResult.response;
console.log('\nTotal tokens:', finalResponse.usageMetadata?.totalTokenCount);
```

**Next.js streaming (App Router):**
```typescript
// app/api/chat/route.ts
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);

export async function POST(req: Request) {
  const { messages } = await req.json();
  const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

  const chat = model.startChat({
    history: messages.slice(0, -1).map((m: { role: string; content: string }) => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }],
    })),
  });

  const streamResult = await chat.sendMessageStream(
    messages[messages.length - 1].content
  );

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of streamResult.stream) {
        controller.enqueue(encoder.encode(chunk.text()));
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
```

### Pattern 8: Multi-Turn Chat

```typescript
const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-flash',
  systemInstruction: 'You are a helpful coding assistant.',
});

const chat = model.startChat({
  history: [
    { role: 'user', parts: [{ text: 'Hello!' }] },
    { role: 'model', parts: [{ text: 'Hi! How can I help you today?' }] },
  ],
  generationConfig: {
    maxOutputTokens: 8192,
    temperature: 0.7,
  },
});

const result1 = await chat.sendMessage('What is TypeScript?');
console.log(result1.response.text());

const result2 = await chat.sendMessage('How does it differ from JavaScript?');
console.log(result2.response.text());
```

### Pattern 9: Context Caching (Large Shared Contexts)

```typescript
import { GoogleAICacheManager } from '@google/generative-ai/server';

const cacheManager = new GoogleAICacheManager(process.env.GOOGLE_API_KEY!);

// Create a cache with large shared content (minimum 32K tokens)
const cache = await cacheManager.create({
  model: 'gemini-2.5-flash',
  displayName: 'large-document-cache',
  systemInstruction: {
    role: 'system',
    parts: [{ text: 'You are an expert analyst of this document.' }],
  },
  contents: [
    {
      role: 'user',
      parts: [{ text: largeDocumentContent }],   // Must be >= 32K tokens
    },
  ],
  ttlSeconds: 3600,   // Cache for 1 hour
});

// Use cached model
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
const cachedModel = genAI.getGenerativeModelFromCachedContent(cache);

const result = await cachedModel.generateContent('What are the main conclusions?');
```

---

## Phase 3 — Agent Patterns

### Autonomous Function-Loop Agent

```typescript
async function runAgent(
  task: string,
  toolDeclarations: FunctionDeclaration[],
  handlers: Record<string, (args: Record<string, unknown>) => Promise<unknown>>,
  maxTurns = 10,
): Promise<string> {
  const model = genAI.getGenerativeModel({
    model: 'gemini-2.5-pro',
    tools: [{ functionDeclarations: toolDeclarations }],
    toolConfig: { functionCallingConfig: { mode: FunctionCallingMode.AUTO } },
  });

  const chat = model.startChat();
  let result = await chat.sendMessage(task);

  for (let turn = 0; turn < maxTurns; turn++) {
    const calls = result.response.functionCalls();
    if (!calls || calls.length === 0) {
      return result.response.text();
    }

    const responses = await Promise.all(
      calls.map(async (call) => ({
        functionResponse: {
          name: call.name,
          response: await handlers[call.name]?.(call.args) ?? { error: 'Unknown tool' },
        },
      }))
    );

    result = await chat.sendMessage(responses);
  }

  throw new Error('Agent exceeded max turns');
}
```

### Grounded Research Agent

```typescript
const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-pro',
  tools: [
    { googleSearchRetrieval: { dynamicRetrievalConfig: { mode: DynamicRetrievalMode.MODE_DYNAMIC } } },
    { functionDeclarations: customTools },
  ],
  systemInstruction: 'You are a research agent. Use Google Search for current facts. Use custom tools for internal data.',
});
```

---

## Phase 4 — Error Handling & Rate Limits

```typescript
import { GoogleGenerativeAI, GoogleGenerativeAIError } from '@google/generative-ai';

async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof GoogleGenerativeAIError) {
        // Check for rate limit (429) or server error (500+)
        const status = (error as { status?: number }).status;
        if ((status === 429 || (status && status >= 500)) && attempt < maxRetries) {
          const delay = Math.pow(2, attempt) * 1000;
          console.warn(`Error ${status}. Retrying in ${delay}ms...`);
          await new Promise(r => setTimeout(r, delay));
          continue;
        }
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

**Safety filters:** Gemini returns a `SAFETY` finish reason if content is blocked. Check `result.response.promptFeedback` to diagnose.

```typescript
const result = await model.generateContent(prompt);
if (result.response.promptFeedback?.blockReason) {
  console.warn('Blocked:', result.response.promptFeedback.blockReason);
  return null;
}
```

---

## Phase 5 — Vertex AI (Enterprise)

```typescript
import { VertexAI } from '@google-cloud/vertexai';

const vertex = new VertexAI({
  project: process.env.GOOGLE_CLOUD_PROJECT!,
  location: process.env.GOOGLE_CLOUD_LOCATION ?? 'us-central1',
});

const model = vertex.getGenerativeModel({
  model: 'gemini-2.5-flash',
});

const result = await model.generateContent({
  contents: [{ role: 'user', parts: [{ text: 'Hello!' }] }],
});

console.log(result.response.candidates?.[0]?.content?.parts?.[0]?.text);
```

**When to use Vertex AI:**
- HIPAA / GDPR compliance required
- Data residency requirements (pick specific Google Cloud region)
- Enterprise IAM and audit logging
- Very high volume with committed use discounts

---

## Phase 6 — Cost Reference (verify at ai.google.dev/gemini-api/docs/pricing)

| Model | Input (≤200K) | Input (>200K) | Output | Status |
|-------|--------------|---------------|--------|--------|
| gemini-2.5-flash-lite | $0.10/M | $0.10/M | $0.40/M | GA ✅ |
| gemini-2.5-flash | $0.30/M | $0.30/M | $2.50/M | GA ✅ |
| gemini-2.5-pro | $1.25/M | $2.50/M | $10–$15/M | GA ✅ |
| gemini-3-flash-preview | $0.50/M | — | $3.00/M | Preview ⚠️ |
| gemini-3.1-pro-preview | $2–$4/M | $4/M | $12–$18/M | Preview ⚠️ |

**Free tier:** All stable models available — rate-limited. Suitable for development and low-volume production.

**Google Search grounding:** 5,000 queries/month free, then $14/1,000 queries.

**Context caching:** Storage fee + reduced read price. Minimum 32K tokens to cache.

---

## Output

When building or scaffolding:
1. Fetch the model overview URL to confirm current model IDs
2. Read any existing code files before modifying
3. Use `gemini-2.5-flash` as default (stable, balanced) — upgrade to `gemini-2.5-pro` for complex reasoning
4. Default to Gemini API (simpler); switch to Vertex AI only if compliance requires it
5. Generate TypeScript with strict types — no `any`
6. Include safety filter handling (check `blockReason`)
7. Include error handling with exponential backoff
8. Write files to their appropriate path (e.g. `src/lib/ai/`, `src/agents/`, `src/app/api/`)

Always state which model ID you used, whether it's GA or Preview, and why.
