---
name: asset-series
description: Generate a visually consistent set of image assets using Nano Banana 2. Use for course module covers, book chapter headers, video series thumbnails, or any batch that needs visual continuity.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Generate a consistent asset series using Nano Banana 2: $ARGUMENTS

$ARGUMENTS should include:
- The series concept (e.g., "8 course module covers for The Forgotten Ways")
- List of individual items with titles/descriptions
- Optionally: a reference image for style consistency
- Optionally: asset type preset (see asset-generate for presets)
- Empty — ask the user for the series concept and item list

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `src/lib/config/tenant.config.ts` for brand context
3. Read `src/app/globals.css` for design tokens
4. If generating course covers, read relevant course data from the database or content files
5. Understand the series scope — how many items, what they represent

## Series Types

### Course Module Covers (8 per course)
- One cover per week/module
- Consistent layout, varying subject/imagery per module topic
- Module number visible
- Course title consistent across all

### Book Chapter Headers
- One per chapter
- Consistent framing, varying visual motif per chapter theme
- Chapter number and title

### Video Series Thumbnails
- One per episode
- Consistent template, varying episode-specific elements
- Episode number, title, speaker

### Article Series Cards
- One per article in a thematic series
- Consistent card layout, varying hero imagery
- Article title and category

### Podcast Episode Artwork
- One per episode or season
- Consistent framing with episode-specific variations
- Episode number, guest name if applicable

## Consistency Framework

NB2 supports up to 5 character consistency and 14 object tracking. Use these features to maintain visual continuity:

### 1. Define a Style Anchor
Create a detailed style description that stays constant across all items:

```
STYLE ANCHOR (use for every item in this series):
- Medium: editorial photography style, shot on Sony A7IV, 85mm f/1.4
- Lighting: warm golden-hour side lighting, soft shadows
- Color palette: warm earth tones — terracotta (#C75B39), sage (#87A878), amber (#D4A84B), cream (#FAF5E4)
- Texture: subtle film grain, slightly warm color grade
- Composition: subject occupies the left 60%, negative space on right for text overlay
- Mood: warm, contemplative, inviting
```

### 2. Define Variable Elements
For each item in the series, only vary the subject/motif:

```
ITEM 1 — "Missional Renaissance"
- Subject: an open compass lying on a hand-drawn map, with a small seedling growing beside it

ITEM 2 — "The DNA of Movement"
- Subject: a close-up of interwoven threads in warm earth colors, suggesting organic connection

ITEM 3 — "Apostolic Genius"
- Subject: a circle of diverse hands holding a shared piece of bread over a wooden table
```

### 3. Use Reference Images
If a first generation looks perfect, use it as a reference for subsequent items:
```
"Generate an image in the exact same style, lighting, color palette, and composition as the reference image, but change the subject to [NEW SUBJECT]"
```

## Execution

### Step 1 — Define the Series Brief
Create a structured brief:

```markdown
## Series: [SERIES NAME]
### Style Anchor
[Constant style description — medium, lighting, palette, mood, composition]

### Items
1. [TITLE] — [Subject/motif description]
2. [TITLE] — [Subject/motif description]
...
```

Show the brief to the user for approval.

### Step 2 — Generate the First Item
Generate item 1 with the full style anchor + item-specific description. This establishes the visual baseline.

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// Generate first item to establish style
const firstResult = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: `${STYLE_ANCHOR}\n\n${ITEM_1_DESCRIPTION}\n\nGenerate this as an image.`,
  config: {
    responseModalities: ["image", "text"],
  },
});

// Save first image
let firstImageBase64: string;
for (const part of firstResult.candidates[0].content.parts) {
  if (part.inlineData) {
    firstImageBase64 = part.inlineData.data;
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.mkdirSync("public/images/generated/series/<series-slug>", { recursive: true });
    fs.writeFileSync("public/images/generated/series/<series-slug>/01-<item-slug>.png", buffer);
  }
}
```

### Step 3 — User Review of Baseline
Show the first image to the user. If approved, proceed. If not, refine until the style baseline is locked.

### Step 4 — Generate Remaining Items with Reference
Use the approved first image as a style reference for all subsequent items:

```typescript
// For items 2..N, include the first image as a style reference
for (let i = 1; i < items.length; i++) {
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash-exp",
    contents: [
      {
        role: "user",
        parts: [
          { inlineData: { data: firstImageBase64, mimeType: "image/png" } },
          {
            text: `This is a reference image for style, lighting, color palette, and composition. Generate a NEW image in the EXACT SAME visual style, but with a different subject:\n\n${STYLE_ANCHOR}\n\nSubject for this item: ${items[i].description}\n\nMaintain identical: color palette, lighting direction, film grain, composition layout, and mood. Only change the subject matter.`,
          },
        ],
      },
    ],
    config: {
      responseModalities: ["image", "text"],
    },
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
      const buffer = Buffer.from(part.inlineData.data, "base64");
      const num = String(i + 1).padStart(2, "0");
      fs.writeFileSync(
        `public/images/generated/series/<series-slug>/${num}-${items[i].slug}.png`,
        buffer
      );
    }
  }
}
```

### Step 5 — Review & Refinement Pass
After generating all items, review as a set. Common refinements:
- "Item 3 is too cool/blue — warm it up to match the others"
- "Item 5's composition is too centered — shift subject left to match the series layout"
- "The grain texture is inconsistent on item 7 — match item 1's grain level"

## Output Format

```
## Asset Series Report

### Series: The Forgotten Ways — Course Module Covers
### Items: 8 modules
### Style: Editorial photography, warm earth tones, golden-hour lighting

### Style Anchor
> [The full style anchor description]

### Generated Files
| # | Title | File | Status |
|---|-------|------|--------|
| 01 | Missional Renaissance | public/images/generated/series/forgotten-ways/01-missional-renaissance.png | ✅ |
| 02 | The DNA of Movement | public/images/generated/series/forgotten-ways/02-dna-of-movement.png | ✅ |
| 03 | Apostolic Genius | public/images/generated/series/forgotten-ways/03-apostolic-genius.png | ✅ |
| ... | ... | ... | ... |

### Consistency Check
- ✅ Color palette consistent across all 8 items
- ✅ Lighting direction consistent
- ✅ Composition layout consistent
- ⚠️ Item 5 grain slightly heavier — consider refinement
- ✅ Text placement zones consistent

### Next Steps
- Review all items as a set
- Use `/asset-edit` for individual refinements
- Use `/asset-text-overlay` to add module numbers/titles
```

## Naming Convention

```
public/images/generated/series/<series-slug>/
  01-<item-slug>.png
  02-<item-slug>.png
  ...
```

## Tips for Best Consistency

1. **Generate the hero item first** — spend time getting item 1 perfect before batch generating
2. **Use the same style anchor verbatim** — copy-paste, don't paraphrase
3. **Reference the first image** — always include it as a reference for subsequent generations
4. **Review as a grid** — consistency issues are obvious when viewed side-by-side
5. **Fix outliers immediately** — regenerate inconsistent items before moving on
6. **Limit variation to one dimension** — only change the subject; keep everything else identical
