# Prompt: <Title that names the outcome — lead with a verb>

**Target agent:** <Claude Code / Cursor / Codex / Aider / any capable coding agent>
**Audience for review:** <who reads the result — engineer, designer, PM, the user>
**Repo / surface:** <repo name and the path or route this prompt operates on>
**Last updated:** <YYYY-MM-DD>

---

## 1. Role and stance

You are <role — e.g. "a senior full-stack engineer working in this Next.js 16
+ Supabase repo">. <One or two lines on the stance to take — e.g. "Prefer
small, reversible edits. Read before you write. Cite the files you change.">

## 2. Goal

<One paragraph. Plain-language statement of the outcome the user actually
wants. Lead with the verb. Name the user-visible change. Do not bury the
goal in background.>

## 3. Context — only what's load-bearing

- **Why now:** <motivating constraint, incident, deadline, or decision>
- **Key files:** `<path:line>` — short note. `<path:line>` — short note.
- **Related prompts / docs:** [<title>](<relative-path>), [<title>](<relative-path>)
- **What's already been tried:** <one bullet per attempt, with outcome>
- **Constraints:** <stack rules, design tokens, security boundaries, perf
  budgets — anything that narrows the solution space>

## 4. Definition of Done

Concrete, observable, verifiable. Each line is a thing a human or a CI step
can check.

- [ ] <user-visible behavior X works in route Y>
- [ ] `<typecheck command>` passes
- [ ] `<test command>` passes (name the spec)
- [ ] No regressions in <named surface> — spot-check by <how>
- [ ] Copy / tone matches <named reference doc>, if applicable
- [ ] Files touched stay within: <named scope>

## 5. Output format

<What the executing agent should produce. For code: which files may be
created/modified, which must not be touched, commit message style, PR
shape. For content: length, tone, headings, citations, links.>

## 6. Approach (recommended path, not a cage)

1. <Read X and Y; confirm the assumption Z.>
2. <First change.>
3. <Second change.>
4. <Verify with the commands in Section 9.>
5. <Self-check against Section 4 and report.>

Flag the steps where you should pause and surface a tradeoff to the user
rather than choosing silently.

## 7. Guardrails — do not

- <Known anti-pattern specific to this repo or this surface.>
- <File or system explicitly out of scope.>
- <Pattern that prior attempts got wrong.>

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
   targeted edits and re-run the loop.

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
