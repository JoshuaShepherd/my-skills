---
name: asset-composite
description: Combine multiple generated images into a single composite — grids, collages, mood boards, before/after comparisons, or series overviews. Use when reviewing batches, creating mood boards, or building multi-image marketing assets.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Create a composite image from multiple sources: $ARGUMENTS

$ARGUMENTS should include:
- Paths to the images to composite (files or a directory)
- Layout style (grid, collage, comparison, mood-board, strip)
- Optionally: output dimensions and aspect ratio
- Optionally: labels, captions, or overlay text
- Empty — ask the user for the images and layout

## Before Starting

1. Verify all source images exist
2. Check if `sharp` is installed (`pnpm list sharp`) — install if needed for programmatic compositing
3. Read `src/lib/config/tenant.config.ts` for brand context (labels, colors)
4. Determine the layout type

## Layout Types

### 1. Grid — Equal-Size Tiles
All images at the same size in a regular grid. Best for:
- Series overview (8 course module covers in a 4×2 grid)
- Variant comparison (4 generated options side by side)
- Social media carousel preview

### 2. Collage — Mixed Sizes
Featured image large, supporting images smaller. Best for:
- Mood boards
- Marketing assets
- Visual direction presentations

### 3. Before/After — Side by Side
Two images split horizontally or vertically. Best for:
- Edit comparisons
- Brand-check before/after
- Style transfer demonstrations

### 4. Mood Board — Freeform
Images, color swatches, typography samples, and text labels arranged organically. Best for:
- Design direction proposals
- Brand visual language exploration
- Creative briefs

### 5. Strip — Horizontal or Vertical Sequence
Images in a single row or column, suggesting sequence or progression. Best for:
- Storyboard frames
- Course module progression
- Timeline visualizations

## Execution Methods

### Method A — NB2 Compositing (AI-Assembled)
Use Nano Banana 2 to compose images together with AI understanding of layout and aesthetics.

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// Load all source images
const imageParts = imagePaths.map((p) => ({
  inlineData: {
    data: fs.readFileSync(p).toString("base64"),
    mimeType: p.endsWith(".png") ? "image/png" : "image/jpeg",
  },
}));

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [
    {
      role: "user",
      parts: [
        ...imageParts,
        {
          text: `Arrange these ${imagePaths.length} images into a ${LAYOUT_TYPE} layout. ${LAYOUT_INSTRUCTIONS}. Generate this as a single composite image.`,
        },
      ],
    },
  ],
  config: { responseModalities: ["image", "text"] },
});
```

### Method B — Programmatic Compositing (Sharp)
Use the `sharp` library for pixel-perfect, deterministic layouts.

```typescript
import sharp from "sharp";
import * as fs from "fs";
import * as path from "path";

// Grid layout
async function createGrid(
  imagePaths: string[],
  columns: number,
  cellSize: number,
  gap: number,
  bgColor: string = "#FFFFFF"
) {
  const rows = Math.ceil(imagePaths.length / columns);
  const width = columns * cellSize + (columns - 1) * gap;
  const height = rows * cellSize + (rows - 1) * gap;

  // Create base canvas
  const canvas = sharp({
    create: {
      width,
      height,
      channels: 4,
      background: bgColor,
    },
  });

  // Resize and position each image
  const composites = await Promise.all(
    imagePaths.map(async (imgPath, i) => {
      const col = i % columns;
      const row = Math.floor(i / columns);
      const resized = await sharp(imgPath)
        .resize(cellSize, cellSize, { fit: "cover" })
        .toBuffer();
      return {
        input: resized,
        left: col * (cellSize + gap),
        top: row * (cellSize + gap),
      };
    })
  );

  const result = await canvas.composite(composites).png().toBuffer();
  return result;
}

// Before/After comparison
async function createComparison(
  beforePath: string,
  afterPath: string,
  width: number = 2400,
  height: number = 1200,
  gap: number = 4,
  labelBefore: string = "Before",
  labelAfter: string = "After"
) {
  const halfWidth = Math.floor((width - gap) / 2);

  const before = await sharp(beforePath)
    .resize(halfWidth, height, { fit: "cover" })
    .toBuffer();
  const after = await sharp(afterPath)
    .resize(halfWidth, height, { fit: "cover" })
    .toBuffer();

  const canvas = sharp({
    create: { width, height, channels: 4, background: "#1a1a1a" },
  });

  const result = await canvas
    .composite([
      { input: before, left: 0, top: 0 },
      { input: after, left: halfWidth + gap, top: 0 },
    ])
    .png()
    .toBuffer();
  return result;
}

// Strip layout (horizontal)
async function createStrip(
  imagePaths: string[],
  cellHeight: number = 600,
  gap: number = 8
) {
  const cellWidth = Math.round(cellHeight * (16 / 9)); // assume 16:9 cells
  const totalWidth = imagePaths.length * cellWidth + (imagePaths.length - 1) * gap;

  const composites = await Promise.all(
    imagePaths.map(async (imgPath, i) => {
      const resized = await sharp(imgPath)
        .resize(cellWidth, cellHeight, { fit: "cover" })
        .toBuffer();
      return {
        input: resized,
        left: i * (cellWidth + gap),
        top: 0,
      };
    })
  );

  const canvas = sharp({
    create: { width: totalWidth, height: cellHeight, channels: 4, background: "#FFFFFF" },
  });

  return canvas.composite(composites).png().toBuffer();
}
```

### Method C — HTML/CSS Composite (Browser Render)
For complex layouts with text labels, use an HTML page rendered via a headless browser.

```typescript
// Build an HTML layout, then screenshot it using the chrome-devtools MCP
// This approach supports text labels, custom fonts, and complex styling

const html = `
<div style="display: grid; grid-template-columns: repeat(${columns}, 1fr); gap: ${gap}px; padding: ${gap}px; background: ${bgColor};">
  ${imagePaths.map((p, i) => `
    <div style="position: relative; aspect-ratio: 16/9; overflow: hidden; border-radius: 8px;">
      <img src="file://${path.resolve(p)}" style="width: 100%; height: 100%; object-fit: cover;" />
      ${labels?.[i] ? `<div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px 12px; background: rgba(0,0,0,0.6); color: white; font-family: Inter, sans-serif; font-size: 14px;">${labels[i]}</div>` : ""}
    </div>
  `).join("")}
</div>
`;
```

## Preset Configurations

| Layout | Columns | Cell Size | Gap | Output Size | Best For |
|--------|---------|-----------|-----|-------------|----------|
| `grid-2x2` | 2 | 800px | 8px | 1608×1608 | 4 variants, social |
| `grid-4x2` | 4 | 500px | 8px | 2024×1008 | 8 module covers |
| `grid-3x3` | 3 | 600px | 8px | 1816×1816 | 9-item collection |
| `comparison` | 2 | 1200×800 | 4px | 2404×800 | Before/after |
| `strip-h` | N | 600×337 | 8px | varies | Storyboard |
| `strip-v` | 1 | 800×450 | 8px | 800×varies | Vertical scroll |
| `mood-3` | featured+2 | mixed | 12px | 2000×1200 | Mood board |

## Output Format

```
## Composite Report

### Layout: Grid (4×2)
### Source Images: 8 files from public/images/generated/series/forgotten-ways/
### Output: public/images/generated/composite/forgotten-ways-overview.png

### Composition
| Position | Source File | Label |
|----------|-----------|-------|
| (1,1) | 01-missional-renaissance.png | Week 1 |
| (1,2) | 02-dna-of-movement.png | Week 2 |
| ... | ... | ... |

### Settings
- Cell size: 500×500px
- Gap: 8px
- Background: #FFFFFF
- Labels: Module titles, bottom overlay
- Total output: 2024×1008px

### Next Steps
- Use `/asset-brand-check` to audit the composite
- Use `/asset-deliver` to package for sharing
- Individual images can be refined with `/asset-edit`
```

## Dependencies

If using programmatic compositing (Method B), ensure `sharp` is installed:
```bash
pnpm add sharp
```

For HTML rendering (Method C), the chrome-devtools MCP server must be available.

## Error Recovery

| Issue | Fix |
|-------|-----|
| Images different sizes | Sharp `resize` with `fit: "cover"` normalizes all images |
| Missing image in set | Skip the slot or fill with a placeholder with the label "Coming Soon" |
| Output too large | Reduce cell size or output resolution |
| Labels cut off | Increase label area padding, reduce font size |
| Color inconsistency across grid | Run `/asset-brand-check` on individual images first |
