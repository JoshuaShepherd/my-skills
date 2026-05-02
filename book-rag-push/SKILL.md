---
name: book-rag-push
description: >
  Phase 04b of the books pipeline — fan out the canonical `chunks.jsonl` to
  three vector stores (OpenAI Vector Stores, Gemini File Search, Anthropic
  Files API) and the in-house pgvector. Idempotent — only re-uploads chunks
  whose `sha256` changed since the last run; updates `vector_store_ids` map
  in chapter frontmatter to record which store/version each chapter lives in.
  Includes the smoke test (same query against all four stores, diff results).
  Use after `/book-chunk` produces an updated `chunks.jsonl`. Trigger phrases:
  "push to vector stores", "upload chunks", "phase 04 fan-out", "rag deploy",
  "smoke test rag".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "04b"
  reference: "docs/html/books-pipeline.html#phase-4"
---

# Book RAG Push — Phase 04b: Chunks → 3 Vector Stores

## Purpose

Take the canonical `<book-dir>/.ingest/chunks.jsonl` produced by `/book-chunk` and fan it out to four destinations:

1. **pgvector** (`book_chunks` table in Supabase) — primary, with HNSW cosine index.
2. **OpenAI Vector Stores** — accessed via `file_search` tool in Responses API.
3. **Gemini File Search** — accessed via `fileSearch` tool in `generateContent`.
4. **Anthropic Files API** — accessed via `document` blocks with citations + memory tool for agentic sessions.

Each chunk's `sha256` is the source of truth for "has this chunk changed". We only re-upload what's new or modified.

## Invocation

`$ARGUMENTS`:

- **`<book-slug-or-dir>`** — Required.
- **`--targets <list>`** — Comma-separated. Default: `pgvector,openai,gemini,claude`.
- **`--dry-run`** — Print upload plan without making API calls.
- **`--smoke-query <text>`** — Final smoke-test query. Default: `"What is this book mostly about?"`.

## Process

### Step 1 — Pre-flight

1. Verify `chunks.jsonl` exists under `<book-dir>/.ingest/`. If not, run `/book-chunk` first.
2. Verify env vars per target: `OPENAI_API_KEY`, `OPENAI_VECTOR_STORE_ID` (if existing), `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `DATABASE_URL` (for pgvector).
3. Read previous run's manifest (if any) at `<book-dir>/.ingest/rag-state.json`. Build a set of `id → sha256` for last-uploaded state per target.

### Step 2 — Fan out per target (parallel where safe)

#### 2a. pgvector (in-house)

```typescript
import { db } from "@/lib/database";
import { bookChunks } from "@/lib/database/schema/books";

for (const chunk of changedChunks) {
  const embedding = await embed(`${chunk.context_prefix}\n\n${chunk.text}`);
  await db.insert(bookChunks).values({
    chapter_id: chapterIdMap[chunk.chapter_slug],
    section_id: sectionIdMap[chunk.section_anchor],
    ordinal: chunk.ordinal,
    content: chunk.text,
    context_prefix: chunk.context_prefix,
    page_start: chunk.page_start,
    page_end: chunk.page_end,
    token_count: chunk.token_count,
    embedding,
    embedding_model: "voyage-3-large",
    embedding_version: manifest.rag.embedding_version,
    content_sha256: chunk.sha256,
  }).onConflictDoUpdate({
    target: [bookChunks.chapter_id, bookChunks.ordinal],
    set: { content: chunk.text, embedding, content_sha256: chunk.sha256 },
  });
}
```

#### 2b. OpenAI Vector Stores

One vector store per book per language: `book:<slug>:<lang>`. Pre-chunk and pass each chunk as its own `.md` file with tight `static` chunking bounds so OpenAI's default chunker doesn't re-split across our boundaries.

```typescript
const store = await openai.vectorStores.create({
  name: `book:${manifest.slug}:${manifest.language}`,
  metadata: { book_slug: manifest.slug, language: manifest.language, version: manifest.version },
});

for (const batch of chunkBatches(changedChunks, 500)) {
  await openai.vectorStores.fileBatches.uploadAndPoll(store.id, {
    files: batch.map((c) => new File(
      [`${c.context_prefix}\n\n<!-- page: ${c.page_start} -->\n${c.text}`],
      `${c.id}.md`,
      { type: "text/markdown" }
    )),
    chunking_strategy: { type: "static", static: { max_chunk_size_tokens: 600, chunk_overlap_tokens: 100 } },
    attributes: batch.map((c) => c.metadata) as any,
  });
}
```

Cap `max_num_results: 12` at query time (default 20 is too costly).

#### 2c. Gemini File Search

One File Search store per book: `book:<slug>:<lang>`. Storage uses ~3× source size; query-time embeddings are free. Hard limit: 100MB per file, ≤20GB per store. For a multi-book corpus, one store per book per language stays well under.

```typescript
const store = await ai.fileSearchStores.create({
  displayName: `book:${manifest.slug}:${manifest.language}`,
});
for (const c of changedChunks) {
  await ai.fileSearchStores.documents.upload(store.name, {
    file: `${c.context_prefix}\n\n<!-- page: ${c.page_start} -->\n${c.text}`,
    mimeType: "text/markdown",
    metadata: { book_slug: c.book_slug, chapter: `${c.chapter}`, page_start: `${c.page_start}` },
    chunkingConfig: { maxTokensPerChunk: 600, overlapTokens: 80 },
  });
}
```

#### 2d. Anthropic Files API

Claude has no first-party vector store. Pattern: upload one PDF/MD file per **chapter** (not per chunk — too many) to Files API; rely on your own pgvector + Voyage rerank for retrieval; pass top-k `document` blocks with `citations.enabled: true`. Use the memory tool to persist retrieved context across an agentic session.

```typescript
const file = await client.beta.files.upload({
  file: await Bun.file(`<book-dir>/${slug}-ch03-missional-dna.md`).arrayBuffer(),
  purpose: "document",
});
// store file.id in vector_store_ids.claude per chapter
```

### Step 3 — Update vector_store_ids in chapter frontmatter

After each successful upload, update each chapter's frontmatter:

```yaml
vector_store_ids:
  openai: vs_abc123
  gemini: fileSearchStores/fw-en-v1
  claude: file_xyz789
last_indexed_at: 2026-04-28T18:30:00Z
```

Recompute `content_sha256` only if frontmatter content changed (it should, but `last_indexed_at` shouldn't trigger rechunking — see Issue 16 of the corresponding fix prompts).

### Step 4 — Persist run state

Write `<book-dir>/.ingest/rag-state.json`:

```json
{
  "ran_at": "2026-04-28T18:30:00Z",
  "targets": {
    "pgvector": { "uploaded": 12, "skipped": 4225, "store": "supabase://book_chunks" },
    "openai":   { "uploaded": 12, "skipped": 4225, "store": "vs_abc123" },
    "gemini":   { "uploaded": 12, "skipped": 4225, "store": "fileSearchStores/fw-en-v1" },
    "claude":   { "uploaded": 12, "skipped": 4225, "store": "files_xyz789" }
  },
  "manifest_version": "1.2.0",
  "embedding_version": "v3"
}
```

### Step 5 — Smoke test

Run the same query against all four stores; print results side by side.

```typescript
const query = process.argv["--smoke-query"] ?? "What is this book mostly about?";

const pg = await ragSearchPgvector(query, { book_slug, k: 5 });
const oai = await openai.responses.create({
  model: "gpt-5",
  tools: [{ type: "file_search", vector_store_ids: [openaiStoreId], max_num_results: 5 }],
  input: query,
});
const gem = await ai.models.generateContent({
  model: "gemini-2.5-pro",
  contents: query,
  tools: [{ fileSearch: { fileSearchStoreNames: [geminiStoreName] } }],
});
const cla = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    { role: "user", content: [
      { type: "document", source: { type: "file", file_id: claudeFileId }, citations: { enabled: true } },
      { type: "text", text: query },
    ]},
  ],
});

console.table({ pgvector: pg.topIds, openai: oai.topCitations, gemini: gem.topCitations, claude: cla.topCitations });
```

Verify:

- All four stores return at least 1 citation.
- The top-3 citations from each store have non-trivial Jaccard overlap (≥ 30%).
- No store returns the same exact ID for unrelated queries (sanity check on attribute filtering).

### Step 6 — Report

```
Phase 04b — RAG fan-out
  pgvector:  +12 chunks   (4237 total in book_chunks)
  OpenAI:    +12 files    (vs_abc123 — 4237 files)
  Gemini:    +12 docs     (fileSearchStores/fw-en-v1 — 4237 docs)
  Claude:    +0 files     (chapter-level — no chapters changed)

  Smoke test: "What is this book mostly about?"
    pgvector: ch03-0007, ch01-0002, ch07-0014   ✓
    OpenAI:   ch03-0007, ch01-0002, ch04-0009   ✓
    Gemini:   ch03-0007, ch01-0002, ch07-0014   ✓
    Claude:   ch03-0007, ch04-0009, ch01-0002   ✓
    Top-3 Jaccard: 0.62 (✓ ≥ 0.30)

  Verdict: PASS — book is live in all four stores
```

## Versioning

Bump `book.json:version` whenever:

- Chapters added or removed.
- Pagination changes.
- Embedding model or chunking strategy changes (also bump `embedding_version`).

The ingest script reads `chunks.jsonl` and only re-uploads chunks whose `sha256` changed — keeps store costs flat across copy edits.

## Cost Notes (April 2026)

| Provider | Per-book cost (300pp) | Notes |
|---|---|---|
| pgvector + Voyage | ~$0.50 (embeddings) + storage | One-time embed; Voyage `voyage-3-large` ~$0.18/1M tokens |
| OpenAI Vector Stores | ~$0.50 indexing + per-query embeddings | Pre-chunk + small static bounds keeps cost predictable |
| Gemini File Search | ~$0.50 indexing + free queries | **Cheapest at query time** — query embeddings free, only model I/O charged |
| Anthropic Files | $0 indexing + per-query input tokens | Pay nothing to upload; pay full input tokens per query |

Gemini wins on multi-query economics; pgvector wins on full control + filtering.

## Out of Scope

- Generating chunks — `/book-chunk`.
- Schema validation — `/book-frontmatter`.
- Stripe entitlement checks — separate concern in the e-reader app.

## References

- [docs/html/books-pipeline.html#phase-4](../../../docs/html/books-pipeline.html#phase-4)
- [OpenAI Vector Stores](https://developers.openai.com/api/reference/typescript/resources/vector_stores)
- [Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search)
- [Claude Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Voyage rerank-2.5](https://docs.voyageai.com/docs/reranker)
