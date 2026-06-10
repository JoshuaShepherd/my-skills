---
name: book-pipeline
description: >
  Orchestrate the full books pipeline (Phases 01 → 04) for a single book from
  PDF/EPUB to live on all four vector stores. Routes through `/book-convert`
  → `/book-validate` → `/book-audit` → optional `/book-fix` →
  `/book-frontmatter` → `/book-ingest` → `/book-chunk` → `/book-rag-push`,
  with quality gates between phases. Idempotent — safe to re-run after a
  fix or copy edit. Use to ingest a brand-new book end-to-end, or to
  re-process a corrected book through every downstream stage. Trigger
  phrases: "run the full pipeline", "ingest this book end to end",
  "phase 01 through 04", "ship this book".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
metadata:
  pipeline_phase: "all"
  reference: "docs/html/books-pipeline.html#runbook"
---

# Book Pipeline — Full End-to-End Orchestrator

## Purpose

Run a single book all the way from a PDF or EPUB in `_inbox/` to live across pgvector, OpenAI Vector Stores, Gemini File Search, and Anthropic Files. Enforce quality gates so a broken phase blocks advancement. Skip work that's already done (idempotent on re-run).

## Pipeline graph

```
                  /book-convert (Phase 01)
                       │
                       ▼
                  /book-validate (Phase 01b — 5-layer harness)
                       │
                       ▼
                  /book-audit (BookQuality v1.0)
                       │
              ┌────────┴────────┐
            GREEN              YELLOW or RED
              │                    │
              │                    ▼
              │              /book-fix (writes fix-<slug>.md;
              │               optionally executes)
              │                    │
              │                    ▼
              │              re-run /book-audit
              │                    │
              └────────┬───────────┘
                       │
                       ▼
                  /book-frontmatter (Phase 02 — Zod validation)
                       │
                       ▼
                  /book-ingest (Phase 03 — Supabase upsert)
                       │
                       ▼
                  /book-chunk (Phase 04a — chunks.jsonl)
                       │
                       ▼
                  /book-rag-push (Phase 04b — fan out + smoke test)
                       │
                       ▼
                       ✓
```

## Invocation

`$ARGUMENTS`:

- **`<input-file-or-book-slug>`** — Either a path to a PDF/EPUB in `_inbox/` (for a brand-new book) OR a `<book-slug>` whose corpus already exists (for re-processing). Required.
- **`--from-phase <phase>`** — Resume from a phase. Default: auto-detect (skip phases whose outputs already exist and are unchanged).
  - Values: `convert | validate | audit | fix | frontmatter | ingest | chunk | rag-push`
- **`--stop-after <phase>`** — Stop after this phase completes. Default: `rag-push`.
- **`--auto-fix`** — On YELLOW/RED audit, automatically run `/book-fix --mode=execute` and re-audit. Default: `false` (ask the user).
- **`--targets <list>`** — Pass-through to `/book-rag-push`. Default: `pgvector,openai,gemini,claude`.
- **`--dry-run`** — Print the planned phase sequence without running.

## Process

### Phase routing

For each phase, decide: skip (output up to date), run, or fail. Use these signals:

| Phase | Skip if | Run if |
|---|---|---|
| Convert | `corpus/alan_hirsch/<slug>/*.md` exists AND `_inbox/<slug>.<ext>` mtime older than chapter mtime | otherwise |
| Validate | `<book-dir>/.ingest/validation-*.json` exists, verdict PASS, all chapter SHAs match | otherwise |
| Audit | `docs/build/audits/<slug>-*.md` exists from current week | otherwise |
| Fix | only if audit verdict ≠ GREEN | n/a |
| Frontmatter | `<book-dir>/.ingest/frontmatter-*.json` PASS, all SHAs match | otherwise |
| Ingest | DB row's `manifest:version` matches `book.json:version` AND no chapter SHA changed | otherwise |
| Chunk | `<book-dir>/.ingest/chunks.jsonl` exists, all chunk SHAs match | chapter SHA changed |
| RAG-push | `<book-dir>/.ingest/rag-state.json` records each target's last upload at current chunk SHA set | chunks changed |

### Step 1 — Detect input + slug

If `$ARGUMENTS` is a file path, infer slug from filename. If it's a slug, look up `_inbox/<slug>.pdf` or `_inbox/<slug>.epub`.

### Step 2 — Run phases (sequential, with gates)

For each phase:

1. Print `▶ Phase 01 — Convert` (or whatever).
2. Invoke the corresponding skill via `Skill` tool with the right arguments.
3. Read the skill's structured summary output.
4. **Gate:** if the phase failed, stop and report. Do not advance.
5. **Skip:** if the skill reports "no work to do, output current", note it and advance.
6. **Quality gate after audit:** branch on verdict.
   - GREEN → advance to frontmatter.
   - YELLOW / RED → if `--auto-fix`, run `/book-fix --mode=execute` and re-audit; otherwise stop and ask.

### Step 3 — Final report

```
Pipeline complete: <book-slug>
  ✓ Phase 01 Convert       (skipped — up to date)
  ✓ Phase 01b Validate     (skipped — up to date)
  ✓ BookQuality Audit       GREEN  (4 minor low-severity findings)
  ✓ Phase 02 Frontmatter    18/18 chapters validated
  ✓ Phase 03 Ingest         3 chapters changed; 47 sections regenerated
  ✓ Phase 04a Chunk         +12 added, ~7 modified, 4218 unchanged
  ✓ Phase 04b RAG push      pgvector +12 · openai +12 · gemini +12 · claude +0
                            smoke test: top-3 Jaccard 0.62 ✓

  Verdict: ✓ Live on all four stores
  Total wall time:   8m 42s
  Total API cost:    $1.34

  Next: monitor `book_chunks` for query coverage; watch
        `corpus/alan_hirsch/_archive/<slug>-*` for any pre-fix snapshots
        that can be deleted after a successful 30-day soak.
```

## Operating Principles

1. **Each phase is its own skill.** This skill is a thin orchestrator — never duplicate phase logic. If a phase needs a behavior change, change the phase skill, not this orchestrator.
2. **Quality gates are non-negotiable.** A book that fails validation does not get a frontmatter pass; a RED audit does not get ingested. The pipeline halts and surfaces the problem.
3. **Idempotent re-runs.** Running the pipeline twice on an unchanged book should produce the same artifacts and skip every phase. Running it on a book where Ch.4 was hand-edited should re-validate, re-audit, re-chunk, and re-push only the affected chunks.
4. **Pre-archive on every destructive step.** `/book-convert` and `/book-fix` archive the current state before overwriting; this skill verifies those archives exist before allowing those phases to run.
5. **Cost transparency.** Every phase reports its API spend; this skill aggregates and prints a total.

## Anti-patterns

- ❌ Running `/book-rag-push` without `/book-audit` first — that's how fabricated content lands in production retrieval.
- ❌ Skipping `/book-validate` because Phase 01 "looked fine" — the harness exists because eyeballing doesn't catch alternate-line drops.
- ❌ Auto-fixing a RED audit without human review — content rewrites need eyes; the prompt-based approach in `/book-fix --mode=generate` is safer.
- ❌ Marking a book "live" without the smoke test in `/book-rag-push` confirming all four stores agree on the top results.

## References

- [docs/html/books-pipeline.html#runbook](../../../docs/html/books-pipeline.html#runbook) — End-to-end runbook brief
- All sibling skill SKILL.md files
- [docs/build/prompts/](../../../docs/build/prompts/) — Remediation prompt exemplars
- [docs/build/audits/](../../../docs/build/audits/) — Past audit reports (created on demand)
