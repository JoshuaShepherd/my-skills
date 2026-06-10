---
name: asset-author-style
description: Define and maintain a consistent visual identity for an author/thought leader across all image assets. Creates a style guide document that all other asset-* skills reference for consistency. Use once to establish the look, then all headshots, heroes, and portraits will match.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Define or update the author visual style guide: $ARGUMENTS

$ARGUMENTS should include:
- `create` — Create a new author style guide from reference photos
- `update` — Update an existing style guide with new preferences
- `show` — Display the current style guide
- `apply [image-path]` — Check if an image matches the style guide
- Optionally: reference image paths showing the "look" the user wants
- Optionally: verbal description of desired aesthetic
- Empty — check if a guide exists; if not, start creation

## Purpose

This skill creates a single source of truth — the **Author Style Guide** — stored at
`_docs/asset-prompts/author-style-guide.md`. Every other asset skill (`/asset-headshot`,
`/asset-hero-portrait`, `/asset-generate`, etc.) checks for this file and follows it
to ensure visual consistency across all author imagery.

Without this guide, each generation is independent and may drift in lighting, color grade,
background treatment, or overall feel. With it, every output matches the established look.

## Before Starting

1. Read `src/lib/config/tenant.config.ts` for brand identity and existing image URLs
2. Check if `_docs/asset-prompts/author-style-guide.md` already exists
3. If creating: gather reference images (existing headshots, hero images, or aspirational references)
4. If updating: read the current guide and understand what needs to change

## Style Guide Document Structure

The style guide is a structured markdown document with specific, actionable descriptions
that can be pasted directly into NB2 prompts:

```markdown
---
name: author-style-guide
description: Visual identity system for [AUTHOR NAME] across all platform imagery
author: [AUTHOR NAME]
created: [DATE]
updated: [DATE]
reference_images:
  - [path or URL to reference image 1]
  - [path or URL to reference image 2]
---

# Author Visual Style Guide — [AUTHOR NAME]

## 1. Subject Description

### Physical Description (for NB2 prompt consistency)
[A precise, respectful physical description of the author as they appear in the
reference photos. This ensures NB2 maintains likeness when extending backgrounds
or modifying lighting. Include age range, build, hair, skin tone, and typical
presentation — but only visible, factual attributes.]

Example:
> A man in his early 60s with warm olive-toned skin, short grey-white hair with
> natural texture, trimmed grey beard. Athletic-lean build. Typically wears relaxed,
> thoughtful attire — linen shirts, casual jackets, earth-toned colors. Expressive
> hands, warm and direct eye contact. His presence reads as scholarly yet accessible,
> serious yet warm.

### Expression & Energy
[The default expression/vibe to maintain across imagery]

Example:
> Engaged and warm. A slight, knowing smile — the look of someone who has thought
> deeply about something and is genuinely excited to share it with you. Never stern
> or distant. Never performatively casual. Authentic intellectual warmth.

### Wardrobe Defaults
[What the author typically wears; what looks "right" on them]

Example:
> Earth-toned casual-scholarly: linen shirts in cream, sage, or warm grey. Occasionally
> a casual blazer or lightweight jacket in charcoal or warm navy. Open collar. No ties.
> No logos. The aesthetic is "thoughtful person, not trying too hard."

---

## 2. Lighting Profile

### Key Light
[Primary light description — direction, quality, temperature]

Example:
> Warm directional light from the upper-left (10 o'clock position). Large, soft source
> (like a window or large softbox). Not harsh — the shadows should be present but
> gentle. The light should feel like "warm afternoon through a study window."

### Fill
> Warm reflected fill from the right side, approximately 2 stops below key.
> Shadows are never cold or black — they maintain warm brown-amber undertones.

### Rim/Hair Light
> Subtle warm rim light from above-behind, catching the edges of hair and shoulders.
> Creates gentle separation from the background without looking like a studio setup.

### Overall Quality
> The lighting should feel natural and warm — never clinical, never flat, never
> harshly directional. The reference is "beautiful natural light in a well-designed
> space" — not "professional studio with lighting grid."

---

## 3. Color Grade

### Temperature
> Warm. Always warm. The overall image temperature should lean toward golden/amber.
> Color temperature equivalent: approximately 5200K-5800K (warm daylight to slightly
> warm interior). Never cool, never neutral-clinical.

### Palette Anchors
| Element | Color Reference | Notes |
|---------|----------------|-------|
| Skin highlights | Warm, natural, healthy | Never orange, never grey |
| Skin shadows | Warm brown undertone | Never cold purple or blue |
| Background lights | Amber, honey, cream | #D4A84B to #FAF5E4 range |
| Background darks | Warm charcoal, espresso | #2C2220 to #3D3D3D range |
| Clothing | Earth tones | Sage, cream, warm grey, terracotta |

### Film Reference
> The color grade should feel like: Kodak Portra 400 pushed half a stop — warm,
> slightly desaturated, beautiful skin tones, golden highlights. Not Fuji Velvia
> (too saturated). Not digital-clean. A touch of organic warmth and grain.

### Saturation
> Slightly pulled back from reality. Not desaturated/moody, not hyper-saturated.
> About 85-90% of natural saturation. Colors should feel rich but calm.

### Contrast
> Medium. Not flat, not punchy. Enough contrast to give the image structure and
> dimension, but soft enough to feel inviting. Lifted blacks (darkest point is
> warm charcoal #2C2220, not pure black).

---

## 4. Background Treatment

### Preferred Backgrounds (ranked)
1. **Warm bokeh study** — Out-of-focus bookshelves, warm lamplight, amber/walnut tones.
   The default. Suggests scholarship, depth, thoughtfulness.
2. **Community space** — Slightly more open, warm interior. Tables, chairs, warm light.
   Suggests accessibility, conversation, relationship.
3. **Outdoor/neighborhood** — Urban setting, natural light, community context.
   Suggests mission, movement, engagement with the world.
4. **Branded gradient** — Amber-to-charcoal smooth gradient.
   For marketing uses, OG images, text-heavy layouts.
5. **Clean studio** — Warm grey to cream gradient.
   For formal headshots, press/media uses.

### Background Rules
- Backgrounds should NEVER compete with the subject for attention
- Depth of field: always shallow enough that background reads as "environment" not "scene"
- Background colors must come from the warm palette — no cool tones
- When extending a background (outpainting), match the existing environment seamlessly

---

## 5. Composition Principles

### Framing
> The subject should always have breathing room — not tightly cropped to the edges.
> Minimum 10% of frame as space around the subject in any direction.
> The subject's eyes should be approximately at the upper-third line (rule of thirds).

### Gaze Direction
> Default: looking directly at camera (connection with viewer) OR looking slightly
> toward the text/content zone (guiding the viewer's eye to the message).
> Never: looking away from both camera and content, or looking down.

### Posture
> Relaxed but present. Slight forward lean suggests engagement. Shoulders open,
> not hunched. Hands may be visible and expressive (common in teaching moments)
> but should not be the focus.

### Negative Space
> Always include intentional negative space — for text overlay, for visual rest,
> for editorial balance. The subject should occupy 35-50% of the frame in hero
> images, 60-80% in headshots.

---

## 6. Do Not

These are explicit anti-patterns — never do these:

- ❌ Cold/blue lighting or shadows
- ❌ High-contrast dramatic shadows that obscure the face
- ❌ Corporate headshot against grey seamless paper
- ❌ Overly retouched/smoothed skin (maintain natural texture)
- ❌ Altered facial features, de-aging, or idealization
- ❌ Pure black anywhere in the image (use warm charcoal instead)
- ❌ Environmental elements that suggest wealth/luxury
- ❌ The subject looking aggressive, stern, or unapproachable
- ❌ Perfectly centered composition (too static/formal)
- ❌ Hard studio flash look
- ❌ Stock photo aesthetic (too posed, too perfect, too generic)
- ❌ Inconsistent lighting direction across image set

---

## 7. Reference Prompt Blocks

These are copy-paste-ready blocks for other asset skills to include in their prompts:

### BLOCK: Subject Likeness
```
[Paste the physical description from Section 1. This ensures NB2 maintains consistency
when the source image is not provided as a reference.]
```

### BLOCK: Lighting Setup
```
[Paste the complete lighting profile from Section 2.]
```

### BLOCK: Color Grade
```
[Paste the color grade specification from Section 3.]
```

### BLOCK: Background (Warm Bokeh)
```
[Paste the warm bokeh background description from Section 4.]
```

### BLOCK: Full Style Anchor
```
[Combined blocks 1-4 for complete consistency — use in /asset-series as the style anchor.]
```
```

## Creation Process

### Step 1 — Gather References

Ask the user for:
1. **2-3 existing photos** they consider "on brand" or closest to the desired look
2. **Verbal description** of the look they want (warm? scholarly? approachable? cinematic?)
3. **Anti-references** — what they DON'T want (corporate? cold? over-processed?)
4. **Aspirational references** — other thought leaders, authors, or brands whose visual style they admire

### Step 2 — Analyze Reference Images

Read each reference image and extract:
- Lighting direction, quality, and temperature
- Background type and treatment
- Color palette (dominant colors, shadows, highlights)
- Composition and framing
- Expression and energy
- Overall mood/vibe

### Step 3 — Draft the Style Guide

Write the complete style guide following the structure above. Be specific and actionable —
every description should be precise enough to paste directly into an NB2 prompt.

### Step 4 — Validate with a Test Generation

Generate one test headshot and one test hero using the style guide:

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// Load reference image
const refBytes = fs.readFileSync(referenceImagePath);
const refBase64 = refBytes.toString("base64");

// Generate test headshot using style guide blocks
const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [
    {
      role: "user",
      parts: [
        { inlineData: { data: refBase64, mimeType: "image/webp" } },
        {
          text: `Using this reference photo of the subject, create a professional headshot
following this exact style specification:

${STYLE_GUIDE_LIGHTING_BLOCK}

${STYLE_GUIDE_COLOR_GRADE_BLOCK}

${STYLE_GUIDE_BACKGROUND_BLOCK}

Maintain the subject's exact likeness from the reference photo.
Crop: head and upper shoulders, 1:1 aspect ratio.

Generate this as an image.`,
        },
      ],
    },
  ],
  config: { responseModalities: ["image", "text"] },
});
```

### Step 5 — Review & Iterate

Show the test generation to the user:
- Does the lighting match the desired feel?
- Is the color grade right?
- Does the background treatment work?
- Is the overall mood/vibe correct?

Iterate on the style guide until the test generation matches the user's vision.

### Step 6 — Save the Style Guide

Write to `_docs/asset-prompts/author-style-guide.md`.

## Update Process

When updating an existing style guide:

1. Read the current guide
2. Identify what needs to change and why
3. Update only the affected sections
4. Regenerate a test image to verify the change
5. Save the updated guide with new `updated` date

## Apply / Audit Process

When checking if an image matches the style guide:

1. Read the style guide
2. Read the image to audit
3. Compare against each section:
   - Lighting direction and quality
   - Color temperature and grade
   - Background treatment
   - Subject presentation
   - Composition
4. Score each dimension and report

## Output Format — `create`

```
## Author Style Guide Created

### Author: Alan Hirsch
### File: _docs/asset-prompts/author-style-guide.md
### Reference Images: 3 analyzed

### Style Summary
- **Lighting**: Warm directional from upper-left, soft fill, subtle rim
- **Color Grade**: Kodak Portra 400 warm, slightly desaturated, lifted blacks
- **Backgrounds**: Warm bokeh study (default), community space, branded gradient
- **Mood**: Scholarly yet warm, authentic, inviting
- **Film Reference**: Portra 400 pushed half stop

### Test Generations
1. Headshot (1:1): public/images/generated/style-test/alan-headshot-test.png ✅
2. Hero (16:9): public/images/generated/style-test/alan-hero-test.png ✅

### Integration
All asset-* skills will now check for this guide and follow it automatically:
- `/asset-headshot` — lighting, color grade, backgrounds
- `/asset-hero-portrait` — compositions, mood, color treatment
- `/asset-series` — style anchor derived from guide
- `/asset-brand-check` — audit criteria updated to match guide
- `/asset-generate` — brand context informed by guide

### Next Steps
- Review the test generations against your expectations
- If adjustments needed, run `/asset-author-style update`
- Generate your first production headshot with `/asset-headshot`
```

## Output Format — `show`

```
## Author Style Guide — Alan Hirsch

### Quick Reference
| Dimension | Setting |
|-----------|---------|
| Lighting | Warm directional upper-left, soft fill, warm rim |
| Temperature | 5200-5800K (warm daylight) |
| Grade | Portra 400 warm, 85-90% saturation, lifted blacks |
| Default BG | Warm bokeh study (amber/walnut, shallow DOF) |
| Composition | Rule of thirds, eyes at upper third, breathing room |
| Mood | Scholarly, warm, authentic, inviting |

### Reference Prompt Blocks Available
1. `BLOCK: Subject Likeness` — physical description for NB2 consistency
2. `BLOCK: Lighting Setup` — complete 3-point warm lighting spec
3. `BLOCK: Color Grade` — full color treatment spec
4. `BLOCK: Background (Warm Bokeh)` — default background description
5. `BLOCK: Full Style Anchor` — all blocks combined for /asset-series

Use `/asset-author-style show` with `--full` for complete block contents.
```

## Output Format — `apply`

```
## Style Guide Compliance Check

### Image: public/images/generated/headshot/alan-instructor.png
### Style Guide: _docs/asset-prompts/author-style-guide.md

| Dimension | Guide Spec | Image Analysis | Match |
|-----------|-----------|----------------|-------|
| Key light direction | Upper-left, 10 o'clock | Upper-left ✓ | ✅ |
| Light quality | Soft, warm, window-like | Soft ✓, warm ✓ | ✅ |
| Color temperature | 5200-5800K warm | ~5500K estimated | ✅ |
| Skin tone | Warm, natural, healthy | Slightly cool in shadows | ⚠️ |
| Background | Warm bokeh study | Warm bokeh ✓ | ✅ |
| Saturation | 85-90% of natural | ~80% — slightly low | ⚠️ |
| Black point | Warm charcoal, lifted | Pure black in corners | ❌ |
| Expression | Warm, engaged, authentic | Warm, engaged ✓ | ✅ |
| Composition | Rule of thirds, breathing room | Centered — off spec | ⚠️ |

### Overall: 6/9 dimensions match (⚠️ Minor adjustments needed)

### Recommended Edits
1. Warm up shadow areas — shift from cool to warm undertone
2. Lift the blacks — darkest point should be #2C2220, not pure black
3. Bump saturation slightly — from ~80% to ~87%
4. Reframe slightly off-center using rule of thirds

Use `/asset-edit` with these instructions to bring the image into compliance.
```
