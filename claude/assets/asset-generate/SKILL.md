---
name: asset-generate
description: Generate image assets using Nano Banana 2 (Gemini Flash Image). Use when creating hero images, course covers, book covers, thumbnails, social cards, or any visual asset for the platform.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Generate an image asset using Nano Banana 2: $ARGUMENTS

$ARGUMENTS should include:
- A description of the desired image (subject, mood, style)
- Optionally: asset type (hero, cover, thumbnail, social, og, banner)
- Optionally: aspect ratio, resolution, output path
- Optionally: reference image path(s) for style/subject matching
- Empty — ask the user what they want to generate

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Read `src/lib/config/tenant.config.ts` to understand the tenant brand context
3. Read `src/app/globals.css` to understand the color palette and design tokens
4. Determine the appropriate asset preset from the table below

## Asset Presets

| Asset Type     | Aspect Ratio | Resolution | Thinking Mode | Typical Use                         |
|----------------|-------------|------------|---------------|--------------------------------------|
| `hero`         | `16:9`      | `2048`     | `high`        | Page hero backgrounds                |
| `cover-course` | `16:9`      | `2048`     | `high`        | Course cover images                  |
| `cover-book`   | `3:4`       | `2048`     | `high`        | Book cover images                    |
| `thumbnail`    | `16:9`      | `1024`     | `minimal`     | Card thumbnails for listings         |
| `social`       | `1:1`       | `1024`     | `minimal`     | Social media square posts            |
| `og`           | `16:9`      | `1024`     | `minimal`     | Open Graph / link preview images     |
| `banner`       | `4:1`       | `2048`     | `minimal`     | Wide banners, email headers          |
| `portrait`     | `9:16`      | `2048`     | `high`        | Mobile-first vertical images         |
| `podcast`      | `1:1`       | `1024`     | `minimal`     | Podcast artwork                      |
| `avatar`       | `1:1`       | `512`      | `minimal`     | Profile images, small icons          |

If the user doesn't specify a type, infer from context or ask.

## Prompt Construction — The Brief Method

Structure every prompt using this 5-part brief. Write in natural, descriptive language — NOT keyword soup. NB2 is a reasoning model that understands intent, physics, and composition.

### 1. SUBJECT (Who/What)
Describe the primary subject with specificity. Name materials, textures, ages, expressions.
- BAD: "a church leader"
- GOOD: "a middle-aged man with warm brown skin and short grey hair, wearing a linen shirt, gesturing passionately while speaking"

### 2. ACTION & RELATIONSHIPS (What's Happening)
Describe the scene dynamics — interaction between subjects, movement, energy.
- "leading a small group gathered in a circle on a sun-dappled patio"
- "hands resting on an open, well-worn Bible on a wooden table"

### 3. SETTING (Where, When, Atmosphere)
Place, time of day, weather, mood, cultural context.
- "in a bright, airy community hall in Melbourne, Australia, mid-morning golden light streaming through floor-to-ceiling windows"
- "an intimate home gathering, warm evening lamplight, bookshelves visible in the background"

### 4. STYLE & MEDIUM (Visual Language)
Name specific photographic or artistic references:
- **Photography**: "shot on Sony A7IV, 85mm f/1.4, shallow depth of field, natural light, warm color grading"
- **Illustration**: "watercolor illustration with visible brushstrokes, muted earth tones, editorial style"
- **Conceptual**: "minimalist flat illustration, geometric shapes, limited palette of warm terracotta and sage green"
- **Abstract**: "abstract texture, layered paper collage effect, warm amber and cream tones"

### 5. COMPOSITION & CAMERA (Framing)
Shot type, angle, lens behavior, negative space:
- "medium close-up, slightly off-center composition with rule of thirds, shallow depth of field blurring the background"
- "wide establishing shot, low angle, dramatic sky in upper third"
- "overhead flat lay, centered symmetrical composition"

## Brand Context for Alan Hirsch Platform

Always incorporate these brand qualities unless the user specifies otherwise:

### Tone & Mood
- **Warm, scholarly, missional** — not corporate, not clinical
- **Community-oriented** — images should feel inviting, relational, human
- **Formation-focused** — suggest growth, journey, transformation
- **Grounded in practice** — real settings, not stock-photo sterility

### Color Affinity
- Warm earth tones: terracotta, amber, sage, cream, warm grey
- Accent with the platform's primary color (warm amber/gold)
- Avoid: cold blues, neon, high-saturation corporate palettes
- Dark mode assets: rich, warm darks (not pure black), warm highlights

### Visual Motifs
- Open books, journals, handwritten notes
- Small group gatherings, circles, shared meals
- Urban neighborhoods, streets, community spaces
- Maps, pathways, journeys
- Natural textures: wood, linen, paper, stone

## Execution

### Step 1 — Compose the Prompt
Write the full NB2 prompt following the brief method above. Show it to the user for approval before generating.

### Step 2 — Generate via Gemini API
Use the following script pattern (adapt as needed):

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

const result = await ai.models.generateImages({
  model: "imagen-4.0-generate-001",  // Imagen 4.0
  prompt: "<THE_COMPOSED_PROMPT>",
  config: {
    numberOfImages: 4,        // Generate 4 variations
    aspectRatio: "16:9",      // From preset
    // resolution handled by model
  },
});

// Save generated images
for (let i = 0; i < result.generatedImages.length; i++) {
  const img = result.generatedImages[i];
  const buffer = Buffer.from(img.image.imageBytes, "base64");
  const outPath = path.join("public/images/generated", `${slug}-${i + 1}.png`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buffer);
}
```

**IMPORTANT**: If the `@google/genai` package is not installed, install it first:
```bash
pnpm add @google/genai
```

If the Imagen API is not available or the user prefers the Gemini multimodal approach, use:
```typescript
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",  // or latest available
  contents: "<THE_COMPOSED_PROMPT>. Generate this as an image.",
  config: {
    responseModalities: ["image", "text"],
  },
});

// Extract image parts from response
for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 3 — Save & Report
- Save images to `public/images/generated/<asset-type>/<slug>-<n>.png`
- Convert to WebP for production use if needed: use sharp or similar
- Report the file paths and let the user review

## Output Format

```
## Asset Generation Report

### Prompt
> [The full prompt used]

### Settings
- Model: nano-banana-2
- Aspect ratio: 16:9
- Resolution: 2048
- Thinking mode: high
- Variations: 4

### Generated Files
1. public/images/generated/hero/forgotten-ways-1.png
2. public/images/generated/hero/forgotten-ways-2.png
3. public/images/generated/hero/forgotten-ways-3.png
4. public/images/generated/hero/forgotten-ways-4.png

### Next Steps
- Review the generated images and select the best one
- Use `/asset-edit` to refine if needed
- Use `/asset-text-overlay` to add text if needed
```

## Iterative Refinement

If the first generation is close but not right, use NB2's conversational editing:
- "Make the lighting warmer and more golden"
- "Move the subject slightly to the left, more negative space on the right"
- "Reduce the saturation, make it feel more muted and scholarly"

Do NOT re-prompt from scratch — refine iteratively.

## Error Handling

- Missing `GOOGLE_GENERATIVE_AI_API_KEY` → stop with instructions to add it to `.env.local`
- API rate limit → wait and retry once, then report
- Content policy block → adjust prompt (remove specific person references, etc.) and retry
- Generation failure → report error details and suggest prompt modifications
