---
name: build-prompt
description: >
  Turn a rough idea, voice memo, or half-formed brief into a fully engineered
  markdown prompt at docs/build/prompts/<slug>.md for any agentic coding
  situation (Claude Code, Cursor, Codex, Aider, etc.). Embeds the four
  prompt-engineering pillars — Clear Communication, Context, Definition of
  Done, Iteration — plus role, output format, guardrails, and a closed-loop
  acceptance protocol. Interprets confidently; asks only when truly ambiguous;
  iterates with the user until the Definition of Done is met.
argument-hint: '<rough idea, request, or paste of notes>'
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# build-prompt

Use this skill when the user wants to author or refine a prompt under
`docs/build/prompts/` — i.e. a durable, repo-checked-in instruction that
they (or another agent) will hand to Claude Code, Cursor, Codex, Aider, or
similar to do real engineering work.

Your job is to convert the user's rough expression (`$ARGUMENTS`) into a
fully-engineered markdown prompt that another capable agent can execute
end-to-end without re-asking the user. Do not over-clarify; do not pad.
Interpret confidently from what they said and what the repo shows.

---

## What a "good prompt" must contain

Every prompt this skill produces embeds these layers. If any are weak, the
prompt is not done.

1. **Clear communication.** Say what you actually want. Name the audience
   (which agent / which human reviewer), the format, and the constraints.
   Treat the model as a capable collaborator who needs the same instructions
   any new hire would need on day one — not less, not more.
2. **Context — only the relevant parts.** Who the audience is, what tone to
   strike, what's already been tried, what the constraints are, what files
   or systems are load-bearing. Link the specific files (`path:line`) and
   prior prompts/docs the agent will need. Skip everything else.
3. **Definition of Done.** Concrete, observable, verifiable. "Write me a
   fundraising appeal" is vague. "Write me a 400-word fundraising appeal to
   lapsed mid-level donors in the tone of a personal letter from our ED,
   focused on our youth program's recent expansion, ending with a specific
   gift ask" is a Definition of Done. The prompt must spell out what
   finished looks like in checkable terms.
4. **Iteration.** First output is rarely final. The prompt must tell the
   executing agent how to iterate, how to surface tradeoffs, when to ask
   the human, and when to keep going. It should also close the loop:
   verify against the DoD, then stop.

The skill also embeds the supporting structure every strong prompt needs:

- **Role / identity** for the executing agent (what stance to take).
- **Output format** (file path(s), structure, what to write vs. propose).
- **Examples or references** (when a tone, layout, or pattern is non-obvious).
- **Reasoning approach** (when to think step-by-step, when to plan first,
  when to act).
- **Guardrails** (what NOT to do — known failure modes, files not to touch,
  patterns to avoid).
- **Acceptance criteria & verification commands** (typecheck, lint, tests,
  smoke checks, screenshots — whatever proves the DoD is met).
- **Closed-loop protocol** (how the agent reports back and how iteration
  terminates).

---

## Process

### Step 1 — Read the user's input and the repo, then decide if you can proceed

`$ARGUMENTS` is whatever the user typed. It may be a one-liner, a paragraph,
or a paste of notes. Read it. Then quickly orient:

1. Is there a `docs/build/prompts/` directory already? (`ls docs/build/prompts/`
   — create the directory if missing.)
2. Are there 1–3 sibling prompts that look like the right shape to match?
   Skim them for tone, depth, and conventions.
3. Is there a `CLAUDE.md`, `AGENTS.md`, or `docs/design/DESIGN.md` worth
   referencing in the prompt's Context section? Skim only the parts the
   prompt will actually need to cite.
4. Does the user's input name files, routes, or tables? If so, verify they
   exist before quoting them in the prompt.

**Ask the user a question only if a load-bearing fact is genuinely unknowable
from input + repo.** Examples of load-bearing unknowns: the target file the
prompt operates on, the user role of the executor, an ambiguous reference
("the thing we discussed last week"). Examples that are NOT worth asking:
preferred section ordering, exact word count, whether to include examples —
make a reasonable call and let iteration correct it.

If you must ask, ask **at most one** focused question. Otherwise proceed.

### Step 2 — Draft the prompt

Generate the markdown file at `docs/build/prompts/<slug>.md` where `<slug>`
is short kebab-case derived from the user's intent (5 words or fewer when
possible). If a file at that path already exists, treat the run as
**adding to / refining** it rather than overwriting — preserve prior
content, append or edit surgically, and note the edit in the log section
at the bottom.

Use the canonical structure in [template.md](template.md). The skeleton:

```markdown
# Prompt: <Title that names the outcome>

**Target agent:** <Claude Code / Cursor / Codex / any capable coding agent>
**Audience for review:** <who reads the result — engineer, designer, PM, the user>
**Repo / surface:** <repo name and the path or route this prompt operates on>
**Last updated:** <YYYY-MM-DD>

---

## 1. Role and stance

You are <role — e.g. "a senior full-stack engineer working in this Next.js 16
+ Supabase repo">. <One or two lines on the stance to take — e.g. "Prefer
small, reversible edits. Read before you write. Cite the files you change.">

## 2. Goal (one paragraph)

<Plain-language statement of the outcome the user actually wants. Lead with
the verb. Name the user-visible change. Do not bury the goal in background.>

## 3. Context — only what's load-bearing

- **Why now:** <motivating constraint, incident, deadline, or decision>
- **Key files:** <path:line — path:line — short note on what each does>
- **Related prompts / docs:** <links to sibling prompts or design docs>
- **What's already been tried:** <one bullet per attempt, with outcome>
- **Constraints:** <stack rules, design tokens, security boundaries, perf
  budgets, anything that narrows the solution space>

## 4. Definition of Done

Concrete, observable, verifiable. Each line is a thing a human or a CI step
can check.

- [ ] <user-visible behavior X works in route Y>
- [ ] <typecheck / lint / tests pass — name the commands>
- [ ] <no regressions in surface Z — name what to spot-check>
- [ ] <copy / tone matches reference doc, if applicable>
- [ ] <files touched stay within the named scope>

## 5. Output format

<What the executing agent should produce: files to change, commits to make,
PRs to open, artifacts to write. If the prompt is for content (copy, docs),
specify length, tone, headings, citations. If it's for code, specify which
layers may be touched and which must not.>

## 6. Approach (recommended path, not a cage)

<3–7 numbered steps the agent should generally follow. End with verification
and a self-check against the DoD. Leave room for judgment; flag the places
where the agent should pause and surface a tradeoff to the user.>

## 7. Guardrails — do not

- <known anti-patterns specific to this repo or this surface>
- <files / systems explicitly out of scope>
- <patterns that prior attempts got wrong>

## 8. Iteration protocol (closed loop)

1. Produce the first pass end-to-end. Do not stop short for confirmation
   unless a Section 7 guardrail forces a pause.
2. Self-check against Section 4. Report which boxes are checked and which
   are not, with one-line reasons for any gap.
3. If gaps remain that you can fix without new information, fix them and
   re-check. Repeat until either all boxes are checked or you hit a
   genuine unknown.
4. When all DoD boxes are checked, post a final summary: what changed,
   how to verify, and what was deliberately left out of scope.
5. Treat the first user reply as iteration input, not approval. Apply
   targeted edits ("more concise", "wrong tone here", "rewrite this
   paragraph in our voice") and re-run the loop.

## 9. Verification commands

```bash
<typecheck command>
<lint command>
<test command — unit / e2e>
<smoke check — curl, screenshot, manual route>
```

## 10. Attempt log (append-only)

| Date (ISO) | Actor | Summary | Outcome |
|------------|-------|---------|---------|
| <YYYY-MM-DD> | build-prompt skill | Initial draft from user input | Drafted |
```

Adapt the skeleton to the prompt's nature. A copy/editorial prompt does not
need a "Verification commands" code block — replace it with a tone or
reference check. A migration prompt needs explicit rollback notes. Do not
mechanically copy sections that don't apply; do not skip the four pillars.

### Step 3 — Write the file, then run the iteration loop

1. Use the `Write` tool to create `docs/build/prompts/<slug>.md`. If the
   file already exists, use `Read` then `Edit` to append or refine
   surgically.
2. Tell the user, in 2–4 lines, what you wrote and where. Quote the title
   and the DoD bullet count. Do not paste the whole file back.
3. Invite iteration with a concrete prompt: "Want it tighter on X? Different
   tone? Different DoD bar?" Do not ask abstract "does this look good?"
   questions — give them levers to pull.
4. Apply the user's iteration as targeted `Edit` calls. Re-state what
   changed in 1–2 lines.
5. Continue until the user says "done", or the DoD as written is met and
   the user has no further changes.
6. On final close, append a row to the prompt's Section 10 attempt log.

### Step 4 — When the prompt is done

A prompt is done when:

- The four pillars are all present and load-bearing (not boilerplate).
- The DoD is concrete enough that a different agent could execute the
  prompt without re-asking the user.
- The user has had a chance to redirect tone, scope, or emphasis at least
  once.
- The attempt log is updated.

Tell the user the prompt is done and where it lives. Suggest, in one line,
how they'd run it (e.g. "paste the contents into Claude Code, or reference
this file from another prompt").

---

## Style rules for the prompts you produce

- **Lead with the verb.** "Ship a working per-org workspace nav preset."
  not "This prompt is about navigation."
- **Name the audience.** Every prompt has a target agent and a human
  reviewer. Both belong in the header.
- **Cite, don't summarize, the repo.** When referencing a file, use the
  exact path. When referencing a line range, use `path:line` or
  `path:line-line`. Don't paraphrase what's already in the code.
- **No vague modifiers in the DoD.** Replace "clean", "robust", "good UX"
  with observable outcomes — a route renders, a test passes, a tone
  matches a named reference.
- **One next prompt at a time.** If the user's input contains several
  follow-on prompts, generate the first and list the others as
  "Follow-on prompts (do not start yet)" at the bottom.
- **Markdown only.** Tables for parallel structure, code fences for
  commands and schema, bullet lists for parallel items. No HTML unless
  the user explicitly wants it.
- **Inter-prompt links.** When a related prompt already exists under
  `docs/build/prompts/`, link it instead of duplicating its content.

---

## What this skill does NOT do

- It does not execute the prompt it produces. The prompt is an artifact;
  running it is a separate act.
- It does not author code in `src/` as a side effect. The only file it
  writes is the prompt markdown (and possibly the `docs/build/prompts/`
  directory if missing).
- It does not invent files, routes, tables, or stakeholders. If a fact
  is not in the user's input or the repo, either ask or omit.

---

## Related skills

- [studio-prompt](../../studio/studio-prompt/SKILL.md) — Generates AI Studio Build-mode
  prompts (system instructions + build prompt + iterations) for UI
  prototyping. Use that when the target tool is AI Studio, not a coding
  agent.
- [figma-prompt](../../design/figma-prompt/SKILL.md) — Generates Figma Make prompts
  for design artifacts.
- [authoring-skills](../authoring-skills/SKILL.md) — How to author the
  skill itself, not the prompts it produces.
