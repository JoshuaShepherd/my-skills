---
name: app-architect
description: Generate a full architectural documentation package for any app, project, or feature — a _PURPOSE.md narrative plus individual page-level specs, navigation, and cross-cutting concerns. Outputs to _docs/ai-studio/ for use in AI Studio or any prototyping tool.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Generate an architectural documentation package for: $ARGUMENTS

$ARGUMENTS should include:
- A description of the app, project, page, or feature to architect
- Optionally: the intended audience or user base
- Optionally: key flows or interactions to emphasize
- Optionally: a project slug for the output directory name
- Empty — ask the user to describe what they want to build

## Purpose

This skill produces a **complete architectural documentation package** — a set of markdown files that fully explain what a project is, what each page must accomplish, and how the pieces connect. The output is designed so that both a human collaborator and an AI prototyping tool (Google AI Studio, Claude, Cursor, etc.) can read the docs and understand the entire project without ambiguity.

**This is not a coding prompt.** It does not prescribe components, frameworks, styling, or implementation details. It describes *what* each surface needs to do and *why* — clearly enough that any competent builder could implement it in any stack.

**What it produces:**
- A project directory under `_docs/ai-studio/[project-slug]/`
- `_PURPOSE.md` — the overall narrative: what this thing is, who it's for, and why it exists
- One markdown file per page (e.g., `home.md`, `dashboard.md`, `settings.md`)
- `_NAVIGATION.md` — navigation structure and routing logic
- `_CROSS_CUTTING.md` — shared concerns that span multiple pages (auth, notifications, state, etc.)

## Elicitation — Before Generating

If the user's description is brief or ambiguous, ask **up to 3 targeted questions** to fill critical gaps. Do NOT ask all three if the description already provides enough context.

1. **Who uses this?** — What are the user roles or personas? What are they trying to accomplish?
2. **What's the core loop?** — What is the primary action a user takes repeatedly? What does success look like?
3. **What are the boundaries?** — Is this a standalone app, a feature within a larger platform, a marketing site, a tool? What's in scope and what's not?

If the user gives a detailed brief, skip straight to generation. Bias toward action — don't over-interview.

## Thinking Process

Before writing any files, work through this analysis internally:

1. **Identify the core purpose** — In one sentence, what does this project exist to do?
2. **Map the user roles** — Who interacts with this, and what does each role need?
3. **Derive the pages** — What distinct screens or views are required to fulfill the purpose? Don't invent pages for the sake of it — only include what's necessary.
4. **Trace the flows** — How does a user move through the pages? What's the happy path? What are the key decision points?
5. **Identify cross-cutting concerns** — What behaviors span multiple pages? (auth, navigation, search, notifications, data persistence, error handling, etc.)
6. **Name the project** — Derive a slug from the description (e.g., "course marketplace" → `course-marketplace`)

## File Specifications

### _PURPOSE.md

The overall project narrative. Written in clear, confident prose — not bullet points, not user stories, not technical specs. This document should read like a product brief that makes anyone who reads it understand *exactly* what this thing is.

Structure:

```markdown
# [Project Name]

## What This Is
[2-4 paragraphs of narrative prose. Explain the project as if you're telling a smart colleague about it over coffee. What problem does it solve? Who is it for? What does the experience feel like? What makes it distinct from alternatives?]

## Who It Serves
[For each user role or persona: who they are, what they need, and what success looks like for them. Written as prose, not a list of user stories.]

## The Core Experience
[Describe the primary flow — what a user does from first arrival to achieving their goal. Walk through it narratively, not as numbered steps. Convey the *feel* of using the product.]

## What Success Looks Like
[How would you know this project is working? What are the observable outcomes — not metrics, but behaviors and experiences that indicate the product is fulfilling its purpose?]

## Scope & Boundaries
[What is explicitly in scope. What is explicitly out of scope. What might be added later but is not part of this version.]

## Pages Overview
| Page | File | Purpose |
|------|------|---------|
| [Page name] | `[filename].md` | [One-line purpose] |
| ... | ... | ... |
```

**Rules for _PURPOSE.md:**
- Write in narrative prose, not bullet lists or user stories
- Be specific enough that a builder could make architectural decisions from this alone
- Don't describe UI — describe *what the user needs to accomplish*
- Don't prescribe technology — describe *what the system needs to do*
- Include enough domain context that someone unfamiliar with the space could understand the project

### Individual Page Files ([page-name].md)

One file per page. Each file is a complete specification of what that page must accomplish.

Structure:

```markdown
# [Page Name]

## Role in the Project
[1-2 sentences: where this page sits in the overall hierarchy and flow. What comes before it? What comes after? Why does it exist as a distinct page rather than part of another?]

## What This Page Must Accomplish
[2-3 paragraphs of narrative prose describing what the page needs to do. Not wireframe instructions — describe the *job* of the page. What question does the user arrive with? What state should they leave in?]

## User Arrives With
- [What context, intent, or state the user brings to this page]
- [What they've already done or seen before getting here]
- [What they expect to find]

## User Leaves With
- [What the user should know, have done, or feel after this page]
- [What action they're ready to take next]
- [What decision they've made]

## Key Content & Information
[What information must be present on this page for it to succeed. Not layout — content. What does the user need to see, read, or interact with?]

## Interactions & Behaviors
[What can the user *do* on this page? What are the key actions, and what happens when they take them? Include the happy path and meaningful edge cases.]

## States
- **Loading**: [What the user sees while data loads]
- **Empty**: [What the user sees when there's no data yet]
- **Error**: [What the user sees when something goes wrong]
- **Authenticated vs. Anonymous**: [How the page differs based on auth state, if applicable]

## Connections
- **Navigates to**: [What pages this page links to or redirects to]
- **Navigated from**: [What pages typically lead here]
- **Data dependencies**: [What data this page needs, described conceptually — not API endpoints]
```

**Rules for page files:**
- One file per page, no exceptions
- Name files with lowercase kebab-case matching the page name (e.g., `course-detail.md`, `user-profile.md`)
- Focus on *what* and *why*, never *how*
- Describe content requirements, not layout
- Describe behaviors, not components
- Include states (loading, empty, error) — these are often where products fail
- Always describe what the user arrives with and leaves with — this forces clarity about the page's actual job

### _NAVIGATION.md

How users move through the project.

Structure:

```markdown
# Navigation & Routing

## Navigation Model
[Describe the overall navigation pattern. Is it a top nav? Sidebar? Tab bar? Breadcrumb-driven? Context-dependent? Why was this model chosen for this type of project?]

## Primary Navigation
[The main navigation items — what's always visible or accessible. For each item: where it goes and why it's in the primary nav.]

## Secondary Navigation
[Any sub-navigation, contextual navigation, or in-page navigation. Breadcrumbs, tabs within pages, sidebar sections, etc.]

## Routing Logic
[How does the URL structure map to the pages? Are there dynamic segments? Protected routes? Redirects? Describe the routing tree conceptually.]

## Navigation State
[Does the nav change based on context? Auth state? Current section? Active page? Describe how navigation responds to state.]

## Key Flows
[Describe 2-4 critical user flows as sequences of page transitions. E.g., "Discovery → Detail → Enrollment → Dashboard". Show the path, not the UI.]
```

### _CROSS_CUTTING.md

Shared concerns that span multiple pages and wouldn't be fully covered in any single page file.

Structure:

```markdown
# Cross-Cutting Concerns

## Authentication & Authorization
[Who can access what? How does auth state affect the experience? What's the auth flow?]

## Data & State Management
[What data is shared across pages? What state persists across navigation? What's ephemeral?]

## Search & Discovery
[If applicable: how do users find things? Is there global search? Filtering? Sorting?]

## Notifications & Feedback
[How does the system communicate with the user? Toasts, alerts, email, empty states, success confirmations?]

## Error Handling
[How are errors surfaced? Is there a global error boundary? How do individual page errors differ from system-level errors?]

## Responsive Behavior
[High-level responsive expectations — not breakpoints, but behavioral expectations. Does the mobile experience differ in flow or just in layout?]

## Accessibility
[Key accessibility requirements for this project — not a generic checklist, but specific concerns given the content type and audience.]

## [Any Other Relevant Concern]
[Add sections for anything else that spans pages: real-time features, offline support, internationalization, analytics events, etc. Only include what's relevant to this project.]
```

## Execution Steps

### Step 1 — Understand the Project
Read the user's description carefully. If it references existing code, read the relevant files. If it references an external product, use what you know. If it's a new concept, work from the description.

### Step 2 — Derive the Architecture
Identify: purpose, users, pages, flows, and cross-cutting concerns. Don't invent complexity — only include pages and concerns that are genuinely required.

### Step 3 — Create the Directory
Create `_docs/ai-studio/[project-slug]/` if it doesn't exist.

### Step 4 — Write _PURPOSE.md First
This is the anchor document. Everything else must be consistent with it.

### Step 5 — Write Page Files
One file per page, in order of importance to the user flow. Start with the most critical page.

### Step 6 — Write _NAVIGATION.md
Describe how the pages connect. This often reveals missing pages or unnecessary ones — adjust accordingly.

### Step 7 — Write _CROSS_CUTTING.md
Cover everything that spans pages. Only include sections relevant to this project.

### Step 8 — Report
Summarize what was created.

## Output Summary

After generating all files, output:

```
## App Architecture: [Project Name]

### Files Created
- `_docs/ai-studio/[slug]/_PURPOSE.md` — Overall project narrative
- `_docs/ai-studio/[slug]/[page-1].md` — [One-line purpose]
- `_docs/ai-studio/[slug]/[page-2].md` — [One-line purpose]
- ...
- `_docs/ai-studio/[slug]/_NAVIGATION.md` — Navigation and routing
- `_docs/ai-studio/[slug]/_CROSS_CUTTING.md` — Shared concerns

### Architecture Summary
- Pages: [count]
- User roles: [list]
- Core flow: [one-sentence description of the primary user journey]

### How to Use
1. Start with `_PURPOSE.md` to understand the full project
2. Read page files in flow order to understand the user journey
3. Reference `_NAVIGATION.md` for routing and page connections
4. Reference `_CROSS_CUTTING.md` for shared behaviors
5. Paste any or all files into AI Studio / Claude / Cursor as context for building
```

## Anti-Patterns

- **Don't prescribe UI.** No wireframes, no layout descriptions, no "put a button here." Describe what the page must accomplish, not how it should look.
- **Don't prescribe technology.** No framework names, no component libraries, no API patterns. Describe what the system must do.
- **Don't over-page.** A settings page with 3 fields doesn't need its own file if it's a modal or tab within another page. Only create page files for genuinely distinct screens.
- **Don't under-specify states.** Every page has loading, empty, and error states. Document them — they're where most products break.
- **Don't write user stories.** Write narrative prose. "As a user I want to..." is less useful than a clear paragraph explaining what the page needs to do and why.
- **Don't be generic.** Every sentence should be specific to *this* project. If a sentence could apply to any project, it's not useful.
- **Don't include implementation hints.** No "use React Query for data fetching" or "this should be a server component." The architecture is stack-agnostic.
- **Don't skip the connections.** Every page file must describe what the user arrives with and leaves with. This is what makes the architecture a *system* rather than a collection of pages.
