---
name: story-architect
description: Narrative structure skill for fiction and creative non-fiction — plot architecture, character arcs, scene construction, tension/release, theme, and pacing. Use when planning, outlining, diagnosing, or restructuring a narrative. Also use when building agents that generate structured stories.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Design or diagnose narrative structure: $ARGUMENTS

$ARGUMENTS can include:
- A story concept to outline (`outline: [concept]`)
- An existing manuscript or draft to diagnose (`diagnose: [path or text]`)
- A character to arc-map (`character: [name/description]`)
- A scene to construct (`scene: [situation]`)
- A format: `novel`, `short-story`, `novella`, `screenplay`, `narrative-nonfiction`, `memoir`, `essay`
- A genre context (`genre: [genre]`)
- An agent story-generation system to audit (`agent-audit: [path]`)
- Empty — ask what the user is building

---

## Part 1: Story Architecture

Every narrative — fiction or non-fiction — is built on the same structural skeleton: a character who wants something, encounters resistance, and is changed by the encounter. Everything else is ornamentation on that spine.

### The Three Essential Questions

Before any structural work, answer:

1. **What does the protagonist want?** (External goal — concrete, statable in one sentence)
2. **What does the protagonist need?** (Internal need — often in tension with the want)
3. **What stands in the way?** (Opposition — external antagonist AND internal resistance)

If you can't answer these, the story doesn't have a spine yet. Structure cannot compensate for a missing spine.

### Structural Models

Use the model that fits. Don't force a story into a model — let the story's nature select its shape.

#### Three-Act Structure (Universal)

```
ACT 1 (25%) — Setup
├── Opening Image — the world before change
├── Inciting Incident — the event that makes the old life impossible
├── Debate/Refusal — the protagonist resists the call
└── First Act Turn — commitment to the journey (no going back)

ACT 2 (50%) — Confrontation
├── Fun & Games — the promise of the premise delivered
├── Midpoint — false victory or false defeat (raises stakes)
├── Bad Guys Close In — escalating opposition
├── All Is Lost — the lowest point; something "dies"
└── Dark Night of the Soul — the moment before transformation

ACT 3 (25%) — Resolution
├── Break into Three — new insight or plan
├── Finale — final confrontation using lessons learned
├── Final Image — the world after change (mirrors opening)
```

#### Five-Act Structure (for complex narratives)

```
ACT 1 — Exposition (introduce world, character, stakes)
ACT 2 — Rising Action (complications multiply, alliances form/break)
ACT 3 — Climax (the central confrontation or revelation)
ACT 4 — Falling Action (consequences unfold, reversals)
ACT 5 — Denouement (new equilibrium, thematic resolution)
```

#### The Story Circle (Dan Harmon / Campbell distilled)

```
1. A character is in a zone of comfort (YOU)
2. But they want something (NEED)
3. They enter an unfamiliar situation (GO)
4. They adapt to it (SEARCH)
5. They find what they wanted (FIND)
6. But pay a heavy price (TAKE)
7. They return to their familiar situation (RETURN)
8. Having changed (CHANGE)
```

#### Kishotenketsu (East Asian four-act — no central conflict required)

```
Ki (Introduction) — establish the situation
Sho (Development) — develop the situation further
Ten (Twist) — an unexpected element enters
Ketsu (Conclusion) — reconcile the twist with the established situation
```

Use Kishotenketsu for: literary fiction, slice-of-life, contemplative narratives, stories about harmony rather than conflict.

#### Non-Fiction Narrative Structures

**Braided narrative**: Weave 2-3 story threads that converge thematically. Each thread follows its own arc. The power is in the juxtaposition.

**Frame narrative**: A present-day story frames a historical or retrospective narrative. The present thread provides urgency; the past thread provides depth.

**Thematic spiral**: Return to the same theme at increasing depth. Each pass adds complexity. Works for essays, memoirs, and idea-driven non-fiction.

---

## Part 2: Character Arcs

Characters are the delivery mechanism for theme. The arc IS the argument.

### Arc Types

**Positive change arc**: Character starts with a false belief (the Lie), encounters truth through conflict, and ultimately embraces the truth. Most common arc.
- Setup: Show the Lie in action — it "works" but at a cost
- Conflict: The Lie is challenged repeatedly
- Crisis: The Lie fails catastrophically
- Resolution: The character chooses truth over the Lie

**Flat arc**: Character already holds the truth. The world around them has the Lie. The character's steadfastness changes the world. (Atticus Finch, Captain America)

**Negative arc / Tragedy**: Character has a chance at truth but chooses the Lie, or is destroyed by the world's corruption. (Macbeth, Walter White, Gatsby)

**Disillusionment arc**: Character starts with a positive belief that turns out to be a Lie. They end wiser but sadder. The "truth" is a harder, darker reality.

### Character Construction

**The want/need split**: The external goal (want) and the internal need must be in tension. The story's central question is whether the character will get what they want, what they need, or both.

**Wound → Lie → Want → Need:**
- **Wound**: Something happened before the story that shaped the character
- **Lie**: The false belief the character holds because of the wound
- **Want**: What the character pursues to cope with the wound (driven by the Lie)
- **Need**: What the character actually requires to heal (requires abandoning the Lie)

**Opposition as mirror**: The best antagonists embody an alternative response to the same thematic question. They are not random obstacles — they are arguments against the protagonist's worldview.

### Supporting Character Functions

Every character serves a structural purpose:

| Function | Role | Example |
|----------|------|---------|
| **Mentor** | Provides truth the protagonist isn't ready to hear | Gandalf, Haymitch |
| **Mirror** | Reflects the protagonist's situation from a different angle | A character who made the choice the protagonist is facing |
| **Shadow** | Embodies the protagonist's fear or worst-case future | What the protagonist could become |
| **Catalyst** | Forces change by disruption | Arrives and makes the old status quo impossible |
| **Confidant** | Creates space for the protagonist to vocalize internal conflict | Watson, Ron Weasley |

---

## Part 3: Scene Construction

A scene is the fundamental unit of storytelling. Every scene must do at least TWO of these three things or it should be cut:

1. **Advance the plot** (something changes in the external situation)
2. **Reveal character** (we learn something new about who someone is)
3. **Deepen theme** (the story's argument is developed)

### Scene Architecture

```
GOAL — What does the POV character want in this scene?
CONFLICT — What opposes them?
OUTCOME — Do they get it? (Yes/No/Yes-but/No-and)
```

**The "Yes-but / No-and" principle:**
- **Yes**: They get what they want → boring (use sparingly)
- **No**: They don't get it → neutral (use at dark moments)
- **Yes, but**: They get it, but a new problem arises → propulsive (primary engine)
- **No, and**: They don't get it, and things get worse → escalation (raises stakes)

### Scene-Sequel Rhythm

**Scene** (action): Goal → Conflict → Disaster
**Sequel** (reaction): Emotion → Thought → Decision → New Goal

Fast pacing: Short sequels, quick emotional processing
Slow pacing: Long sequels, deep emotional processing
Literary pacing: Sequels as long or longer than scenes

### Scene Openings

Enter late. Start as close to the conflict as possible. Skip the character arriving, sitting down, ordering coffee — unless those details serve character or theme.

### Scene Endings

Leave early. End on the turn — the moment when the situation changes. Don't narrate the character processing what just happened (that's the sequel's job).

---

## Part 4: Tension and Pacing

### Types of Tension

1. **Dramatic tension**: The reader knows something the character doesn't (dramatic irony)
2. **Mystery tension**: The reader doesn't know something and wants to (curiosity)
3. **Suspense tension**: The reader knows the danger and watches the character approach it (dread)
4. **Interpersonal tension**: Two characters want incompatible things in the same scene
5. **Internal tension**: The character's want and need are in conflict

### Pacing Controls

| Tool | Speeds Up | Slows Down |
|------|-----------|-----------|
| **Sentence length** | Short, clipped | Long, flowing |
| **Scene length** | Short scenes, rapid cuts | Extended scenes |
| **White space** | More breaks | Dense paragraphs |
| **Dialogue ratio** | High dialogue | High narration |
| **Time compression** | "Three weeks passed" | Moment-by-moment |
| **Detail density** | Sparse, essential only | Rich, immersive |

**The tension wave**: Stories breathe. Tension rises, peaks, releases, then rises higher. The pattern is: establish → escalate → peak → brief release → escalate higher. Never sustain maximum tension — the reader goes numb.

### Micro-tension (line-level)

Every paragraph should contain a micro-tension: a question, a contradiction, an unresolved implication. The reader turns pages not because of plot (that's macro-tension) but because of micro-tension — the sentence-level pull of "what does that mean?" and "what happens next?"

---

## Part 5: Theme

Theme is not a message. It is a question the story explores from multiple angles. The story's events constitute an argument, but the conclusion should feel discovered, not declared.

**Theme as question**: "Is loyalty more important than truth?" "Can a person change?" "What do we owe each other?"

**Theme through structure**:
- The protagonist's arc embodies one answer
- The antagonist embodies another
- Supporting characters represent variations
- The plot forces the question into crisis
- The resolution demonstrates (not states) where the story lands

**Thematic resonance**: When setting, imagery, dialogue, and plot all independently point toward the same question without any of them stating it directly — that's resonance. It's the highest achievement in narrative craft.

**Never state the theme.** If a character says "I guess the real treasure was the friends we made along the way," the story has failed. Theme should be felt, not heard.

---

## Mode: Outline

When creating a story outline:

1. Answer the Three Essential Questions
2. Map the character's Wound → Lie → Want → Need
3. Select the structural model that fits
4. Outline the major beats (inciting incident, midpoint, crisis, climax, resolution)
5. For each beat, specify: what happens, what changes, what the protagonist learns/loses
6. Map the tension wave — where are the peaks and releases?
7. Identify the theme-as-question
8. Deliver as a structured outline with act breaks clearly marked

## Mode: Diagnose

When diagnosing an existing narrative:

1. Identify the structural model being used (intentionally or accidentally)
2. Check for the Three Essential Questions — are they answerable?
3. Map the character arc — is there a clear Lie/Truth/Want/Need?
4. Check scene-by-scene: does each scene do 2 of 3 (plot, character, theme)?
5. Map the tension wave — where does it sag?
6. Check pacing — are scenes and sequels in rhythm?
7. Identify the theme — is it emerging from the structure or being imposed on it?
8. Deliver a diagnostic report with specific prescriptions

## Mode: Agent Audit

When auditing an agent that generates stories:

1. Read the agent's instructions/prompts
2. Check: does it encode structural principles, or just "write a story about X"?
3. Most story-generating agents fail because they lack:
   - Character arc awareness (characters are static)
   - Scene-level goal/conflict/outcome
   - Tension management (flat or all-climax)
   - Theme integration (stated, not embodied)
4. Recommend structural additions to the agent's instructions
5. Draft a "Narrative Structure" section for the agent's system prompt

---

## Rules

- Structure serves story, not the other way around. If a story breaks a structural rule and it works, the story is right.
- Outlining is not a creative straitjacket — it's a map. You can always leave the road.
- A perfectly structured story with flat characters is worse than a messy story with living characters. Structure is necessary but not sufficient.
- Don't confuse plot with story. Plot is what happens. Story is what it means.
- The reader should never see the scaffolding. If structure is visible, it's over-engineered.
- Every structural principle in this skill applies to narrative non-fiction as much as fiction. True stories have arcs too — the craft is in finding them.
