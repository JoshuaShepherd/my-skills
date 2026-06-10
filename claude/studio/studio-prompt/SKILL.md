---
name: studio-prompt
description: Generate a complete AI Studio prompt package — System Instructions, Build Prompt, and Iteration Templates — for any UI feature or app. Uses intent-first prompting so AI Studio acts as the expert designer: business goals and mood direction, never hex codes or Tailwind classes.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep
---

Generate a complete AI Studio prompt package for: $ARGUMENTS

$ARGUMENTS should include:
- What you want to build (e.g., "course detail page", "a checkout flow", "an analytics dashboard", "the homepage hero")
- Optionally: business context ("needs to convert visitors to enrolled students")
- Optionally: visual direction ("warm and scholarly", "clean and developer-focused")
- Empty — ask the user what they want to build

---

## When to Use This Skill

- You want to prototype a page, component, or full app in Google AI Studio Build mode
- You need a prompt that gives AI Studio enough direction to produce excellent design without over-constraining it with tokens, classes, or hex codes
- You want a prompt that front-loads business goals so AI Studio makes good design decisions autonomously
- You want the complete three-part prompt package: system instructions + build prompt + iteration templates

---

## Process

### Step 1: Gather Context

Before generating, collect the following. If the user provided them in their message, use what's there. If not, ask in a single message — no more than 5 questions, grouped clearly:

**Required:**
1. **What is being built?** (page, component, feature — be specific)
2. **Business goal:** What does this UI need to accomplish for the platform?
3. **User:** Who uses this, and what context do they arrive with?
4. **Success criterion:** How do you know the design worked? (Observable outcome)

**Optional (ask only if not inferable):**
5. **Visual direction:** Any mood, aesthetic reference, or style preference? (Or: "Let AI Studio decide")
6. **Key sections or content:** What information/sections must appear?
7. **Anything to avoid:** Known anti-patterns, competitor patterns to avoid, specific don'ts?

If the user gives only a rough description (e.g., "a checkout flow" or "the course detail page"), infer what you reasonably can from the platform context and ask only for the gaps.

---

### Step 2: Generate the Prompt Package

Produce three clearly separated sections, formatted for direct copy-paste into AI Studio.

---

## Output Format

```
---
## ✦ SYSTEM INSTRUCTIONS
*Paste once into the "System Instructions" field in AI Studio. Persists for the entire session.*

---
## ✦ BUILD PROMPT
*Paste as your first message in the Build chat.*

---
## ✦ ITERATION TEMPLATES
*Use these as follow-up messages during refinement.*
```

Each section is described in detail below.

---

## Section 1: System Instructions

Write persistent session instructions that define:

1. **The designer/engineer persona** — Who the AI is. Combine engineering precision with aesthetic sensibility. Reference 2-3 real product design cultures as shorthand (Linear, Stripe, Vercel, Notion, Apple, Airbnb, etc.).

2. **The tech stack** — React + TypeScript + Tailwind CSS + shadcn/ui + App Router. Explicit TypeScript props. Mobile-first.

3. **The coding standards:**
   - Semantic HTML always
   - WCAG AA accessibility minimum
   - Tailwind utility classes only — no inline styles, no CSS modules
   - No hardcoded colors — semantic Tailwind conventions
   - All interactive states: hover, focus, active, disabled
   - All data states: loading (skeleton loaders), empty state, error state, success state
   - Animations: only transform and opacity, always respect prefers-reduced-motion
   - No layout shifts on load

4. **The design principles** — 4-5 pithy principles that shape every design decision. Make these specific to the use case and aesthetic direction.

**Example:**
```
You are a principal UI engineer and product designer. Your work reflects the design rigour of Stripe, the developer clarity of Vercel, and the quiet elegance of Notion. You build interfaces that are visually purposeful and technically sound.

Tech stack: React with TypeScript, Tailwind CSS, shadcn/ui components, Next.js App Router. All components have explicit TypeScript prop types. Mobile-first responsive.

Standards:
- Semantic HTML: use article, section, nav, main, header, footer, aside
- WCAG AA minimum — keyboard navigation works, focus states are visible and beautiful
- Tailwind utility classes only — no inline styles, no CSS modules
- No hardcoded colors — semantic Tailwind color conventions throughout
- Every interactive element: hover, focus, active, disabled states all designed
- Every data state designed: skeleton loaders, empty states, error states, success states
- Animations only on transform and opacity, always with prefers-reduced-motion media query
- Zero layout shifts on load

Design principles:
- Whitespace is structure, not emptiness — use it intentionally
- Typography hierarchy carries more meaning than color
- Every state a user can reach is an intentional design decision
- Motion should feel inevitable, not clever
- The best design is the one the user doesn't notice — it just works
```

---

## Section 2: Build Prompt

Structure in this exact order:

### 2.1 Feature Statement
```
Build [feature name + type — e.g., "a course detail page" / "an analytics dashboard" / "a user onboarding flow"].
```

### 2.2 Business Context (lead with the why)
```
**Why this exists:** [Business goal in one sentence — what does this accomplish for the platform?]

**Who uses it:** [User description + their context when they arrive — e.g., "a prospective student arriving from a Google search result, already interested in the topic"]

**Success criterion:** [Observable outcome — e.g., "the user understands the course value and finds the enrollment CTA without scrolling on desktop, within 10 seconds of landing"]
```

### 2.3 Layout Pattern (structural skeleton — be specific, not stylistic)

Name the pattern and describe how sections flow. Use these vocabulary terms:

| Pattern | Description |
|---------|-------------|
| `Hero-centric` | Full-bleed hero, content scrolls beneath |
| `Split composition` | Two-column, copy + visual side by side |
| `Storytelling scroll` | Full-width sections reveal the narrative sequentially |
| `Content hub` | Search/filter bar above a card grid |
| `Bento grid` | Modular card system with varying sizes |
| `Dashboard shell` | Fixed sidebar + header, scrollable main content |
| `Compact utility` | Dense, functional, data-first |
| `Focused form` | Centered, progressive, step-by-step |

Example:
```
**Layout:** Hero-centric. Full-viewport header with headline, subhead, and primary CTA. Below the fold: Storytelling scroll — four full-width sections unfold in sequence: [curriculum overview → instructor credibility → student outcomes → pricing/enrollment]. Sticky enrollment CTA slides in from the bottom edge when the hero scrolls out of view on desktop.
```

### 2.4 Visual Mood (direction without implementation — the most important section)

This is where most prompts fail. Do NOT prescribe:
- Hex codes or CSS color values
- Tailwind class names
- Specific component names
- Pixel values or spacing units

DO use:
- Experiential language ("should feel like...")
- Evocative metaphors ("like stepping into...")
- Product/brand reference anchors ("the density of Linear, the whitespace of Apple")
- Mood vocabulary (see vocabulary tables in the best practices doc)
- Typography personality descriptions

**Template:**
```
**Visual mood:** [Style name/keyword] — [one-sentence experiential description of what it should feel like to use this].

**Reference anchors:** [2-3 evocative quality references — real products or cultural touchstones that signal the design quality and density you want, without prescribing the exact look]

**Color direction:** [Mood vocabulary — e.g., "warm and scholarly", "dark mode excellence", "vibrant and modern" — with a brief emotional rationale]

**Typography:** [Personality description — e.g., "confident display serif for headlines that stops the scroll; friendly humanist sans for body text with generous line height"]
```

**Style vocabulary to draw from (pick what fits):**
- `Warm Academic` — deep warm backgrounds, scholarly depth, bookish richness
- `Linear / Vercel aesthetic` — precise dark mode, developer-centric, subtle borders
- `Editorial` — strong typographic hierarchy, magazine-quality layout
- `Minimalist Luxury` — maximum whitespace, premium restraint, subtle metallic accents
- `Glassmorphism` — frosted layers, translucent depth, modern luminosity
- `Soft UI` — tactile, monochromatic, subtle shadow depth
- `Bento Grid` — modular, information-dense, systematic
- `Aurora UI` — vibrant gradients, luminous, energetic
- `Bold Brutalism` — high contrast, unapologetic, oversized type

### 2.5 Motion & Interaction Intent (natural language only)

```
**Motion:** [How content enters, how cards/elements respond to hover, how the page behaves on scroll, how loading states appear]. Never describe CSS keyframes — describe the feeling and behavior.
```

Example:
```
**Motion:** Content enters the viewport by fading up gently — like a conversation unfolding, not a spotlight turning on. Cards lift with a subtle shadow on hover — a quiet invitation to interact. The sticky enrollment CTA slides in from the bottom edge with a smooth ease — unhurried but purposeful. Loading states use skeleton loaders that match the exact shape of the content they'll reveal.
```

### 2.6 Required Content Sections

List the specific sections/content that MUST appear, without prescribing their exact visual implementation:

```
**Sections to include:**
1. [Section name] — [one sentence on its purpose and what content it must contain]
2. ...
```

### 2.7 Guardrails (what to avoid)

Always include this block. Customize based on the use case, but always keep the standard guardrails:

```
**Avoid:**
- Low-contrast text — every text element must pass WCAG AA contrast
- More than 2 font families on the same page
- Auto-playing carousels, animations, or videos
- Lorem ipsum — use realistic, domain-appropriate placeholder content
- Hamburger menus on desktop viewports
- Hover-dependent interactions with no mobile equivalent
- Layout shifts on load
- Pure black on pure white — too harsh; use near-black and off-white
- Icons without labels or accessible tooltips
- [Any use-case-specific anti-patterns from Step 1]
```

### 2.8 Placeholder Content Direction

```
**Placeholder content:** Use realistic [domain] content throughout. [2-3 sentences describing what domain-specific content should look like — e.g., "Course titles should sound like real theology/leadership courses. Instructor bios should sound like a published author with 20+ years of experience. Student testimonials should feel specific and credible, not generic."]
```

---

## Section 3: Iteration Prompt Templates

Generate 5-8 ready-to-use follow-up prompts tailored to the specific feature being built. Always include these categories:

**1. Aesthetic/visual refinement:**
```
The [section name] feels [too light / too dense / visually flat / overwhelming]. Adjust only the [typography weight / spacing / color depth / border treatment] so it feels [desired quality]. Keep all other sections unchanged.
```

**2. Mobile layout:**
```
On mobile, the [section] isn't working — [describe what's wrong]. Rework only the mobile layout for this section. Keep desktop and all other sections unchanged.
```

**3. Interaction quality:**
```
The [element — e.g., card hover / CTA button / accordion] feels too static. Make the interaction feel [desired quality — e.g., "more alive / more confident / more subtle"]. Change only this element's interaction states.
```

**4. Content replacement:**
```
Replace all placeholder content in [section] with realistic copy for [domain and audience]. Keep the layout, spacing, and all visual styles exactly as they are.
```

**5. Empty/loading states:**
```
Design the loading state for [section] — use skeleton loaders that exactly match the shape of the loaded content. Also design the empty state for when [scenario — e.g., "no courses are enrolled yet"]. Keep all other sections unchanged.
```

**6. Density adjustment:**
```
The overall information density feels [too sparse / too packed]. Adjust the spacing and layout rhythm across the page so it feels [desired quality]. Do not change any colors, typography sizes, or interactive behaviors.
```

**Feature-specific templates** — add 2-3 more based on what makes sense for the specific feature (e.g., for a checkout flow: payment method selector, order summary collapse, form validation states).

---

## Quality Checklist (run before outputting)

Before finalizing the prompt package, verify:

- [ ] Business goal is stated in the build prompt before any design direction
- [ ] No hex codes anywhere in the build prompt
- [ ] No Tailwind class names anywhere in the build prompt
- [ ] No pixel values in the build prompt
- [ ] No specific shadcn component names in the build prompt
- [ ] Visual mood uses experiential language, not technical specs
- [ ] At least 2 reference anchors in the mood section
- [ ] Guardrails section is present
- [ ] Placeholder content direction specifies the domain
- [ ] At least 5 iteration templates generated
- [ ] System instructions include all 4 parts: persona, tech stack, coding standards, design principles

---

## Save the Output

After generating, save to:
```
_docs/studio-prompts/[feature-slug]/PROMPT.md
```

Include the date at the top of the file.

---

## Example Output Stub (abbreviated)

```
---
## ✦ SYSTEM INSTRUCTIONS

You are a principal UI engineer and product designer with the aesthetic precision of Stripe, the developer clarity of Vercel, and the thoughtful depth of Notion...

[Full system instructions block]

---
## ✦ BUILD PROMPT

Build a course detail page.

**Why this exists:** To convert interested visitors into enrolled students by making the course value immediately legible and the enrollment path obvious.

**Who uses it:** A prospective student arriving from a Google search or social referral, already interested in the course topic, evaluating whether this specific course is right for them.

**Success criterion:** The user understands what they'll learn, why this instructor is credible, and what enrollment costs — all without scrolling — and finds the CTA immediately.

**Layout:** Hero-centric...

**Visual mood:** Warm Academic — should feel like stepping into a well-curated independent bookshop at golden hour...

[Full build prompt]

---
## ✦ ITERATION TEMPLATES

**Visual refinement:**
"The hero section feels visually flat — the headline doesn't have enough presence. Increase only the headline's typographic weight and visual contrast so it anchors the page. Keep everything else unchanged."

[Full set of templates]
```
