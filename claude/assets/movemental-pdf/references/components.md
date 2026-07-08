# Movemental PDF Component Library

A catalog of reusable HTML/CSS components. Each component is shown with its HTML, its CSS (copy into the document's `<style>` block, or merge into the starter template's CSS), and a one-paragraph note on when to use it. The full CSS for every component is also pre-wired in `starter.html` so the typical workflow is "copy starter.html, then add the HTML for each component you need."

## Table of contents

1. [Cover](#cover) — title page
2. [Section opener](#section-opener) — page that introduces a major section
3. [Layer page](#layer-page) — numbered section with kicker, title, italic tagline, body, checklist, stakes callout
4. [Brand panel](#brand-panel) — warm-gray panel with left rule (parties block, framework quote, callouts)
5. [Stakes callout](#stakes-callout) — "What is at stake without it" emphasis block
6. [Framework block](#framework-block) — extended indented quote/script in a brand panel
7. [Total card](#total-card) — large-number callout for engagement values, prices
8. [Statistic trio](#statistic-trio) — three-column comparative stat cards
9. [Big statistic solo](#big-statistic-solo) — single-statistic horizontal card
10. [Statistic trio big-number](#statistic-trio-big-number) — three side-by-side big-number cards
11. [Data header](#data-header) — section divider within The Data sections
12. [Checklist](#checklist) — items with hollow-square checkboxes
13. [Bullet list](#bullet-list) — items with small circular markers
14. [Layers overview table](#layers-overview-table) — numbered grid for architecture overviews
15. [Comparison table](#comparison-table) — side-by-side option comparison
16. [Payment / data table](#payment-table) — clean horizontal-rule table
17. [Self-assessment item](#self-assessment-item) — labeled question with interpretation
18. [Pattern block](#pattern-block) — "how to read X" interpretation panel
19. [TOC entries](#toc-entries) — dotted-leader contents listing
20. [Module / appendix grid](#module-grid) — numbered modules with title + meta + description
21. [Stage row](#stage-row) — labeled-process stage (Movemental Path style)
22. [Signature blocks](#signature-blocks) — for MOUs and contracts
23. [Citations list](#citations-list) — numbered bracketed references
24. [Colophon](#colophon) — final-page identification mark
25. [Running header / footer](#running-header-footer) — what goes in the render script

---

## Cover

The first page. Full bleed (no header/footer). Always begins with the wordmark, has a tracked-caps kicker, a large multi-line title in Inter 100/200, an optional subtitle/lede, a thin black rule, and meta at the bottom in a two-column grid or a single line.

```html
<section class="cover">
  <img class="logo" src="logo.png" alt="Movemental">

  <div class="kicker-row">
    Memorandum of Understanding <span class="sep">·</span> Volume One
  </div>

  <h1>It Starts<span class="line2">With Safety.</span></h1>

  <p class="sub">A field guide for building<br>your AI Organizational Guidebook.</p>

  <div class="cover-rule"></div>

  <div class="authors">
    Brad Brisco <span class="sep">·</span> Alan Hirsch <span class="sep">·</span> Joshua Shepherd
  </div>

  <div class="edition">
    <div>Edition 1.1 <span style="opacity:0.5;">·</span> Movemental <span style="opacity:0.5;">·</span> 2026</div>
    <div>movemental.ai</div>
  </div>
</section>
```

For documents without authors (MOUs, proposals), replace `.authors` with a four-cell `.meta` grid (Prepared for / Prepared by / Date / Value). See `starter.html` for the alternate cover variant.

```css
.cover {
  page-break-after: always;
  height: 11in; width: 8.5in;
  padding: 1.0in 1.0in 0.9in 1.0in;
  display: flex; flex-direction: column;
  background: #fff;
}
.cover .logo { width: 2.4in; margin-bottom: 1.0in; }
.cover .kicker-row {
  font-size: 8.5pt; letter-spacing: 0.28em; text-transform: uppercase;
  color: var(--muted); font-weight: 500; margin-bottom: 0.25in;
}
.cover .kicker-row .sep { opacity: 0.5; padding: 0 0.5em; }
.cover h1 {
  font-weight: 100; font-size: 64pt; line-height: 1.0;
  letter-spacing: -0.025em; margin: 0 0 0.05in 0; color: var(--ink);
}
.cover h1 .line2 { display: block; font-weight: 200; margin-top: 0.05in; }
.cover .sub {
  font-weight: 300; font-size: 15pt; line-height: 1.35;
  color: var(--ink-soft); margin: 0.35in 0 0 0; max-width: 5.4in;
}
.cover .cover-rule {
  width: 1.4in; height: 1px; background: var(--ink);
  margin: 0.45in 0;
}
.cover .authors {
  font-weight: 500; font-size: 10pt; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--ink);
}
.cover .authors .sep { color: var(--quiet); padding: 0 0.45em; }
.cover .edition {
  margin-top: auto;
  display: flex; justify-content: space-between; align-items: flex-end;
  padding-top: 0.4in; border-top: 1px solid var(--rule);
  font-size: 9pt; color: var(--muted);
  letter-spacing: 0.14em; text-transform: uppercase; font-weight: 500;
}
```

If the title is short and one-line (e.g., "Annual Report 2026"), drop the `.line2` span and reduce h1 to 52pt. If it's three lines, drop to 44pt.

---

## Section opener

The standard opening of any body section. Tracked-caps kicker, big title in Inter 200, optional lede paragraph, then prose. Each top-level body section is wrapped in `<section class="page">` which forces a new page.

```html
<section class="page">
  <div class="kicker">Authors' Note</div>
  <h2 class="section-title">Where this work comes from, and what we are inviting you into.</h2>
  <p class="lede">AI will mirror and amplify the humanity it finds sitting before it in any given interaction.</p>
  <p>Body prose continues here…</p>
</section>
```

```css
section.page { page-break-before: always; }
section.page:first-of-type { page-break-before: avoid; }

.kicker {
  font-size: 8.5pt; letter-spacing: 0.26em; text-transform: uppercase;
  font-weight: 500; color: var(--muted); margin: 0 0 0.18in 0;
}
h2.section-title {
  font-weight: 200; font-size: 28pt; line-height: 1.1;
  letter-spacing: -0.012em; color: var(--ink);
  margin: 0 0 0.3in 0; max-width: 5.8in;
}
h2.section-title.small { font-size: 22pt; }
.lede {
  font-weight: 300; font-size: 12pt; line-height: 1.5;
  color: var(--ink-soft); margin: 0 0 0.2in 0; max-width: 5.8in;
}
h3.subhead {
  font-weight: 500; font-size: 12pt; color: var(--ink);
  margin: 0.35in 0 0.1in 0; page-break-after: avoid;
}
h4.label {
  font-weight: 600; font-size: 8.5pt; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--ink);
  margin: 0.25in 0 0.08in 0; page-break-after: avoid;
}
```

For long sections that subdivide, use `h3.subhead` for the main subdivisions and `h4.label` for the tracked-caps labels above small paragraphs (used heavily in Process & Roles for "For a church.", "For a nonprofit.", etc.).

---

## Layer page

A specialized section opener for numbered architectural layers (Layer 01 Statement, Layer 02 Policy, etc.). The kicker becomes a tag, the title is rendered slightly smaller than a section title, an italic tagline sits beneath, and a hairline separator marks the start of body content.

```html
<section class="page">
  <div class="layer-tag">Layer 01</div>
  <h2 class="layer-title">AI Organizational Statement.</h2>
  <div class="layer-tagline">What we believe about AI in relation to our mission.</div>
  <p>The Statement is the highest-level layer of your Guidebook…</p>

  <h4 class="label">A complete Statement contains:</h4>
  <ul class="checklist">
    <li>A mission alignment clause…</li>
    <li>A posture statement…</li>
  </ul>

  <div class="stakes">
    <span class="stakes-label">What is at stake without it:</span>
    every layer below reads as arbitrary administrative compliance.
  </div>
</section>
```

```css
.layer-tag {
  font-size: 8.5pt; letter-spacing: 0.26em; text-transform: uppercase;
  font-weight: 500; color: var(--muted); margin: 0 0 0.1in 0;
}
h2.layer-title {
  font-weight: 200; font-size: 26pt; line-height: 1.1;
  letter-spacing: -0.012em; color: var(--ink); margin: 0 0 0.06in 0;
}
.layer-tagline {
  font-style: italic; font-weight: 300; font-size: 11.5pt;
  color: var(--muted); margin: 0 0 0.22in 0;
  border-bottom: 1px solid var(--rule); padding-bottom: 0.16in;
}
```

---

## Brand panel

The most-used emphasis container. Warm-gray background, 2px black left rule, 0.18in padding. Variants below (Stakes Callout, Framework Block, Total Card) are all brand panels with different content patterns.

```html
<div class="panel">
  <div class="panel-label">Movemental</div>
  <div class="panel-body">
    <strong>Movemental, LLC</strong><br>
    Joshua Shepherd<br>
    Founder &amp; Chief Technology Officer
  </div>
</div>
```

```css
.panel {
  padding: 0.2in 0.25in;
  background: var(--bg-panel);
  border-left: 2px solid var(--ink);
  page-break-inside: avoid;
}
.panel-label {
  font-size: 8.5pt; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--muted); font-weight: 500; margin-bottom: 0.08in;
}
.panel-body { font-size: 10pt; line-height: 1.5; }
```

For a two-column parties block (MOU style), wrap two panels in a `.parties` grid:

```html
<div class="parties">
  <div class="panel">…</div>
  <div class="panel">…</div>
</div>
```

```css
.parties { display: grid; grid-template-columns: 1fr 1fr; gap: 0.45in; }
```

---

## Stakes callout

The "What is at stake without it" line at the end of every layer page. A compact brand panel with an inline label.

```html
<div class="stakes">
  <span class="stakes-label">What is at stake without it:</span>
  every layer below reads as arbitrary administrative compliance. The first hard case produces an internal argument with no grounding to settle it.
</div>
```

```css
.stakes {
  margin: 0.18in 0 0.05in 0;
  padding: 0.14in 0.22in;
  background: var(--bg-panel);
  border-left: 2px solid var(--ink);
  font-size: 9.5pt; color: var(--ink-soft);
  page-break-inside: avoid;
}
.stakes-label {
  display: inline; font-weight: 600; color: var(--ink); letter-spacing: 0.04em;
}
```

---

## Framework block

A longer brand panel for extended quotes, scripts, or worked examples. The transparency framework on page 12 of the Field Guide uses this. Multiple paragraphs separated by normal spacing inside the panel.

```html
<div class="framework">
  <p>We are addressing AI Safety in our organization. AI is already affecting our work…</p>
  <p>If we do nothing, specific things become likely…</p>
  <p>We are choosing one specific process. Contributors are [named]. Deciders are [named]…</p>
</div>
```

```css
.framework {
  margin: 0.18in 0;
  padding: 0.22in 0.28in;
  background: var(--bg-panel);
  border-left: 2px solid var(--ink);
  font-size: 10pt; line-height: 1.6; color: var(--ink-soft);
}
.framework p { margin-bottom: 0.55em; }
.framework p:last-child { margin-bottom: 0; }
```

---

## Total card

A larger brand panel built specifically for engagement values, prices, or single-fact highlights. The big number is Inter 200 at 22pt.

```html
<div class="total-card">
  <div class="label">Total engagement value</div>
  <div class="amount">$15,000</div>
  <div class="note">Fifteen thousand dollars, inclusive of all facilitation, platform access, recipe configuration, deliverables, and 30 days of post-engagement asynchronous support.</div>
</div>
```

```css
.total-card {
  margin: 0.1in 0 0.2in 0;
  padding: 0.22in 0.28in;
  border: 1px solid var(--rule);
  border-left: 3px solid var(--ink);
  background: var(--bg-panel);
  display: grid; gap: 0.1in;
  page-break-inside: avoid;
}
.total-card .label {
  font-size: 8.5pt; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--muted); font-weight: 500;
}
.total-card .amount {
  font-size: 22pt; font-weight: 200; letter-spacing: -0.01em;
}
.total-card .note { font-size: 9.5pt; color: var(--ink-soft); }
```

---

## Statistic trio

Three side-by-side cards showing comparative data for three cohorts. Each card has a cohort label, two stats (a "high" stat in `--ink` and a "low" stat in `--quiet`), and a source line. Used for "the capability gap" type comparisons.

```html
<div class="stat-trio">
  <div class="stat-card">
    <div class="cohort">Nonprofits</div>
    <div class="stat-row">
      <div class="stat-pair">
        <div class="big">92<span style="font-size:0.55em;">%</span></div>
        <div class="desc">Use AI in some capacity</div>
      </div>
      <div class="stat-pair">
        <div class="big muted-num">7<span style="font-size:0.55em;">%</span></div>
        <div class="desc">Report major capability gains</div>
      </div>
    </div>
    <div class="stat-source">Virtuous · 2026 · n=346</div>
  </div>
  <!-- Two more .stat-card siblings -->
</div>
```

```css
.stat-trio {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.18in;
  margin: 0.18in 0 0.25in 0;
}
.stat-card {
  padding: 0.18in;
  background: var(--bg-panel);
  border-top: 2px solid var(--ink);
  page-break-inside: avoid;
}
.stat-card .cohort {
  font-size: 7.5pt; letter-spacing: 0.22em; text-transform: uppercase;
  font-weight: 600; color: var(--ink); margin-bottom: 0.14in;
}
.stat-row { display: flex; flex-direction: column; gap: 0.12in; }
.stat-pair { display: flex; align-items: baseline; gap: 0.1in; }
.stat-pair .big {
  font-weight: 200; font-size: 28pt; line-height: 1;
  color: var(--ink); min-width: 1in; letter-spacing: -0.02em;
}
.stat-pair .big.muted-num { color: var(--quiet); }
.stat-pair .desc {
  font-size: 9pt; color: var(--ink-soft); line-height: 1.35; flex: 1;
}
.stat-source {
  margin-top: 0.14in; padding-top: 0.08in;
  border-top: 1px solid var(--rule-faint);
  font-size: 7pt; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--muted); font-weight: 500;
}
```

---

## Big statistic solo

A horizontal card with one big number on the left and explanatory text on the right. Used when a single statistic deserves a full row of attention.

```html
<div class="stat-solo">
  <div class="big-num">43%</div>
  <div class="body">
    of Protestant churchgoers disagree with their pastor using AI for sermon preparation.
    <div class="source">Lifeway Research · 2026 · n=1,200</div>
  </div>
</div>
```

```css
.stat-solo {
  margin: 0.16in 0;
  padding: 0.2in 0.22in;
  background: var(--bg-panel);
  border-top: 2px solid var(--ink);
  display: grid; grid-template-columns: 1.7in 1fr; gap: 0.2in;
  align-items: center;
  page-break-inside: avoid;
}
.stat-solo .big-num {
  font-weight: 200; font-size: 48pt; line-height: 1;
  color: var(--ink); letter-spacing: -0.025em;
}
.stat-solo .body { font-size: 10pt; color: var(--ink-soft); line-height: 1.45; }
.stat-solo .source {
  margin-top: 0.08in;
  font-size: 7pt; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--muted); font-weight: 500;
}
```

---

## Statistic trio big-number

Three side-by-side cards, each with a single big number stacked over a description and a source. Used for "the harm landscape" and "the governance gap" type sections.

```html
<div class="stat-trio-solo">
  <div class="stat-card">
    <div class="big-num">$893M</div>
    <div class="desc">in adjusted losses tied specifically to AI-enabled scams in 2025.</div>
    <div class="source">FBI Internet Crime Report · 2025</div>
  </div>
  <!-- two more .stat-card siblings -->
</div>
```

```css
.stat-trio-solo {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.18in;
  margin: 0.18in 0;
}
.stat-trio-solo .stat-card { padding: 0.2in 0.18in; }
.stat-trio-solo .big-num {
  font-weight: 200; font-size: 38pt; line-height: 1;
  color: var(--ink); margin-bottom: 0.08in; letter-spacing: -0.022em;
}
.stat-trio-solo .desc {
  font-size: 9pt; line-height: 1.4; color: var(--ink-soft); min-height: 1.2in;
}
.stat-trio-solo .source {
  margin-top: 0.1in; padding-top: 0.07in;
  border-top: 1px solid var(--rule-faint);
  font-size: 7pt; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--muted); font-weight: 500;
}
```

---

## Data header

A small section divider used between subsections within The Data (or any data-heavy section). Title + sub on a hairline underline.

```html
<div class="data-header">
  <div class="data-h">The capability gap.</div>
  <div class="data-sub">Across every sector studied, the cohort that turns AI adoption into measurable capability sits between five and seven percent…</div>
</div>
```

```css
.data-header {
  margin: 0.35in 0 0.05in 0;
  padding-bottom: 0.06in;
  border-bottom: 1px solid var(--rule);
  page-break-after: avoid;
}
.data-header .data-h { font-size: 14pt; font-weight: 300; color: var(--ink); margin: 0; }
.data-header .data-sub { font-size: 9pt; color: var(--muted); margin-top: 0.04in; }
```

---

## Checklist

Items with a hollow square checkbox to the left. Used for "A complete X contains:" lists in layer pages. The checkbox is a real bordered element, not a Unicode character — it prints cleanly at any zoom.

```html
<ul class="checklist">
  <li>A mission alignment clause naming the relational and mission commitments AI use must serve rather than displace</li>
  <li>A posture statement naming the organization's stance toward both fear and uncritical enthusiasm about AI</li>
</ul>
```

```css
ul.checklist {
  list-style: none; margin: 0.05in 0 0.2in 0; padding: 0;
}
ul.checklist li {
  position: relative;
  padding: 0.04in 0 0.04in 0.28in;
  margin-bottom: 0.06in;
  line-height: 1.55;
  page-break-inside: avoid;
}
ul.checklist li::before {
  content: "";
  position: absolute; left: 0; top: 0.13in;
  width: 7pt; height: 7pt;
  border: 1px solid var(--ink);
  background: transparent;
}
```

---

## Bullet list

Items with a small circular gray marker. Used for general bulleted lists where checkboxes would be wrong (scope items, deliverables, etc.).

```html
<ul class="bullets">
  <li>A primary point of contact for engagement coordination</li>
  <li>A designated point person for each team</li>
</ul>
```

```css
ul.bullets {
  list-style: none; margin: 0.05in 0 0.2in 0; padding: 0;
}
ul.bullets li {
  position: relative;
  padding: 0.02in 0 0.02in 0.22in;
  margin-bottom: 0.04in;
  line-height: 1.55;
}
ul.bullets li::before {
  content: "";
  position: absolute; left: 0; top: 0.135in;
  width: 4pt; height: 4pt;
  border-radius: 50%;
  background: var(--accent);
}
```

---

## Layers overview table

A numbered architecture grid: thin large number on the left, bold name in middle, description on the right, with horizontal rules between rows. Used for the "five layers of your AI Guidebook" overview and any similar enumerated architecture.

```html
<div class="layers-overview">
  <div class="layer-row">
    <div class="num">01</div>
    <div class="name">Statement</div>
    <div class="desc">What we believe about AI in relation to our mission.</div>
  </div>
  <!-- more .layer-row siblings -->
</div>
```

```css
.layers-overview { margin: 0.2in 0 0 0; }
.layer-row {
  display: grid;
  grid-template-columns: 0.55in 1.7in 1fr;
  align-items: baseline;
  padding: 0.18in 0;
  border-bottom: 1px solid var(--rule);
  page-break-inside: avoid;
}
.layer-row .num {
  font-weight: 200; font-size: 22pt; color: var(--quiet);
  line-height: 1; letter-spacing: -0.01em;
}
.layer-row .name { font-weight: 600; font-size: 12pt; color: var(--ink); }
.layer-row .desc { font-size: 10.5pt; color: var(--ink-soft); line-height: 1.5; }
```

---

## Comparison table

Side-by-side option comparison (SafeGuide vs SafeStart, pricing tiers, etc.). The left column is tracked-caps row labels. Each value column has a bold name + small tracked-caps subtitle in the header. Horizontal rules between rows only.

```html
<table class="compare">
  <thead>
    <tr>
      <th style="width: 1.3in;"></th>
      <th>
        <div class="name">SafeGuide</div>
        <div class="tag">Self-directed</div>
      </th>
      <th>
        <div class="name">SafeStart</div>
        <div class="tag">Facilitated by Movemental</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="rowlabel">Cost</td>
      <td class="col">Free.</td>
      <td class="col">$1,000.</td>
    </tr>
    <!-- more rows -->
  </tbody>
</table>
```

```css
table.compare {
  width: 100%; border-collapse: collapse;
  margin: 0.15in 0; font-size: 9.5pt;
  table-layout: fixed;
}
table.compare thead th {
  text-align: left; vertical-align: bottom;
  padding: 10pt 12pt 12pt 12pt;
  border-bottom: 1px solid var(--ink);
  font-weight: 500; page-break-after: avoid;
}
table.compare thead .name { font-size: 13pt; font-weight: 600; color: var(--ink); margin-bottom: 4pt; }
table.compare thead .tag {
  font-size: 8pt; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--muted); font-weight: 500;
}
table.compare tbody td {
  padding: 10pt 12pt; vertical-align: top;
  border-bottom: 1px solid var(--rule);
  line-height: 1.45; page-break-inside: avoid;
}
table.compare tbody .rowlabel {
  font-size: 8pt; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--muted); font-weight: 600;
  width: 1.3in; padding-right: 14pt;
}
```

---

## Payment table

A simpler horizontal-rule table for payment schedules, line items, or any tabular data with a tracked-caps header row.

```html
<table class="payments">
  <thead>
    <tr>
      <th style="width:55%">Tranche</th>
      <th style="width:15%">Amount</th>
      <th style="width:30%">Due</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tranche 1 — Engagement initiation</td>
      <td class="amount">$7,500</td>
      <td>Net 15 from MOU signing</td>
    </tr>
  </tbody>
</table>
```

```css
table.payments {
  width: 100%; border-collapse: collapse;
  margin: 0.1in 0 0.2in 0; font-size: 10pt;
}
table.payments th, table.payments td {
  text-align: left; padding: 9pt 12pt;
  border-bottom: 1px solid var(--rule); vertical-align: top;
}
table.payments thead th {
  font-weight: 500; font-size: 8.5pt; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--muted);
  border-bottom: 1px solid var(--ink); padding-bottom: 8pt;
}
table.payments td.amount { font-variant-numeric: tabular-nums; }
```

---

## Self-assessment item

A labeled question with a short interpretation paragraph. Used for the five-question self-assessment in the Field Guide. Each item is separated by a top hairline rule.

```html
<div class="assessment-item">
  <div class="tag">Layer 01 — Statement</div>
  <div class="q">Does your board or governing body have a written, ratified position on AI?</div>
  <div class="interp">A strong answer is a signed Statement or equivalent document of record. A weak answer is "we have talked about it."…</div>
</div>
```

```css
.assessment-item {
  margin: 0.18in 0;
  padding: 0.16in 0 0.05in 0;
  border-top: 1px solid var(--rule);
  page-break-inside: avoid;
}
.assessment-item .tag {
  font-size: 8.5pt; letter-spacing: 0.22em; text-transform: uppercase;
  font-weight: 600; color: var(--muted); margin-bottom: 0.08in;
}
.assessment-item .q {
  font-weight: 500; color: var(--ink);
  font-size: 11pt; line-height: 1.45; margin: 0 0 0.08in 0;
}
.assessment-item .interp {
  font-size: 9.5pt; color: var(--ink-soft); line-height: 1.5;
}
```

---

## Pattern block

A brand panel that contains a series of inline-labeled interpretive lines. Used for "how to read your pattern" sections.

```html
<div class="pattern-block">
  <p><span class="label">No to three or more layers.</span>Begin Safety now. Your Guidebook is largely unwritten…</p>
  <p><span class="label">Yes or partial on most layers.</span>Begin Safety this quarter…</p>
  <p><span class="label">Yes on all five.</span>You are likely already in the high-performer cohort…</p>
</div>
```

```css
.pattern-block {
  margin: 0.2in 0 0 0;
  padding: 0.16in 0.22in;
  background: var(--bg-panel);
  border-left: 2px solid var(--ink);
  page-break-inside: avoid;
}
.pattern-block .label {
  font-weight: 600; color: var(--ink); margin-right: 0.5em;
}
.pattern-block p { margin-bottom: 0.45em; }
.pattern-block p:last-child { margin-bottom: 0; }
```

---

## TOC entries

Dotted-leader contents listing. Each entry is a flex row with the section number (optional), label, and right-aligned page number. The dot pattern is implemented as a `border-bottom: 1px dotted` on each entry.

```html
<div class="toc">
  <div class="toc-entry major">
    <span class="toc-num"></span>
    <span class="toc-label">Introduction — Why we begin here</span>
    <span class="toc-page">PG_INTRO</span>
  </div>
  <div class="toc-entry sub">
    <span class="toc-num">01</span>
    <span class="toc-label">AI Organizational Statement</span>
    <span class="toc-page">PG_L1</span>
  </div>
</div>
```

Use `PG_X` placeholders for page numbers and run the TOC two-pass workflow described in SKILL.md. `.major` is for top-level entries; `.sub` is indented for subsections (like the five layers nested under "The five layers of your AI Guidebook").

```css
.toc { margin: 0.05in 0; }
.toc-entry {
  display: flex; align-items: baseline;
  padding: 0.085in 0;
  border-bottom: 1px dotted var(--rule);
  font-size: 10pt;
}
.toc-entry.major { font-weight: 500; color: var(--ink); }
.toc-entry.sub {
  padding-left: 0.32in;
  color: var(--ink-soft); font-size: 9.5pt;
}
.toc-num {
  width: 0.4in;
  font-variant-numeric: tabular-nums;
  color: var(--quiet); font-weight: 500;
  font-size: 8.5pt; letter-spacing: 0.1em;
}
.toc-label { flex: 1; }
.toc-page {
  font-variant-numeric: tabular-nums;
  color: var(--muted); font-weight: 500;
}
```

---

## Module / appendix grid

Used for the appendix in the MOU (eight numbered modules with title + duration + description). A two-column grid: numbered ID on the left, content stack on the right.

```html
<div class="modules">
  <div class="module">
    <div class="id">01</div>
    <div>
      <div class="title">Where We Are — Assessment and Orientation</div>
      <div class="meta-line">60 min</div>
      <div class="desc">Read-back of team assessment, orientation to the Movemental AI Path, introduction to the three deliverables and traffic-light adjudication discipline.</div>
    </div>
  </div>
  <!-- more .module siblings -->
</div>
```

```css
.modules { margin: 0.1in 0 0 0; }
.module {
  display: grid; grid-template-columns: 0.5in 1fr; gap: 0.15in;
  padding: 0.12in 0;
  border-bottom: 1px solid var(--rule-faint);
  page-break-inside: avoid;
}
.module:last-child { border-bottom: none; }
.module .id {
  font-weight: 600; font-size: 14pt;
  color: var(--accent); line-height: 1;
  padding-top: 2pt; font-variant-numeric: tabular-nums;
}
.module .title { font-weight: 600; color: var(--ink); margin-bottom: 0.04in; }
.module .meta-line {
  font-size: 8.5pt; color: var(--muted);
  letter-spacing: 0.04em; margin-bottom: 0.05in;
}
.module .desc { font-size: 10pt; line-height: 1.5; }
```

---

## Stage row

A two-column row with a labeled stage name on the left and a description on the right. Used for the "four-stage Movemental Path" listing on the About page.

```html
<div class="stage">
  <div class="stage-name">Safety</div>
  <div class="stage-desc">What this Field Guide is about. Two weeks, the AI Organizational Guidebook with its five layers. The foundation everything else is built on.</div>
</div>
```

```css
.stage {
  display: grid; grid-template-columns: 1in 1fr; gap: 0.2in;
  padding: 0.18in 0;
  border-bottom: 1px solid var(--rule);
  page-break-inside: avoid;
}
.stage-name {
  font-weight: 600; font-size: 12pt; color: var(--ink);
  letter-spacing: -0.005em;
}
.stage-desc {
  color: var(--ink-soft); font-size: 10pt; line-height: 1.55;
}
```

---

## Signature blocks

A two-column grid of signature lines. Used in MOUs and any document needing physical signatures.

```html
<div class="signatures">
  <div class="sig">
    <div class="label-strong">For Movemental, LLC</div>
    <div class="line"></div>
    <div class="field">Signature</div>
    <div class="line"></div>
    <div class="field">Joshua Shepherd · Founder &amp; Chief Technology Officer</div>
    <div class="line"></div>
    <div class="field">Date</div>
  </div>
  <div class="sig">
    <div class="label-strong">For [Counterparty]</div>
    <div class="line"></div>
    <div class="field">Signature</div>
    <div class="line"></div>
    <div class="field">Name &amp; Title</div>
    <div class="line"></div>
    <div class="field">Date</div>
  </div>
</div>
```

```css
.signatures {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.4in;
  margin-top: 0.25in; page-break-inside: avoid;
}
.sig { border-top: 1px solid var(--ink); padding-top: 0.2in; }
.sig .label-strong { font-weight: 600; font-size: 11pt; margin-bottom: 0.25in; }
.sig .line {
  border-bottom: 1px solid var(--ink-soft);
  height: 0.32in; margin-bottom: 0.04in;
}
.sig .field {
  font-size: 8.5pt; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--muted); font-weight: 500; margin-bottom: 0.18in;
}
```

---

## Citations list

A numbered list with bracketed citation numbers. Each item is separated by a faint hairline. The number is positioned absolutely so the text aligns cleanly.

```html
<ol class="citations">
  <li>Virtuous and Fundraising.AI. <em>The 2026 Nonprofit AI Adoption Report</em>. Released February 16, 2026…</li>
  <li>Barna Group and Pushpay. <em>Technology for Missional Impact: State of Church Tech 2026</em>. Released March 9, 2026…</li>
</ol>
```

```css
ol.citations {
  list-style: none; counter-reset: cite;
  padding: 0; margin: 0;
}
ol.citations li {
  counter-increment: cite;
  position: relative;
  padding: 0.1in 0 0.1in 0.42in;
  border-bottom: 1px solid var(--rule-faint);
  font-size: 9pt; line-height: 1.45;
  page-break-inside: avoid;
}
ol.citations li::before {
  content: "[" counter(cite) "]";
  position: absolute; left: 0; top: 0.12in;
  font-weight: 600; color: var(--ink);
  font-variant-numeric: tabular-nums;
}
```

---

## Colophon

The final page. Centered logo, "Colophon" kicker, title, subtitle, edition/year line, authors line, rights paragraph, URL. Always the last page.

```html
<section class="page">
  <div class="colophon">
    <img class="logo-c" src="logo.png" alt="Movemental">
    <div class="meta-c">Colophon</div>
    <div class="title-c">It Starts With Safety.</div>
    <div class="sub-c">A Field Guide for Building Your AI Organizational Guidebook.</div>
    <div class="meta-c">Edition 1.1 <span style="opacity:0.5;">·</span> Movemental <span style="opacity:0.5;">·</span> 2026</div>
    <div class="authors-c">Brad Brisco <span style="color:var(--quiet);">·</span> Alan Hirsch <span style="color:var(--quiet);">·</span> Joshua Shepherd</div>
    <div class="rights">© 2026 Movemental. This document may be freely shared in its entirety with attribution. For permission to excerpt, contact josh@movemental.ai.</div>
    <div class="url">movemental.ai</div>
  </div>
</section>
```

```css
.colophon { text-align: center; padding-top: 1.5in; }
.colophon .logo-c { width: 1.8in; margin: 0 auto 0.5in auto; display: block; }
.colophon .title-c { font-weight: 300; font-size: 18pt; color: var(--ink); margin-bottom: 0.06in; }
.colophon .sub-c { font-weight: 300; font-size: 11pt; color: var(--ink-soft); margin-bottom: 0.5in; }
.colophon .meta-c {
  font-size: 9pt; color: var(--muted);
  letter-spacing: 0.14em; text-transform: uppercase;
  font-weight: 500; margin-bottom: 0.06in;
}
.colophon .authors-c {
  font-size: 10pt; color: var(--ink); font-weight: 500;
  letter-spacing: 0.1em; margin: 0.05in 0 0.5in 0;
}
.colophon .rights {
  font-size: 8.5pt; color: var(--muted);
  max-width: 4.5in; margin: 0 auto; line-height: 1.55;
}
.colophon .url {
  margin-top: 0.4in; font-size: 10pt; color: var(--ink);
  font-weight: 500; letter-spacing: 0.1em;
}
```

---

## Running header / footer

These live in the render script, not the HTML. The render script (`scripts/render.py`) injects them via Playwright's `header_template` and `footer_template` parameters. The skill's default templates:

**Header** (right-aligned doc title, optional mini-wordmark left):
```
[mini-wordmark]                          DOCUMENT TITLE · DOCUMENT SUBTITLE
```

**Footer** (movemental.ai left, page number right):
```
MOVEMENTAL.AI                                                  Page X
```

To customize header/footer text for a specific document, edit the constants near the top of `render.py` — `HEADER_TITLE` and `FOOTER_LEFT` — rather than passing args. This keeps the render command short and the chrome consistent within each document.

The header reserves 0.75in of top margin; the footer reserves 0.6in of bottom margin. Both are tuned so neither overlaps body content. If a custom header is taller (multi-line, for example), increase `BODY_MARGIN_TOP` in render.py to match.
