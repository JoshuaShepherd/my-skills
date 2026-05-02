---
name: dialogue-craft
description: Dialogue craft for fiction and conversational AI agents — subtext, character voice differentiation, pacing, exposition handling, conflict in conversation, and the art of what people don't say. Use when writing dialogue, designing agent conversation patterns, or auditing dialogue quality.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Write or improve dialogue: $ARGUMENTS

$ARGUMENTS can include:
- A scene to write dialogue for (`scene: [description]`)
- Existing dialogue to improve (`improve: [text or path]`)
- A conversation to diagnose (`diagnose: [text or path]`)
- Characters involved (`characters: [names/descriptions]`)
- A context: `fiction`, `screenplay`, `game`, `chatbot`, `agent-conversation`, `interview`
- An agent conversation flow to design (`agent-flow: [description]`)
- Empty — ask what the user needs

---

## Why Dialogue is Hard

Dialogue is not transcribed speech. Real people repeat themselves, trail off, use filler words, circle back, and take ten sentences to say what could be said in two. Dialogue in fiction (or in a well-designed agent) is *compressed* speech — it sounds natural but every line does work.

The three functions of dialogue. Every line must serve at least one:

1. **Reveal character** — How someone says something tells us who they are
2. **Advance the scene** — The situation changes because of what was said
3. **Create tension** — There's a gap between what's said and what's meant

Lines that serve none of these are small talk. Cut them.

---

## Part 1: The Principles

### Subtext — The Engine of Good Dialogue

**Subtext is the gap between what a character says and what they mean.**

People rarely say what they actually feel. They deflect, they lie, they change the subject, they attack the wrong thing, they agree when they disagree, they joke about what hurts. The *surface* of dialogue is words. The *substance* is subtext.

**How to create subtext:**

**Misdirection**: Character talks about one thing but means another.
```
"How's the new apartment?"
"The kitchen has great light."
[She doesn't mention that she's alone in it.]
```

**Avoidance**: Character dodges the real subject.
```
"Did you talk to Dr. Reeves?"
"Did you know they're closing the diner on Fourth Street?"
```

**Saying the opposite**: Character says the opposite of what they feel.
```
"I'm happy for you. Really."
[The "really" is the tell — people don't add "really" when they mean it.]
```

**Displacement**: Emotion directed at the wrong target.
```
"Would it kill you to close the cabinet doors?"
[This fight is not about cabinet doors.]
```

**Silence**: The most powerful subtext is absence. A character who says nothing in a moment that demands a response.

### Character Differentiation

If you can swap two characters' dialogue without the reader noticing, the voices aren't distinct.

**Differentiation tools:**

| Tool | Example |
|------|---------|
| **Vocabulary range** | A professor uses "ameliorate." A plumber uses "fix." |
| **Sentence length** | A nervous character talks fast — short, clipped. A confident one takes their time. |
| **Directness** | Some characters ask directly. Others circle. |
| **Question habits** | Some characters answer questions. Others deflect with questions. |
| **Filler and hedging** | "Well..." "I mean..." "Sort of..." — each character has their own verbal tics |
| **Register shifts** | A character who code-switches between professional and casual under different stress levels |
| **Silence tolerance** | Some characters fill silence compulsively. Others weaponize it. |
| **Humor style** | Dry wit vs. self-deprecation vs. sarcasm vs. no humor at all |

**The swap test**: Read a line of dialogue without the attribution. Can you tell who's speaking? If not, the voice isn't distinct enough.

### Pacing in Dialogue

**Fast pacing** (rapid exchanges):
```
"Where?"
"East side. Under the bridge."
"When?"
"Midnight."
"Alone?"
"Does it matter?"
```
Use for: tension, conflict, urgency, interrogation.

**Slow pacing** (longer speeches, pauses, action beats):
```
Sarah set her coffee down. She looked at the ring on the counter between them, then out the window where the neighbor's kid was drawing on the sidewalk with chalk.
"I found it in your coat pocket," she said. "I wasn't looking for it."
He didn't move.
"I wasn't looking for anything," she said.
```
Use for: emotional weight, revelation, intimacy, devastation.

**The push-pull**: Alternate between fast and slow. A rapid exchange builds tension; a slow beat lets it detonate.

### Exposition in Dialogue

Exposition in dialogue is the fastest way to kill a scene. Characters explaining things to each other that they both already know ("As you know, Bob...") is the cardinal sin.

**Rules for exposition in dialogue:**

1. **Characters should only say things the other character doesn't know.** If both know it, the reader learns it through action, narration, or context.

2. **Conflict makes exposition invisible.** If the information is delivered DURING an argument, the reader absorbs the facts while being engaged by the emotion.
   ```
   "You moved three thousand miles for a job that pays less than—"
   "It's not about the money, Dad."
   "It's never about the money until the money runs out."
   ```
   [The reader just learned: new city, lower pay, family tension. No one "explained" anything.]

3. **Questions from characters who genuinely don't know.** New characters, outsiders, children — people who have a natural reason to ask.

4. **Disagreement reveals.** Two characters arguing about how something happened reveals the facts AND the characters' perspectives simultaneously.

**Never:**
- "As you know, [information dump]..."
- "Let me explain how this works..."
- "Remember when we [backstory the reader needs]?"
- Characters telling each other things they both know for the reader's benefit

### Conflict in Conversation

Dialogue without conflict is a transcript. Conflict doesn't mean fighting — it means incompatible desires in the same conversation.

**Types of dialogue conflict:**

| Type | Mechanism | Example |
|------|-----------|---------|
| **Direct opposition** | Characters want opposite things | A negotiation. A breakup. |
| **Cross-purposes** | Characters want different things | One wants to confess; the other wants to plan dinner. |
| **Power dynamics** | One character has leverage | An interview. A parent-child talk. |
| **Information asymmetry** | One character knows something the other doesn't | The reader knows one is lying. |
| **Internal vs. external** | What the character says vs. what they want to say | A character agreeing while seething. |

---

## Part 2: Dialogue Mechanics

### Attribution (Dialogue Tags)

**"Said" is invisible.** Use it 80-90% of the time. The reader's eye skips right over it.

**Avoid:**
- Creative synonyms: "exclaimed," "declared," "opined," "interjected," "queried"
- Adverb-laden tags: "said angrily," "said softly," "said sarcastically"
- Impossible tags: "smiled," "laughed," "shrugged" (you can't smile a sentence)

**Better than adverbs — action beats:**
```
❌ "I don't care," she said angrily.
✅ "I don't care." She shoved the chair back from the table.
```

**When to use no tag at all:** In two-person dialogue, once the rhythm is established, you can drop tags for several exchanges. The reader tracks who's speaking by alternation.

**When to use something other than "said":** "Asked" for questions. "Whispered" or "shouted" when volume is narratively important and can't be conveyed otherwise. That's about it.

### Action Beats

Action beats are the small physical actions interspersed with dialogue. They serve three purposes:

1. **Pacing** — Slow the conversation down, create breathing room
2. **Character** — What a character does while talking reveals more than what they say
3. **Setting** — Keep the reader grounded in the physical space

**Good action beats are specific and telling:**
```
She picked at the label on her beer bottle. [nervous, avoidant]
He lined up the salt and pepper shakers until they were perfectly parallel. [controlling]
She looked at her phone, put it face-down, then picked it up again. [waiting for something]
```

**Bad action beats are generic:**
```
She nodded. He smiled. She shrugged. He sighed.
[These are the dialogue equivalent of clip art. They convey nothing specific.]
```

### Formatting

- Each new speaker gets a new paragraph. Always. No exceptions.
- Dialogue within narration: keep the tag close to the speech. Don't bury attribution at the end of a long paragraph.
- Long speeches: break them up with action beats, reactions from the listener, or paragraph breaks within the speech.
- Interior thought during dialogue: italics or free indirect discourse, depending on the work's conventions. Be consistent.

---

## Part 3: Dialogue for AI Agents and Conversational Interfaces

Everything above applies to agent-generated dialogue, but agents have additional challenges.

### The Agent Dialogue Problem

Most AI agents produce dialogue that:
- Is too helpful too fast (no conversational arc)
- Never uses subtext (everything is surface)
- Has no personality differentiation from other agents
- Doesn't match register to context
- Over-explains (the "As you know, Bob" problem, but with the user as Bob)
- Uses formulaic openings and closings ("Certainly!", "I hope this helps!")

### Designing Agent Conversation Patterns

**Conversation arc**: Even a utility conversation has a shape.
```
Greeting → Understanding → Working → Resolution → Close
```

Each phase has different characteristics:
- **Greeting**: Warm but brief. Match the user's energy.
- **Understanding**: Ask clarifying questions. Don't assume.
- **Working**: Focused, efficient. Show progress.
- **Resolution**: Confirm, summarize only if complex.
- **Close**: Clean exit. No lingering.

**Register matching**: The agent's formality level should match the user's, not a preset default. A user who writes "hey what's up" should not get "Good afternoon! I'd be happy to assist you today."

**Information pacing**: Don't dump everything at once. Reveal information at the pace the user can absorb it. In complex explanations, pause for confirmation: "Does that make sense so far?" or break into digestible chunks.

**Conversational subtext for agents**: An agent can't lie or deflect (and shouldn't), but it CAN:
- Acknowledge the emotion behind a question before answering the literal question
- Read between the lines: "It sounds like you've been working on this for a while" (inferred from frustration signals)
- Mirror language: use the user's terminology, not your own preferred terms

### Agent Dialogue Anti-Patterns

| Anti-pattern | Example | Fix |
|-------------|---------|-----|
| **The Over-Greeter** | "Hello! I'm so glad you're here! How can I help you today? I'm ready to assist with anything you need!" | One sentence. Match the user's energy. |
| **The Disclaimerer** | "While I'm an AI and can't guarantee..., I'll try my best to..." | Skip the disclaimer. Just help. |
| **The Bullet-Lister** | Every response is a numbered list | Use prose for simple answers. Lists for genuinely enumerable things. |
| **The Summarizer** | "In summary, we've discussed..." at the end of every response | Only summarize when the conversation was genuinely complex. |
| **The Hedge-Speaker** | "It might be worth considering..." "Perhaps you could..." "It's possible that..." | Be direct. "Do this." "This works because." |
| **The Echo** | Restating the user's question before answering it | Answer directly. The user knows what they asked. |

### Agent Dialogue Voice Design

For each agent, define:

1. **Greeting style**: How does this agent say hello? (Or does it skip the greeting?)
2. **Question style**: How does this agent ask for clarification? (Direct? Gentle? Multiple choice?)
3. **Explanation style**: How does this agent teach? (Analogies? Step-by-step? Show-then-explain?)
4. **Error style**: How does this agent handle mistakes or confusion? (Apologize? Redirect? Humor?)
5. **Closing style**: How does this agent end a conversation? (Summary? Invitation? Clean exit?)

---

## Mode: Write

When writing dialogue for a scene:

1. Identify each character's **want** in the scene (what they're trying to get)
2. Identify the **subtext** (what they're not saying)
3. Identify the **conflict** (why they can't both get what they want)
4. Write the dialogue with action beats and minimal attribution
5. Run the swap test — can you tell who's speaking without tags?
6. Check: does every line serve at least one of the three functions?

## Mode: Improve

When revising existing dialogue:

1. Identify on-the-nose dialogue (characters saying exactly what they mean)
2. Find exposition dumps — convert to conflict-delivered information
3. Check voice differentiation — run the swap test
4. Cut small talk that doesn't serve character, plot, or tension
5. Replace creative dialogue tags with "said" or action beats
6. Check pacing — is there variation between fast and slow exchanges?
7. Deliver the revised version with annotations explaining changes

## Mode: Agent Flow

When designing agent conversation patterns:

1. Map the conversation arc (greeting → understanding → working → resolution → close)
2. Define the agent's dialogue voice (greeting/question/explanation/error/closing styles)
3. Identify potential friction points and design graceful handling
4. Write 3 sample conversations showing the agent at its best
5. Write 1 sample showing how the agent handles a difficult user
6. List the anti-patterns to explicitly forbid in the agent's instructions

---

## Rules

- Dialogue is not transcription. Every line is compressed, purposeful, and layered.
- Subtext is not optional. If every character says exactly what they mean, the dialogue is flat.
- "Said" is invisible. Use it. Stop reaching for synonyms.
- Action beats > adverbs. Show the emotion, don't label it.
- The swap test is non-negotiable. Distinct characters speak distinctly.
- Exposition through conflict is invisible. Exposition through monologue is deadly.
- For agents: the user's time is sacred. Don't waste it with verbose greetings, disclaimers, or summaries. Help fast, help well, sound human.
