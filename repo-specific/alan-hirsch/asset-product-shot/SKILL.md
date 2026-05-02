---
name: asset-product-shot
description: Generate clean product/object photography prompts using Nano Banana 2. Use for book mockups, course materials, merchandise, or any object that needs a professional studio-quality shot on white or contextual background.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Generate a product photography shot using Nano Banana 2: $ARGUMENTS

$ARGUMENTS should include:
- The object to photograph (book, journal, workbook, merchandise, device, etc.)
- Optionally: background style (white, contextual, lifestyle)
- Optionally: camera angle and lighting preferences
- Optionally: whether this is for scroll-stop (paired with exploded-view)
- Empty — ask the user what product/object to shoot

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `src/lib/config/tenant.config.ts` for brand context
3. Determine the object category and select the appropriate shot template

## Shot Styles

### 1. Clean White — Hero Product Shot
Pure white (#FFFFFF) background, studio lighting, catalog quality. Best for:
- E-commerce listings
- Start frames for scroll-stop video
- Product comparison layouts
- Clean web assets

### 2. Contextual — Lifestyle Setting
Object placed in a real-world context that reinforces brand. Best for:
- Social media content
- Blog/article headers
- Course marketing imagery

### 3. Flat Lay — Overhead Arrangement
Bird's-eye view, object with related items arranged artfully. Best for:
- Resource collections
- Course materials overview
- "What's included" imagery

### 4. Detail / Macro — Texture Close-Up
Extreme close-up on material, texture, or typography. Best for:
- Quality-signaling imagery
- Book interior/typography showcases
- Tactile material emphasis

## Object-Specific Templates

### Books

```
BOOK — CLEAN WHITE

Professional product photography of a hardcover book titled "[TITLE]" by [AUTHOR].
The book is positioned at a [3/4 front-facing / slightly angled / standing upright] angle
on a pure white background (#FFFFFF).

Cover design: [describe the cover — colors, imagery, typography style, finish (matte/gloss)].
The book is [closed / slightly fanned / standing with pages visible from the side].
[Dust jacket visible / no dust jacket — cloth binding].

Spine text clearly readable: "[TITLE]" and "[AUTHOR]" in [font description].
Page edges visible, showing [cream/white] paper stock. The book looks substantial —
approximately [X] pages thick.

Soft studio lighting from upper-left with a large softbox, subtle shadow beneath and to
the right of the book. No harsh reflections. Clean, minimal, editorial product photography.

Shot on Phase One IQ4 150MP, 90mm lens, f/8, focus-stacked for edge-to-edge sharpness.
16:9 aspect ratio. 8K quality.
```

```
BOOK — LIFESTYLE CONTEXT

A well-loved copy of "[TITLE]" by [AUTHOR] resting on a [weathered wooden table /
linen tablecloth / leather-topped desk]. The book is [open to a marked page / closed with
a bookmark ribbon visible / stacked with 2-3 other books].

Surrounding context: [a ceramic mug of coffee / reading glasses / a journal with handwritten
notes / a warm lamp casting golden light / a small potted plant]. The scene feels lived-in,
scholarly, warm — a space where ideas are explored.

Natural window light from the left, warm color temperature. Shallow depth of field —
the book is in sharp focus, surrounding objects softly blurred. Warm earth tones throughout:
cream, amber, walnut, sage.

Shot on Sony A7IV, 50mm f/1.4, natural light. Editorial lifestyle photography.
16:9 aspect ratio.
```

### Journals / Workbooks

```
JOURNAL — FLAT LAY

Overhead flat-lay photography of a [leather-bound / linen-covered / kraft paper] journal
titled "[TITLE]" centered in frame on a [wooden / marble / linen] surface.

The journal is [closed / open to a page with handwritten notes and sketches]. Surrounding
items arranged artfully: [a quality pen (uncapped) / colored pencils / sticky note tabs /
a small stack of reference cards / a pair of reading glasses / a sprig of dried lavender].

Consistent spacing between objects (2-3cm gaps). The arrangement follows a balanced,
editorial composition — not cluttered, not sparse. Each item is positioned with intentional
angles, nothing perfectly parallel.

Soft, even overhead lighting with no harsh shadows. Warm white balance. The overall feel
is curated but authentic — a real working space, not a catalog setup.

Shot overhead on a copy stand, 35mm equivalent, f/5.6 for even sharpness.
1:1 aspect ratio for social, or 16:9 for web headers.
```

### Course Materials / Resource Collections

```
COURSE MATERIALS — ARRANGED SET

Professional flat-lay of a course resource kit for "[COURSE TITLE]":

Central item: [the main workbook/guide, prominently placed].
Surrounding items (arranged in a balanced composition):
- [A smaller companion booklet or quick-reference card]
- [Printed assessment or reflection worksheet]
- [A branded bookmark or postcard]
- [A quality pen]
- [Optional: USB drive, certificate preview, stickers]

All items use a consistent visual language: [warm earth tones / clean minimal design /
hand-illustrated elements]. The arrangement suggests completeness — everything you need
for the learning journey.

White or warm cream background. Soft overhead lighting, minimal shadows.
Styled with 2-3cm spacing between items, nothing overlapping.

Shot overhead, focus-stacked, even sharpness throughout.
16:9 aspect ratio.
```

### Physical Merchandise

```
MERCH — CLEAN PRODUCT

Professional product photography of a [t-shirt / mug / tote bag / hat] featuring
[design description — graphic, text, logo, pattern].

The item is [laid flat / on a mannequin torso / floating against white background /
hung on a wooden hanger]. [For mugs: 3/4 angle showing both the graphic and the handle].

Material details visible: [cotton texture / ceramic gloss / canvas weave]. The [print/
embroidery/screen print] is crisp and well-defined.

Clean white background, studio lighting with soft shadows. Product photography style —
accurate color representation, no excessive post-processing.

Shot on [appropriate camera], 85mm, f/8, product photography lighting setup.
1:1 for product listings, 16:9 for web banners.
```

## Camera & Lighting Presets

| Style | Camera | Lens | Aperture | Lighting | Notes |
|-------|--------|------|----------|----------|-------|
| Clean White | Phase One IQ4 | 90mm macro | f/8 | Large softbox above + white bounce cards | Focus-stacked, pure white BG |
| Lifestyle | Sony A7IV | 50mm | f/1.4–f/2.8 | Natural window light, warm | Shallow DOF, warm grade |
| Flat Lay | Copy stand rig | 35mm equiv | f/5.6 | Even overhead panel | Even sharpness edge-to-edge |
| Detail/Macro | Sony A7RV | 90mm macro | f/4–f/5.6 | Diffused side light | Focus-stacked, extreme detail |
| Dramatic | Phase One | 120mm | f/4 | Single key light + negative fill | Moody shadows, editorial |

## Execution

### Step 1 — Identify the Object & Style
Determine what's being shot and which template fits. If the object doesn't match any template, adapt the closest one.

### Step 2 — Compose the Prompt
Build the full prompt from the appropriate template. Customize:
- Object-specific details (title, colors, materials)
- Brand-appropriate styling (warm earth tones for Alan Hirsch)
- Camera and lighting setup
- Aspect ratio for intended use

Show prompt to user for approval.

### Step 3 — Generate via NB2
```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: `${PRODUCT_SHOT_PROMPT}. Generate this as a photorealistic product photograph.`,
  config: {
    responseModalities: ["image", "text"],
  },
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = path.join("public/images/generated/product", `${slug}.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 4 — Review & Refine
If the shot needs adjustment, use `/asset-edit` for refinements:
- "Adjust the shadow direction — light should come from upper-left"
- "Make the book cover colors warmer"
- "Remove the slight reflection on the surface"

## Output Format

```
## Product Shot Report

### Object: [OBJECT DESCRIPTION]
### Style: [Clean White / Lifestyle / Flat Lay / Detail]

### Prompt
> [Full prompt used]

### Settings
- Aspect ratio: 16:9
- Camera style: Phase One IQ4, 90mm, f/8
- Lighting: Soft studio, upper-left key
- Background: Pure white (#FFFFFF)

### Generated Files
1. public/images/generated/product/mdna-book-1.png

### Next Steps
- Review and select
- Use `/asset-edit` to refine
- Use `/asset-exploded-view` to create a deconstructed version
- Use `/asset-video-prompt` to animate between assembled and exploded states
```

## Scroll-Stop Pairing

When generating a product shot for scroll-stop content:
1. Generate the clean white product shot here (start frame)
2. Use `/asset-exploded-view` to generate the deconstructed version (end frame)
3. Use `/asset-video-prompt` to create the transition animation prompt
4. Use `/asset-deliver` to package all prompts in a polished HTML page
