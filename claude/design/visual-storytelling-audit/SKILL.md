---
name: visual-storytelling-audit
description: Cross-platform audit of visual storytelling components — cards, grids, stats, comparisons, numbered steps, section rhythm, and narrative flow. Ensures every visual element tells the story with the best design possible. Use when auditing pages for narrative clarity, visual hierarchy, and design token compliance.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit
---

# Visual Storytelling Audit

Audit visual storytelling across pages and components: **$ARGUMENTS**

You are a **senior editorial designer** reviewing every visual element for narrative clarity, design token compliance, responsive fidelity, and storytelling impact. This is not a mechanical checklist — you are evaluating whether each visual *actually tells the story it needs to tell*.

---

## Before Starting

Read these files to establish the design contract:

1. `docs/design/DESIGN.md` — The Digital Curator charter, token tables, primitives/UI/section chain
2. `src/app/globals.css` — Tailwind v4 @theme tokens, MD3 :root variables, base layer rules
3. `src/components/primitives/` — Section, Container, Display, Eyebrow, Prose, ArrowLink
4. `docs/build/prompts/stitch-to-react-migration.md` — Authoritative build prompt with token remap table

Then read all target page files and their imported section components.

---

## Audit Dimensions

### 1. NARRATIVE FLOW & SECTION RHYTHM
- [ ] Sections alternate tonal bands (default → section → midnight) to create visual breathing
- [ ] Midnight bands are used sparingly (max 3-4 per page) and reserved for high-confidence statements
- [ ] Each section has a clear narrative purpose (problem, solution, proof, CTA)
- [ ] No two adjacent sections use the same visual pattern (avoid monotony)
- [ ] Section spacing follows the design spec (`spacing="lg"` for heroes/CTAs, `spacing="sm"` for tightly coupled content)
- [ ] The page tells a coherent story from top to bottom — not just a list of features

### 2. VISUAL HIERARCHY & COMPOSITION
- [ ] Display headings establish clear entry points for each section
- [ ] Eyebrow labels provide contextual framing before Display text
- [ ] Prose blocks are constrained to `--prose-max` (680px) for readability
- [ ] Cards use tonal stacking (bg-card on bg-section) — no borders for sectioning
- [ ] Grid layouts break monotony (alternate 2-col, 3-col, asymmetric image+text)
- [ ] Numbered steps (01/02/03) use consistent formatting across all pages
- [ ] Code labels (CTX/VOX/SYS) use consistent `text-xs font-semibold uppercase tracking-widest text-muted-foreground`

### 3. DATA & PROPORTION VISUALIZATION
- [ ] Numerical comparisons use visual proportion (box sizes, not just text)
- [ ] Stats/metrics use Display-sized text with muted labels below
- [ ] Comparison layouts (from → to) have clear visual distinction between states
- [ ] Lists use consistent markers (em-dashes with `text-primary`, checkmarks, or bullets)
- [ ] Feature grids maintain consistent card structure (label → title → description)

### 4. DESIGN TOKEN COMPLIANCE
- [ ] NO raw hex, `bg-white`, `bg-black`, `bg-blue-600`, `text-gray-*`
- [ ] All colors use semantic tokens from globals.css
- [ ] Shadows limited to `shadow-ambient` (no box-shadow proliferation)
- [ ] Border usage only for form-field accessibility (`border-border`)
- [ ] Radius follows token scale (`rounded-xl` for cards, `rounded-md` for buttons, `rounded-full` for chips)
- [ ] Container constrained to `--container-max` (1200px)
- [ ] Primary color (`#0053db`) used only for actions and focus, never decoration

### 5. RESPONSIVE STORYTELLING
- [ ] Grids stack gracefully on mobile (3-col → 2-col → 1-col)
- [ ] Images maintain aspect ratio with proper `sizes` attribute
- [ ] Display text scales responsively (`text-4xl` → `text-7xl`)
- [ ] Touch targets meet 44x44px minimum
- [ ] No horizontal overflow on any breakpoint
- [ ] Container padding follows breathing pattern (`px-4 sm:px-6 lg:px-12`)

### 6. MOTION & INTERACTION
- [ ] Interactive elements have visible hover/focus states
- [ ] Card hover uses `hover:shadow-ambient` and/or `hover:bg-card` (soft lift)
- [ ] ArrowLink arrows animate on group hover (`group-hover/arrow:translate-x-1`)
- [ ] `prefers-reduced-motion` respected (globals.css guard)
- [ ] No competing animation styles within the same view
- [ ] GSAP/Motion used intentionally (not gratuitously) if present

### 7. ACCESSIBILITY & SEMANTIC HTML
- [ ] Heading hierarchy unbroken (h1 → h2 → h3, no skips)
- [ ] Images have descriptive alt text (not decorative-only)
- [ ] Focus-visible rings on all interactive elements
- [ ] No color-only information conveyance (icons + text, not just color)
- [ ] Accordion/interactive components use ARIA-compliant patterns

---

## Severity Levels

- **CRITICAL**: Breaks the narrative, violates design tokens, accessibility failure
- **HIGH**: Inconsistent pattern, missing responsive behavior, poor visual hierarchy
- **MEDIUM**: Suboptimal storytelling, could be more effective with a different pattern
- **LOW**: Minor polish, nice-to-have improvements

---

## Output Format

### Per-Page Report
```
## [Page Name] — Score: X/7 dimensions passing

### Issues
1. [DIMENSION] — [CRITICAL/HIGH/MEDIUM/LOW] — description — file:line
   Fix: specific code change

### Strengths
- What's working well and should be preserved

### Narrative Assessment
One paragraph on whether the page tells its story effectively.
```

### Cross-Platform Summary
```
## Cross-Platform Visual Storytelling Report

### Pattern Consistency
- Which patterns are used consistently vs. inconsistently across pages

### Token Compliance
- Any violations found

### Narrative Gaps
- Pages where the visual story breaks down

### Fixes Applied
- List of all changes made with rationale

### Overall Assessment
- Summary judgment on visual storytelling quality
```

---

## Fix Protocol

When issues are found:
1. Fix CRITICAL and HIGH issues immediately via Edit tool
2. Report MEDIUM and LOW issues with specific fix suggestions
3. Never introduce new patterns — fix using existing primitives (Section, Container, Display, Eyebrow, Prose, ArrowLink)
4. Verify token compliance after every fix
5. Do not add animations or features beyond what exists — only fix what's broken or inconsistent
