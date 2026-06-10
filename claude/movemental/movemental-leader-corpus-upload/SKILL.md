---
name: movemental-leader-corpus-upload
description: Load a movement leader's research into Supabase movement_leader_corpus_data and the related onboarding tables (corpus_review_items, onboarding_tasks, movement_leader_welcome_letters, organizations.onboarding_state). Runs the research:bridge → etl → publish → publish-letter → verify pipeline that compiles the on-disk research tree (profile/, content/, network/, reflected-understanding) into the typed JSONB columns (identity, biography, theology, voice_analysis, calling_profile, books, articles, audio, videos, frameworks, organizations, reflected_understanding_md). Use this WHENEVER asked to push/load/sync/ETL a movement leader's research or dossier into Supabase, wire up movement_leader_corpus_data, fill empty dossier dimensions (videos, audio, frameworks, "A Letter"/reflected understanding, theology, calling), re-run the corpus pipeline, or onboard a leader's corpus — even if the request says "dossier" or "/profile" rather than "corpus_data". Knows the file→column→parser map and the critical substrate rule (substrate-loaded leaders must be wired via targeted SQL, never re-ETL'd).
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent, mcp__claude_ai_Supabase__execute_sql, mcp__claude_ai_Supabase__get_advisors
---

# Movemental Leader Corpus Upload

Load movement-leader research into the single shared Supabase table `movement_leader_corpus_data` (one row per leader, keyed `movement_leader_id`, unique → upsert) plus the onboarding tables that read from it. The dashboard `/profile` Author Dossier renders from these rows.

```
/movemental-leader-corpus-upload $ARGUMENTS    # slug | comma-list | all
```

Supabase project: `vhaiiiykcukrlyvwlgip`. Run the pipeline from the **`movemental-visual-editor-main`** repo with `.env.local` loaded. Research SSOT: `../movemental-ai/docs/movement_leader_research/<slug>/`.

## The model (read before acting)

- **One row per leader, upsert on `movement_leader_id`.** Never create a parallel table. The bridge rule binds it together: `organizations.slug === movement_leaders.slug === research folder name`.
- **Two loaders, two `source_version` prefixes.** Know which one produced a leader before you touch them:
  - **`merged:` / `corpus:`** — compiled from the on-disk research tree by `scripts/etl-movement-leader-research.ts` (`research:etl`). **Safe to re-ETL.**
  - **`substrate:` / `legacy-write:`** — loaded historically by a different system. Their `videos/audio/frameworks/calling` are **not reproducible from files**. **NEVER `research:etl` them** — it overwrites rich columns with empty file-derived ones. Wire their gaps with a **targeted SQL `UPDATE` of just the one column** (see references). The legacy `substrate_md`/`substrate_sections`/`manifest` columns still exist but their loader code is not in this repo — treat them as read-only history.
- **Leader-safe JSONB.** Staff-only sections (Gap Analysis, Movemental Fit, "Recommendation: onboard", Audience/TAM, Commerce) must never reach leader-visible columns. The ETL strips them at ingest via `stripStaffSections` (`src/lib/services/movement-leader-research/markdown.ts`). Columns you set by hand-SQL must be hand-checked leader-safe.
- **Don't clobber what the substrate carries.** `calling_profile` and `reflected_understanding_md` are preserved across re-ETL when the files don't supply them.

## The pipeline (file-based leaders)

Run per slug, in order. Each step is idempotent.

```bash
pnpm research:bridge        -- --slug=<slug>   # ensure movement_leaders row links the org owner
pnpm research:etl           -- --slug=<slug>   # compile research tree → corpus_data JSONB columns
pnpm research:publish       -- --slug=<slug> --unlock  # corpus_review_items, affiliates, themes, brand prefill, onboarding tasks
pnpm research:publish-letter -- --slug=<slug>          # movement_leader_welcome_letters + view_welcome_letter task (dry-run with --dry-run first)
pnpm research:verify        -- --slug=<slug>   # gate: org, leader, slug bridge, corpus content, RU, review counts
```

`--all` runs every cohort slug — only after every slug's research tree is ready.

## File → column → parser map (summary)

| Column | Source file | Parser expectation |
| --- | --- | --- |
| `calling_profile` | `summary.md` (1st para) + `profile/calling-profile.md` | narrative exec-summary paragraph (prose, not bullets/metadata) |
| `biography` | `biography.md` or `profile/biography.md` | first prose paragraph ≥ ~80 chars → bio |
| `identity` / `theology` | `profile/identity.md` / `profile/theology.md` | free markdown |
| `voice_analysis` | `profile/voice-analysis.md` | `\| Tone \|` + `\| Register \|` rows; `**Recurring phrases**:` (quoted); `**Favorite metaphors**:` (bold) |
| `books` | `content/books.md` | `### Title` + `\| Published \| YYYY \|` + `**Description**:` (or wide catalog table) |
| `articles` / `audio` / `videos` | `content/{articles,audio,videos}.md` | pipe table with a **Title** (or **Episode Title**) header column |
| `frameworks` | `content/frameworks.md` | `### name` + Field/Value table + a trailing **one-sentence prose summary** (the dossier card body) |
| `organizations` | `network/organizations.md` | free markdown blob |
| `reflected_understanding_md` | `reflected-understanding/<slug>.md` (shared dir) | leader-safe markdown; **exclude Audience/TAM + Commerce** |

**Full formats, the welcome-letter contract, the dossier-card mapping, and the substrate SQL recipes are in [references/file-column-parser-map.md](references/file-column-parser-map.md) — read it before authoring or hand-wiring.**

## Filling empty dossier dimensions

A dossier card is empty when its column is `[]`/empty. To fill it, author the source file above, then load it (re-ETL for file-based leaders; SQL for substrate). For breadth across many leaders, delegate one subagent per leader to author the files (grounded in existing research + web verification, no fabricated dates/ISBNs/URLs), then run the pipeline centrally yourself. `frameworks` had no ETL path before 2026-06; `parseFrameworkSections` + the `content/frameworks.md` read added it.

## New-leader branch

If a slug has no `movement_leaders` row, it is a NEW leader — invoke **`movemental-tenant-provision`** for it first (Phase 0 gates → identity → auth user → user_profile → owned org → owner membership), then re-resolve and continue. Never hand-insert auth users here, and never upload an orphan corpus.

## Verify + post-check (always)

1. `research:verify` green for every file-based slug.
2. Dossier-gap check — confirm targeted columns are non-empty:
   ```sql
   SELECT o.slug, jsonb_array_length(COALESCE(mlcd.videos,'[]'::jsonb)) videos,
          jsonb_array_length(COALESCE(mlcd.audio,'[]'::jsonb)) audio,
          jsonb_array_length(COALESCE(mlcd.frameworks,'[]'::jsonb)) frameworks,
          length(COALESCE(mlcd.reflected_understanding_md,'')) ru
   FROM organizations o JOIN movement_leaders ml ON ml.slug=o.slug
   JOIN movement_leader_corpus_data mlcd ON mlcd.movement_leader_id=ml.id
   WHERE o.slug = ANY($slugs) ORDER BY o.slug;
   ```
3. Leader-safe check — must return **false** for every leader:
   ```sql
   (mlcd.biography::text||mlcd.identity::text||mlcd.calling_profile::text||mlcd.theology::text||COALESCE(mlcd.reflected_understanding_md,''))
     ~* '(gap.analysis|movemental.fit|movemental.analysis|recommendation:.{0,4}onboard)'
   ```
   If a substrate leader leaks, scrub the offending column in place (apply `stripStaffSections` to its string subfields via `tsx` + `UPDATE`) — do not re-ETL.
4. After any DDL, run `get_advisors` (security + performance) and block on new HIGH/CRITICAL touching this table.

## Hard rules

1. **Substrate leaders: SQL-only, never re-ETL.** This is the single most important rule — re-ETL silently wipes their substrate videos/audio/frameworks/calling.
2. **Idempotent upsert** on `movement_leader_id`. Re-running must not duplicate rows or drop `calling_profile` / `reflected_understanding_md`.
3. **Leader-safe always.** No Gap-Analysis / Movemental-Fit / Audience-TAM / Commerce copy in leader-visible columns.
4. **Provision before upload** for new leaders via `movemental-tenant-provision` — never an ad-hoc auth insert.
5. **Secrets are server-only.** `DATABASE_URL` / service-role keys come from `.env.local`; never echo them or write them to a tracked file.
6. **Don't endorse RU.** Never set `reflected_understanding_endorsed_at` unless the operator explicitly asks (flips the UI chip Preliminary → Endorsed).

## Related skills

- **`movemental-tenant-provision`** — adds a new leader-tenant; this skill calls it for the new-user branch.
- **`movemental-welcome-letter` / `-publish`** — author/publish the onboarding letter that `research:publish-letter` loads.
- **`movement-leader-substrate`** — produces collated research input (legacy substrate path).
