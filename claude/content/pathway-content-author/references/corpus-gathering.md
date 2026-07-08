# Reference — Corpus Gathering

The standard, repeatable way to find and cite the author's own material for a pathway, from the
repo. The rule above all: **gather before you write, and never write a position the author has
not taken.**

## Where the material lives

Two sources, used together:

- **The books corpus** — the author's ingested books (processed to MDX/markdown). This is the
  primary source for frameworks, scripture engagement, historical examples, stories/cases,
  practices, and the author's own naming of distortions. Look under the books repo / corpus
  location for this author (e.g. a per-book directory or `corpus/books/<slug>`).
- **`movement_leader_research/<author>/`** (or the cleaned `dashboard-content/`) — the research
  dossier: bibliography (what books exist and what they cover), theological and vocational
  profile, content analysis, and the voice files. Use this to (a) choose the right primary corpus
  for the theme and (b) confirm the author's framework names and positions before you cite them.

Find these with `Glob`/`Grep` rather than assuming paths — repos vary per author.

## Step A — Choose the primary corpus for the theme

From the bibliography and content analysis in the research dossier, pick the **one or two books**
that most directly carry the theme. Match on the theme's keywords and the author's framework
names. Confirm with the user if the choice is not obvious. Record the choice as `primary_corpus`.

## Step B — Gather per section

Each canonical section needs a particular *kind* of corpus material. Gather it section by section
so you never write an ungrounded section:

| Section | What to find in the corpus |
|---------|----------------------------|
| Hero / provocation | The author's sharpest framing of the problem or tension — often a book's opening, a diagnosis, a provocative reframe |
| Overview + recovery | The author's statement of what is at stake and what is to be recovered/reclaimed |
| Model / framework | The framework's primary source chapter(s); the author's own definitions |
| Scripture thread | Passages where the author engages the biblical material for this theme |
| Historical context | The author's historical parallels and the data they cite |
| Cases (plural) | The author's narrative witnesses — named people, communities, movements, with authentic detail |
| Practices | The author's embodied invitations / practice material / "what to do" passages |
| Curated resources | The bibliography entries, companion pillar/cluster articles, companion course |
| Distortions | Where the author names cheap, reduced, domesticated, or counterfeit versions |
| FAQs | Recurring questions the author addresses about this theme |

If a section's corpus is thin, narrow that section honestly rather than padding it from outside
the author's work. Note the narrowing in the output.

## Step C — Extract with citations

For every fact, framework, story, example, or practice you carry into a section, capture a
citation as you go:

- `claim` — the substantive content being cited (in your words or a short, properly attributed
  quote)
- `source` — the corpus item: book + chapter (preferred), or talk / interview / article
- `page` — where available
- `type` — book / talk / interview / article / external

These become the citations block (see the template). Each maps cleanly to a footnotes-registry
entry (`src/lib/citations/<author>-claims.json`) when `pathway-author` runs later.

**Quotation discipline.** Prefer paraphrase in the author's own register over long quotation.
Keep any direct quote short and attributed. The goal is the author's *thinking and voice*, carried
faithfully — not blocks of transcribed text.

## Step D — The grounding gate

Before writing, confirm you have, for this theme, from this author's corpus: the framework, at
least one scripture engagement, at least one historical parallel, **at least two cases**, at
least one set of practices, and **at least two named distortions**. If any is missing from the
corpus, surface it to the user — that gap may mean a different primary corpus, or a narrower
pathway, but it never means inventing the missing material.
