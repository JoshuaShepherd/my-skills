---
name: asset-mockup
description: Place generated images into real-world context mockups — laptop screens, phone frames, book mockups, poster frames, billboard mockups. Use for marketing previews, social media content, and stakeholder presentations.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Create a device or context mockup: $ARGUMENTS

$ARGUMENTS should include:
- Path to the image to mockup (the content to place into the frame)
- Mockup type (laptop, phone, book, poster, billboard, tablet, browser, etc.)
- Optionally: scene context (desk, hand-held, coffee shop, etc.)
- Optionally: additional styling (angle, lighting, environment)
- Empty — ask the user for the image and mockup type

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read the source image to understand its content and aspect ratio
3. Read `src/lib/config/tenant.config.ts` for brand context
4. Determine the mockup type and scene

## Mockup Types

### Device Mockups

#### Laptop / MacBook
```
A realistic MacBook Pro sitting on a [clean wooden desk / marble surface / minimal white desk],
screen angled at approximately 110 degrees toward the viewer. The screen displays the
following content: [DESCRIBE THE SCREEN CONTENT OR REFERENCE IMAGE].

The laptop is positioned at a [3/4 angle from the left / straight-on / slight angle from right].
[Surrounding context: a ceramic coffee mug, a small plant, a notebook with pen — minimal,
editorial desk setup].

Warm natural lighting from a window to the left. Shallow depth of field — the laptop screen
is in sharp focus, desk accessories softly blurred. The screen shows realistic bezels and
reflections — not a flat paste, but a natural screen appearance with subtle light falloff
at the edges.

Shot on Sony A7IV, 50mm f/1.8, natural window light. Lifestyle product photography.
16:9 aspect ratio.
```

#### Phone / iPhone
```
A realistic iPhone [15 Pro / latest] held in a human hand at a natural reading angle,
or lying on a [wooden table / linen surface / marble counter]. The screen displays:
[DESCRIBE SCREEN CONTENT].

[If hand-held]: The hand is relaxed, natural grip, warm skin tones. The phone is held
at a slight angle, not perfectly flat to camera — natural viewing position.
[If flat]: The phone lies at a slight angle on the surface, not perfectly straight.

Screen shows realistic content with proper iOS status bar, rounded corners matching the
device bezels. Subtle screen reflections and light gradient.

Warm, natural lighting. [Indoor lifestyle / outdoor café / studio white background].
9:16 for full vertical, or 1:1 for social posts.
```

#### Tablet / iPad
```
A realistic iPad [Pro / Air] in [landscape / portrait] orientation, [propped on a stand /
lying on a table / held in two hands]. Screen displays: [CONTENT DESCRIPTION].

[Context: sitting on a kitchen counter, in a reading nook, on a meeting table].
Screen shows realistic bezels, home indicator bar, and subtle ambient reflections.

Natural lighting, warm tones. Product lifestyle photography.
```

#### Browser Window
```
A clean browser window (Safari or Chrome) showing a website. The browser chrome is visible:
address bar showing "[URL]", standard navigation buttons, tab bar.

The website content displayed is: [DESCRIBE OR REFERENCE THE PAGE CONTENT].

The browser window sits against a [macOS desktop with subtle wallpaper / clean solid
background]. Window has realistic shadow and rounded corners (macOS style).

Clean, technical screenshot aesthetic but with photographic quality lighting and depth.
16:9 aspect ratio.
```

### Print Mockups

#### Book (Physical)
```
A photorealistic mockup of a [hardcover / paperback] book. The cover displays:
[DESCRIBE COVER DESIGN — title, author, imagery, colors].

The book is [standing upright at a slight angle / lying flat / stacked with 2 other books].
[The spine is visible showing the title and author name].

[Setting: on a wooden bookshelf alongside other books / on a reading table / held in
someone's hands / against a white studio background].

The cover wraps realistically around the book form — you can see the slight curve at the
spine, the paper texture of the pages visible at the edges, and the way the cover material
[reflects light / shows matte texture / has embossed text].

Professional book product photography. Warm lighting, editorial feel.
[3:4 for portrait-oriented book / 16:9 for landscape scene with book].
```

#### Poster / Print
```
A framed poster or art print mounted on a [white gallery wall / brick wall / warm wooden
panel wall]. The frame is [thin black / natural wood / white gallery-style / floating frame].

The poster displays: [DESCRIBE THE POSTER CONTENT].

The frame casts a subtle shadow on the wall. The print shows realistic paper texture
behind glass — slight reflections from ambient light. Frame dimensions proportional to
a [A3 / 18x24" / 24x36"] print.

[Surrounding context: a plant in the corner, a reading chair, gallery lighting from above].

Interior photography style, warm tones, natural light supplemented by gallery spots.
16:9 or 4:3 depending on wall composition.
```

#### Billboard / Large Format
```
A photorealistic urban billboard displaying: [DESCRIBE THE BILLBOARD CONTENT].

The billboard is [mounted on a building wall / free-standing roadside / at a bus stop /
on a subway platform]. The surrounding environment is [a city street / a highway / an
urban neighborhood].

The billboard content is clearly legible despite the environmental context. Realistic
perspective distortion — the billboard surface follows the correct vanishing point.
Weather and lighting: [daylight / golden hour / night with billboard lit].

Environmental photography with realistic urban context. 16:9 aspect ratio.
```

## Execution

### Method A — NB2 Generation (Recommended)
Use Nano Banana 2 to generate the entire mockup scene with the content described in the prompt.

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// If we have the actual content image, include it as reference
const parts: any[] = [];

if (contentImagePath) {
  const imgBytes = fs.readFileSync(contentImagePath);
  parts.push({
    inlineData: { data: imgBytes.toString("base64"), mimeType: "image/png" },
  });
  parts.push({
    text: `Place the content from this image onto the screen/surface of the mockup described below. The content should appear naturally on the device/surface — with realistic perspective, reflections, and bezels. Do not alter the content itself.\n\n${MOCKUP_PROMPT}`,
  });
} else {
  parts.push({
    text: `${MOCKUP_PROMPT}\n\nGenerate this as a photorealistic image.`,
  });
}

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [{ role: "user", parts }],
  config: { responseModalities: ["image", "text"] },
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = path.join("public/images/generated/mockup", `${slug}-mockup.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Method B — Programmatic Compositing
For pixel-perfect screen placement, use sharp to composite the content image onto a device frame template.

```typescript
import sharp from "sharp";

// Requires a device frame template image with a transparent screen area
// Templates stored in public/images/mockup-frames/
async function compositeOntoDevice(
  contentPath: string,
  framePath: string,
  screenRegion: { left: number; top: number; width: number; height: number },
  outputPath: string,
) {
  const content = await sharp(contentPath)
    .resize(screenRegion.width, screenRegion.height, { fit: "cover" })
    .toBuffer();

  const result = await sharp(framePath)
    .composite([{
      input: content,
      left: screenRegion.left,
      top: screenRegion.top,
    }])
    .png()
    .toBuffer();

  fs.writeFileSync(outputPath, result);
}
```

## Brand-Aligned Scene Contexts

For the Alan Hirsch platform, default to these scene styles:

### Warm Study / Reading Nook
Wooden desk, warm lamp, books, journal, ceramic mug. Scholarly, intimate.

### Community Gathering Space
A shared table, multiple devices, notes, conversation-ready.

### Modern Minimal
Clean desk, single device, plant, natural light. Contemporary but warm.

### Outdoor / Neighborhood
Café table, park bench, community setting. Missional, outward-focused.

## Output Format

```
## Mockup Report

### Content: [Source image description]
### Device/Context: [Mockup type — e.g., MacBook on wooden desk]

### Prompt
> [Full prompt used]

### Generated Files
1. public/images/generated/mockup/forgotten-ways-laptop-mockup.png

### Scene Details
- Device: MacBook Pro, 3/4 angle from left
- Setting: Warm wooden desk, natural window light
- Context items: Coffee mug, notebook, small plant
- Aspect ratio: 16:9

### Next Steps
- Use `/asset-edit` to adjust scene details
- Use `/asset-text-overlay` to add marketing copy
- Use `/asset-brand-check` to verify brand alignment
```

## Common Mockup Workflows

| Workflow | Steps |
|----------|-------|
| Course marketing | Generate hero → `/asset-mockup` laptop showing course page → social post |
| Book launch | `/asset-product-shot` book → `/asset-mockup` physical book in scene → OG card |
| App preview | Screenshot content → `/asset-mockup` phone in hand → social story |
| Website showcase | Page screenshot → `/asset-mockup` browser window → portfolio |

## Error Recovery

| Issue | Fix |
|-------|-----|
| Content distorted on screen | Add "content appears at natural perspective, not stretched or skewed" |
| Device looks unrealistic | Specify exact device model: "iPhone 15 Pro in Natural Titanium" |
| Content not visible enough | "The screen content is the hero of the image — ensure it is clearly visible and in sharp focus" |
| Reflections obscure content | "Minimal screen reflections — the content should be fully legible" |
| Scene too busy | Reduce context items: "minimal desk setup — just the device and one small object" |
