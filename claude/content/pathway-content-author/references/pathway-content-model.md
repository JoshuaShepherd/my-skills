# Reference — The Pathway Content Model

What each of the twelve canonical sections must contain, the pedagogy that runs through them,
and the completeness rules. This is the content contract; the full platform spec is
`pathway-page-canonical-spec.md` in the repo. Read this whole file before writing sections.

## Contents
- The twelve sections (what each must contain)
- The four pedagogical necessities (and where each is discharged)
- Completeness rules (the four sections people shortchange)
- Citation requirement
- Length and shape

---

## The twelve sections — what each must contain

The pathway is twelve sections, in this order, grouped **Understand → Examine → Apply → Go
deeper**. Write all twelve; never reorder; never drop one.

**Understand**
1. **Hero / provocation.** Opens with the reframing question. Names what is at stake. Voice at
   its highest. This is the page's quotable opening — it must unsettle a reduced assumption, not
   merely introduce a topic.
2. **Overview.** What this pathway is, what it asks of the reader, and what the reader will be
   able to see or do at the end. Include the *recovery* framing — what the pathway helps the
   reader recover or reclaim (this is where a "recover" parameter, if the theme has one, lives).
3. **The model / framework.** The substantive framework the pathway is built around, drawn from
   the companion pillar and the author's corpus, in the author's own terms.

**Examine**
4. **The scripture thread.** The biblical material that grounds the pathway's claims. Substantive
   engagement in the author's register — woven, not proof-texted.
5. **The historical context.** Why this matters at this cultural moment; specific historical
   parallels the author actually uses.
6. **The cases.** **Plural.** Concrete narrative witnesses — people, communities, movements that
   have walked something like this path. A single case fails this section. Tell them as the
   author tells them.

**Apply**
7. **The practices.** What the reader is invited to *do* — specific, embodied, time-bounded. Not
   "consider this." This discharges the *action* necessity.
8. **The curated resources.** Pointers into the corpus, the companion pillar/cluster articles,
   the companion course (when live), and vetted external material. Mostly structural; voice only
   in the framing line.
9. **The AI Lab.** A short, in-voice invitation into conversation with the pathway's agent, tuned
   to hold the reframing question without resolving it. **Required** — never omitted.

**Go deeper**
10. **FAQs.** The questions a reader asks at *this* point in the pathway, answered substantively.
    Questions plain; answers in voice. Feeds FAQ schema downstream.
11. **Distortion warnings.** **Required.** What this pathway is *not* — the cheap, reduced, or
    misleading versions the reader will meet elsewhere. Use the author's own language for
    reduction/domestication where the corpus provides it.
12. **Invitation.** The single concrete next step: pathway→course, pathway→cohort, or
    pathway→deeper-pathway. Names a *specific* next move. Discharges the *community* necessity.

---

## The four pedagogical necessities

Every pathway must carry all four **in strong form**. An absent reflection structure is a
*failure*, not a weakness. Map them onto the sections as you write:

| Necessity | Carried by | Bar |
|-----------|------------|-----|
| **Dissonance** | Hero (1), Model (3), Distortions (11) | Some passage unsettles the reader's current frame |
| **Action** | Practices (7) | Specific, embodied, time-bounded |
| **Reflection** | A structured reflection-questions block (attach to Practices, or as its own block after it) | Structured questions the reader works through. A vague "journal on this" is *weak*; absence is *failure* |
| **Community** | Invitation (12) | Concrete — a *named* cohort or a *named* practice partnership, not "find someone to talk to" |

The reflection block is the one most often missing from a content draft. Include it explicitly,
as 3–6 questions that make the reader process what the practices surfaced.

---

## Completeness rules — the four that get shortchanged

Before output, confirm each of these. They are the sections a fast draft tends to thin out:

1. **Cases are plural** (section 6). At least two distinct witnesses.
2. **Distortion warnings present** (section 11). At least two named distortions.
3. **AI Lab invitation present** (section 9).
4. **Invitation is concrete** (section 12). One specific next step, named.

A draft missing any of these is incomplete and will fail `pathway-audit`. Do not deliver it.

---

## Citation requirement

Every **substantive** section (1–7, 11 especially) cites **≥3 corpus sources**. Use inline
footnote markers (`[^1]`, `[^2]`, …) and collect them in the citations block at the end of the
template, one entry per marker, mirroring the footnotes-registry schema: `claim`, `source` (book
chapter / talk / interview / article), `page` (where available), `type`. Curated resources (8)
and FAQs (10) cite where they make a substantive claim. The AI Lab (9) and the bare invitation
(12) need not cite. Every marker must resolve to an entry; no orphan markers, no invented
sources. See `corpus-gathering.md` for how to produce these.

---

## Length and shape

Pathways are long-form formation products, not articles. As a guide: hero tight and sharp;
overview and model substantial; examine sections full; practices concrete and enumerated;
distortions pointed; invitation short and decisive. Favor the author's natural section rhythm
over a fixed word count. When in doubt, depth over breadth — a pathway earns its length by taking
the reader somewhere, not by padding sections.
