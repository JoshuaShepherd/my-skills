---
name: course-audit
description: Audit course content for structural integrity, voice fidelity, pedagogical coherence, and alignment with the transformation loop. Use to validate authored content before it goes to the platform.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit course content: $ARGUMENTS

$ARGUMENTS should specify: course slug and optionally week number or section type. If empty, audit the entire course.

## Before Starting

1. Read `courses/CONTENT_QUALITY_GUIDE.md` — checklist, scoring rubric, and craft guide (primary audit reference)
2. Read `courses/COURSE_STRATEGY.md` — the canonical structure reference
3. Read `courses/ALAN_HIRSCH_VOICE_PROMPTING_MASTER_GUIDE.md` — voice system
4. Read all content for the course in `courses/courses/[slug]/`

## Scoring

Use the 0–100 rubric in `CONTENT_QUALITY_GUIDE.md` Part 2. Score each of the 10 dimensions (0–10), apply weights, and sum. Report both the dimension scores and the weighted total. Use the interpretation table to assign a rating (Exceptional / Strong / Solid / Developing / Incomplete / Not ready).

## Audit Dimensions

### 1. Structural Integrity
- All 8 weeks present?
- Each core week (2-7) has all 8 transformation loop sections in correct order?
- Week 1 has orientation sections? Week 8 has synthesis/sending sections?
- Word counts within targets for each section type?

### 2. Voice Fidelity
Score each teaching section against the Five Voice Markers:
| Marker | Weight | Min |
|--------|--------|-----|
| Christocentric Anchoring | 30% | 0.7 |
| Pastoral Warmth | 20% | 0.5 |
| Narrative Imagery | 15% | 0.6 |
| Theological Depth | 10% | 0.7 |
| Prophetic Intensity | 25% | 0.5-0.8 |

Flag any failure modes: corporate tone, antithesis patterns, missing Christocentric anchor, practice before grounding.

### 3. Pedagogical Coherence
- Does each dissonance prompt actually create productive tension?
- Does each teaching section advance the course narrative (not just cover a topic)?
- Do case studies show the concept at work (not summarize the teaching)?
- Are action steps concrete, time-boxed, and doable in 7 days?
- Do reflection prompts look backward at action taken?
- Do cohort meetings create genuine shared risk?

### 4. Arc Integrity
- Does the course build progressively across weeks?
- Is there a Christocentric spine connecting all weeks?
- Does Week 1 orient without overwhelming?
- Does Week 8 synthesize and send (not just summarize)?
- Would a learner who completed all 8 weeks be genuinely formed — or just informed?

### 5. Theological Alignment
- Do the frameworks (mDNA, APEST, etc.) appear as theological realities, not topics?
- Is Scripture woven into argument (not proof-texted)?
- Are historical examples accurate and well-sourced?
- Does the content honor Alan's actual position (check corpus material)?

## Output Format

For each dimension, provide:
- **Score**: Pass / Needs Work / Fail
- **Evidence**: Specific sections with specific issues
- **Recommendations**: Actionable revision guidance

End with a summary: overall readiness, top 3 priorities for revision, and whether the course is ready for platform ingestion.

### 6. Chat Section Quality (New)

- Do all chat sections (dissonance, action, reflection) have both **learner priming** and **companion shaping** subsections?
- Does companion shaping include: goal, opening moves, constraints, and closing guidance?
- Does the dissonance companion avoid resolving the week's theology?
- Does the action companion ensure one step, one time box, one named witness?
- Does the reflection companion include compassionate handling for learners who did not complete the step?

### 7. Checklist Compliance

Run the full checklist from `CONTENT_QUALITY_GUIDE.md` Part 1 (sections A–F). Report any unchecked items.
