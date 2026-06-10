---
name: stitch-iterate
description: Refine and edit existing Stitch screens using targeted prompts. Uses edit_screens to adjust content, functionality, or states without regenerating from scratch.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__stitch__edit_screens, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

Iterate on Stitch screens: $ARGUMENTS

$ARGUMENTS should include:
- What to change (e.g., "add a search bar to the library screen", "show empty state for the dashboard", "add user role badges")
- A project ID or project name to identify which project
- Optionally: specific screen IDs to edit
- Optionally: device type override
- Empty — ask the user what they want to refine

## Purpose

This skill edits existing Stitch screens using `edit_screens`. It's for refinement — adjusting content, adding missing functionality, correcting states, or changing what a screen does — without regenerating from scratch.

Use this when:
- A generated screen is missing content or actions
- The screen needs additional states (empty, error, loading)
- Business rules need to be reflected in the screen
- The user wants to add, remove, or change functionality
- Content needs to be more realistic or domain-specific

Do NOT use this for:
- Visual design changes (colors, fonts, spacing) — let Stitch handle those or use `/stitch-variants`
- Complete redesigns — use `/stitch-build` to regenerate instead
- Exploring alternatives — use `/stitch-variants` instead

## Before Starting

1. **Identify the project** — Get the project ID from the user or find it via `list_projects`
2. **List existing screens** — Call `list_screens` to see what's available
3. **Read the target screen(s)** — Call `get_screen` to understand the current state before editing
4. **Understand the change** — What specifically needs to be different? Frame it as content/function, not design.

## Edit Prompt Best Practices

### DO:
- **Be surgical** — Describe exactly what to change, not what to keep the same
- **Focus on content and function** — "Add a notification count to the user's name area" not "add a red badge"
- **Reference what exists** — "The screen currently shows a list of courses. Add a way to filter them by category and difficulty level."
- **Specify new content with examples** — "Add a progress indicator showing how many steps are complete. Example: 'Step 2 of 5 — Payment Details'"
- **Describe new states** — "When the search returns no results, show a message suggesting the user broaden their search terms"

### DON'T:
- **Don't re-describe the entire screen** — Only describe what's changing
- **Don't prescribe design** — No colors, layouts, components, or visual treatment
- **Don't combine unrelated changes** — Make one focused edit at a time for best results
- **Don't contradict the existing screen** — Build on what Stitch already generated

### Edit Prompt Template:
```
[What exists now — one sentence of context].

[What to change]:
- [Specific addition, removal, or modification]
- [Another change if closely related]

[New content/data with realistic examples if applicable].

[New state description if adding a state].
```

### Examples of Good Edit Prompts:
```
The course list currently shows all courses together. Add the ability to filter courses by category (e.g., "Leadership", "Technical Skills", "Communication") and by difficulty level (e.g., "Beginner", "Intermediate", "Advanced"). When filters are active, show which filters are applied and how many results match.
```

```
Add an empty state for when the user has no enrolled courses yet. The message should encourage them to browse the course catalog and include a way to navigate there. Example: "You haven't enrolled in any courses yet. Explore our catalog to find your next learning opportunity."
```

```
The user profile area currently shows just the user's name. Add their role (e.g., "Team Lead"), their organization name (e.g., "Acme Corp"), and the number of courses they've completed (e.g., "12 courses completed").
```

### Examples of Bad Edit Prompts:
```
❌ Make it look more modern and clean
❌ Add a blue sidebar with navigation links
❌ Put a card component with rounded corners showing the user's stats
❌ Rebuild the whole page with a different layout
```

## Execution Steps

### Step 1 — Identify Target
```
Call list_projects → find the project
Call list_screens with projectId → find the screen(s) to edit
Call get_screen → understand current state
```

### Step 2 — Compose Edit Prompt
Write the edit prompt following best practices above. Focus on what's changing, reference what exists.

### Step 3 — Execute Edit
Call `edit_screens` with:
- `projectId`: the project ID
- `selectedScreenIds`: array of screen IDs to edit
- `prompt`: the composed edit prompt
- `deviceType`: match the original screen's device type (or override if the user specifies)
- `modelId`: GEMINI_3_1_PRO (default) or GEMINI_3_FLASH for quick iterations

### Step 4 — Report
```markdown
## Screen Updated: [Screen Name]

**Change:** [1-sentence summary of what changed]
**Screen ID:** [screen ID]
**Project:** [project ID]

Open Stitch to review the visual result.
```

## Iterating on Multiple Screens

When editing multiple screens with the same change (e.g., adding consistent navigation across a flow):

1. **Select all relevant screen IDs** — Pass them all in `selectedScreenIds`
2. **Describe the change as a cross-screen concern** — "All screens in this flow should show the current step number and allow the user to go back to the previous step"
3. **Be explicit about consistency** — "Apply this change consistently across all selected screens"

## Chaining Edits

For complex refinements, chain multiple focused edits rather than one large edit:

1. First edit: Add the new content/functionality
2. Second edit: Add the states (empty, error, loading)
3. Third edit: Refine the placeholder content to be more realistic

Smaller, focused edits produce better results than large, multi-concern edits.

## Anti-Patterns

- **Don't retry immediately** — Edit operations take time. If it times out, check `get_screen` later.
- **Don't re-describe the whole screen** — Stitch already knows what's there. Only describe changes.
- **Don't mix design and function edits** — Keep each edit focused on one concern.
- **Don't use this for exploration** — If you want to try different approaches, use `/stitch-variants` instead.
- **Don't fight Stitch's design choices** — If you don't like the visual approach, generate variants rather than trying to force design changes through content edits.

## Workflow

Part of the Stitch workflow: stitch-build → stitch-iterate → stitch-variants → stitch-export
