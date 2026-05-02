---
name: ai-lab-notebook-gemini
description: >
  Expert guidance for managing and optimizing the AI Lab Notebook's Gemini integration
  in this repo — context cache vs File API decisions, corpus manifest lifecycle (48h
  expiry), Gemini/Claude backend switching, model↔cache ID locking, grounded source
  discovery, and build-time upload pipeline. Use whenever the user mentions the ai-lab
  notebook, the Gemini corpus, GEMINI_CORPUS_CACHE_ID, GOOGLE_GENERATIVE_AI_API_KEY,
  notebook chat failures, "corpus not loading", manifest expired, Google Search
  grounding in sources discover, or scripts/gemini-corpus-upload.ts /
  scripts/gemini-corpus-cache.ts. For generic Gemini API questions unrelated to this
  notebook, defer to the `gemini-api` skill.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
---

# AI Lab Notebook — Gemini Integration Skill

The Alan Hirsch AI Lab Notebook is a NotebookLM-style variant of `/ai-lab` that grounds
chat and artifacts in Alan's ~1M-word published corpus. This skill is the operational
manual for the Gemini half of that system: how the corpus reaches the model, what can
silently break, and how to optimize cost and latency.

**Authoritative docs (always fetch fresh when in doubt — Gemini APIs move quickly):**
- Models: https://ai.google.dev/gemini-api/docs/models
- File API: https://ai.google.dev/gemini-api/docs/files
- Context caching: https://ai.google.dev/gemini-api/docs/caching
- Grounding with Google Search: https://ai.google.dev/gemini-api/docs/grounding
- Pricing: https://ai.google.dev/gemini-api/docs/pricing

---

## 1. Where Everything Lives (this repo)

| Concern | Path |
|---|---|
| Notebook page (flag-gated) | `src/app/(public)/ai-lab/page.tsx` — legacy `/ai-lab/notebook` → `permanentRedirect` in `src/app/(public)/ai-lab/notebook/page.tsx` |
| Chat route | [src/app/api/ai-lab-notebook/chat/route.ts](src/app/api/ai-lab-notebook/chat/route.ts) |
| Artifacts route | [src/app/api/ai-lab-notebook/artifacts/route.ts](src/app/api/ai-lab-notebook/artifacts/route.ts) |
| Source discovery (Google Search grounded) | [src/app/api/ai-lab-notebook/sources/discover/route.ts](src/app/api/ai-lab-notebook/sources/discover/route.ts) |
| LLM router (Gemini ↔ Claude) | [src/lib/ai-lab-notebook/notebook-llm.ts](src/lib/ai-lab-notebook/notebook-llm.ts) |
| Corpus config (env, model, cache id) | [src/lib/ai-lab-notebook/corpus.ts](src/lib/ai-lab-notebook/corpus.ts) |
| Corpus manifest I/O (Node-only) | [src/lib/ai-lab-notebook/corpus-gemini-files.ts](src/lib/ai-lab-notebook/corpus-gemini-files.ts) |
| Message augmentation | [src/lib/ai-lab-notebook/augment-notebook-model-messages.ts](src/lib/ai-lab-notebook/augment-notebook-model-messages.ts) |
| Manifest (committed, 48h TTL — legacy) | [src/lib/ai-lab-notebook/corpus-manifest.json](src/lib/ai-lab-notebook/corpus-manifest.json) |
| File Search manifest (persistent) | [src/lib/ai-lab-notebook/file-search-manifest.json](src/lib/ai-lab-notebook/file-search-manifest.json) |
| Build-time upload script (legacy) | [scripts/gemini-corpus-upload.ts](scripts/gemini-corpus-upload.ts) |
| Context cache creator | [scripts/gemini-corpus-cache.ts](scripts/gemini-corpus-cache.ts) |
| **File Search store creator** | [scripts/gemini-file-search-create.ts](scripts/gemini-file-search-create.ts) |
| **File Search uploader (delta)** | [scripts/gemini-file-search-upload.ts](scripts/gemini-file-search-upload.ts) |
| **File Search verifier (canaries)** | [scripts/gemini-file-search-verify.ts](scripts/gemini-file-search-verify.ts) |
| Scope presets + file_search tool | [src/lib/ai-lab-notebook/scope.ts](src/lib/ai-lab-notebook/scope.ts) |
| Automatic scope inference | [src/lib/ai-lab-notebook/scope-inference.ts](src/lib/ai-lab-notebook/scope-inference.ts) |
| Golden-query regression suite | [tests/corpus-retrieval/](tests/corpus-retrieval/) |

**SDKs in use:**
- `@google/genai` — native Gemini SDK used by both scripts (`genai.files.upload`, `genai.caches.create`, `genai.files.get`)
- `@ai-sdk/google` — Vercel AI SDK wrapper used by chat/artifacts/discover routes (`google(modelId)`, `google.tools.googleSearch({})`)

Do **not** mix these in the same call site. Scripts use the native SDK; routes use the AI SDK.

---

## 2. Four Corpus Delivery Modes — Priority-Resolved

As of Phase 5 (April 2026) the notebook resolves **four** retrieval modes in
priority order. Selection is env-driven; `getCorpusRetrievalMode()` in
`corpus.ts` is the authoritative picker.

| Pri | Mode | Trigger | Where corpus lives | Cost profile | Freshness |
|---|---|---|---|---|---|
| **1** | **File Search** (preferred) | `GEMINI_FILE_SEARCH_STORE_ID` set | Gemini-side indexed chunks with semantic retrieval + citations | Free storage, $0.15/M one-time indexing, standard input for retrieved chunks (~10K tokens/query) | Persistent; delta-upload via `pnpm notebook:store:upload` |
| **2** | Context Cache | `GEMINI_CORPUS_CACHE_ID` set | Cached content blob (whole corpus, up to 1M tokens) | ~25% cached-input discount + storage fee | Re-run `pnpm notebook:cache` every 7 days |
| **3** | File API manifest | `corpus-manifest.json` present + unexpired | File parts attached per request | Full input cost every request | 48h TTL; `pnpm build:with-legacy-file-api` |
| **4** | Catalog-only | nothing set | Just titles in system prompt — **ungrounded** | Cheapest | N/A |

**Resolution logic is in `getCorpusRetrievalMode()`**
([src/lib/ai-lab-notebook/corpus.ts](src/lib/ai-lab-notebook/corpus.ts)):
```
if GEMINI_FILE_SEARCH_STORE_ID valid → "file-search" (Mode 1)
if GEMINI_CORPUS_CACHE_ID valid    → "cache"        (Mode 2)
else (app side)                    → "catalog-only" (Mode 4)
                                     (manifest mode is detected at call time
                                      by augment-notebook-model-messages.ts)
```

### Why File Search wins by default (Phase 5 research summary)

- Corpus (~1.8M tokens) exceeds any 1M-token context window. Mode 2/3 must drop books.
- Semantic retrieval surfaces only relevant chunks (~10K tokens) per query → ~99% cost reduction vs Mode 2.
- Automatic citations via `grounding_metadata` — no prompt-engineering hacks.
- Persistent (no 48h/7d expiry churn).
- Supports metadata filters: scope to `book`, `concept`, `framework`, etc.

Keep Mode 2 for rollback; keep Mode 3 as a legacy fallback only.

### Decision rubric — which mode to use when

- **High traffic production (dozens+ calls/hour):** Mode A (context cache). The
  cheapest cache discount (~25% of input) compounds fast. Pay the one-time 7-day cache
  cost.
- **Low traffic / intermittent preview:** Mode B (File API manifest). No cache storage
  fee; refreshes naturally on every `pnpm build`.
- **Corpus is bigger than the model window:** Mode B. Mode A fails at
  `~1,048,576` tokens for `gemini-2.5-flash`
  ([gemini-corpus-cache.ts:53](scripts/gemini-corpus-cache.ts#L53)). The corpus is
  currently ~1.77M tokens by the chars/4 heuristic, so Mode A only works on a subset
  (set `GEMINI_CACHE_CORPUS_SUBDIR` to a subfolder under `corpus/alan_hirsch`).
- **Dev / no API key:** Mode C. The build script is designed to exit 0 when
  `GOOGLE_GENERATIVE_AI_API_KEY` is unset
  ([gemini-corpus-upload.ts:126](scripts/gemini-corpus-upload.ts#L126)).

### The model↔cache locking rule (non-negotiable)

When `GEMINI_CORPUS_CACHE_ID` is set, the inference model **must match the cache
model**. The code enforces this at
[corpus.ts:142-148](src/lib/ai-lab-notebook/corpus.ts#L142-L148):

```ts
export const CORPUS_CACHE_MODEL = "gemini-2.5-flash";  // stable only
export function getCorpusModelId() {
  if (getCorpusCacheId()) return CORPUS_CACHE_MODEL;   // lock to cache model
  return process.env.GEMINI_MODEL || "gemini-3-flash-preview";
}
```

**Why it matters:** Setting `GEMINI_MODEL=gemini-3-flash-preview` while
`GEMINI_CORPUS_CACHE_ID` is also set does nothing — the code silently ignores
`GEMINI_MODEL`. To experiment with preview models, you must **unset
`GEMINI_CORPUS_CACHE_ID`** for that run. Preview models cannot be used as cache models;
they don't support caching at all.

---

## 3. Backend Switching — Gemini vs Claude

The notebook can run on either Gemini or Claude. Controlled by a single env var,
resolved in `getNotebookLlmBackend()`
([notebook-llm.ts:20](src/lib/ai-lab-notebook/notebook-llm.ts#L20)):

```
AI_LAB_NOTEBOOK_LLM unset | "gemini"            → Gemini backend
AI_LAB_NOTEBOOK_LLM="anthropic" | "claude"      → Claude backend
```

**Things that change with the backend:**
- `resolveNotebookLlm()` swaps `google(...)` for `anthropic(...)`
- When Gemini: `providerOptions` includes `{ google: { cachedContent } }` if cache id is set
- When Claude: **no corpus attachment happens at all** — the augment step early-returns
  (see [augment-notebook-model-messages.ts:29](src/lib/ai-lab-notebook/augment-notebook-model-messages.ts#L29)). Claude only sees the catalog titles in the system prompt + user-pasted sources.

**Sources discovery is Gemini-only, always.** The `/sources/discover` route uses
`google.tools.googleSearch({})` for live web grounding
([discover/route.ts:38-40](src/app/api/ai-lab-notebook/sources/discover/route.ts#L38-L40)).
Google Search grounding has no Claude equivalent. If `GOOGLE_GENERATIVE_AI_API_KEY`
is missing, source discovery fails even when `AI_LAB_NOTEBOOK_LLM=anthropic`. Don't try
to route it through Claude.

---

## 4. Environment Variables — Complete Reference

| Var | Purpose | Where read |
|---|---|---|
| `GOOGLE_GENERATIVE_AI_API_KEY` | Gemini API key (native SDK + AI SDK both honor it) | upload/cache scripts; AI SDK picks up automatically |
| `GEMINI_MODEL` | Inference model when no cache is active | [corpus.ts:147](src/lib/ai-lab-notebook/corpus.ts#L147), [discover/route.ts:33](src/app/api/ai-lab-notebook/sources/discover/route.ts#L33) |
| `GEMINI_CORPUS_CACHE_ID` | Context cache name (e.g. `cachedContents/abc…`) | [corpus.ts:124](src/lib/ai-lab-notebook/corpus.ts#L124) |
| `AI_LAB_NOTEBOOK_LLM` | Backend selector (`gemini`/`anthropic`) | [notebook-llm.ts:21](src/lib/ai-lab-notebook/notebook-llm.ts#L21) |
| `AI_LAB_NOTEBOOK_ANTHROPIC_MODEL` | Claude model id override | [notebook-llm.ts:50](src/lib/ai-lab-notebook/notebook-llm.ts#L50) |
| `ANTHROPIC_API_KEY` | Required when backend = anthropic | [notebook-llm.ts:42](src/lib/ai-lab-notebook/notebook-llm.ts#L42) |
| `GEMINI_CORPUS_DIR` | Absolute path to corpus markdown (overrides default) | [gemini-corpus-upload.ts:57](scripts/gemini-corpus-upload.ts#L57) |
| `ALAN_BOOKS_GITHUB_REPO` + `GITHUB_TOKEN` | Vercel/CI fallback — shallow-clone corpus | [gemini-corpus-upload.ts:71-73](scripts/gemini-corpus-upload.ts#L71-L73) |
| `ALAN_BOOKS_CORPUS_SUBDIR` | Subdir within cloned repo (default `corpus/alan_hirsch`) | [gemini-corpus-upload.ts:76](scripts/gemini-corpus-upload.ts#L76) |
| `SKIP_GEMINI_CORPUS_UPLOAD` | `true` → upload script exits 0 without running | [gemini-corpus-upload.ts:121](scripts/gemini-corpus-upload.ts#L121) |
| `GEMINI_CORPUS_UPLOAD_STRICT` | `true` → upload script **fails the build** if no corpus found | [gemini-corpus-upload.ts:142](scripts/gemini-corpus-upload.ts#L142) |
| `FORCE_ALAN_BOOKS_CLONE` | Force the clone path locally for testing | [gemini-corpus-upload.ts:69](scripts/gemini-corpus-upload.ts#L69) |
| `GEMINI_CACHE_CORPUS_SUBDIR` | Cache creator — subset to fit in 1M token window | [gemini-corpus-cache.ts:50](scripts/gemini-corpus-cache.ts#L50) |

**Silent-failure pattern:** Almost every "corpus not available" state produces a
`console.warn`, not an exception. The app then falls back to Mode C (catalog-only) and
the user sees ungrounded answers. Always check Vercel build logs + dev server warnings
before assuming things work.

---

## 5. Operational Playbooks

### Playbook A — "The notebook isn't citing Alan's books anymore"

1. **Check backend.** If `AI_LAB_NOTEBOOK_LLM=anthropic`, Claude never gets the corpus
   attached — switch to Gemini or accept catalog-only grounding.
2. **Check cache path:**
   ```bash
   grep "GEMINI_CORPUS_CACHE_ID" .env.local
   ```
   If set, verify the cache still exists (not expired):
   ```bash
   npx tsx -e "import('@google/genai').then(async m => {
     const g = new m.GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });
     const list = await g.caches.list();
     for await (const c of list) console.log(c.name, c.expireTime, c.usageMetadata);
   })"
   ```
   TTL is 7 days from creation. If expired → re-run `scripts/gemini-corpus-cache.ts`.
3. **Check manifest path** (Mode B):
   ```bash
   cat src/lib/ai-lab-notebook/corpus-manifest.json | head -20
   ```
   If `expiresAt` is in the past: the 48h File API window closed. Re-run
   `npx tsx scripts/gemini-corpus-upload.ts`. The chat path already
   console-warns this in [corpus-gemini-files.ts:27-31](src/lib/ai-lab-notebook/corpus-gemini-files.ts#L27-L31).
4. **Check API key** — if `GOOGLE_GENERATIVE_AI_API_KEY` is unset, both upload and
   context cache scripts exit 0 silently. The app then runs in Mode C.
5. **Confirm augmentation reached the model.** Add a one-time log in the chat route
   before streaming:
   ```ts
   console.log('[notebook] corpus grounded:', notebookGeminiHasFullCorpusContext());
   ```

### Playbook B — "Re-run the build-time upload now"

```bash
# Standard re-run (uses local ~/Desktop/Dev/repos/alan-books corpus)
npx tsx scripts/gemini-corpus-upload.ts

# Force the Vercel/CI clone path for testing
FORCE_ALAN_BOOKS_CLONE=true ALAN_BOOKS_GITHUB_REPO=owner/repo \
  GITHUB_TOKEN=ghp_... npx tsx scripts/gemini-corpus-upload.ts

# Point at a specific folder
GEMINI_CORPUS_DIR=/abs/path/to/corpus_subset npx tsx scripts/gemini-corpus-upload.ts
```

The script writes `src/lib/ai-lab-notebook/corpus-manifest.json`. **Commit it** — Vercel
reads from the repo at deploy time, and the `prebuild` hook runs it again anyway.

### Playbook C — "Create or refresh the context cache"

```bash
# Full corpus (will fail if > 1M tokens)
npx tsx scripts/gemini-corpus-cache.ts

# Subset (recommended — currently full corpus exceeds gemini-2.5-flash window)
GEMINI_CACHE_CORPUS_SUBDIR=books npx tsx scripts/gemini-corpus-cache.ts
```

Copy the printed cache name into `.env.local`:
```
GEMINI_CORPUS_CACHE_ID=cachedContents/abc123…
```

**Consider a weekly cron** — the TTL is 7 days hard-coded at
[gemini-corpus-cache.ts:60](scripts/gemini-corpus-cache.ts#L60). A Vercel cron or
GitHub Action running `pnpm tsx scripts/gemini-corpus-cache.ts` on a 6-day schedule
keeps the cache live without manual intervention. Use the `vercel-plugin:cron` pattern
or a lightweight cron job; avoid in-app refresh on every request.

### Playbook D — "Switch models for an experiment"

```bash
# Preview model — requires clearing the cache id first
unset GEMINI_CORPUS_CACHE_ID
GEMINI_MODEL=gemini-3-flash-preview pnpm dev
```

If you want to test a new model **and** keep grounding, use Mode B (File API manifest)
— it has no model lock.

### Playbook E — "Tune the source discovery route"

The grounded-search route prompts for up to 10 sources. Current model defaults to
`process.env.GEMINI_MODEL || 'gemini-3-flash-preview'`. Flash-tier is appropriate —
there is no benefit to running Pro on source discovery. If discovery is slow, check:
- Network latency to `generativelanguage.googleapis.com`
- `maxDuration = 60` cap in the route
- JSON parse — currently a single `/\[[\s\S]*\]/` regex. If the model wraps the JSON
  in fences or adds prose, the regex still matches the first `[…]` block. If parsing
  fails silently (returns `{ sources: [] }`), log the raw `text` before parsing.

---

## 6. Optimization Reference

### Cost hierarchy (cheapest → most expensive at notebook scale)

1. **Mode A (cache) on flash-lite** — best cost if the corpus fits. But `flash-lite`
   is not currently the cache model.
2. **Mode A (cache) on flash** — current default. Cached input ≈ 25% of non-cached
   input; output unchanged.
3. **Mode B (File API) on flash** — no cache discount; 48h refresh.
4. **Mode B on pro** — only when a specific query needs deeper reasoning. The notebook
   chat route uses one model per request, so routing by query is not supported today.
5. **Mode A on pro** — stable but expensive. Only if cache discount makes it pencil
   out at your traffic.

### Latency tips
- Chat route already streams via `streamText` → `toTextStreamResponse()`. Don't
  buffer.
- Sources discovery is a single non-streaming `generateText` — OK because the result
  is structured JSON, not prose.
- Context cache calls have materially lower TTFT than File API calls (Google caches
  the KV state, not just input tokens).

### When to escalate to Vertex AI RAG Engine
The corpus comment in [corpus.ts:7-9](src/lib/ai-lab-notebook/corpus.ts#L7-L9) mentions
Vertex AI RAG Engine as a future path. Consider it only when:
- The corpus materially exceeds 1M tokens and chunk-level retrieval matters
- You need embedding-based semantic search within the corpus rather than full-context
- You're already on Vertex for compliance reasons

For the current ~1M-word corpus and flash-tier usage, **stick with context cache or
File API**. Adding a vector DB hop would increase complexity without obvious win.

---

## 6b. The 1M-Token Ceiling (Critical — corpus is bigger than any Gemini model)

**Every Gemini model** — `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3-flash-preview`,
`gemini-3-pro-preview` — has an **input window of exactly 1,048,576 tokens** (confirmed
against the live `models/` endpoint on 2026-04-11). There is currently no Gemini model
with a larger context.

**Alan's full English corpus is ~1.77M tokens** by the chars/4 heuristic. It **will
never fit** in a single request regardless of which model you pick. This means:

- **Mode B (File API) MUST upload a subset.** Uploading the full corpus is a silent
  time bomb: the upload succeeds, the manifest looks healthy, and every chat request
  fails at runtime with *"The input token count exceeds the maximum number of tokens
  allowed (1048576)"*.
- **Mode A (context cache) also requires a subset.** The cache script's
  `GEMINI_CACHE_CORPUS_SUBDIR` has always enforced this; the upload script now does
  too via `GEMINI_UPLOAD_CORPUS_SUBDIR`.

The upload script's token pre-check (added 2026-04-11) enforces this hard — it **fails
the build** before upload if the estimated corpus exceeds 1M tokens, and warns if it
exceeds the 850K soft budget (leaving headroom for system prompt + user message +
output).

### Current working subset (as of 2026-04-11)

The default notebook subset is set via environment:

```bash
GEMINI_UPLOAD_CORPUS_SUBDIR=the-forgotten-ways,5q,the-permanent-revolution,_topics,_comparisons
```

This produces ~528K tokens — comfortably under budget, covers the three core books
(*The Forgotten Ways*, *5Q*, *The Permanent Revolution*) plus topic guides and
inter-book comparison notes. When you add books or change focus, rerun
`pnpm notebook:upload` with an updated subset env var and commit the new manifest.

### When you need the full corpus

Options, in order of effort:

1. **Narrow the subset per deployment.** E.g. a pathway-focused tenant ships with
   only the books that pathway cites.
2. **Switch to Mode A cache + subset.** Same subset filter, but pays less per
   request at volume. Cache TTL is 7 days.
3. **Adopt embeddings + top-k retrieval.** Pre-embed the whole corpus with Gemini
   (or Vertex) embeddings and retrieve the top N chunks per query. This is the
   NotebookLM approach at scale. Build cost is real; complexity is real. Only do
   this when a single subset genuinely can't serve your query distribution.
4. **Wait for a Gemini model with a bigger window.** Not a plan.

---

## 7. Common Pitfalls (things this repo has already hit)

1. **Mixing `@google/genai` and `@ai-sdk/google`.** Scripts use the native SDK for
   file uploads (`files.upload`, `files.get`, `caches.create`); routes use the AI SDK
   (`google(modelId)`). File URIs from the native SDK *are* consumable by the AI SDK
   via `{ type: 'file', data: new URL(uri), mediaType: 'text/plain' }` — see
   [augment-notebook-model-messages.ts:36-42](src/lib/ai-lab-notebook/augment-notebook-model-messages.ts#L36-L42).
2. **`.mdx` in corpus.** The upload script walks both `.md` and `.mdx`
   ([gemini-corpus-upload.ts:262](scripts/gemini-corpus-upload.ts#L262)). Unlike
   OpenAI vector stores, Gemini's File API accepts arbitrary text — no extension
   rename required, because files are concatenated into `text/plain` blobs and
   uploaded as batches.
3. **Translation folders.** Both scripts explicitly skip `-es`, `-pt`, `-pt-BR`
   folder suffixes. When adding new locales, update the filter in both
   [gemini-corpus-upload.ts:253-259](scripts/gemini-corpus-upload.ts#L253-L259)
   and [gemini-corpus-cache.ts:188-194](scripts/gemini-corpus-cache.ts#L188-L194).
4. **Batch size assumption.** Upload script uses `MAX_BATCH_CHARS = 2_000_000`
   (~500K tokens). Don't raise this blindly — the File API accepts larger blobs, but
   the native SDK file `state: ACTIVE` polling takes longer on bigger files, and the
   current 30-attempt ×2s loop may time out.
5. **Manifest in git.** `corpus-manifest.json` is committed
   ([corpus-gemini-files.ts:17-19](src/lib/ai-lab-notebook/corpus-gemini-files.ts#L17-L19))
   so Vercel deploys have something to read before `prebuild` runs. Don't gitignore
   it; stale content is fine because `prebuild` always regenerates.
6. **`GEMINI_CORPUS_UPLOAD_STRICT=true` locally.** Will fail the build if the corpus
   isn't present locally. Only set this on Vercel if you're certain the clone path is
   configured; otherwise every build breaks.

---

## 8. Verification Commands

**Primary:** use the bundled verify script. It does everything below in one call:

```bash
pnpm notebook:verify
```

It reports the resolved corpus mode (as seen by the app after placeholder
filtering), checks each manifest file is `ACTIVE` on Gemini, and validates any
`GEMINI_CORPUS_CACHE_ID` against a live `caches.get`. Non-zero exit on any
problem, so it's safe in CI.

Other package scripts:
- `pnpm notebook:upload` — re-run Mode B upload (same as `scripts/gemini-corpus-upload.ts`)
- `pnpm notebook:cache` — create/refresh a Mode A cache

Lower-level probes (when you need to debug the verify script itself):

```bash
# List live Gemini caches on this API key
pnpm tsx -e "
  import('@google/genai').then(async ({ GoogleGenAI }) => {
    const g = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });
    for await (const c of g.caches.list()) {
      console.log(c.name, '| expires:', c.expireTime, '| tokens:', c.usageMetadata?.totalTokenCount);
    }
  });
"

# List live Gemini files on this API key
pnpm tsx -e "
  import('@google/genai').then(async ({ GoogleGenAI }) => {
    const g = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });
    for await (const f of g.files.list()) {
      console.log(f.name, '| state:', f.state, '| expires:', f.expirationTime, '| name:', f.displayName);
    }
  });
"
```

### Placeholder-cache auto-rejection (added 2026-04-11)

`getCorpusCacheId()` at [corpus.ts](src/lib/ai-lab-notebook/corpus.ts) rejects
obvious placeholder values (short hashes, strings containing `abc123`, `xxx`,
`placeholder`, `example`, `todo`) and returns `null` with a `console.warn`.
This is a defense-in-depth layer on top of the skill guidance — a stale/demo
cache id in `.env.local` can no longer silently break every chat call.

When the rejection fires:
- App logs: `[corpus] GEMINI_CORPUS_CACHE_ID hash is too short to be real — ignoring`
- App falls through to Mode B (File API manifest)
- `pnpm notebook:verify` reports the raw value as a **warning** and shows the
  resolved mode that the app will actually use

The fix is still to unset or replace the env var — the auto-rejection just
prevents a hard outage while you do it.

---

## 9. When to Defer to Other Skills

- **Generic Gemini API questions** (new tool calls, video input, Vertex, pricing on
  unrelated projects): use the `gemini-api` skill. This skill only covers the
  notebook's integration.
- **Claude side of the notebook backend**: use the `claude-api` skill. The Claude
  branch of `resolveNotebookLlm()` has no corpus attachment logic; it's an ordinary
  `streamText` call.
- **Vector store / RAG alternatives** (if the corpus grows past Gemini's window): use
  the `openai-vector-store` skill as a reference for what that pattern looks like.
- **Env var management on Vercel**: use the `env-setup` or `vercel-plugin:env` skill.

---

## 10. Quick Reference Card

```
CORPUS DELIVERY:
  Mode A  cache    → GEMINI_CORPUS_CACHE_ID set        → cheapest, 7d TTL, model-locked
  Mode B  files    → corpus-manifest.json present       → 48h TTL, auto via pnpm build
  Mode C  catalog  → neither                            → titles only, ungrounded

BACKEND:
  AI_LAB_NOTEBOOK_LLM = gemini (default) | anthropic

MODEL LOCK:
  if cache id set → model FORCED to gemini-2.5-flash
  else            → GEMINI_MODEL || gemini-3-flash-preview

SCRIPTS:
  pnpm tsx scripts/gemini-corpus-upload.ts    # Mode B — files, 48h
  pnpm tsx scripts/gemini-corpus-cache.ts     # Mode A — cache,  7d

FAIL-OPEN BEHAVIOR:
  Missing API key → exit 0, silent fallback to Mode C
  Expired manifest → console.warn, silent fallback to Mode C
  Wrong backend   → Claude ignores corpus entirely (no warning)
```

Always state explicitly which mode is active and which env vars are driving it when
answering operational questions.
