---
name: video-consult
description: Consult on video production for a course — scripture grounding, narrative arc, storyboard, scene structure, and script. Bridges Alan's voice, course theology, and Remotion video production. Use when planning or authoring video content for any course.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Consult on video production: $ARGUMENTS

$ARGUMENTS should include:
- Course slug or name (e.g., `mdna`, `reframation`, `mdna`)
- Optionally: specific week or module (e.g., `week 3`, `all weeks`)
- Optionally: video type (opening video, explainer, promo, social cut, course trailer)
- Optionally: specific topic, theme, or scripture passage to ground in
- Empty — ask the user what course and video they're working on

---

## Before Starting

### 1. Understand the Course Context

Read in this order — stop as soon as you have enough context:

1. Check for existing course content in `content-library/courses/[slug]/` — read any authored weeks for theological themes, arc, and progression
2. If this is the mDNA course, read `/Users/joshuashepherd/Desktop/Dev/repos/mdna-course/editor/data/course.json` for canonical content
3. Read `_docs/COURSE_STRATEGY.md` if it exists — authoritative reference for course structure
4. Read `_docs/TRANSFORMATIONAL_COURSE_CHARTER.md` if it exists — the Four Necessities (dissonance, action, reflection, community)

### 2. Understand the Video System

1. Read `_docs/videos/README.md` — production workflow, project structure, current state
2. Read `_docs/videos/style-guide/brand-tokens.md` — colors, typography, motion tokens
3. Read `_docs/videos/style-guide/motion-principles.md` — easing, pacing, composition rules
4. Read `_docs/videos/templates/script-template.md` — canonical script format
5. Read `_docs/videos/templates/storyboard-template.md` — canonical storyboard format
6. Check for existing scripts/storyboards in `_docs/videos/courses/[slug]/scripts/` and `storyboards/`

### 3. Understand the Shared Scene Library

Read `_docs/videos/courses/_shared/scripts/course-explainer-scenes.md` — the 14-scene explainer library serves as a reference for tone, structure, and visual vocabulary.

---

## Consultation Modes

Determine which mode the user needs. If unclear, ask.

### Mode A: Full Video Plan (Scripture → Arc → Storyboard → Script)

For when starting from scratch on a video. This is the primary mode.

**Step 1 — Theological Grounding**

Identify the scripture and theological foundations for this video:

- What is the core concept this video must land? (From the course week's teaching content)
- What scripture passages ground it? (Woven, not proof-texted — per Alan's voice)
- What historical examples illuminate it? (Early church, Chinese underground church, SMRC, Methodist movement)
- What Alan Hirsch frameworks apply? (mDNA, APEST/5Q, Shema, sentness, incarnational-missional)
- What books/chapters are the corpus sources? (Cite as: *The Forgotten Ways* ch3, *5Q* ch7, etc.)

Output a **Theological Brief** — 200-400 words covering the above. This becomes the foundation everything else builds on.

**Step 2 — Narrative Arc**

Design the story structure for this video. Every video — whether 30 seconds or 5 minutes — has an arc.

For **opening videos** (weekly, ~5 min):
- Hook: name the tension or question the week confronts (15-20s)
- Core concept: plain language, first-person "we" (60-90s)
- Grounding: one scriptural or historical anchor (45-60s)
- Implication: what this means for the learner's life (30-45s)
- Invitation: closing question or anticipation for what's next (15-20s)

For **explainer videos** (course-level, 2-5 min):
- Use the three-act structure from the shared scene library:
  - Act 1 — What transformation means (composites, tension)
  - Act 2 — Why the current approach fails (data, reality)
  - Act 3 — How formation works (method, the loop)
  - Close — CTA

For **social cuts / promos** (15s-60s):
- Single tension → single insight → CTA
- Front-load the most compelling 3 seconds (the hook)

For **module recaps / synthesis** (1-3 min):
- What we explored → what we did → what changed → what's next

Output an **Arc Document** — a numbered sequence of beats with estimated duration per beat.

**Step 3 — Scene Breakdown & Storyboard**

For each beat in the arc, define:

| Field | Description |
|-------|-------------|
| **Time** | Start–end timecode |
| **Narration** | Exact voiceover text (word count noted) |
| **Alan quote** | On-screen quote from published works, if applicable |
| **Visual** | Detailed visual description — composition, motion, metaphor |
| **On-screen text** | Any titles, labels, callouts |
| **Motion** | Animation/transition description using motion-principles vocabulary |
| **Assets needed** | NB2 backgrounds, illustrations, or code-only elements |
| **Transition out** | How this scene exits to the next |

Use the storyboard template format from `_docs/videos/templates/storyboard-template.md`.

**Step 4 — Script**

Write the full narration script with production notes, using the script template from `_docs/videos/templates/script-template.md`.

Include:
- Scene-by-scene narration at ~145 wpm (cinematic, not rushed)
- Alan Hirsch quotes — properly attributed to specific books
- Production notes: key concept, corpus references, dissonance moment, call to action
- Asset requirements table

---

### Mode B: Scripture & Theology Consult

For when the user has a video concept but needs help grounding it theologically.

1. Read the video concept or existing script
2. Identify theological gaps: Where is the Christocentric anchoring? Where is the scriptural grounding? Where are the historical examples?
3. Suggest specific scripture passages, Alan frameworks, and historical parallels
4. Rewrite or annotate sections to strengthen theological depth
5. Apply the alan-voice markers: Christocentric anchoring, pastoral warmth, narrative imagery, theological depth, prophetic intensity

Output: annotated script or theological brief with specific suggestions.

---

### Mode C: Arc & Structure Consult

For when the user has content but needs help with narrative structure.

1. Read existing content (script, teaching notes, or course section content)
2. Identify the narrative arc — is there a clear hook → tension → grounding → implication → invitation?
3. Diagnose structural issues: Does it front-load information? Does practice appear before understanding? Does it rush to resolution?
4. Propose a revised arc with beat-by-beat timing
5. Flag pacing issues — are there enough breathing moments? Is the dissonance held long enough?

Output: revised arc document with structural notes.

---

### Mode D: Storyboard & Visual Consult

For when the user has a script but needs visual direction.

1. Read the script
2. For each scene, propose visual concepts using the brand vocabulary:
   - Warm charcoal backgrounds, gold accents, organic textures
   - Abstract/silhouette figures, never photorealistic
   - Typography-driven scenes vs. image-driven scenes
   - Motion language from `motion-principles.md`
3. Identify which scenes need AI-generated assets (NB2 backgrounds) vs. code-only animation
4. Write NB2 prompt anchors for any generated assets
5. Note Remotion composition considerations (scene type, transition type, duration in frames)

Output: storyboard document using the canonical template.

---

## Voice Guidelines

All narration and script content must follow Alan Hirsch's voice. The five markers:

1. **Christocentric anchoring** (30%) — Jesus is Lord. Every framework points back to Jesus.
2. **Pastoral warmth** (20%) — "We" language. Invitational, not prescriptive.
3. **Narrative imagery** (15%) — Organic metaphors: movement, seeds, fire, rivers. Historical stories.
4. **Theological depth** (10%) — Grounded in Scripture and tradition. Accessible but deep.
5. **Prophetic intensity** (25%) — Reframing questions. Productive dissonance. Calls to risk.

**Anti-patterns** (never use): corporate consultant tone, detached academic voice, antithesis patterns ("Not X, but Y"), generic motivational language, bullet-point lists as primary content.

**Rhetorical posture**: Alan speaks from ahead — he describes what the audience doesn't yet see as though it is already visible. He challenges the frame before engaging the question within it.

**Scripture usage**: Woven, not leading. No sermon-like openings. No proof-texting. Scripture governs the argument but rarely opens it.

---

## Output & File Placement

Save all outputs to the appropriate per-course directory:

| Output | Save to |
|--------|---------|
| Theological brief | `_docs/videos/courses/[slug]/scripts/[video-id]-theology.md` |
| Arc document | `_docs/videos/courses/[slug]/storyboards/[video-id]-arc.md` |
| Script | `_docs/videos/courses/[slug]/scripts/[video-id]-script.md` |
| Storyboard | `_docs/videos/courses/[slug]/storyboards/[video-id]-storyboard.md` |
| NB2 prompts | `_docs/videos/prompts/[video-id]-prompts.md` |

**Naming convention**: `[video-id]` = `[course]-w[NN]-[type]` (e.g., `mdna-w03-opening`, `mdna-explainer`, `reframation-w05-social-30s`)

---

## Cross-Skill Integration

This skill is designed to work with the other content skills in this project:

- **`/course-author`** — Use its output as source material. The main teaching, dissonance prompts, and case studies provide the theological substance that videos distill.
- **`/alan-voice`** — Apply for voice audit on any narration script. Run in audit mode to score the five markers.
- **`/asset-video-prompt`** — Hand off to this skill when you need AI video model prompts (Runway, Kling, Pika) for specific scenes.
- **`/course-validate`** — Ensure the video content aligns with the Four Necessities and course structure.
- **`/course-scaffold`** — Reference for understanding which weeks have which section types and where opening videos fit.

---

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- Every video must serve at least one of the Four Necessities (dissonance, action, reflection, community)
- Scripture woven, not leading — per Alan's voice
- Practice never appears before understanding
- Narration pace: ~145 wpm (cinematic, measured)
- All on-screen text handled in Remotion code — never baked into generated images
- Use brand tokens from `brand-tokens.md` — no off-brand colors or fonts
- Use motion vocabulary from `motion-principles.md` — no ad-hoc animation descriptions
- Ground everything in Alan's actual published works — never fabricate quotes or frameworks
- Always check for existing content before creating new — build on what's there
