---
name: editorial-lens
description: Multi-level editorial review — from developmental editing (structure, argument, arc) through line editing (prose quality, voice) to copy editing (grammar, consistency, fact-checking). Use when reviewing any written work or auditing an agent's output quality.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Review or edit: $ARGUMENTS

$ARGUMENTS can include:
- A file path or text to review (`review: [path or text]`)
- A specific edit level (`level: developmental | line | copy | all`)
- A genre or format context (`genre: [genre]`, `format: article | chapter | essay | script | marketing`)
- An agent output to review (`agent-output: [text]`, `agent-path: [path to agent instructions]`)
- A focus area (`focus: structure | voice | pacing | clarity | argument | consistency`)
- Empty — ask what the user needs reviewed

---

## The Three Editorial Lenses

Professional editing operates at three distinct levels. Most writers (and most AI agents) conflate them, which produces reviews that are simultaneously too shallow and too scattered. This skill separates them cleanly.

### Lens 1: Developmental Editing

**What it sees:** The big picture. Structure, argument, arc, pacing, coherence, theme.

**Questions this lens asks:**
- Does this piece have a clear spine? (For fiction: want/need/obstacle. For non-fiction: thesis/argument/evidence.)
- Is the structure serving the content, or fighting it?
- Are there sections that should be cut, moved, expanded, or split?
- Does the pacing work? Where does the reader's attention sag?
- Is the opening earning the reader's continued attention?
- Does the ending land? Or does it deflate, summarize, or trail off?
- For fiction: Do the character arcs complete? Is the tension wave shaped well?
- For non-fiction: Does the argument build? Is evidence placed where it's needed? Is the "so what?" clear?

**Developmental edit output format:**

```markdown
## Developmental Assessment

### Spine
[Is the core argument/arc clear? State it in one sentence. If you can't, that's the first problem.]

### Structure Map
[Walk through the piece section by section. For each: what it does, whether it earns its place, and what it needs.]

| Section | Function | Verdict | Notes |
|---------|----------|---------|-------|
| [Section name] | [What it does] | Keep / Cut / Move / Expand / Rework | [Specific notes] |

### Pacing Analysis
[Where does the piece move well? Where does it drag? Where is it rushed?]

### Opening Assessment
[Does the opening create a question? Establish voice? Ground the reader? Score 1-5.]

### Closing Assessment
[Does the ending land? Resonate? Summarize (bad) or reveal (good)? Score 1-5.]

### Top 3 Structural Priorities
1. [Most important structural change needed]
2. [Second]
3. [Third]
```

---

### Lens 2: Line Editing

**What it sees:** Prose quality at the paragraph and sentence level. Voice, rhythm, clarity, imagery, verb power, economy.

This lens applies the seven lenses from `prose-craft`:

1. **Rhythm and Cadence** — Sentence length variation, stress patterns, paragraph rhythm
2. **Concrete and Sensory Language** — Specificity ladder, sensory engagement, camera focal length
3. **Verb Power** — Active voice, precise verbs, adverb elimination
4. **POV Discipline** — Head-hopping, impossible knowledge, tonal consistency
5. **Subtext and Implication** — Behavioral subtext, loaded objects, dialogue gaps
6. **Opening and Closing Sentences** — First/last sentence strength per paragraph/section
7. **Economy and Precision** — Bloat, redundancy, throat-clearing, dead words

**Line edit output format:**

```markdown
## Line Edit Assessment

### Overall Prose Quality: [1-5]

### Lens Scores

| Lens | Score | Key Evidence |
|------|-------|-------------|
| Rhythm & Cadence | [1-5] | [Best passage / worst passage] |
| Concrete & Sensory | [1-5] | [Where abstract / where grounded] |
| Verb Power | [1-5] | [To-be count, weak verb examples] |
| POV Discipline | [1-5] | [Any violations] |
| Subtext | [1-5] | [Over-explained vs. implied] |
| Openings & Closings | [1-5] | [Strongest / weakest] |
| Economy | [1-5] | [Bloat examples, dead words count] |

### Voice Consistency
[Is the voice consistent throughout? Where does it drift? What does it drift toward?]

### Top 5 Line-Level Revisions
[Quote the passage, explain the issue, show the revised version]

1. **Original:** "[quote]"
   **Issue:** [what's wrong]
   **Revised:** "[improved version]"

2. ...
```

---

### Lens 3: Copy Editing

**What it sees:** Correctness, consistency, and factual accuracy at the word level.

**Checklist:**

**Grammar and Mechanics:**
- [ ] Subject-verb agreement
- [ ] Tense consistency (no unmotivated tense shifts)
- [ ] Pronoun clarity (no ambiguous "they" or "it")
- [ ] Parallel structure in lists and comparisons
- [ ] Comma usage (serial comma consistency, no comma splices)
- [ ] Hyphenation consistency (compound modifiers, prefixes)
- [ ] Quotation mark style consistency (curly vs. straight, single vs. double)

**Internal Consistency:**
- [ ] Names spelled consistently throughout
- [ ] Numbers formatted consistently (spelled out vs. numerals)
- [ ] Terminology used consistently (same concept = same word, always)
- [ ] Chronological consistency (dates and timelines don't contradict)
- [ ] Point of view maintained (no unmotivated shifts)
- [ ] Tone consistent (no register breaks without purpose)

**Fact-Checking (for non-fiction):**
- [ ] Dates and years verified
- [ ] Names and titles verified
- [ ] Statistics attributed and plausible
- [ ] Quotes properly attributed
- [ ] Historical claims accurate
- [ ] No fabricated sources or citations

**Copy edit output format:**

```markdown
## Copy Edit Report

### Error Count by Category
| Category | Count | Severity |
|----------|-------|----------|
| Grammar | [n] | [High/Med/Low] |
| Consistency | [n] | [High/Med/Low] |
| Factual | [n] | [High/Med/Low] |

### Issues Found
[List each issue with location, category, and fix]

1. **[Location]** — [Category] — "[problematic text]" → "[corrected text]" — [explanation]
```

---

## Mode: Full Review (All Three Lenses)

When running a complete editorial review:

1. **Read the entire piece first.** Do not start commenting until you've read it all.
2. **Developmental lens first.** Structure before sentences. If the structure is broken, line edits are premature.
3. **Line edit second.** Only on sections that survive the developmental assessment.
4. **Copy edit last.** Only on text that's structurally and stylistically stable.
5. **Synthesize.** Provide a priority-ranked action list that combines all three lenses.

**Full review output:**

```markdown
# Editorial Review: [Title]

## Executive Summary
[2-3 sentences: what works, what's the biggest issue, what the writer should focus on first]

## Developmental Assessment
[Full Lens 1 output]

## Line Edit Assessment
[Full Lens 2 output]

## Copy Edit Report
[Full Lens 3 output]

## Priority Action List
[Ranked list combining all lenses — what to fix first, second, third]

1. **[Priority 1]** — [Lens] — [Specific action]
2. **[Priority 2]** — [Lens] — [Specific action]
3. ...
```

## Mode: Agent Output Review

When reviewing AI agent output:

1. Identify the agent's purpose and voice (from instructions or context)
2. Run all three lenses but weight them differently:

| Lens | Weight for Agent Output | Why |
|------|------------------------|-----|
| Developmental | 30% | Agents often produce structurally sound but soulless output |
| Line Edit | 50% | **This is where agents fail most.** Flat prose, repetitive structure, weak verbs |
| Copy Edit | 20% | Agents are usually grammatically correct |

3. Check specifically for AI writing tells:
   - Excessive hedging ("It's important to note that...", "It's worth mentioning...")
   - Formulaic transitions ("Furthermore," "Additionally," "Moreover,")
   - Symmetric paragraph lengths (all medium, no variation)
   - Missing sensory detail (all abstract, no concrete)
   - Opening with definitions instead of hooks
   - Closing with summaries instead of images
   - Lists where prose would be better
   - "Overall," as a closing word
   - Emoji or exclamation marks in formal contexts

4. Recommend specific prompt/instruction changes to fix the issues

## Mode: Comparative Review

When comparing two versions of the same piece (draft A vs. draft B):

1. Read both versions
2. Map the structural changes (what was added, cut, moved, reworked)
3. Evaluate: did the changes improve or weaken each dimension?
4. For each change: verdict (improvement / regression / neutral) + evidence

---

## Rules

- **Never rewrite without permission.** An editorial review identifies problems and suggests solutions. It does not substitute the editor's voice for the writer's.
- **Be specific.** "The pacing drags in the middle" is a diagnosis. "Section 3 (paragraphs 8-14) spends 400 words establishing context that could be done in 100" is useful.
- **Quote the text.** Every issue should include the specific passage being discussed. The writer needs to find what you're talking about.
- **Prioritize ruthlessly.** A writer can absorb 5-7 revision priorities. A list of 30 issues is a list of zero issues — it overwhelms and paralyzes.
- **Developmental before line.** Never line-edit a section that should be cut. Never copy-edit a sentence that needs rewriting.
- **Praise what works.** If a passage is strong, say so and say why. This is not kindness — it's information. The writer needs to know what to protect during revision.
- **Separate taste from craft.** "I wouldn't have written it this way" is taste. "This sentence has three to-be verbs and no sensory detail" is craft. Only flag craft.
