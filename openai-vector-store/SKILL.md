---
name: openai-vector-store
description: >
  Expert guidance for managing OpenAI vector stores — health checks, completeness audits,
  upload safeguards, junk/duplicate detection, surgical repair vs full re-upload decisions,
  API key/project scoping, and .mdx→.md workarounds. Use this skill whenever the user
  mentions vector store uploads, vector store health, missing files in a vector store,
  OpenAI file search setup, or asks about OPENAI_VECTOR_STORE_ID configuration. Also
  trigger when diagnosing "store looks wrong", "files missing", "temp files in store",
  or "upload script broke". Covers both Node.js and Python upload patterns.
---

# OpenAI Vector Store — Best Practices

## Project Scoping (Most Common Silent Failure)

Vector stores are **strictly scoped to the OpenAI project** that created them. An API key from Project A cannot read, write, or delete a vector store owned by Project B — it returns 404 or 401, not a permissions error. This is the most common source of confusion.

**Checklist when a store returns 404 unexpectedly:**
1. List all stores accessible to the active key: `client.vectorStores.list()`. If the target ID is absent, you're using the wrong key.
2. Compare the key's project (`openai-project` header in error responses) against the project shown in the OpenAI dashboard for that store.
3. Stores created in the **web Playground** live in the "Default project" — API access requires a key from that same project.
4. Resources cannot be moved between projects. Either switch keys or re-upload to the correct project.

**In multi-key environments** (e.g., `~/.env.shared` + per-project `.env.local`):
- The key that runs the upload script and the key the platform uses **must belong to the same project**.
- When `dotenv.config({ path: '.env.local', override: true })` is used in Node.js, it only overrides keys present in `.env.local` — other keys (like `OPENAI_API_KEY`) inherit from the shell environment, which may differ from what's in `.env.shared`.
- Always verify the active key by running `client.vectorStores.list()` before any destructive operation.

---

## File Type Support

| Extension | Supported | Notes |
|-----------|-----------|-------|
| `.md` | ✓ Yes | UTF-8 required; occasional false rejections — retry on failure |
| `.txt` | ✓ Yes | UTF-8 required |
| `.pdf` | ✓ Yes | Best for structured documents |
| `.mdx` | ✗ No | Not in OpenAI's supported list — **must rename to `.md` before upload** |
| `.json` | ⚠ Unreliable | Listed but inconsistently accepted |
| `.csv` / `.xlsx` | ✗ Removed | Dropped from the supported list |

**The `.mdx` workaround:**
Files must be written to a temp path with a `.md` extension before uploading. The OpenAI Node.js SDK infers filename and MIME type from `stream.path` on a `fs.createReadStream`. If the path is the temp directory name rather than the file, the directory name becomes the uploaded filename.

```js
// CORRECT — temp file gets the right name
const tempPath = path.join(TEMP_DIR, filename.replace(/\.mdx$/i, '.md'));
fs.writeFileSync(tempPath, content, 'utf8');
const file = await client.files.create({
  file: fs.createReadStream(tempPath),  // stream.path = tempPath → filename = "slug.md"
  purpose: 'assistants',
});
fs.unlinkSync(tempPath); // clean up immediately

// WRONG — passing a directory stream or wrong path results in the dir name as filename
// e.g. TEMP_DIR = ".vector-store-upload-temp" → file gets named ".vector-store-upload-temp.md"
```

For non-filesystem streams, use the SDK's `toFile()` helper to set the filename explicitly:
```js
import { toFile } from 'openai';
const file = await client.files.create({
  file: await toFile(buffer, 'slug.md', { type: 'text/markdown' }),
  purpose: 'assistants',
});
```

---

## Limits

| Limit | Value |
|-------|-------|
| Max files per vector store | 10,000 (default) |
| Max file IDs per `files.create` call | 1 |
| Max file IDs per `fileBatches.create` | 500 |
| Max file size | 512 MB (effective: 5M tokens) |
| Batch creation convenience limit | 200 files/call is a safe working batch size |

---

## Health Check Pattern

Run this whenever a store looks suspicious or after any upload:

```js
async function auditStore(client, vsId, inventory) {
  // 1. Retrieve store metadata
  const vs = await client.vectorStores.retrieve(vsId);
  console.log('Store:', vs.id, '| status:', vs.status, '| file_counts:', vs.file_counts);

  // 2. List all files with their names
  const storeFiles = [];
  let page = await client.vectorStores.files.list(vsId, { limit: 100 });
  while (true) {
    for (const f of page.data) storeFiles.push(f);
    if (!page.hasNextPage()) break;
    page = await page.getNextPage();
  }

  // Fetch actual filenames from Files API
  const details = await Promise.all(
    storeFiles.map(f => client.files.retrieve(f.id).then(r => ({ id: f.id, status: f.status, filename: r.filename })))
  );

  // 3. Check for junk files (directory name used as filename — a common upload bug)
  const junk = details.filter(f => !f.filename.match(/\.[a-z]+$/i) || f.filename.includes('temp'));

  // 4. Check for duplicates
  const nameCounts = {};
  for (const f of details) nameCounts[f.filename] = (nameCounts[f.filename] || 0) + 1;
  const dupes = Object.entries(nameCounts).filter(([, c]) => c > 1);

  // 5. Check completeness against local inventory
  const storeNames = new Set(details.map(f => f.filename));
  const invNames = inventory.map(e => e.filename.replace(/\.mdx$/i, '.md'));
  const missing = invNames.filter(n => !storeNames.has(n));
  const extra = [...storeNames].filter(n => !invNames.includes(n));

  // 6. Check for failed files
  const failed = details.filter(f => f.status === 'failed');

  return { total: storeFiles.length, junk, dupes, missing, extra, failed };
}
```

**Interpreting results:**
- **Junk files** (e.g., all named `.vector-store-upload-temp.md`): the upload script passed a directory path as the file stream. See `.mdx` workaround above. These files contain no useful content.
- **Duplicate filenames**: a previous upload was not fully cleared before re-uploading. Degrades retrieval quality.
- **Missing files**: artifacts (quote banks, topic guides, supplemental) are often missing when they were `.mdx` files that failed silently. Confirm the temp-file workaround is working.
- **Failed files**: check `last_error` on the vector store file object for the reason.

---

## Surgical Fix vs Full Re-Upload

**Use surgical fix when:**
- Store has mostly good files with isolated problems (some junk, some missing, some dupes)
- Re-uploading 400+ files takes too long and most content is correct
- The store is actively being used and you want minimal downtime

**Surgical fix steps:**
1. Get all files with names (Files API `retrieve` on each)
2. Delete junk files: `vectorStores.files.del(vsId, fileId)` then `files.del(fileId)`
3. Delete extra copies of duplicates (keep one, delete the rest)
4. Upload only missing files, attach via batch
5. Poll batch to completion, verify

**Use full re-upload when:**
- The store is severely corrupted or more than 30% of files are wrong
- You want a guaranteed clean state
- The store is not yet in production use

**Full re-upload steps:**
1. Clear: list all file IDs, delete each from the vector store with `vectorStores.files.del()`, then delete from Files API with `files.del()`. Or delete the store entirely and recreate.
2. Upload all files fresh
3. Write an updated doc index after verifying

---

## Upload Script Safeguards

Add these checks to any upload script before running:

```js
// 1. Verify the API key can access the target store before doing anything destructive
async function verifyAccess(client, vsId) {
  const list = await client.vectorStores.list({ limit: 20 });
  const found = list.data.find(vs => vs.id === vsId);
  if (!found) {
    const ids = list.data.map(vs => vs.id).join(', ');
    throw new Error(
      `Vector store ${vsId} not found with this API key.\n` +
      `Accessible stores: ${ids || 'none'}\n` +
      `Check that OPENAI_API_KEY belongs to the same project as OPENAI_VECTOR_STORE_ID.`
    );
  }
  return found;
}

// 2. Temp file cleanup — ensure temp dir is always cleaned up even on crash
process.on('exit', () => {
  if (fs.existsSync(TEMP_DIR)) {
    for (const f of fs.readdirSync(TEMP_DIR)) fs.unlinkSync(path.join(TEMP_DIR, f));
  }
});

// 3. After batch completes, always check file_counts.failed
const batch = await client.vectorStores.fileBatches.retrieve(vsId, batchId);
if (batch.file_counts.failed > 0) {
  console.warn(`${batch.file_counts.failed} files failed to index. Check individual file statuses.`);
}
```

---

## Batch Status — What "completed" Actually Means

A batch reaching `completed` status means processing finished, **not** that all files succeeded. Always check `file_counts.failed` after polling completes. A batch with `{ completed: 490, failed: 3, total: 493 }` still returns status `completed`.

```js
async function pollBatch(client, vsId, batchId, intervalMs = 5000, maxAttempts = 120) {
  for (let i = 0; i < maxAttempts; i++) {
    const b = await client.vectorStores.fileBatches.retrieve(vsId, batchId);
    if (b.status !== 'in_progress') {
      if (b.file_counts.failed > 0) {
        console.warn('Failed files:', b.file_counts.failed);
        // To find which files failed, list vector store files and filter by status === 'failed'
      }
      return b;
    }
    await new Promise(r => setTimeout(r, intervalMs));
  }
  throw new Error('Batch polling timed out');
}
```

---

## Doc Index

After any upload, write a local index (`_index/vector_store_docs_index.json`) recording:
- `vector_store_id` — which store this was uploaded to
- `generated_at` — ISO timestamp
- `total_files` / `by_type` — summary counts
- `documents[]` — each file's `openai_file_id`, `type`, `path`, `filename`

This index is the source of truth for diagnosing completeness and for surgical fixes. Without it, you must fetch names for all files via the Files API on every audit (slow at 500+ files).

The index becomes stale whenever files are added/removed outside the upload script. Re-generate it after every upload.

---

## Environment Setup

```
.env.shared             ← OPENAI_API_KEY + OPENAI_VECTOR_STORE_ID shared defaults
.env.local (per repo)   ← Override OPENAI_VECTOR_STORE_ID if the repo uses a different store
                           Do NOT set OPENAI_API_KEY here unless you explicitly want a different project
```

If the upload script uses `dotenv.config({ path: '.env.local', override: true })`, it only loads what's in `.env.local`. The `OPENAI_API_KEY` comes from the shell environment (set by direnv from `.env.shared` or similar). This means the active API key during upload may differ from what you see in `.env.shared` if direnv loaded a different key. Verify with `console.log(process.env.OPENAI_API_KEY.slice(0, 10))` and `client.vectorStores.list()` to confirm which project you're in.

---

## Quick Diagnostic Script

Save as `scripts/audit-vector-store.js` and run ad hoc:

```js
#!/usr/bin/env node
require('dotenv').config({ path: '.env.local', override: true });
const OpenAI = require('openai').default;
const { buildInventory } = require('./lib/vector-store-inventory');

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const vsId = process.env.OPENAI_VECTOR_STORE_ID;

async function main() {
  if (!vsId) throw new Error('OPENAI_VECTOR_STORE_ID not set');

  // Verify access
  const list = await client.vectorStores.list({ limit: 50 });
  const vs = list.data.find(v => v.id === vsId);
  if (!vs) {
    console.log('Accessible stores:', list.data.map(v => `${v.id} (${v.name}, ${v.file_counts?.total} files)`).join('\n'));
    throw new Error(`Store ${vsId} not accessible with this key`);
  }
  console.log(`Store: ${vs.id} | ${vs.name} | status: ${vs.status} | files: ${JSON.stringify(vs.file_counts)}`);

  // Fetch all file details
  const files = [];
  let page = await client.vectorStores.files.list(vsId, { limit: 100 });
  while (true) { for (const f of page.data) files.push(f); if (!page.hasNextPage()) break; page = await page.getNextPage(); }
  const details = await Promise.all(files.map(f => client.files.retrieve(f.id).then(r => ({ id: f.id, status: f.status, filename: r.filename }))));

  // Analysis
  const nameCounts = {};
  for (const f of details) nameCounts[f.filename] = (nameCounts[f.filename] || 0) + 1;
  const junk = details.filter(f => !path.extname(f.filename) || f.filename.includes('-upload-temp'));
  const dupes = Object.entries(nameCounts).filter(([, c]) => c > 1).map(([n, c]) => `${n} x${c}`);
  const failed = details.filter(f => f.status === 'failed');

  const inv = buildInventory();
  const storeNames = new Set(details.map(f => f.filename));
  const missing = inv.filter(e => !storeNames.has(e.filename.replace(/\.mdx$/i, '.md')));

  console.log(`\nJunk: ${junk.length} | Dupes: ${dupes.length} | Failed: ${failed.length} | Missing: ${missing.length}`);
  if (junk.length) console.log('Junk:', junk.map(f => f.filename).join(', '));
  if (dupes.length) console.log('Dupes:', dupes.join(', '));
  if (failed.length) console.log('Failed:', failed.map(f => f.filename).join(', '));
  if (missing.length) console.log('Missing by type:', missing.reduce((a, e) => { a[e.type] = (a[e.type]||0)+1; return a; }, {}));
}

const path = require('path');
main().catch(e => { console.error(e.message); process.exit(1); });
```
