# Typography & content hierarchy checks

The question this pass answers: **is typography doing real narrative work, or is it decoration?**

A Movemental page earns its editorial voice by letting type structure the argument — not by scattering large, elegant statements across whitespace. "Modern editorial" is a discipline, not a look.

---

## 1. Headline hierarchy

Verify the page uses a **real hierarchy** that mirrors the argument's structure:

- **H1 (Display)** — one per page, carries the thesis or the page's promise.
- **H2** — one per major section, names the **job** of that section.
- **H3** — inside sections, labels sub-arguments or card headings.
- **Eyebrow (ConceptLabel)** — contextualizes the section (category, audience, stage, kind).
- **Body** — explanation, evidence, prose.

**Flag:**

- Multiple H1s (competing theses).
- Sections without a clear H2 — the page becomes a prose drift.
- H3s used where H2s should be (flat hierarchy makes every section feel equal).
- H2 copy that is the same shape three times in a row (see §3 below).

**Rule of thumb:** if you skim only the H2s on the page, the argument should still be legible as a sequence.

---

## 2. Big-statement density (monotony check)

The most common Movemental failure mode: a page delivers its ideas through a **sequence of large statements** with little structural variation.

**Symptom:** three or more consecutive sections shaped like `eyebrow + giant headline + short muted explanation`. The page feels calm, but the reader never gets a change of rhythm — no comparison, no card, no rail, no quote.

**Fix patterns:**

- Break up statement sequences with a **rail** (numbered process, e.g., the AI Stewardship Sequence).
- Insert a **pair or triad** (two equal errors + "the real challenge"; informational + relational).
- Insert a **card grid** (audience cards, Stages, "what must come together").
- Insert a **pull quote** or **bridge** (shorter, different voice, downward visual cue).

**Target ratio:** at most **2 consecutive** "statement sections" before the rhythm changes.

---

## 3. Section-opening variety

If every section opens the same way, the page feels flat.

**Check the sequence of section openings** across the page. A healthy page alternates among:

- Divider rule + eyebrow + H2 (the default)
- Eyebrow only, no rule (visual restart)
- Card grid opening (the rail IS the anchor)
- Two-column "H2 | intro paragraph" split
- Quote-first opening (rare; use sparingly)

**Target:** at least **three distinct opening shapes** across the page. All-default is monotony.

---

## 4. Body copy density and contrast

The explanatory paragraphs beneath big headlines carry more weight than they look. Check:

- **Is body copy too gray?** If `text-muted-foreground` runs the entire explanatory paragraph, the page reads as "low-energy under strong headlines." Promote the **first sentence** to `text-foreground`, or bold the structurally load-bearing clause.
- **Is body copy too long?** Paragraphs over ~4 lines in the explanatory zone dilute the headline's force. Split or trim.
- **Is body copy too dense?** If a paragraph mixes three ideas, separate them.
- **Is body copy too weak?** If the paragraph restates the headline in softer words, cut it.

**Contrast levels — every page should have distinct weights for:**

| Role | Treatment |
| ---- | --------- |
| **Thesis** | H1 or H2 with the strongest typographic weight |
| **Support** | Body text, medium contrast |
| **Evidence** | Inline citation or pull-quote, distinct shape |
| **Explanation** | Muted body, smaller |
| **CTA** | Button, tonal contrast, arrow affordance |

If two of these collapse into the same treatment, the page lacks contrast.

---

## 5. Emphasis discipline (bold, italic, SerifEm)

Emphasis is a **precision instrument**. Every emphasized phrase must earn its emphasis.

**Check:**

- **SerifEm italics** — one per headline max. If two italic phrases appear in the same headline, keep only the structurally load-bearing one.
- **Bold inside body** — use for the **single** structural claim of the paragraph. Two bolds per paragraph = zero bolds.
- **UPPERCASE / eyebrow text** — reserved for labels. Do not use as a stylistic flourish mid-sentence.
- **Color emphasis** — prefer `text-foreground` on `text-muted-foreground` background to create emphasis rather than introducing a new color.

**Red flag:** a page where every section headline italicizes a word. The instrument becomes decoration.

---

## 6. Eyebrow consistency

Eyebrows (small caps labels above headlines) should have a **consistent grammar** across the page:

- All short (2–5 words), all same register.
- Label a **category** or **function**, not a fragment of the headline.
- Do not include verbs or full sentences.

**Examples — strong:** `Orientation` · `Two intelligences` · `Process` · `Why Movemental` · `Grounding`

**Examples — weak:** `How we work` (gerund phrase, vaguer than a noun), `What's next` (question-shaped), `We believe that...` (sentence fragment).

---

## 7. Tonal stacking (DESIGN.md pattern)

Movemental's design charter requires **tonal stacking** — alternating `Section` variants (`default` / `section` / `midnight`) to create perceptual contrast without decorative borders.

**Check:**

- Are two consecutive sections the same variant? That's a monotony risk unless the content calls for it.
- Does the **Midnight** variant appear where the emotional job is weight/urgency or culmination (consequence, movement, final CTA), not where relief/pivot is needed?
- Are there **decorative 1px section borders**? If yes, remove — depth should come from tonal stacking.

---

## 8. Breathing vs. evasion

Movemental pages aim for breathing layout — but there is a difference between **breathing** and **evasive**:

| Breathing | Evasive |
| --------- | ------- |
| Spacing matches density of thought | Large empty space around thin content |
| Reader's eye gets rest between heavy claims | Reader's eye asks "is that all?" |
| Padding scales with section weight | Every section has `py-lg` regardless of content |

**Test:** if a section could be ~20% tighter vertically and feel more purposeful, it is currently evasive.

---

## 9. Hierarchy for proof blocks

When the page includes proof — logos, quantitative claims, testimonials, citations — typography must clearly mark these as **evidence**, not as another body paragraph:

- Quantitative claim → use `.evidence-note` or equivalent L2b pattern with the citation visible.
- Logo strip → distinct container, consistent logo size, muted background.
- Pull quote → serif, large, attribution visible.
- Case study link → card-shaped, clearly a link-out.

**Flag:** a statistic rendered as ordinary body text. Its own weight must set it apart.

---

## 10. Mobile hierarchy (quick check)

Most hierarchy reviews focus on desktop. Do a **mobile pass**:

- Does the H1 still balance (`text-balance`) at ~375px?
- Do two-column grids collapse to a readable stack without losing rhythm?
- Does a triad (three equal items) stack without becoming monotonous vertically?
- Do eyebrows remain legible at smaller sizes?

If mobile feels like "one long scroll of muted body text," the page has too little typographic variation.

---

## Output for Pass 3

Summarize for the output template's **D. Typography & hierarchy score**:

- **What is visually working** — the shapes, contrasts, or rhythms the page gets right.
- **Where hierarchy collapses** — specific sections where the argument's structure is not mirrored by type.
- **Monotony risks** — sequences where rhythm is flat.

Quote specific section names/ids; do not generalize.
