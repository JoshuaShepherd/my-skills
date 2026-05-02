
Generate an image with text overlay using Gemini Image Generation: $ARGUMENTS

$ARGUMENTS should include:
- The text to render on the image
- Context: what the image is for (OG card, social post, banner, certificate, etc.)
- Optionally: background description or source image path for editing text onto
- Optionally: typography style preferences
- Empty — ask the user for the text and context

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `{{CONFIG_PATH}}` for brand name and tagline
3. Read `{{STYLES_PATH}}` for font family and color tokens
4. Determine the output format from the presets below

## Text Asset Presets

| Asset Type      | Dimensions       | Aspect Ratio | Text Zones                                    |
|-----------------|-----------------|-------------|-----------------------------------------------|
| `og-image`      | 1200×630        | `16:9`      | Title (large), subtitle (small), logo corner   |
| `social-square` | 1080×1080       | `1:1`       | Headline centered, attribution bottom          |
| `social-story`  | 1080×1920       | `9:16`      | Quote centered, attribution bottom             |
| `twitter-card`  | 1200×675        | `16:9`      | Title left, visual right                       |
| `banner-email`  | 600×200         | `3:1`       | Single headline centered                       |
| `banner-wide`   | 1920×480        | `4:1`       | Title left-aligned, visual right               |
| `certificate`   | 1920×1357       | `√2:1`      | Title top, recipient center, details bottom    |
| `quote-card`    | 1080×1080       | `1:1`       | Quote text centered, attribution bottom-right  |
| `chapter-title` | 1920×1080       | `16:9`      | Chapter number + title centered                |

## Text Rendering Rules for Gemini

### 1. Always Quote the Text
Enclose all desired text in double quotes within the prompt:
- GOOD: `The image should display "The {{COURSE_NAME}}" in bold serif text`
- BAD: `Write The {{COURSE_NAME}} on the image`

### 2. Specify Typography Explicitly
Name the font style, weight, size relationship, and color:
- "Bold, condensed sans-serif font similar to Oswald, white text with a subtle drop shadow"
- "Elegant serif typeface similar to Playfair Display, warm cream color ({{BRAND_LIGHT}}), italic for the subtitle"
- "Clean, modern sans-serif similar to Inter, medium weight, dark charcoal ({{BRAND_DARK}})"

### 3. Describe Placement Precisely
Use spatial language and compositional terms:
- "The title 'Formation' is centered horizontally, positioned in the upper third of the image"
- "Author name '{{AUTHOR_NAME}}' in small caps, bottom-right corner with 40px padding from edges"
- "Quote text centered vertically and horizontally, with generous margins (at least 15% from each edge)"

### 4. Describe Text Hierarchy
When multiple text elements exist, define their relationship:
- "The main title 'The {{COURSE_NAME}}' is 3x larger than the subtitle 'Reactivating Apostolic Movements'"
- "Chapter number '01' in a very large, light-opacity font behind the chapter title"

### 5. Background-Text Contrast
Always ensure readability:
- Light text on dark/image backgrounds: add text shadow or darken the background region
- Dark text on light backgrounds: ensure sufficient contrast
- "Add a semi-transparent dark gradient overlay behind the text area to ensure readability"

## Prompt Template — OG Image

```
Create a 1200x630 Open Graph image for a web page.

Background: [warm abstract texture / gradient / photograph description matching brand]

Text elements:
1. Main title: "[TITLE TEXT]" — bold, condensed sans-serif font similar to Oswald, white color, centered horizontally, positioned in the upper-middle area. Large and commanding.
2. Subtitle: "[SUBTITLE TEXT]" — regular weight sans-serif similar to Inter, warm cream color, centered below the title, smaller size (about 40% of the title size).
3. Brand mark: "[{{AUTHOR_NAME}}]" — small, bottom-left corner, clean sans-serif, warm amber color, with subtle opacity.

The background should have a warm, scholarly feel with earth tones — terracotta, amber, and sage. Add a subtle dark gradient overlay in the text area for contrast. The overall composition should feel editorial and refined, not corporate.
```

## Prompt Template — Quote Card

```
Create a 1080x1080 square quote card.

Background: warm, muted textured background — aged paper or linen texture in cream and soft amber tones.

Text: "[THE QUOTE TEXT]" — serif typeface similar to Playfair Display, dark charcoal color ({{BRAND_DARK}}), centered both vertically and horizontally, with generous margins (at least 120px from each edge). The text should be large enough to read easily at social media thumbnail size.

Attribution: "— {{AUTHOR_NAME}}" — smaller sans-serif font, warm terracotta color, right-aligned, below the quote with 24px spacing.

Add subtle decorative quotation marks (") in very large, light-opacity warm amber behind the quote text. The overall feel should be warm, scholarly, and inviting.
```

## Execution

### Step 1 — Compose the Prompt
Build the full prompt using the templates above, customized for the user's content. Show the prompt to the user for approval.

### Step 2 — Generate
```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// For text-on-image generation, use Gemini multimodal
const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: "<THE_COMPOSED_PROMPT>. Generate this as an image.",
  config: {
    responseModalities: ["image", "text"],
  },
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = path.join("{{OUTPUT_DIR}}/text", `${slug}.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 3 — Verify Text Accuracy
After generation, verify:
- Text is spelled correctly (Gemini is good but not perfect)
- Text is legible at the target display size
- Contrast meets WCAG AA (4.5:1 for body text)
- If text is wrong, refine: "The text should read '[CORRECT TEXT]' — currently it shows '[WRONG TEXT]', please fix the spelling"

### Step 4 — Text Editing on Existing Images
To add text to an existing image:
```typescript
const imageBytes = fs.readFileSync("<SOURCE_IMAGE_PATH>");
const base64Image = imageBytes.toString("base64");

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [
    {
      role: "user",
      parts: [
        { inlineData: { data: base64Image, mimeType: "image/png" } },
        { text: "Add the text '[TEXT]' to this image. [TYPOGRAPHY AND PLACEMENT INSTRUCTIONS]" },
      ],
    },
  ],
  config: {
    responseModalities: ["image", "text"],
  },
});
```

## Output Format

```
## Text Overlay Report

### Asset Type: OG Image (1200×630)

### Text Content
- Title: "The {{COURSE_NAME}}"
- Subtitle: "Reactivating Apostolic Movements"
- Brand: "{{AUTHOR_NAME}}"

### Prompt
> [Full prompt used]

### Generated Files
1. {{OUTPUT_DIR}}/text/{{course-slug}}-og.png

### Text Verification
- ✅ Title text accurate
- ✅ Subtitle text accurate
- ✅ Brand text accurate
- ✅ Contrast sufficient

### Next Steps
- Review the generated image
- Use `/asset-edit` to refine colors/composition
- If text has errors, request a refinement pass
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Misspelled text | Re-prompt with explicit correction: "Fix the spelling — it should read '[CORRECT]'" |
| Text too small | "Make the title text approximately 2x larger" |
| Poor contrast | "Add a semi-transparent dark overlay (50% opacity black) behind the text area" |
| Text cut off at edges | "Increase margins around the text to at least 15% of the image dimensions on each side" |
| Wrong font style | Be more specific: "Use a bold, condensed grotesque sans-serif — NOT a rounded or decorative font" |
