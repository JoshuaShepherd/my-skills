# File → column → parser map (full detail)

Read this when authoring research files or hand-wiring substrate leaders. The parsers live in `src/lib/services/movement-leader-research/markdown.ts` and the ETL in `corpus-etl.ts`.

## Table of contents
- [Narrative columns](#narrative-columns)
- [Catalog columns (books / articles / audio / videos)](#catalog-columns)
- [Frameworks](#frameworks)
- [Voice analysis](#voice-analysis)
- [Reflected understanding (RU / "A Letter")](#reflected-understanding)
- [Welcome letter contract](#welcome-letter-contract)
- [Dossier card mapping](#dossier-card-mapping)
- [Substrate leaders: SQL wiring recipes](#substrate-sql)

## Narrative columns

- `summary.md` → `calling_profile.{summary,markdown}` + `bio_long/bio_short`. The ETL takes the **first prose paragraph** after the H1 as the summary, so it must be prose (≥ ~80 chars), not bullets or `**Field**:` metadata lines.
- `biography.md` or `profile/biography.md` → `biography`. First substantial prose paragraph becomes the leader's long bio.
- `profile/identity.md` → `identity`; `profile/theology.md` → `theology`. Free markdown.
- All narrative text is passed through `stripStaffSections` at ingest — staff headings (Gap Analysis, Movemental Fit/Opportunities/Recommendation, What We Will Not Do, At-A-Glance Scorecard, Competitive Landscape, Commerce, Audience Profile) and inline "Movemental Fit …"/"gap-analysis"/"recommendation: onboard" fragments are dropped.

## Catalog columns

`content/books.md` → `books[]`: `### Title` sections; year from a `| Published | YYYY |` table row, excerpt from a `**Description**:` line. A single wide `| # | Title | Role | Publisher | Year | URL |` table also parses.

`content/articles.md`, `content/audio.md`, `content/videos.md` → `articles/audio/videos[]`: pipe tables whose header row contains a **Title** (or **Episode Title**) column. Optional columns matched by header keyword: Date/Published, URL, Channel/Platform/Podcast/Outlet/Publisher, Type, Duration. Rules:
- One data row = one item. Leave URL cell `—` when unverified — never invent links.
- No aggregate rows: titles like "various", "multiple", "summary", "total", "blog archive", "100+ episodes" are skipped, as are heading rows like "Guest appearances"/"Podcasts hosted".

`content/content-audit.md` → merged into books/articles/videos/audio (split on `##` headings; tables or `- Ref — "Title" (year)` bullets).

## Frameworks

`content/frameworks.md` → `frameworks[]` as `{ name, markdown }` via `parseFrameworkSections`. One `###` block per framework:

```markdown
### <Framework Name>

| Field | Value |
|-------|-------|
| Introduced | <year> (*<book/source>*) |
| Components | <key parts> |
| Source | [<label>](<url>) |

<One-sentence prose summary — becomes the dossier card body.>
```

The heading text becomes `name`; the body (table + summary) becomes `markdown`. Ground in the leader's books/research — 5–9 frameworks is typical for a rich leader. Do not invent frameworks.

## Voice analysis

`profile/voice-analysis.md` → `voice_analysis` via `parseVoiceAnalysisMarkdown`. Include, verbatim enough to match:

```markdown
| Tone | <descriptors, e.g. warm, prophetic> |
| Register | <e.g. practitioner / pastoral> |
```

then a `**Recurring phrases**:` block with several straight-double-quoted `"phrases"`, and a `**Favorite metaphors**:` block with **bold** items.

## Reflected understanding

`reflected-understanding/<slug>.md` in the SHARED dir `../movemental-ai/docs/movement_leader_research/reflected-understanding/` → `reflected_understanding_md`. (Per-leader `<slug>/reflected-understanding/*.md` also works and takes precedence.)

Leader-safe "A Letter". Mirror `reflected-understanding/alan-hirsch.md`: sections `## Calling`, `## Existing Content (before the platform we're building)`, `## Constraints`. Second person, ~600–1200 words. **Exclude Audience/TAM sizing and Commerce/revenue analysis** (staff-only) and any Movemental-Fit scoring. `research:verify` wants > 200 chars for slugs flagged `requiresReflectedUnderstandingMd`.

## Welcome letter contract

`welcome-letter.md` → `movement_leader_welcome_letters` via `research:publish-letter` (validated):
- Line 1: leader's first name only.
- Then exactly 7 paragraphs, blank line between each.
- Body 900–1100 words. Never the word "ecosystem". Final line: `— Movemental`.
- Voice arc: inventory → fragmentation → embodied wisdom → Movemental AI → dashboard work → 12-month vision → next-season charge.
- Dry-run first: `pnpm research:publish-letter -- --slug=<slug> --dry-run`.

## Dossier card mapping

`src/lib/author-dossier/corpus-content.ts` builds the dossier:
- Framework cards: `title = frameworks[].name`, `body = lastProseLine(frameworks[].markdown)` — that's why each framework block must END with a one-sentence prose summary.
- Stats/media cards read the array lengths and item `title`/`year`/`reference`/`link`.

## Substrate SQL

Substrate leaders (`source_version` `substrate:`/`legacy-write:`) must NOT be re-ETL'd. Author the same files, then wire the specific columns by SQL, scoped by slug. Run from `movemental-visual-editor-main` so imports resolve.

RU column (parameterized — no quoting issues; reuse the project's `db`):

```ts
// scripts/_tmp-wire.ts  (delete after running)
import "./load-dotenv-for-scripts";
import { readFileSync } from "node:fs";
import { sql } from "drizzle-orm";
import { db } from "../src/lib/database/db";
import { parseContentCatalogTables } from "../src/lib/services/movement-leader-research/markdown";
async function main() {
  for (const slug of ["jr-woodward", "liz-rios"]) {
    const ru = readFileSync(`../movemental-ai/docs/movement_leader_research/reflected-understanding/${slug}.md`, "utf8");
    await db.execute(sql`UPDATE movement_leader_corpus_data mlcd SET reflected_understanding_md = ${ru}, last_synced_at = now() FROM movement_leaders ml WHERE mlcd.movement_leader_id = ml.id AND ml.slug = ${slug}`);
  }
  // videos: parse the authored file, set only if empty (don't overwrite substrate)
  const vids = parseContentCatalogTables(readFileSync("../movemental-ai/docs/movement_leader_research/lucas-pulley/content/videos.md", "utf8"), "content/videos.md")
    .map((v) => ({ ...v, contentType: "video" }));
  await db.execute(sql`UPDATE movement_leader_corpus_data mlcd SET videos = ${JSON.stringify(vids)}::jsonb FROM movement_leaders ml WHERE mlcd.movement_leader_id = ml.id AND ml.slug = 'lucas-pulley' AND jsonb_array_length(COALESCE(mlcd.videos,'[]'::jsonb)) = 0`);
}
main().then(() => process.exit(0)).catch((e) => { console.error(e); process.exit(1); });
```

Scrub a leaked staff section from a substrate leader's `calling_profile` in place (apply `stripStaffSections` to its string subfields, write back) — never re-ETL:

```ts
import { stripStaffSections } from "../src/lib/services/movement-leader-research/markdown";
const rows = (await db.execute(sql`SELECT mlcd.calling_profile AS cp FROM movement_leader_corpus_data mlcd JOIN movement_leaders ml ON ml.id=mlcd.movement_leader_id WHERE ml.slug=${slug}`)) as Record<string, unknown>[];
const cp = (rows[0]?.cp ?? {}) as Record<string, unknown>;
for (const k of ["summary", "oneLiner", "markdown"]) if (typeof cp[k] === "string") cp[k] = stripStaffSections(cp[k] as string);
await db.execute(sql`UPDATE movement_leader_corpus_data mlcd SET calling_profile = ${JSON.stringify(cp)}::jsonb FROM movement_leaders ml WHERE mlcd.movement_leader_id=ml.id AND ml.slug=${slug}`);
```
