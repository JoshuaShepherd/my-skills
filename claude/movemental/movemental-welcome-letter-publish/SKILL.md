---
name: movemental-welcome-letter-publish
description: Publish a finished Movemental dashboard welcome letter to the production Supabase database so the named movement leader sees it on their next dashboard load. Use whenever the user says "publish the welcome letter for <author>", "push <author>'s welcome letter live", "ship the dashboard letter", "publish welcome letter from <file>", or any phrasing that combines a finished welcome letter with making it visible to the leader. Companion to the movemental-welcome-letter skill, which generates the draft; this skill takes the finished draft (file or pasted text) and wires it into the right tenant. Run this after the human has read the draft and is ready to make it live.
allowed-tools: Read, Bash, Glob, mcp__claude_ai_Supabase__list_projects, mcp__claude_ai_Supabase__execute_sql, mcp__claude_ai_Supabase__get_advisors
---

# Movemental welcome-letter publisher

Take a finished welcome letter for a specific movement leader and publish it to the `movement_leader_welcome_letters` table on the Movemental Supabase project. The leader sees it on their next dashboard load via RLS; the previous published letter (if any) is archived in the same operation.

This skill is the **publish half** of a two-skill workflow:

| Skill | Role |
|---|---|
| [[movemental-welcome-letter]] | Drafts the 1,000–1,050-word letter from the leader's `fragmentation-story.md` dossier. Saves to `docs/movement_leader_research/<slug>/welcome-letter.md`. |
| `movemental-welcome-letter-publish` (this skill) | Takes that saved draft (or any file the operator points at) and ships it to the database, scoped to the right tenant. |

## When to invoke

Invoke when the operator wants a welcome letter to actually go live for a leader. Don't invoke this to write or edit a letter — that's the upstream skill. Don't invoke for "draft" or "preview" requests.

Typical phrasings:
- "publish Brad Brisco's welcome letter"
- "push the welcome letter live for `<slug>`"
- "ship the dashboard welcome from `<path>`"
- "publish welcome letter from the file we just wrote"
- "make Alan's welcome letter visible in the dashboard"

## Input

`$ARGUMENTS` accepts a slug plus optional flags:

- `<slug>` — required. The movement leader's slug (`alan-hirsch`, `brad-brisco`, etc.). Resolves to `public.movement_leaders.slug`.
- `--from=<path>` — path to the markdown file containing the letter. Defaults to `/home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/welcome-letter.md`. Accepts the date-stamped variant `welcome-letter-YYYY-MM-DD.md` if the canonical one is missing.
- `--env=production|staging` — Supabase project. Defaults to **production** (`vhaiiiykcukrlyvwlgip`, name `movemental`). Staging is not currently provisioned for this table; if the operator passes `--env=staging`, stop and ask which project to use.
- `--dry-run` — run all validation + the read-back simulation, but do not write. Recommended on first invocation for a leader.
- `--notes="<text>"` — optional editor note stored on the row (audit only).
- `--no-onboarding-task` — skip the optional onboarding-task wiring in Phase 5.

If `$ARGUMENTS` is empty, list active leaders (one MCP call) and ask which to publish for.

## Project context

| Item | Value |
|---|---|
| Supabase project (prod) | `vhaiiiykcukrlyvwlgip` (name: `movemental`) |
| Tables | `public.movement_leader_welcome_letters`, `public.movement_leader_welcome_letter_views` |
| Status enum | `movement_leader_welcome_letter_status` — `published`, `archived` |
| RLS helpers | `public.is_movemental_staff(uuid)`, `public.is_movement_leader_owner(uuid)`, `public.is_member_of_org(uuid, uuid)` |
| Onboarding task key | `view_welcome_letter` (org-scoped row in `public.onboarding_tasks`) |

The MCP tools (`mcp__claude_ai_Supabase__*`) run as the project's service role. They bypass RLS — that means the read-back check in Phase 4 must explicitly simulate the leader's identity (use `SET LOCAL ROLE authenticated` + `SET LOCAL request.jwt.claim.sub`) rather than relying on the MCP's elevated access.

## Phase 1 — Resolve and validate

1. **Pick the project.** Call `mcp__claude_ai_Supabase__list_projects` once; confirm the production project id matches `vhaiiiykcukrlyvwlgip`. Reject mismatches.

2. **Resolve the leader.** Single SQL call:

   ```sql
   SELECT ml.id            AS movement_leader_id,
          ml.slug, ml.full_name, ml.email,
          ml.user_id, ml.status::text,
          up.first_name, up.email AS profile_email,
          o.id             AS organization_id,
          o.slug           AS organization_slug,
          o.name           AS organization_name
   FROM public.movement_leaders ml
   LEFT JOIN public.user_profiles up ON up.id = ml.user_id
   LEFT JOIN public.organizations o  ON o.account_owner_id = up.id
   WHERE ml.slug = :slug;
   ```

   Required: a single row with `status = 'active'`, non-null `user_id`, non-null `organization_id`. If any of those are missing, stop and tell the operator to run `movemental-tenant-provision` first.

3. **Locate the letter file.** Default to `…/movement_leader_research/<slug>/welcome-letter.md`. If absent, glob `welcome-letter-*.md` in the same directory and pick the newest. If still missing, stop with a clear message — this skill does not draft.

4. **Parse the letter.** The file follows the seven-move spec exactly:

   - Line 1: `<First name>` on its own line.
   - Blank line.
   - Seven paragraphs of continuous prose, separated by blank lines.
   - Final line: `— Movemental` (or close variant).

   Extract:
   - `first_name` (line 1, trimmed)
   - `body_md` (everything between the first-name line and the signoff line, trimmed)
   - `signoff` (final line, default to `— Movemental` if missing — but warn)
   - `word_count` of `body_md` only — count whitespace-delimited tokens

5. **Validate.** All must hold; on failure, stop and show the operator the specific failure. Do not write.

   | Check | Rule |
   |---|---|
   | First-name match | `first_name` (case-insensitive) matches the leader's `first_name` from `user_profiles` or the first token of `full_name` |
   | Word count | `900 ≤ word_count ≤ 1100` (DB check is `BETWEEN 900 AND 1100`; the spec target is 1,000–1,050) |
   | Body non-empty | `length(body_md) > 0` |
   | Signoff present | last non-blank line starts with `—` |
   | No FORBIDDEN words | `body_md` does not contain the literal `ecosystem` (case-insensitive). Warn (don't block) if it contains `kingdom`/`multiplication`/`movement`/`apostolic` more than once per paragraph |
   | Paragraph count | exactly seven blank-line-separated paragraphs in `body_md` |

6. **Compute provenance.**
   - `source_corpus_version` — mtime of the leader's `fragmentation-story.md` as ISO 8601 (`stat -c %y …/<slug>/fragmentation-story.md` then format), so we can tell which dossier snapshot the letter came from.
   - `generated_by` — `skill:movemental-welcome-letter` if the letter file was produced by the draft skill (heuristic: file is named `welcome-letter.md` or `welcome-letter-YYYY-MM-DD.md`); otherwise `human:<operator>`.
   - `generation_metadata` — JSON object with `{ "word_count": ..., "paragraph_count": 7, "validation_warnings": [...], "source_file": "...", "source_mtime": "..." }`.

## Phase 2 — Dry-run preview

Before any write, print to chat:

- Resolved leader: slug, full_name, email, `movement_leader_id`, `user_id`, `organization_id`, `organization_slug`
- Source file path + mtime
- Word count, paragraph count, signoff line, first-name line
- Any validation warnings
- A 200-character preview of the first paragraph

If `--dry-run`, stop here.

## Phase 3 — Publish (atomic)

Execute as a single SQL statement so the partial unique index `WHERE status = 'published'` never sees two rows at once. The CTE archives any prior published row and inserts the new one in the same statement:

```sql
WITH
prev_archive AS (
  UPDATE public.movement_leader_welcome_letters
  SET status = 'archived',
      archived_at = now()
  WHERE movement_leader_id = :movement_leader_id
    AND status = 'published'
  RETURNING id, version_number
),
next_version AS (
  SELECT COALESCE(MAX(version_number), 0) + 1 AS v
  FROM public.movement_leader_welcome_letters
  WHERE movement_leader_id = :movement_leader_id
),
inserted AS (
  INSERT INTO public.movement_leader_welcome_letters
    (movement_leader_id, organization_id,
     first_name, body_md, signoff, word_count,
     source_corpus_version, generated_by, generation_metadata,
     version_number, status, published_at,
     created_by_user_id, notes)
  SELECT
    :movement_leader_id, :organization_id,
    :first_name, :body_md, :signoff, :word_count,
    :source_corpus_version, :generated_by, :generation_metadata::jsonb,
    next_version.v, 'published', now(),
    NULL, NULLIF(:notes, '')
  FROM next_version
  RETURNING id, version_number, status, published_at
)
SELECT
  (SELECT id FROM inserted)             AS new_letter_id,
  (SELECT version_number FROM inserted) AS new_version,
  (SELECT published_at FROM inserted)   AS published_at,
  (SELECT id FROM prev_archive)         AS archived_letter_id,
  (SELECT version_number FROM prev_archive) AS archived_version;
```

Bind every `:param` via the call — never string-interpolate `body_md`. The MCP tool's `execute_sql` does not support bound parameters directly, so escape single quotes in `body_md` by doubling them (`'` → `''`) and wrap each parameter in `$tag$ … $tag$` dollar-quoting where the body might contain backticks or other markdown special characters. Generate a unique tag per call (e.g. `$body42$`).

If the insert fails with a constraint violation (`word_count_in_range`, `version_per_leader`, `movement_leader_welcome_letters_one_published`), stop and report — do not retry blindly.

## Phase 4 — Verify under the leader's identity

The MCP runs as service role; it would always succeed. To prove the leader can actually read their letter through RLS, switch identity inside the same connection:

```sql
BEGIN;
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claim.sub = :leader_auth_user_id;  -- == movement_leaders.user_id
SET LOCAL request.jwt.claim.role = 'authenticated';

SELECT id, version_number, status, length(body_md) AS body_len, published_at
FROM public.movement_leader_welcome_letters
WHERE movement_leader_id = :movement_leader_id;

ROLLBACK;
```

Expect: **exactly one row**, `status = 'published'`, `id` matches the `new_letter_id` from Phase 3. Zero rows = RLS is blocking the leader (something is wrong with `is_movement_leader_owner` or the `user_id` linkage). More than one row = the partial unique index failed — escalate.

Then prove an unrelated leader cannot read this row:

```sql
BEGIN;
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claim.sub = :other_leader_auth_user_id;
SET LOCAL request.jwt.claim.role = 'authenticated';

SELECT count(*) AS leak_count
FROM public.movement_leader_welcome_letters
WHERE movement_leader_id = :movement_leader_id;

ROLLBACK;
```

Expect `leak_count = 0`. If non-zero, treat as a security incident — stop, do not advertise the publish to the operator, and ask them to audit RLS before another publish.

Pick `:other_leader_auth_user_id` as the `user_id` of any active leader whose slug is not the target.

## Phase 5 — Optional onboarding-task wiring

Unless `--no-onboarding-task`:

```sql
INSERT INTO public.onboarding_tasks (organization_id, task_key, status, movemental_unlocked, metadata)
VALUES (:organization_id, 'view_welcome_letter', 'unlocked', true,
        jsonb_build_object('welcome_letter_id', :new_letter_id, 'published_at', :published_at::text))
ON CONFLICT (organization_id, task_key) DO UPDATE
SET status = 'unlocked',
    metadata = public.onboarding_tasks.metadata
              || jsonb_build_object('welcome_letter_id', EXCLUDED.metadata->'welcome_letter_id',
                                    'published_at', EXCLUDED.metadata->'published_at'),
    updated_at = now()
WHERE public.onboarding_tasks.status <> 'completed';
```

Note: this assumes a `(organization_id, task_key)` unique constraint exists on `onboarding_tasks`. If the ON CONFLICT fails because the constraint isn't present, fall back to a SELECT-then-INSERT-or-UPDATE pattern. Do not invent a constraint.

The front-end completes this task when the leader acknowledges the letter (POSTs to `movement_leader_welcome_letter_views` with `acknowledged_at`). That's app code, not this skill's job.

## Phase 6 — Report back

Single message to the operator. Include:

1. **Project + leader**: project id, leader slug, full name, organization slug, user_id (last 8 chars only — privacy hygiene).
2. **Publish result**: new `letter_id` (full), `version_number`, `published_at`, archived prior `letter_id` if any.
3. **Validation**: word count, paragraph count, signoff, warnings.
4. **RLS verification**: ✓ leader can read, ✓ other-leader cannot read.
5. **Onboarding task**: created / updated / skipped (with reason).
6. **Source provenance**: file path, mtime, `generated_by`.
7. **Next actions for the operator**: "Tell <full_name> their dashboard welcome is live." — and, if the leader hasn't logged in since publish, the URL they should send.

No body text in the report — the letter is in the database and on disk already.

## Hard rules

1. **Never** publish without successful RLS verification (Phase 4 both checks). The leader must be able to read it; no one else must.
2. **Never** UPDATE a published row's `body_md` in place. The lifecycle is publish-new-version → previous-archives. The body is immutable once stored, for audit reasons.
3. **Never** insert from a file path that didn't exist *before* the skill ran. Don't accept letter content via `$ARGUMENTS` itself — the letter is too long to fit cleanly and the dossier-derived provenance disappears.
4. **Never** widen the read RLS policy from this skill. If a stakeholder wants org-wide or anon read, that's a migration request and needs operator + product approval, not a publish.
5. **Service role** stays out of the chat transcript. The MCP handles credentials; never echo them.
6. **One leader at a time** unless the operator passes a comma-separated slug list and explicitly confirms. Bulk publishes mask per-row failures.

## Done definition

- [ ] Leader resolved with `status='active'`, `user_id` and `organization_id` non-null.
- [ ] Letter file parsed and validated (word count in band, seven paragraphs, signoff present, no `ecosystem`).
- [ ] Single CTE statement archived prior published (if any) + inserted new published row.
- [ ] Leader-identity SELECT returned exactly one row matching the new id.
- [ ] Other-leader-identity SELECT returned zero rows.
- [ ] Onboarding task row present (or operator opted out).
- [ ] Operator received the report with new letter id, version, published_at.

## Failure modes worth naming

| Symptom | Likely cause | Action |
|---|---|---|
| `movement_leaders` lookup returns 0 rows | Slug typo or leader not provisioned | Stop. Suggest `movemental-tenant-provision`. |
| `organization_id` is NULL | Leader's owned org missing | Stop. Run `movemental-tenant-provision <slug>`. |
| Insert raises `word_count_in_range` | Letter is < 900 or > 1100 words | Stop. Tell operator to rerun `movemental-welcome-letter <slug>` and tighten the draft. |
| Insert raises `movement_leader_welcome_letters_one_published` | The CTE pattern was broken (two-statement publish was used) | Stop. Manually archive the duplicate; do not paper over. |
| Phase 4 leader read returns 0 rows | `movement_leaders.user_id` doesn't match a real `auth.users.id`, OR `is_movement_leader_owner` is malfunctioning | Stop. Run the Phase 0 gates of `movemental-tenant-provision`. |
| Phase 4 other-leader read returns >0 rows | RLS policy regression | **Treat as security incident.** Stop, archive the just-published row, escalate. |
