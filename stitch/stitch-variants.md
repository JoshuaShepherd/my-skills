---
name: stitch-variants
description: Generate design variants of existing Stitch screens to explore alternative approaches. Controls creative range, aspects to vary, and number of variants.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__stitch__generate_variants, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

Generate variants for Stitch screens: $ARGUMENTS

$ARGUMENTS should include:
- What to explore (e.g., "try different layouts for the dashboard", "explore color alternatives for the landing page", "reimagine the onboarding flow")
- A project ID or project name
- Optionally: specific screen IDs
- Optionally: creative range ("refine", "explore", "reimagine")
- Optionally: aspects to focus on ("layout", "color", "images", "text font", "text content")
- Optionally: number of variants (1-5)
- Empty — ask the user what they want to explore

## Purpose

This skill generates design variants of existing Stitch screens using `generate_variants`. It's for exploration — trying different visual approaches, layouts, or content treatments without committing to a direction.

Use this when:
- The generated screen works functionally but the user wants to see alternatives
- The user wants to explore a different visual direction
- The user wants to compare subtle refinements side by side
- A screen could benefit from a radically different approach

## Creative Range Guide

Help the user choose the right creative range:

| Range | What It Does | When to Use |
|-------|-------------|-------------|
| **REFINE** | Subtle adjustments — keeps the same basic approach but polishes | "I like this direction but it could be better" |
| **EXPLORE** | Meaningful alternatives — same content, different approaches | "Show me other ways this could work" (default) |
| **REIMAGINE** | Radical rethinking — fundamentally different takes | "I want something completely different" |

## Aspect Focus Guide

When the user has a specific concern, focus the variants:

| Aspect | What Varies | When to Use |
|--------|------------|-------------|
| **LAYOUT** | Arrangement of elements, spatial hierarchy | "I want to see different ways to organize this content" |
| **COLOR_SCHEME** | Colors, contrast, visual weight | "I want to explore different color directions" |
| **IMAGES** | Image style, selection, treatment | "I want to see different image approaches" |
| **TEXT_FONT** | Typography, font choices, type hierarchy | "I want to explore different typography" |
| **TEXT_CONTENT** | Copy, messaging, content voice | "I want to try different messaging" |

If no aspects are specified, all aspects may be varied (broader exploration).

## Variant Prompt Best Practices

The prompt for `generate_variants` should describe WHAT DIRECTION to explore, not what the result should look like:

### DO:
- **Describe the intent** — "Explore approaches that emphasize the course content over the instructor details"
- **Reference the user's goal** — "Find a variant that makes the call-to-action more discoverable for first-time visitors"
- **Name what's not working** — "The current version feels too dense for the amount of content — find variants with more breathing room"
- **Be directional** — "Lean toward approaches that prioritize scannability over immersion"

### DON'T:
- **Don't prescribe the solution** — "Make it a two-column layout with the image on the left" defeats the purpose of variants
- **Don't specify design details** — No colors, fonts, components, or CSS
- **Don't be vague** — "Make it better" gives Stitch nothing to work with

### Prompt Template:
```
[What the screen currently does well — one sentence].

Explore variants that [direction — what to optimize for, what feeling to target, what concern to address].

[Optional: what aspect matters most — e.g., "Focus on how the information hierarchy could work differently"]
```

## Execution Steps

### Step 1 — Identify Target
```
Call list_projects → find the project
Call list_screens with projectId → find screens
Call get_screen → review current state of target screen(s)
```

### Step 2 — Determine Variant Parameters
Based on the user's request, decide:
- **Creative range:** REFINE, EXPLORE, or REIMAGINE
- **Aspects:** Which aspects to focus on (or leave empty for full exploration)
- **Count:** Number of variants (default 3, max 5)
- **Prompt:** Directional prompt following best practices

### Step 3 — Generate Variants
Call `generate_variants` with:
- `projectId`: the project ID
- `selectedScreenIds`: array of screen IDs to vary
- `prompt`: the directional prompt
- `variantOptions`:
  - `creativeRange`: selected range
  - `aspects`: selected aspects (array) or empty
  - `variantCount`: number of variants
- `deviceType`: match the original screen's device type
- `modelId`: GEMINI_3_1_PRO (default) or GEMINI_3_FLASH for faster results

### Step 4 — Report
```markdown
## Variants Generated: [Screen Name]

**Direction:** [1-sentence summary of what was explored]
**Creative Range:** [REFINE | EXPLORE | REIMAGINE]
**Aspects:** [focused aspects or "all"]
**Variants:** [count] generated

**Project:** [project ID]
**Source Screen:** [screen ID]

### Next Steps
- Open Stitch to review and compare the variants visually
- Select the preferred variant as your new baseline
- Use `/stitch-iterate` to refine the chosen variant
- Generate additional variants with a different creative range or aspect focus
```

## Common Variant Workflows

### "I like it but it could be better"
- Creative range: REFINE
- Aspects: Leave empty (all)
- Count: 3
- Prompt: "Refine this screen — keep the overall approach but improve the polish and clarity"

### "Show me layout alternatives"
- Creative range: EXPLORE
- Aspects: [LAYOUT]
- Count: 3-4
- Prompt: "Explore different ways to arrange this content. The current layout [what's working or not working about it]."

### "Start over with a different feel"
- Creative range: REIMAGINE
- Aspects: Leave empty (all)
- Count: 3
- Prompt: "Reimagine this screen. The content and functionality should stay the same, but explore fundamentally different approaches to presenting it."

### "The content is right, the visuals aren't"
- Creative range: EXPLORE
- Aspects: [COLOR_SCHEME, TEXT_FONT]
- Count: 4
- Prompt: "Keep the content and layout but explore different visual treatments. The current version [what's not working about the visual direction]."

## Anti-Patterns

- **Don't generate variants of screens you haven't reviewed** — Always `get_screen` first to understand what you're varying.
- **Don't skip the prompt** — Even though variants work without a detailed prompt, a directional prompt produces dramatically better results.
- **Don't generate too many at once** — 3 is the sweet spot. More than 4-5 creates decision fatigue.
- **Don't use REIMAGINE when you mean REFINE** — Radical exploration is expensive and disorienting when you just need polish.
- **Don't prescribe the variant's design** — The whole point is letting Stitch explore. Constrain the intent, not the implementation.
