---
name: movemental-site-template-publish
description: Publish a Stitch-authored HTML/Tailwind one-page site mockup into the Movemental Studio front-end-template catalog so it shows up as a selectable option in the onboarding template selector. Use WHENEVER the operator hands over a Stitch (or any standalone Tailwind) HTML file and wants it "uploaded to Supabase", "added as a template", "added to the template selector / options", "published as a front-end template", or "turned into a site template". Takes the raw HTML, derives catalog metadata, saves the reference HTML, screenshots a desktop + mobile preview, uploads the previews to the `template-previews` Storage bucket, upserts a `front_end_templates` row (status=published), and verifies the template now appears in the published catalog the selector reads. Runs in the `movemental-visual-editor-main` repo.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__claude_ai_Supabase__execute_sql, mcp__claude_ai_Supabase__list_projects, mcp__claude_ai_Supabase__get_advisors
---

# Movemental site-template publisher

Take a Stitch / standalone Tailwind **one-page site mockup** and land it as a selectable option in the Studio onboarding **template selector**. This is the manual TPL-02 asset+seed flow (the operator-driven alternative to the deferred TPL-90 Stitch-publish automation).

The selector at `/onboarding/template` lists every `front_end_templates` row where `status = 'published'`, ordered by `sort_order` then `title` (see `src/lib/services/custom/site-templates.service.ts` → `listPublishedTemplates`). **A template "appears as an option" iff a published row exists.** Everything else (HTML reference, preview PNGs) makes that row look good and previewable. So the job is: produce assets → write the published row → verify it lists.

## Where everything lives (the contract)

| Thing | Location |
|---|---|
| Catalog table | `public.front_end_templates` (Supabase project `vhaiiiykcukrlyvwlgip`) |
| Version-controlled seed (SSOT) | `supabase/seed-front-end-templates.sql` — idempotent `insert … on conflict (slug) do update` |
| Apply seed | `pnpm seed:templates` (runs the SQL via `DATABASE_URL`) |
| Reference HTML | `docs/html/templates/<slug>/index.html` (standalone, no `src/` imports) |
| Preview assets bucket | Storage `template-previews` (public read) → `template-previews/<slug>/home-desktop.png` (+ `home-mobile.png`, `home-desktop.html`) |
| Types / Zod (do not hand-drift) | `src/lib/site-templates/{types,schemas}.ts` |

**Column shape** (`front_end_templates`): `slug` (unique), `title`, `subtitle?`, `description`, `status` (`draft`|`published`|`deprecated`), `sort_order`, `tags` jsonb (string[]), `design_tokens` jsonb (semantic token→value map), `preview_manifest` jsonb (`[{key,label,device,image_url,html_url?}]`), `hero_config` jsonb (`{screen_key,aspect_ratio,slot_strategy?}`), `default_recommendation_weight`, `published_at`. Validate the row mentally against `src/lib/site-templates/schemas.ts` — `image_url`/`html_url` must be real `https://` URLs; `design_tokens` values are all strings; `hero_config.aspect_ratio` is a string like `"4/5"`.

## When to invoke

Invoke when the operator gives you an HTML/Tailwind file (path or pasted) and wants it added to the picker. Do **not** invoke to design a new mockup from scratch (that's a Stitch/design task) or to change the selector UI/API (TPL-03/04/05). This skill ingests a finished mockup and publishes it.

## Inputs to gather (ask only if missing)

1. **The HTML file** — a path in the repo, or pasted markup. Required.
2. **slug** — kebab-case, unique. Default: derive from the title (e.g. "Quiet Editorial" → `quiet-editorial`). Confirm it doesn't collide with an existing row.
3. **title** — leader-facing name. Derive from `<title>`/hero `<h1>` if not given.
4. **status** — default `published` (so it lists immediately). Use `draft` only if the operator wants it staged and invisible.

Everything else (subtitle, description, tags, design_tokens, hero_config, sort_order, weight) you derive from the HTML — see step 2.

## Procedure

### 1. Read the HTML and pick the slug

Read the file. Decide the **slug** (kebab, unique). Check for collisions:

```bash
grep -n "^  *'<slug>'," supabase/seed-front-end-templates.sql   # quick check
```

and/or via Supabase MCP: `select slug, status from front_end_templates order by sort_order;`. If the slug already exists, this is an **update** (the seed upsert handles it) — tell the operator you're updating, not adding.

### 2. Derive catalog metadata from the HTML

- **subtitle**: one short phrase (e.g. "Cream paper, Newsreader headlines").
- **description**: 1–2 sentences describing what the one-page mockup represents. Always frame it as a *representative public-site style, not the dashboard* (matches existing seed rows).
- **tags**: 2–4 from the controlled vocabulary only — `scholarly`, `warm-paper`, `editorial`, `minimal`, `course-forward`. Do not invent tags (the selector filters on these).
- **design_tokens**: extract from the file's `tailwind.config` colors and `:root`/`<style>` vars. Map to semantic roles: `--background`, `--foreground`, `--primary`, `--card`, `--border`, `--font-serif`, `--font-sans`. All **string** values. Mirror `src/app/globals.css` role names; keep within the file's actual palette (no invented hex).
- **hero_config**: default `{"screen_key":"home-desktop","aspect_ratio":"4/5","slot_strategy":"overlay"}`.
- **sort_order** / **default_recommendation_weight**: place after existing rows (current rows use 10/20/30 sort, 100/80/70 weight). Pick the next sort step (e.g. 40) and a sensible weight unless the operator wants it recommended-first.

### 3. Prepare the reference HTML

Write the markup to `docs/html/templates/<slug>/index.html`. It must be a **standalone** file (Tailwind CDN or inline tokens, no imports from `src/`). Ensure it carries the hero-portrait slot so TPL-05's headshot composite can target it — the home hero image/element needs the `data-mve-hero-slot` attribute (see `reference/template-html-skeleton.html` and the existing `docs/html/templates/warm-scholarly/index.html`). If the Stitch export lacks it, add `data-mve-hero-slot` to the hero portrait element and a `[data-mve-hero-slot]{aspect-ratio:4/5;object-fit:cover}` style. Strip any external tracking scripts.

### 4. Screenshot + upload preview assets

Preview PNGs live in Storage, not git. Use the bundled script (it needs the repo's `@playwright/test` + `@supabase/supabase-js`, so run it from the repo root after copying it into `scripts/`):

```bash
cp .claude/skills/movemental-site-template-publish/scripts/publish-stitch-template-assets.ts scripts/
pnpm exec playwright install chromium    # once, if browsers missing
pnpm tsx scripts/publish-stitch-template-assets.ts --slug <slug>
```

The script renders `docs/html/templates/<slug>/index.html` at 1440×900 (desktop) and 390×844 (mobile), uploads `home-desktop.png` / `home-mobile.png` / `home-desktop.html` to `template-previews/<slug>/`, HEAD-verifies the public URLs, and prints a ready-to-paste **manifest block** (the `image_url`/`html_url` values) plus a copy of the `design_tokens`/`hero_config` defaults. It needs `NEXT_PUBLIC_SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` in `.env.local` (already present for this repo).

If Storage upload is blocked (no service-role key in this environment), fall back to deterministic placeholder URLs `https://picsum.photos/seed/mve-<slug>-desktop/1440/900` and tell the operator the previews are placeholders pending an asset upload — the row will still list.

### 5. Upsert the catalog row (the part that makes it an option)

Add the row to the **version-controlled seed** so it's reproducible, then apply it.

1. Edit `supabase/seed-front-end-templates.sql`: insert a new `values` tuple **before** the `on conflict (slug) do update` line, using `reference/catalog-row.sql.tmpl` filled with the slug/title/subtitle/description/tags/design_tokens/preview_manifest (real Storage URLs from step 4)/hero_config/weight. Keep the trailing comma rules correct (comma between tuples, none before `on conflict`).
2. Apply:

```bash
pnpm seed:templates
```

This upserts by `slug` and prints the published count. Because `published_at` uses `coalesce(existing, excluded)`, re-runs are safe.

> Alternative when you cannot run `pnpm seed:templates` (no `DATABASE_URL`): apply the same single-row `insert … on conflict (slug) do update …` via Supabase MCP `execute_sql`. Still update the seed file so the catalog stays reproducible.

### 6. Verify it's now a selectable option

- **Published row exists:**
  ```bash
  pnpm tsx -e "import 'dotenv/config'" 2>/dev/null # (skip — seed script already prints the count)
  ```
  Prefer Supabase MCP: `select slug, title, status, sort_order from front_end_templates where status='published' order by sort_order;` — confirm the new slug is present with `status='published'`.
- **Asset URLs resolve:** the script HEAD-checks them; if you used MCP/placeholders, spot-check one `image_url` returns 200.
- **Types still align:** `pnpm typecheck` (the row is data, not code, but run it if you touched anything under `src/`).
- Tell the operator the template will appear at `/onboarding/template` for any org without an active claim.

### 7. Clean up / report

- The copied `scripts/publish-stitch-template-assets.ts` may be left (matches the repo's one-off-script convention) or removed — mention which.
- Update the feature's `docs/build/prompts/site-template-selector/RUNNER.md` Session changelog / TPL-02 Attempt log if the operator is tracking the build there.
- Report: slug, title, status, where the reference HTML and preview assets live, and the published count.

## Guardrails — do not

- Do **not** hand-edit `src/lib/database/schema.ts`, `src/lib/site-templates/types.ts`, or `schemas.ts` to fit a template — the row must conform to the existing schema. If a genuinely new column is needed, that's a TPL-01 migration, not this skill.
- Do **not** invent tag slugs outside the controlled vocabulary, or non-string `design_tokens` values.
- Do **not** commit multi-MB PNGs into git — previews belong in Storage; git holds only the reference HTML.
- Do **not** touch `organization_template_claims` (claims are runtime), the selector UI, or the API routes.
- Do **not** set `status='published'` on a half-built row you can't preview — use `draft` so it stays out of the picker until assets land.

## Related

- Build spec: `docs/build/prompts/site-template-selector/` (TPL-00…06, RUNNER.md). This skill operationalizes **TPL-02**.
- Deferred automation: `90-deferred-stitch-publish-pipeline.md` (TPL-90) — full Stitch MCP → Storage → upsert pipeline this skill front-runs by hand.
