---
name: madden-youtube-meta
description: Mine trusted Madden NFL YouTube strategy channels (and paired sites) for competitive meta — formations, plays, adjustments, and pro usage — using transcripts and structured extraction. Use when building playbook notes, meta briefs, or research docs from video sources; pairs with the youtube-transcript skill.
---

# Madden YouTube meta research

Turn **strategy-first** Madden videos into **structured, game-ready notes**: meta snapshot, formations, plays, adjustments, and provenance.

## When to use

- User pastes a YouTube URL or asks “what’s the meta / best plays / what pros run.”
- User wants a **notebook** of schemes from **teaching** channels, not highlight reels.
- User is building content similar to `lab/madden-26/*.md` playbook docs.

## Before you start

1. Read **`references/source-map.md`** in this skill for the curated source tier list and caveats.
2. Confirm **game year** (e.g., Madden 26), **mode** (H2H regs, MUT, Salary Cap), and **patch window** if the user cares about tournament legality.
3. Prefer videos whose titles signal **guides**, **full breakdown**, **complete defense/offense**, **playbook**, or **scheme** over “gameplay” or “pack opening.”

## Workflow

### 1) Ingest the video

- Run **`youtube-transcript`** on the target URL (same repo skill). Save output under something like `lab/madden-26/transcripts/<slug>.md`.
- If captions are missing, say so and fall back to manual notes from the user or another source.

### 2) Extract into a fixed schema

Produce a markdown (or append to an existing research file) with **at least** these sections:

**A. Provenance**

- Channel, video title, URL, upload date (from transcript header).
- Stated credentials (e.g., “MCS,” “belt,” “tournament”) — only if claimed in-video.

**B. Scope**

- Offense / defense / both.
- Playbook(s) and team(s) named in-video.

**C. Meta claims (labeled)**

- Tag each claim: `[verified in video]` vs `[speaker assertion]` vs `[needs patch check]`.
- Separate **“what beats casuals”** from **“what appears in MCS”** if the speaker conflates them.

**D. Formation table**

| Formation (in-game name) | Personnel | Why use it (1 line) | Key plays named | Notes |
|--------------------------|-----------|---------------------|-----------------|-------|

**E. Play cards**

For each play the instructor actually details:

- **Play name** (as in playbook).
- **Setup**: motion, hot routes, blocking RB/TE, line shifts — only what is spoken.
- **Read order**: primary → secondary (progressions).
- **vs coverage**: man, zone, press — as stated.
- **Adjustments**: pre-snap IDs, post-snap coverage rolls — as stated.

**F. Defense (if applicable)**

- Base shell (e.g., 3-3-5, Nickel, 4-3).
- **Coverage** and **match** rules if taught.
- **Blitz** path and **user** responsibility if taught.

**G. Gaps / follow-ups**

- Bullet list of undefined items (“hot route to slot not specified”).
- Suggested next video search queries (formation + “Madden 26” + channel name).

### 3) Meta synthesis (optional but valuable)

If the user wants **meta** (not just one video):

- Pull **2–4** videos from **different** sources in `source-map.md` that share a formation family.
- Build a **consensus** subsection: what repeats vs what conflicts.
- Note **patch sensitivity** (routes, man/zone tuning) explicitly.

### 4) Quality bar

- **No invented play names.** If unclear, mark `[UNCLEAR AUDIO]` or `[NOT NAMED]`.
- Prefer **timestamps** in play cards when the transcript skill preserved them — helps humans re-watch one segment.
- If the video is mostly gameplay with sparse callouts, say **“low extractable density”** and stop early.

## Output location

- Default: user’s active research path (e.g. `lab/madden-26/`) or a new file they specify.
- Do not create unsolicited top-level docs outside the user’s research area unless they ask.

## Related skills

- **`youtube-transcript`** — required for faithful subtitle-based ingestion.
- **`summarize`** — only for quick gist; **not** for playbook extraction (too lossy).
