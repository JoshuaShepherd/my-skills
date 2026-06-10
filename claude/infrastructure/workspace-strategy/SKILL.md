---
name: workspace-strategy
description: "Strategic planning for the workspace doc system — content roadmaps, agentic workflow design, context coding architecture, research priorities, and reflection. Use when deciding what to build, write, or research next in docs/workspace/."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch, TodoWrite
---

Strategize about workspace documents: $ARGUMENTS

$ARGUMENTS should be one of:
- "roadmap" — Generate a content roadmap based on gaps and priorities
- "agentic" — Design agentic workflows for the workspace system
- "context" — Plan context coding architecture for docs
- "research" — Identify research priorities and plan investigations
- "reflect" — Reflect on current state, progress, and direction
- A specific question or topic — Answer strategically
- Empty — Ask the user what they want to think through

## Context: What This Workspace Is

The workspace at `/workspace` is an authenticated collaborative area where Brad Brisco and collaborators work with documents. It's backed by markdown files in `docs/workspace/` organized into sections (sidebar order is defined in `WORKSPACE_SECTION_ORDER` in `src/lib/workspace/docs.ts`):

| Section | Purpose | Current count |
|---------|---------|---------------|
| `books/` | Published books and covocational e-book manuscripts | 6 |
| `articles/` | Covocational and pillar articles | 15 |
| `ideas/` | Notes, brainstorms, backlog | 1 |
| `research/` | Research notes, bibliography, credentials | 3 |
| `insights/` | EEAT pipeline, themes, gap analysis, marketing playbook | 10 |
| `podcasts/` | Podcast notes (placeholder until populated) | 1 |
| `videos/` | Video scripts and outlines (placeholder until populated) | 1 |
| `author/` | Voice identity, writing prompts, digital profile | 3 |
| `projects/` | Active project documents | 1 |
| `meta/` | Conventions, templates, article index (sidebar label: **Editorial**) | 3 |

The frontend reads this via `src/lib/workspace/docs.ts` → API route → React Query hook → sidebar + doc viewer.

## Mode 1: Content Roadmap

When asked for a roadmap, analyze the current workspace state and propose what to create next.

### Step 1: Audit current coverage

Read the EEAT theme taxonomy from `docs/workspace/insights/eeat-content-pipeline.md` and cross-reference against what exists:

```bash
# Count articles per theme
grep -r "themes:" docs/workspace/articles/ | sort
```

Map each Tier 1 theme to its article coverage:
- `missional-ecclesiology` — How many articles?
- `church-planting-multiplication` — How many?
- `covocational-ministry` — How many?
- `missional-living-practice` — How many?
- `neighborhood-place` — How many?

### Step 2: Read the gap analysis

Read `docs/workspace/insights/gap-analysis.md` for identified opportunities.

### Step 3: Read the content ideas

Read `docs/workspace/ideas/platform-content-ideas.md` for brainstormed topics.

### Step 4: Propose roadmap

Present a prioritized list:

```
## Content Roadmap

### High Priority (fills a theme gap)
1. [Article] Title — theme, why it matters
2. [Research] Topic — what it enables

### Medium Priority (deepens existing themes)
3. [Article] Title — theme, builds on X
4. [Project] Title — what it coordinates

### Low Priority (nice to have)
5. ...
```

For each item, note:
- Which section it belongs in
- Which themes it serves
- What existing workspace docs it connects to
- Whether it needs research first

## Mode 2: Agentic Workflow Design

When asked about agentic design, think about how AI agents and automated workflows interact with the workspace.

### Key questions to explore:

1. **Agent-as-author** — How should AI Lab or custom agents use workspace docs as context? What docs should be in their retrieval corpus?

2. **Agent-as-researcher** — How can agents produce research notes that land in `research/` and inform future articles?

3. **Content pipeline automation** — What steps of the authoring workflow (research → outline → draft → review → publish) can be agent-assisted?

4. **Cross-reference intelligence** — How can agents suggest connections between docs, flag contradictions, or identify gaps?

5. **Workspace as agent context** — How should the workspace feed into system prompts? Which sections are "always-on" context vs. retrieved on demand?

### Design principles:

- **Docs are the interface** — Agents read and write markdown. No custom data formats.
- **Human-in-the-loop** — Agents propose; humans approve. Drafts go to `status: draft`.
- **Voice fidelity** — Every agent that writes content must load the voice identity first.
- **Single source of truth** — Workspace docs are canonical. Don't duplicate in vector stores without a sync strategy.

### Output format:

Present designs as:
1. **Workflow diagram** (text-based, showing steps and decision points)
2. **Agent capabilities needed** (what tools, what context, what guardrails)
3. **Implementation plan** (which skills/routes/hooks to build)

## Mode 3: Context Coding Architecture

When asked about context coding, plan how the workspace integrates with the broader codebase and CLAUDE.md system.

### Key concerns:

1. **What should CLAUDE.md know about the workspace?** — Add workspace awareness to project instructions so Claude always knows the docs exist.

2. **Workspace docs as development context** — Which workspace docs should inform feature development? (e.g., voice identity informs AI Lab, EEAT pipeline informs content routes)

3. **Doc-to-code traceability** — How do workspace strategy docs connect to actual implementation? (e.g., gap analysis → new article page → new API route)

4. **Skill composition** — How do workspace skills (`workspace-author`, `workspace-organize`, `workspace-strategy`) compose with platform skills (`new-page`, `type-safety-chain`, etc.)?

5. **Memory integration** — What workspace learnings should be saved to auto-memory vs. kept as workspace docs?

### Decision framework:

| If it's... | Put it in... |
|------------|-------------|
| A fact about the user or project | Auto-memory |
| A strategy or plan | `docs/workspace/insights/` or `projects/` |
| A reference or convention | `docs/workspace/meta/` |
| Voice/writing guidance | `docs/workspace/author/` |
| A one-off conversation insight | Don't persist — ephemeral |
| An engineering decision | `CLAUDE.md` or `docs/internal/` |

### Output format:

Present as:
1. **Current state** — What context is available where
2. **Gaps** — What's missing or misplaced
3. **Proposed changes** — Specific files to create/modify
4. **Implementation order** — What depends on what

## Mode 4: Research Priorities

When asked about research, identify what needs investigation and plan the approach.

### Research categories:

1. **Theological foundations** — Scripture study, doctrine exploration, framework development for workspace content
2. **Literature review** — Academic and practitioner sources that support or challenge Brad's positions
3. **Market/audience research** — Who reads covocational content? What questions do they have? What's trending?
4. **Platform research** — What features would serve the workspace? What do similar platforms do?
5. **Competitive landscape** — What content exists elsewhere on these topics? Where are the gaps?

### Research process:

1. **Define the question** — What specifically do we need to know?
2. **Check the corpus first** — Search books and existing workspace docs
3. **External search** — Use WebSearch for current sources, statistics, perspectives
4. **Synthesize** — Write a research note in `docs/workspace/research/`
5. **Connect** — Link the research to specific content opportunities

### Output format:

```
## Research Priority: [Topic]

**Question:** What do we need to know?
**Why it matters:** What content or decisions depend on this?
**Existing corpus coverage:** What Brad has already written about this
**External sources to investigate:** Specific searches or databases
**Target output:** Research note → informs [article/project/course]
**Estimated effort:** Quick (1 search) / Medium (multiple sources) / Deep (multi-session)
```

## Mode 5: Reflect

When asked to reflect, take stock of the workspace as a whole.

### Reflection prompts:

1. **Coverage** — Are the 5 Tier 1 themes adequately covered? Which is weakest?
2. **Voice consistency** — Do existing articles consistently hit all 5 voice markers?
3. **Organizational clarity** — Does the current section layout still make sense? Should anything move?
4. **Freshness** — Are there docs that are stale or outdated?
5. **Actionability** — Do project docs have clear next steps? Are task lists up to date?
6. **Connections** — Are there docs that should reference each other but don't?
7. **Frontend quality** — Does the workspace render all docs cleanly? Any typography issues?

### Reflection output:

Present as a brief (under 500 words) assessment with:
- **Strengths** — What's working well
- **Gaps** — What's missing or weak
- **Recommendations** — 3-5 specific next actions, each linked to a skill or command

## Composing with Other Skills

This skill works best in sequence with:

- `/workspace-author` — After identifying gaps, write the content
- `/workspace-organize` — After planning new sections, audit the structure
- `/author-research` — For deep external research on specific topics
- `/article-plan` — For detailed article planning before authoring

## Things to Never Do

- Never propose changes to `docs/internal/` or engineering docs — that's a different domain
- Never recommend content without checking what already exists
- Never plan without grounding in the EEAT theme taxonomy
- Never ignore the voice identity when recommending content direction
- Never propose agentic workflows that bypass human review for published content
