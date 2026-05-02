---
name: asset-exploded-view
description: Generate deconstructed/exploded view prompts using Nano Banana 2. Use for scroll-stop content, framework visualizations, concept illustrations, or any object elegantly taken apart into its components.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Generate an exploded/deconstructed view using Nano Banana 2: $ARGUMENTS

$ARGUMENTS should include:
- The object or concept to deconstruct
- Optionally: reference image path of the assembled version (for consistency)
- Optionally: explosion style (mechanical, organic, conceptual)
- Optionally: background (white, contextual)
- Empty — ask the user for the object

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `src/lib/config/tenant.config.ts` for brand context
3. If a reference image exists (assembled version), read it for visual matching
4. Research the real components of the object — accuracy sells realism

## Explosion Styles

### 1. Mechanical Exploded View
Classic engineering/technical illustration style. Components separate along a single axis,
maintaining their spatial relationships. Each piece floats with even spacing.
- Best for: physical products, devices, books, tools
- Feel: precise, technical, satisfying

### 2. Organic Explosion
Components burst outward dynamically — freeze-frame of an explosion. Liquid splashes,
particles scatter, ingredients fly. High-speed photography aesthetic.
- Best for: food, beverages, natural objects, ingredients
- Feel: dramatic, energetic, appetizing

### 3. Conceptual Deconstruction
Abstract representation of a concept broken into its elements. Not a literal physical
deconstruction but a visual metaphor.
- Best for: frameworks (5Q, APEST), theological concepts, course modules
- Feel: editorial, intellectual, diagrammatic

### 4. Layered Peel
Components peel away in layers, like an onion or geological cross-section. Each layer
reveals what's beneath.
- Best for: processes, systems with depth/layers, organizational structures
- Feel: revelatory, educational, sequential

## Component Research

**Critical**: Don't fabricate components. Use real parts for physical objects. For conceptual
deconstructions, use the actual framework elements.

### Physical Object Components

#### Book
- Dust jacket (if hardcover)
- Front cover board
- Back cover board
- Spine piece
- Cloth/paper covering material
- Endpapers (front and back)
- Text block (fanned pages)
- Headbands (top and bottom)
- Bookmark ribbon
- Binding thread/stitching
- Glue/adhesive layer
- Individual signatures (gathered page sets)

#### Journal / Workbook
- Cover (front and back)
- Spiral binding or stitched spine
- Tab dividers
- Printed pages (various section types)
- Pockets / folders
- Elastic closure band
- Pen loop
- Bookmark ribbon

#### Course Resource Kit
- Main workbook
- Quick-reference cards
- Assessment sheets
- Reflection journal
- Certificate template
- Bookmark / postcard
- Branded pen
- USB/digital access card
- Packaging / box

### Conceptual Framework Components

#### 5Q / APEST Framework (Alan Hirsch)
- Apostle element (pioneering, visionary)
- Prophet element (truth, justice, alignment)
- Evangelist element (communication, invitation)
- Shepherd element (care, community, protection)
- Teacher element (wisdom, understanding, training)

#### Missional DNA (mDNA)
- Jesus is Lord
- Disciple-making
- Missional-incarnational impulse
- Apostolic environment
- Organic systems
- Communitas (not community)

#### Formation Journey
- Scripture engagement
- Community practice
- Missional action
- Reflective integration
- Assessment checkpoints

## Prompt Template — Mechanical Exploded View

```
Professional exploded-view product photography of a [OBJECT], elegantly deconstructed
into its individual components, all floating in space against a [clean white background
(#FFFFFF) / warm cream background / dark charcoal background].

Every component is visible and separated:
[LIST EACH COMPONENT ON ITS OWN LINE — 8-15 COMPONENTS]

Each piece floats with even spacing (approximately 2-4cm visual gap between components),
maintaining the general spatial relationship of where they sit in the assembled [OBJECT].
The arrangement follows a [vertical / diagonal / radial] explosion axis.

[COMPONENT-SPECIFIC DETAILS]:
- [Material/texture details for key components]
- [Small details that sell realism: screws arranged neatly, thread visible, etc.]
- [Color consistency with the assembled version]

Soft studio lighting with subtle individual shadows on each floating piece. Components
are pristine and detailed. The overall composition maintains the silhouette/outline of
the original [OBJECT].

Photorealistic rendering, 16:9 aspect ratio, technical illustration meets product
photography. Shot on Phase One IQ4 150MP, focus-stacked for sharpness across all
floating elements. [Same lighting setup as the assembled shot for visual continuity
— if reference image provided].
```

## Prompt Template — Organic Explosion (Food/Beverage)

```
Dramatic high-speed freeze-frame photography of a [FOOD/BEVERAGE] in mid-explosion.

The [glass/bowl/plate] shatters or tips, and every ingredient erupts outward in a
spectacular freeze-frame moment:
[LIST EACH INGREDIENT/ELEMENT]

Each element is captured in sharp, crystalline detail — frozen in motion at 1/10000s
shutter speed. Liquid forms elegant splashes and ribbons. Solid ingredients tumble with
natural rotation. [Ice cubes / crumbs / herbs / garnishes] scatter at the periphery.

The explosion radiates outward from the center, creating a dynamic circular composition.
Every element is lit individually — you can see textures, droplets, and fine details.

Clean [white / dark] background. Studio flash lighting frozen action. Hyper-real detail.
No motion blur — everything is tack-sharp despite the chaos.

Shot at 1/10000s, Phase One IQ4, 120mm macro, f/11, high-speed sync flash.
16:9 aspect ratio, 4K+ resolution.
```

## Prompt Template — Conceptual Deconstruction

```
An elegant conceptual illustration deconstructing the [FRAMEWORK/CONCEPT NAME] into
its [N] core elements, presented as a sophisticated exploded diagram.

Each element is represented as a distinct visual object:
[LIST EACH ELEMENT WITH ITS VISUAL REPRESENTATION]
- "[ELEMENT 1]" — represented as [visual metaphor, e.g., a compass, a flame, a bridge]
- "[ELEMENT 2]" — represented as [visual metaphor]
- ...

The elements are arranged in a [circular / vertical / radial / network] layout,
floating against a warm cream background with subtle paper texture. Fine lines or
threads connect related elements, suggesting their interdependence.

Each element uses a distinct color from the brand palette:
[terracotta for X, sage for Y, amber for Z, etc.]

Typography: Each element is labeled in clean sans-serif text (similar to Inter),
with the framework title "[FRAMEWORK NAME]" in elegant serif (similar to Playfair Display)
centered above or below the arrangement.

Style: editorial illustration, sophisticated infographic meets art print. Warm,
scholarly, inviting — not clinical or corporate. Think Monocle magazine meets
theological journal.

16:9 aspect ratio for web headers, or 1:1 for social media.
```

## Execution

### Step 1 — Identify Object & Components
Research or confirm the real components. List 8-15 items for physical objects,
or the actual framework elements for conceptual deconstructions.

### Step 2 — Match Assembled Version (if exists)
If the user has an assembled product shot (from `/asset-product-shot`):
- Match the camera angle, lighting direction, and color palette exactly
- Add "match the lighting, angle, and color palette of the reference image" to the prompt
- Include the reference image in the API call

### Step 3 — Compose & Generate

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// If reference image exists, include it
const parts: any[] = [];
if (referenceImagePath) {
  const refBytes = fs.readFileSync(referenceImagePath);
  parts.push({
    inlineData: { data: refBytes.toString("base64"), mimeType: "image/png" },
  });
  parts.push({
    text: `This is the assembled version of the object. Generate an exploded/deconstructed view of this same object, matching the lighting, camera angle, and color palette exactly.\n\n${EXPLODED_PROMPT}`,
  });
} else {
  parts.push({ text: `${EXPLODED_PROMPT}\n\nGenerate this as a photorealistic image.` });
}

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [{ role: "user", parts }],
  config: { responseModalities: ["image", "text"] },
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = path.join("public/images/generated/exploded", `${slug}-exploded.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 4 — Review & Refine
Common refinements:
- "Increase spacing between components — they're too close together"
- "The [component] is missing — add it floating at the [position]"
- "Rotate the [component] slightly so the [detail] is visible"
- "Match the lighting direction to the assembled version — light from upper-left"

## Output Format

```
## Exploded View Report

### Object: [OBJECT]
### Style: [Mechanical / Organic / Conceptual / Layered]
### Components: [N] elements

### Component List
1. [Component 1]
2. [Component 2]
...

### Prompt
> [Full prompt used]

### Reference Image
- [Path to assembled version, or "none"]

### Generated Files
1. public/images/generated/exploded/forgotten-ways-book-exploded.png

### Scroll-Stop Workflow
- ✅ Exploded view generated
- Use `/asset-video-prompt` to create the transition animation
- Use `/asset-deliver` to package all prompts

### Next Steps
- Review the exploded view
- Use `/asset-edit` to refine component positions or details
- Pair with the assembled version for video transition
```

## Error Recovery

| Issue | Fix |
|-------|-----|
| Components overlap | "Increase spacing between all components to at least 3cm visual gap" |
| Missing component | "Add [component] floating at [position] in the arrangement" |
| Inconsistent lighting vs assembled | Include assembled image as reference, add "match lighting exactly" |
| Explosion axis unclear | Specify explicitly: "all components separate along a single vertical axis" |
| Background not pure white | "Pure white #FFFFFF background, no gradient, no vignette, no shadow on background" |
| Components look like different object | Include assembled reference, add "these are components of the exact object shown" |
