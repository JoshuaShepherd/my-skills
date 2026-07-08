# Reference — Voice Application

How to load *any* author's documented voice from the repo and apply it to pathway content. The
skill is general; the voice is specific. This file tells you where to find the voice, how to turn
it into a working profile, and how to apply and check it.

## Where an author's voice is documented (priority order)

Look in this order; use the first that exists, and corroborate with the others:

1. **A dedicated voice skill** — e.g. `alan-voice` (`.claude/skills/<author>-voice/SKILL.md` or
   the user skills directory). If one exists for this author, it is authoritative: it carries the
   markers, anti-patterns, posture, and checklist. Use it directly.
2. **`dashboard-content/` Part III — Voice & Editorial Identity** — the cleaned voice files:
   Voice Analysis, Voice Identity, Editorial Bio. Authoritative when no voice skill exists.
3. **`movement_leader_research/<author>/` voice files** — the raw voice analysis / voice identity
   / writing-characteristics / vocabulary files. Use these when the dossier has not been cleaned
   yet.

Find them with `Glob`/`Grep` (`*voice*`, `*Voice Identity*`, etc.). If none exists, **stop** and
tell the user — do not write in a guessed voice.

## Build a working voice profile

From whichever source you found, extract a short profile you can hold while writing:

- **Markers** — the recurring features that make the writing *this author's*: characteristic
  vocabulary and framework terms, sentence rhythm, metaphor systems, the proportion of "we / you /
  I", question density, how scripture and history enter the prose.
- **Signature moves** — how the author opens, builds an argument, and lands. (Many authors have a
  named reasoning pattern in their voice docs; use it.)
- **Rhetorical posture** — where the author speaks *from* (e.g. from ahead, alongside, as
  diagnostician), and the balance of pastoral warmth and prophetic challenge.
- **Anti-patterns** — what the author must never sound like. Capture the author-specific ones from
  the voice docs, plus the universal ones below.

Keep the profile short enough to keep in view for every section.

## Universal anti-patterns (every author)

Regardless of author, pathway prose must avoid:

- **Corporate-consultant register** — "leverage", "optimize", "best practices", "scalable",
  "unlock", "drive outcomes".
- **Detached-academic register** — "research indicates", "it could be argued that", "the
  implications suggest".
- **AI cadence** — the giveaway rhythms of generated prose: mechanical tricolons, "it's not just
  X, it's Y" escalations, hollow summarizing transitions, uniform sentence length.
- **Generic motivational filler** — "you've got this", "believe in yourself".
- **Rushing to practice before understanding** — unless the author's own voice explicitly leads
  with action, do not stack "5 steps" before meaning and grounding are established.

Some authors prohibit specific structures (for example, Alan Hirsch prohibits the antithesis
"not X, but Y" and requires Christocentric anchoring). **Always defer to the author's own voice
documentation for these author-specific rules** — they override any generic default here.

## Apply voice in proportion to the section

Voice is not uniform across the page. Apply it heaviest where the prose is generative and the
author's thinking is on display; lighten it where the section is structural. Use the intensity
table in `SKILL.md`. In short: hero, practices, and invitation peak; curated resources, FAQ
scaffolding, and the AI Lab invitation stay light and plain.

## Check voice before delivering

For each voice-forward section, confirm: the author's markers are present at roughly their
documented density; the signature posture is recognizable; none of the author-specific or
universal anti-patterns appears; and it reads as *this* author and not a neighbor. If a dedicated
voice skill exists with a scoring checklist, run that checklist. Where it falls short, revise the
section — do not ship a pathway that is correct in fact but wrong in voice.
