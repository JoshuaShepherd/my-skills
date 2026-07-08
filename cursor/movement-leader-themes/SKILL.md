---
name: movement-leader-themes
description: >-
  Derives a movement leader's core themes from their book corpus and research, then
  authors docs/themes/CORE_THEMES.md (pathway taxonomy) and per-theme deep-dives
  (12-section pathway content, grounded and cited). Use when standing up or refreshing
  theme docs, generating docs/themes, running movement-leader-themes, or building
  pathway content for a movement leader. Requires voice guide for deep-dives — run
  movement-leader-voice first if missing.
disable-model-invocation: true
---

# Movement Leader Themes

Read a movement leader's **own corpus** and produce canonical theme documents in `docs/themes/`:

1. **`docs/themes/CORE_THEMES.md`** — taxonomy and decision record: which 4–6 themes earn pathway status, rejected candidates, integrated argument, book mapping.
2. **`docs/themes/{slug}.md`** — one deep-dive per core theme: 12-section pathway content in the leader's voice, every substantive claim footnoted.

**Discipline:** themes are read out of the corpus, not imposed. Read full books before naming a theme. Research and config are check-against inputs, never source of truth.

## Invocation

```
/movement-leader-themes {leader-slug}
/movement-leader-themes brad-brisco --taxonomy-only
/movement-leader-themes --theme discipleship
/movement-leader-themes --refresh
```

Run from the **leader repo root**.

| Flag | Effect |
|------|--------|
| `{slug}` or display name | Defaults to cwd repo if obvious |
| `--taxonomy-only` | Write `CORE_THEMES.md` only |
| `--theme {slug}` | Rewrite one deep-dive (taxonomy must exist) |
| `--refresh` | Refresh content; keep existing slug set |
| (empty) | Infer leader from repo; ask if ambiguous |

## Inputs (priority order)

| Source | Path | Weight |
|--------|------|--------|
| **Book corpus** | `docs/books/{book-slug}/chapters/*.md` | **Highest** |
| Book metadata | `docs/books/{book-slug}/*.md`, `README.md` | High |
| Research dossier | `docs/movement_leader_research/{slug}/` | Medium |
| Collated substrate | `**/{SLUG}_RESEARCH_COLLATED.md` | Medium |
| Articles / resources | `docs/**/articles/`, `docs/workspace/` | Medium |
| Voice guide | `docs/voice/{SLUG}_VOICE.md` | **Required for deep-dives** |
| Existing config | `src/lib/config/tenant.config.ts`, `src/lib/content/pathways/*.ts` | Check-against only |

If `docs/books/` is empty, stop and say so. Offer research-only run only if user confirms (lower confidence).

## Execution protocol

**Read this skill, then execute phases 1–4 to completion** unless stopped by a flag.

### Phase 1 — Inventory

```bash
ls docs/books/*/chapters/ 2>/dev/null
ls docs/movement_leader_research/ 2>/dev/null
ls docs/voice/ docs/themes/ 2>/dev/null
```

Build book list (slug, title, chapter count, year). For large corpora, delegate per-book reading via **Task** (`subagent_type: explore`, one agent per book → chapter-level theme notes), then synthesize.

### Phase 2 — Taxonomy

Apply four-test filter (corpus centrality, distinctiveness, course viability, audience demand). Select 4–6 themes. Write `docs/themes/CORE_THEMES.md` per [reference.md](reference.md) Part A. Stop if `--taxonomy-only`.

### Phase 3 — Deep-dives

Ensure voice guide exists — if missing, read and run `.cursor/skills/movement-leader-voice/SKILL.md` first.

For each theme slug, write `docs/themes/{slug}.md` per [reference.md](reference.md) Part B. Multi-theme runs: one Task agent per theme; each loads voice guide + relevant chapters.

### Phase 4 — Verify

- `CORE_THEMES.md`: all theme blocks complete; rejected-themes table present; decision record explains non-obvious calls
- Each `{slug}.md`: 12 sections; plural corpus-grounded cases; ≥2 distortions; ≥3 citations per substantive section; four necessities present
- Cross-check: every taxonomy slug has a deep-dive (unless `--taxonomy-only`); no orphan deep-dives

Print session report: slug, theme count, files written, voice guide used (y/n).

## Key rules

1. **Read books first** — no theme before its chapters are read.
2. **Leader's vocabulary** — coined terms, not generic church-growth labels.
3. **Reject honestly** — rejected-themes table and decision record mandatory.
4. **Every claim traces to corpus** — footnotes with book + chapter + page (or `—`).
5. **Deep-dives in voice** — load `docs/voice/{SLUG}_VOICE.md`.
6. **Cases plural and real** — never invent contemporary examples.
7. **Confirm config by default** — revise only when corpus contradicts; record why.
8. **Reference implementation:** brad-brisco repo, `docs/themes/CORE_THEMES.md` and `docs/themes/{slug}.md`.

## Additional resources

- Taxonomy + deep-dive schemas: [reference.md](reference.md)
