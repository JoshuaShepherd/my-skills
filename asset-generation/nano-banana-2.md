
Generate images using Nano Banana 2 (Gemini 3.1 Flash Image): $ARGUMENTS

$ARGUMENTS should include:
- A description of the desired image (subject, mood, style)
- Optionally: asset type (hero, cover, thumbnail, social, og, banner, portrait, avatar)
- Optionally: aspect ratio, resolution, output path
- Optionally: reference image path(s) for style/subject matching or editing
- Optionally: model preference (nano-banana-2, imagen-4, imagen-4-fast, imagen-4-ultra)
- Empty — ask the user what they want to generate

## Authoritative Documentation

### Primary References
- Gemini Image Generation Guide: https://ai.google.dev/gemini-api/docs/image-generation
- Imagen 4 via Gemini API: https://ai.google.dev/gemini-api/docs/imagen
- Gemini 3.1 Flash Image Model Card: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image-preview
- Gemini API Pricing: https://ai.google.dev/gemini-api/docs/pricing

### Prompt Engineering Guides (Official)
- Google DeepMind Prompt Guide: https://deepmind.google/models/gemini-image/prompt-guide/
- How to Prompt Gemini Image Gen: https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/
- Ultimate Prompting Guide: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
- Prompting Tips (Google Blog): https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/
- Gemini Image Best Practices (Vertex): https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/gemini-image-generation-best-practices

### Vertex AI & Firebase
- Vertex AI Image Generation: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/overview
- Imagen API Reference (Vertex): https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api
- Firebase AI Logic — Imagen: https://firebase.google.com/docs/ai-logic/generate-images-imagen
- Firebase AI Logic — Gemini Image Gen: https://firebase.google.com/docs/ai-logic/generate-images-gemini

### Content Policy & Safety
- Responsible AI for Imagen: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/responsible-ai-imagen

### Quickstart
- Gemini Image Editing Next.js Quickstart: https://github.com/google-gemini/gemini-image-editing-nextjs-quickstart

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Read `{{CONFIG_PATH}}` for brand context if available
3. Read `{{STYLES_PATH}}` for color palette and design tokens if available
4. Determine the model and asset preset from the tables below

## Available Models

### Nano Banana 2 — Gemini Native Image Gen (conversational, edit-capable)
| Model ID | Codename | Best For |
|---|---|---|
| `gemini-3.1-flash-image-preview` | **Nano Banana 2** | Best speed + quality balance, editing, character consistency |
| `gemini-3.0-pro-image` | Nano Banana Pro | Highest quality (slower, ~$0.134/image) |

### Imagen 4 — Standalone Image Generation (no conversational editing)
| Model ID | Tier | Cost/image | Speed |
|---|---|---|---|
| `imagen-4.0-fast-generate-001` | Fast | $0.02 | ~2.7s |
| `imagen-4.0-generate-001` | Standard | $0.04 | ~5s |
| `imagen-4.0-ultra-generate-001` | Ultra | $0.06 | Slowest, highest quality |

**Default model:** `gemini-3.1-flash-image-preview` (Nano Banana 2) for all tasks requiring editing, character consistency, or iterative refinement. Use `imagen-4.0-generate-001` for batch generation of standalone images.

## Asset Presets

| Asset Type | Aspect Ratio | Resolution | Typical Use |
|---|---|---|---|
| `hero` | `16:9` | `2K` | Page hero backgrounds |
| `cover-course` | `16:9` | `2K` | Course cover images |
| `cover-book` | `3:4` | `2K` | Book cover images |
| `thumbnail` | `16:9` | `1K` | Card thumbnails |
| `social` | `1:1` | `1K` | Social media square posts |
| `og` | `16:9` | `1K` | Open Graph / link preview |
| `banner` | `4:1` | `2K` | Wide banners, email headers |
| `portrait` | `9:16` | `2K` | Mobile-first vertical images |
| `podcast` | `1:1` | `1K` | Podcast artwork |
| `avatar` | `1:1` | `512` | Profile images, small icons |
| `ultrawide` | `21:9` | `2K` | Cinematic headers |

## Supported Aspect Ratios

### Nano Banana 2 (Gemini Native)
`1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`

### Imagen 4
`1:1`, `3:4`, `4:3`, `9:16`, `16:9`

### Supported Resolutions (Nano Banana 2)
| imageSize | Approximate Pixels |
|---|---|
| `512` | 512px (avatar/icon) |
| `1K` | ~1024px (default) |
| `2K` | ~2048px |
| `4K` | ~4096px (Nano Banana 2 only) |

## Prompt Construction — The 5-Part Brief

Write prompts as **natural, descriptive paragraphs** — NOT keyword soup. Nano Banana 2 is a reasoning model that understands intent, physics, and composition. A descriptive paragraph always outperforms a comma-separated tag list.

### 1. SUBJECT (Who/What)
Describe the primary subject with specificity. Name materials, textures, ages, expressions.
- BAD: "a church leader"
- GOOD: "a middle-aged man with warm brown skin and short grey hair, wearing a linen shirt, gesturing passionately while speaking"

### 2. ACTION & RELATIONSHIPS (What's Happening)
Describe scene dynamics — interaction between subjects, movement, energy.
- "leading a small group gathered in a circle on a sun-dappled patio"
- "hands resting on an open, well-worn Bible on a wooden table"

### 3. SETTING (Where, When, Atmosphere)
Place, time of day, weather, mood, cultural context.
- "in a bright, airy community hall, mid-morning golden light streaming through floor-to-ceiling windows"

### 4. STYLE & MEDIUM (Visual Language)
Name specific photographic or artistic references:
- **Photography**: "shot on Sony A7IV, 85mm f/1.4, shallow depth of field, natural light, warm color grading"
- **Illustration**: "watercolor illustration with visible brushstrokes, muted earth tones, editorial style"
- **Conceptual**: "minimalist flat illustration, geometric shapes, limited palette of warm terracotta and sage green"
- **Abstract**: "abstract texture, layered paper collage effect, warm amber and cream tones"

### 5. COMPOSITION & CAMERA (Framing)
Shot type, angle, lens behavior, negative space:
- "medium close-up, slightly off-center with rule of thirds, shallow depth of field blurring the background"
- "wide establishing shot, low angle, dramatic sky in upper third"

## Expert Prompt Techniques

### Text Rendering
Nano Banana 2 renders text in images accurately. Wrap desired text in quotes:
- "A vintage book cover with the title 'The Art of Community' in serif typography"
- Use specific font style descriptions: "bold sans-serif", "handwritten script", "engraved serif capitals"

### Character Consistency
Establish a character in the first prompt with specific details, then use follow-up prompts to place them in new contexts. Supports up to 5 characters and 14 objects per workflow.
- First: "A young woman named Aya with short curly black hair, round glasses, wearing an olive canvas jacket"
- Follow-up: "Now show Aya sitting at a desk in a library, reading a thick book under warm lamplight"

### Iterative Refinement
Do NOT re-prompt from scratch. Use conversational editing:
- "Make the lighting warmer and more golden"
- "Move the subject slightly to the left, more negative space on the right"
- "Reduce the saturation, make it feel more muted and scholarly"
- One major edit per turn. Chain 3-4 small edits for best coherence.

### Google Search Grounding
Nano Banana 2 can verify facts and pull real-time visual references before generating. Useful for:
- Accurate depictions of real locations, architecture, flora/fauna
- Current fashion, product designs, brand aesthetics

### Negative Guidance
Describe what you DON'T want sparingly and naturally:
- "The scene should feel candid, not posed or stock-photo-like"
- "Avoid harsh shadows or clinical lighting"

## Execution

### API Pattern 1 — Nano Banana 2 (Gemini Native, recommended)

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

const response = await ai.models.generateContent({
  model: "gemini-3.1-flash-image-preview",
  contents: "<THE_COMPOSED_PROMPT>",
  config: {
    responseModalities: ["image", "text"],
    imageConfig: {
      aspectRatio: "16:9",
      imageSize: "2K",
    },
  },
});

// Extract image parts from response
for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = path.join("generated", `${slug}.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### API Pattern 2 — Imagen 4 (batch generation, no editing)

```typescript
const result = await ai.models.generateImages({
  model: "imagen-4.0-generate-001",
  prompt: "<THE_COMPOSED_PROMPT>",
  config: {
    numberOfImages: 4,
    aspectRatio: "16:9",
    addWatermark: true,
    enhancePrompt: true,
    personGeneration: "allow_adult",
  },
});

for (let i = 0; i < result.generatedImages.length; i++) {
  const img = result.generatedImages[i];
  const buffer = Buffer.from(img.image.imageBytes, "base64");
  const outPath = path.join("generated", `${slug}-${i + 1}.png`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buffer);
}
```

### API Pattern 3 — Conversational Editing (Nano Banana 2)

```typescript
import * as fs from "fs";

// Read the source image
const imageBytes = fs.readFileSync("path/to/source.png");
const base64Image = imageBytes.toString("base64");

const response = await ai.models.generateContent({
  model: "gemini-3.1-flash-image-preview",
  contents: [
    {
      parts: [
        { inlineData: { mimeType: "image/png", data: base64Image } },
        { text: "Make the lighting warmer and add a soft golden hour glow" },
      ],
    },
  ],
  config: {
    responseModalities: ["image", "text"],
  },
});
```

### Step 1 — Compose the Prompt
Write the full 5-part brief prompt. Show it to the user for approval before generating.

### Step 2 — Generate
Run the appropriate API pattern. Default to Nano Banana 2 unless the user wants batch generation (Imagen 4).

### Step 3 — Save & Report
- Save images to the output directory
- Convert to WebP for production use if needed (use sharp)
- Report the file paths and let the user review

## Rate Limits & Costs

| Tier | Limit | Notes |
|---|---|---|
| Free | ~20 requests/day | Reduced from 250 in Dec 2025 |
| Paid | 500-1000 images/day | Depends on plan |
| RPM | 15 requests/minute | All tiers |

| Model | Cost/image |
|---|---|
| Nano Banana 2 (1K) | ~$0.045 |
| Nano Banana Pro | ~$0.134 |
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |
| Batch API | 50% discount |

## Content Safety

- All images include **SynthID** invisible digital watermark
- `personGeneration` options: `"dont_allow"` | `"allow_adult"` (default) | `"allow_all"`
- Safety filters block certain prompts; you are still billed for input tokens on blocked requests
- Failure rates: ~2% generic, up to 15%+ for people/fashion prompts
- No generation of specific real individuals

## Output Format

```
## Asset Generation Report

### Prompt
> [The full prompt used]

### Settings
- Model: gemini-3.1-flash-image-preview (Nano Banana 2)
- Aspect ratio: 16:9
- Resolution: 2K
- Variations: 1

### Generated Files
1. generated/hero/course-slug-1.png

### Next Steps
- Review the generated images and select the best one
- Use conversational editing to refine: "Make the lighting warmer"
- Use `/asset-text-overlay` to add text if needed
```

## Error Handling

- Missing `GOOGLE_GENERATIVE_AI_API_KEY` → stop with instructions to add it to `.env.local`
- API rate limit → wait and retry once, then report
- Content policy block → adjust prompt (remove specific person references, etc.) and retry
- Generation failure → report error details and suggest prompt modifications
- Resolution downgrade → if 2K/4K request returns 1K, note this in the report

## Rules

- Always compose the prompt using the 5-part brief method — never keyword lists
- Default to Nano Banana 2 (`gemini-3.1-flash-image-preview`) for all interactive/editing workflows
- Use Imagen 4 only for batch standalone generation
- Show the prompt to the user before generating
- Use iterative refinement, not full re-prompts
- One major edit per conversational turn
- Always report the model, settings, and file paths in the output
