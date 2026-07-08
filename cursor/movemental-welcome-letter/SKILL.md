---
name: movemental-welcome-letter
description: Draft the Movemental dashboard welcome letter for a specific movement leader from their fragmentation-story dossier. Use whenever the operator says "write the welcome letter for <author>", "draft the dashboard welcome for <leader>", "generate the fragmentation welcome letter", "do a welcome letter for <slug>", or any phrasing that pairs a movement-leader name with the words welcome, letter, or dashboard intro. Reads the leader's research dossier under docs/movement_leader_research/<slug>/ and emits a 1,000–1,050-word, seven-move letter dense with the leader's actual proper nouns — book titles, podcast appearances, partner publications, and the named city of a future practitioner. Save-to-disk is on by default. Pair with movemental-welcome-letter-publish to ship the finished letter to the database.
disable-model-invocation: true
---

# Movemental welcome-letter drafter

Take a movement leader's `fragmentation-story.md` dossier and emit the seven-move welcome letter they see on first dashboard load. Specificity is the credibility — a generic letter that omits the leader's actual book titles, podcast episodes, and partner publications has failed the task even if it scans well.

## Input

`$ARGUMENTS`: a leader slug or display name, plus optional flags.

| Flag | Behavior |
|---|---|
| (positional) | Author slug (`alan-hirsch`, `brad-brisco`, `jr-woodward`, etc.) or display name → kebab-case slug |
| `--dry-run` | Walk the dossier, report MUST-APPEAR coverage, do not draft |
| `--no-save` | Print to chat only, do not write to disk |
| `--save-to=<path>` | Override the default save path |

If `$ARGUMENTS` is empty, list dossiers that have `fragmentation-story.md` and ask which to draft.

## The spec lives in `references/master-prompt.md`

**Re-read `references/master-prompt.md` in full on every invocation.** It is the literal source of truth — the seven moves, the word count band, the MUST-APPEAR list, the FORBIDDEN list, and the sanity checks. This SKILL.md only handles the workflow around that prompt: locating the dossier, extracting facts, saving the file, and reporting back. Do not paraphrase the master prompt from memory; load the file each time.

## Source of truth — dossier location

Canonical (always use this):

```text
/home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/
```

Lightweight mirror (for cross-checking display name + role only):

```text
/home/josh/dev/01-Movemental-Core/movemental-visual-editor-main/docs/movement_leader_research/<slug>.md
```

Hard requirement: `fragmentation-story.md` must exist in the canonical directory. If it doesn't, stop and tell the operator to run the upstream `fragmentation-story` research skill first. This skill is a translator, not a researcher.

## Workflow

### 1. Resolve the slug and locate the dossier

Normalize `$ARGUMENTS` to kebab-case (`"Alan Hirsch"` → `alan-hirsch`, `"JR Woodward"` → `jr-woodward`). Confirm the dossier directory exists. If not, list available dossiers and ask.

### 2. Read the dossier (in this order, skip silently if missing)

1. `fragmentation-story.md` — **primary source.** Every paragraph of the letter draws from this.
2. `content/content-audit.md` + `_misc/content-analysis-root.md` — asset titles, retail platforms, podcast appearances.
3. `_misc/digital-presence-discovery.md` (and `digital-presence/*`) — verified URLs, social handles, partner publications.
4. `summary.md` — short biographical synthesis, current role.
5. `profile/biography.md`, `profile/calling-profile.md` — narrative arc + vocational hinge.
6. `profile/identity.md`, `profile/theology.md`, `network/organizations.md`, `content/books.md` — structured facts (names, frameworks, orgs, titles). Older `_staff/legacy/<SLUG_UPPER>_*.md` profiles only if a freshly researched leader lacks the categorized files.
7. `_staff/gap-analysis.md`, `_staff/movemental-analysis.md` — useful for the embodied-layer paragraph and the four-moves paragraph.
8. `_staff/identity-verification.md` — confirm display name spelling.
9. The mirror file `…/movemental-visual-editor-main/docs/movement_leader_research/<slug>.md` — cross-check display name + role only.

### 3. Extract the working set

The letter cannot be drafted from the master prompt alone — it needs proper nouns. Before generating prose, pull these from the dossier:

- **First name** (used once, at the open).
- **Current institutional role**, exact wording (load-bearing in MOVE 1 and MOVE 7).
- **Book / major work titles** (will be italicized).
- **Years/scope of teaching or practice** (e.g., "18+ years of college-level teaching").
- **≥ 3 institutional containers** — denominations, colleges, networks, conferences, publishers.
- **≥ 4 specific assets by name** across the letter — book, course, podcast episode (by show name), conference, article series.
- **Retail platforms** for the books (Amazon, Christianbook, publisher direct).
- **Partner publications** where articles appear.
- **Specific podcast episodes by show name** (italicize show name; episode number inline).
- **Named gap** — no newsletter / no hosted podcast / no personal YouTube / no unified hub. Pick the one the dossier actually flags.
- **Institutional CRMs / cohort lists / rosters** where the relational layer lives.
- **Embodied-layer items** — judgment calls behind a specific course, curation of a specific conference, pragmatic wisdom of a specific practice.
- **Primary website URL** (used once in MOVE 6).
- **Specific city** for the closing practitioner in MOVE 6 — pick a city present in the dossier (denomination footprint, conference location, network territory). If none, pick a plausible city from their stated geographic scope and note the choice in the report.
- **The specific group the leader's current role serves** — named explicitly in MOVE 7.

If `--dry-run`, stop here and report the working set as a coverage checklist against the MUST APPEAR list in the master prompt. Do not draft.

### 4. Draft

Follow `references/master-prompt.md` verbatim. Output shape:

- First name on its own line.
- Seven paragraphs of continuous prose, in order, no headers / no bullets / no numbered lists inside the letter.
- `— Movemental` on its own line at the foot.
- Word count **between 1,000 and 1,050** (body only, excluding the standalone first-name opener and the signoff line). Hard ceiling 1,075.

Italicize book, course, and podcast **show** titles with Markdown `*italics*`. Organizations, conferences, and platforms in plain text.

### 5. Self-check before output

Run the master prompt's sanity check + FORBIDDEN list. Revise before output if any check fails.

- Every paragraph contains ≥ 1 proper noun from the dossier.
- Swapping names would not turn this into a generic letter.
- MOVE 4 ends on "authorship stays yours" (or near equivalent).
- MOVE 6 has a real URL and a real city — no placeholders.
- MOVE 7 closes on the absence.
- Body word count in 1,000–1,050.
- No "ecosystem". ≤ 1 occurrence per paragraph of "kingdom" / "multiplication" / "movement" / "apostolic". No "And here's the thing" / "Let me be direct". No revenue-model talk. No "imagine someone discovers you" hypotheticals. No reference to "the dossier" or "our research" inside the letter.

### 6. Output and save

1. Print the letter to chat as continuous Markdown.
2. Unless `--no-save`, write to:

   ```text
   /home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/welcome-letter.md
   ```

   If `--save-to=<path>` is set, write there. If the canonical file already exists, write to `welcome-letter-<YYYY-MM-DD>.md` alongside it — never silently overwrite a prior draft.

### 7. Report back

One short message, no body repetition:

- Slug + display name + current role used.
- Word count of the body.
- Sanity-check pass/fail per item.
- Path the letter was saved to (or "not saved").
- Any MUST-APPEAR items the dossier didn't supply, with the placeholder choice you made (e.g. "no city in dossier; used Kansas City because Sentralized Conference runs there").

Mention `movemental-welcome-letter-publish` as the next step if the operator wants to ship it to the leader's dashboard.

## Why this skill exists in two halves

This skill **drafts** the letter. The companion `movemental-welcome-letter-publish` skill **ships** it to Supabase so the leader actually sees it. The split exists because drafting and publishing want different human review checkpoints — the operator should read the draft (and often edit it) before it goes live in front of the leader. Don't fold the two together; the friction is the feature.
