---
name: stitch-export
description: Generate a screen-by-screen feature specification for a Stitch project — documenting what each screen does, its content, user flows, and data requirements. No design or component prescriptions. Output is optimized for Stitch's generate_screen_from_text API.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Export a feature as a Stitch-ready screen specification: $ARGUMENTS

$ARGUMENTS should include:
- The feature, flow, or page set to specify (e.g., "user onboarding flow", "course detail page", "settings dashboard", "checkout experience")
- Optionally: scope constraints ("just the signup screens", "only the main dashboard")
- Optionally: device target ("mobile-first", "desktop", "tablet")
- Optionally: output path for the generated markdown
- Empty — ask the user which feature to export

## Purpose

This skill produces a **screen-by-screen feature specification** — a complete description of *what* each screen does, *what content it contains*, and *how users move between screens*, without prescribing *how it should look* or *what components to use*. The output is structured so each screen spec can be pasted directly into Stitch's `generate_screen_from_text` prompt.

**Include:** Screen purpose, content inventory, user actions, navigation flows, data requirements, business rules, edge cases, empty/error states, placeholder content direction.

**Exclude:** CSS, design tokens, color palettes, component names, animation specs, layout patterns, typography choices, spacing values, visual style direction. Stitch makes those decisions.

## Before Starting

1. Identify the feature's footprint:
   - **Schema tables** — grep for relevant database tables
   - **API routes** — find endpoints the feature calls
   - **Page/component files** — read existing UI to understand current behavior
   - **Config/feature flags** — check for domain context
2. Read relevant documentation for feature narrative context
3. Map the complete user flow — every screen the user touches from entry to completion

## Discovery Strategy

1. **Start from the user journey** — What brings the user here? What do they need to accomplish?
2. **Map every screen** — Each distinct view the user sees is a screen
3. **Identify transitions** — How does the user move between screens?
4. **Find the data** — What information does each screen need to display or collect?
5. **Find the rules** — What business logic governs what the user can see or do?
6. **Find the edges** — What happens when things are empty, broken, or unauthorized?

## Document Structure

Generate a single markdown file with these sections.

### Section 1: Project Overview

```markdown
<project-overview>
# Project: [Project Name]

## What This Is
[2-3 sentences: what the user is trying to accomplish across these screens]

## Who Uses This
[1-2 sentences: the user persona and their context when they arrive]

## Success Criterion
[1 sentence: how you know this feature is working — observable user outcome]

## Screen Map
[List every screen in the flow with a one-line description]
1. [Screen Name] — [what the user sees/does here]
2. [Screen Name] — [what the user sees/does here]
3. ...

## Flow Summary
[Describe the happy-path journey through all screens in narrative form. Include key branching paths.]
</project-overview>
```

### Section 2: Screen Specifications (one per screen)

For EACH screen in the flow, generate a specification block:

```markdown
<screen-spec id="[screen-slug]">
## Screen: [Screen Name]

### Purpose
[1-2 sentences: why this screen exists and what value it delivers to the user]

### What the User Sees
[Describe the content on this screen as a prioritized inventory — most important content first. Describe WHAT information appears, not HOW it's arranged.]

**Primary content:**
- [Most important piece of information or action on this screen]
- [Second most important]

**Supporting content:**
- [Additional context, metadata, secondary information]
- ...

**Actions available:**
- [Primary action: e.g., "Submit enrollment form"]
- [Secondary actions: e.g., "Go back", "Save as draft"]
- [Tertiary actions: e.g., "Skip this step"]

### User Flow
- **Arrives from:** [Previous screen or entry point]
- **Primary path forward:** [What happens when the user completes the main action]
- **Alternative paths:** [Other navigation options — back, skip, branch]
- **Exit points:** [Ways the user can leave this flow]

### Data Requirements
[What data this screen needs to display or collect]

**Displays:**
- [Data field]: [description and source — e.g., "Course title: from course record"]
- ...

**Collects:**
- [Input field]: [what the user provides — e.g., "Email address: required, validated"]
- ...

### Business Rules
- [Rule 1: e.g., "User cannot proceed without accepting terms"]
- [Rule 2: e.g., "Price displays with tax if user's region requires it"]
- ...

### States
- **Loading:** [What the user should understand while data loads]
- **Empty:** [What appears when there is no data — e.g., "No courses enrolled yet"]
- **Error:** [What the user sees if something goes wrong — actionable message]
- **Unauthorized:** [What happens if the user lacks permission]
- **Success:** [Confirmation or feedback after completing the action]

### Placeholder Content
[Direction for realistic placeholder content — domain-specific, not lorem ipsum. E.g., "Course titles should sound like real professional development offerings. Instructor names should be realistic. Prices should reflect plausible tiers."]
</screen-spec>
```

### Section 3: Shared Context

```markdown
<shared-context>
## Domain Vocabulary
- [Term]: [Definition — e.g., "Pathway: A curated learning journey through multiple content types"]
- ...

## Authentication & Authorization
- [Who can access this feature — anonymous, authenticated, specific roles]
- [What changes based on auth state]
- [Tenant/org scoping if applicable]

## Data Model Summary
[Plain-English description of how the key entities relate. E.g., "A Course has many Lessons. Users enroll in Courses, creating an Enrollment that tracks progress."]

## Cross-Screen Rules
- [Rules that apply across multiple screens — e.g., "Navigation always shows current step in multi-step flows"]
- [Consistency requirements — e.g., "User's name appears the same way on every screen"]
- ...
</shared-context>
```

## Execution Steps

### Step 1 — Discover the Feature Footprint
Trace the feature through the codebase: pages → components → API routes → services → schemas. Read every relevant file.

### Step 2 — Map the Screen Flow
Identify every distinct screen the user encounters. Draw the flow: entry → screens → exit. Note all branching paths.

### Step 3 — Draft Screen Specifications
Write each screen spec. Focus on WHAT the user sees and does, never HOW it looks. Prioritize content by importance, not by visual position.

### Step 4 — Write Shared Context
Document vocabulary, auth rules, data relationships, and cross-screen consistency requirements.

### Step 5 — Generate Stitch Prompts
For each screen spec, generate a ready-to-use Stitch prompt (see Stitch Prompt Format below).

### Step 6 — Save and Report
Save the complete document.

## Stitch Prompt Format

For each screen, also generate a **Stitch-ready prompt** — a self-contained text block optimized for `generate_screen_from_text`. This is the prompt that will actually be sent to Stitch.

**Stitch prompt principles:**
- Lead with WHAT the screen is and WHO it's for
- Describe content and functionality, never visual design
- State the information hierarchy — what matters most
- Include the data that should appear (with realistic placeholder values)
- Mention key states (empty, loading, error) inline
- Keep it to one screen per prompt — Stitch works best with focused, single-screen descriptions
- Be specific about what actions are available and what they do
- Mention device target if relevant (desktop/mobile/tablet)
- Do NOT mention colors, fonts, layouts, components, CSS, spacing, or any visual treatment

**Template:**
```markdown
### Stitch Prompt: [Screen Name]

**Device:** [DESKTOP | MOBILE | TABLET | AGNOSTIC]

**Prompt:**
Build a [screen type] for [user persona].

This screen [purpose — what it accomplishes for the user].

The screen displays:
- [Content item 1 with realistic example value]
- [Content item 2 with realistic example value]
- ...

The user can:
- [Action 1 — what it does when activated]
- [Action 2 — what it does when activated]
- ...

[Business rules that affect what appears on screen]

When there is no data to show, [empty state description].
If something goes wrong, [error state description].

Use realistic [domain] content throughout — [specific content direction].
```

## Output Format

```
## Stitch Export: [Feature Name]

### Screens Specified
- [count] screens mapped
- [list screen names]

### Document
Saved to: `_docs/stitch-exports/[feature-slug].md`

### How to Use
1. Create a Stitch project for this feature
2. Use each "Stitch Prompt" section as the prompt for `generate_screen_from_text`
3. Generate one screen at a time — review each before moving to the next
4. Use `edit_screens` with targeted prompts to refine individual screens
5. Use `generate_variants` to explore alternative approaches for key screens

### Recommended Build Order
1. [Screen name] — [why to build this first]
2. [Screen name] — [why next]
3. ...
```

Save to: `_docs/stitch-exports/[feature-slug].md`

Create the directory if it doesn't exist.

## Anti-Patterns

- **Don't prescribe design** — No colors, components, layouts, spacing, typography, or visual style. Stitch handles all design decisions.
- **Don't use implementation language** — No "card component", "sidebar layout", "hero section", "modal dialog". Describe what the user sees and does, not how to build it.
- **Don't combine multiple screens into one prompt** — Stitch generates one screen at a time. Keep prompts focused.
- **Don't use lorem ipsum** — Always specify domain-appropriate realistic content.
- **Don't skip edge cases** — Empty states, error states, loading states, and unauthorized states are critical. Stitch needs to know about them to design for them.
- **Don't over-specify interactions** — Say "the user can filter results by category" not "a dropdown menu with filter options appears in the top-right corner." Let Stitch decide the interaction pattern.
- **Don't forget who the user is** — Every screen prompt should ground Stitch in the user persona and their context.

## Workflow

Part of the Stitch workflow: stitch-build → stitch-iterate → stitch-variants → stitch-export
