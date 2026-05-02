
Create a hero portrait image from an existing author photo: $ARGUMENTS

$ARGUMENTS should include:
- Path or URL to the source author photo
- Hero context: which page/section this is for (home, about, course, article, landing, podcast)
- Optionally: composition style (split, full-bleed, overlay, cinematic, editorial)
- Optionally: mood/atmosphere override
- Optionally: text placement zone needs (left, right, center, bottom)
- Empty — ask the user for the source photo and page context

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `{{CONFIG_PATH}}` — check current `hero.imageUrl` and `hero.backgroundImageUrl`
3. Read the source image to understand current crop, quality, and expression
4. Check for author style guide at `{{ASSET_DOCS_DIR}}/author-style-guide.md`
5. Determine the hero composition style from the templates below

## Hero Compositions

### 1. Split Composition (Current Home Page Pattern)
Author portrait on one side, content/text on the other. The hero image needs generous
negative space for text placement.

```
SPLIT HERO — AUTHOR LEFT, TEXT RIGHT

Take this portrait photo and create a wide 16:9 hero image.

The subject occupies the left 40% of the frame, maintaining their exact likeness,
expression, and clothing from the source photo. The subject is looking slightly
toward the right side of the frame (toward where the text will go).

The right 60% of the frame transitions into a warm, atmospheric background:
[warm gradient from the subject's environment color into a rich, scholarly darkness /
a softly blurred extension of the environment behind them / an abstract warm texture
of layered earth tones].

The transition from subject to background is natural — no hard edge or obvious compositing
boundary. The background in the text zone should be [dark enough for white text /
light enough for dark text] with even tonality (no bright spots that would compete
with text overlay).

Lighting: warm, directional light from the [left/right] illuminating the subject's face.
The light falls off naturally into the background zone. Cinematic quality — think
documentary film still.

Color palette: warm earth tones — amber, terracotta, warm grey, cream highlights
on the subject. The overall warmth should feel like golden hour or warm interior light.

16:9 aspect ratio, 1920×1080 minimum resolution.
```

#### Variant: Author Right, Text Left
```
Mirror the composition — subject on the RIGHT 40%, text zone on the LEFT 60%.
The subject looks slightly toward the left side of the frame.
```

### 2. Full-Bleed Atmospheric
Author fills more of the frame with a dramatic, atmospheric environment.
Text overlays directly on a darker region of the image.

```
FULL-BLEED HERO — ATMOSPHERIC

Take this portrait photo and create an immersive, full-bleed 16:9 hero image.

The subject is positioned [center / rule-of-thirds left / rule-of-thirds right],
framed from [waist up / chest up / mid-torso up]. Their exact likeness, expression,
and clothing are preserved from the source photo.

The environment extends to fill the entire frame: [a warm, book-lined study with
golden lamplight / a community gathering space with soft evening light / an urban
neighborhood street at golden hour / a contemplative outdoor setting with natural light].

The upper portion of the image (top 30%) should have [a natural darkening / a warm
shadow / architectural elements] that allows white text to be overlaid without a
separate overlay element.

Depth of field: the subject is in sharp focus, the environment softly blurred
(f/2.8 equivalent) but recognizable. The environment tells a story about who
this person is and what they care about.

Cinematic color grade: warm, slightly desaturated, film-like. Think A24 documentary
meets editorial portraiture. Rich shadows with warm fill — never cold or clinical.

16:9 aspect ratio, 2048px wide minimum. The image should feel like a frame from
a beautifully shot documentary.
```

### 3. Cinematic Letterbox
Ultra-wide format with dramatic lighting and mood. Premium, film-quality feel.

```
CINEMATIC HERO — LETTERBOX

Take this portrait photo and create an ultra-wide cinematic hero image (21:9 or 2.39:1
aspect ratio).

The subject is positioned using the rule of thirds, with dramatic side lighting
creating a [Rembrandt / split / broad] lighting pattern on their face. One side
of the face is warmly lit, the other falls into rich, warm shadow (never cold shadow).

The environment is [mostly darkness with selective warm light revealing elements /
a dramatically lit interior with pools of warm light / a moody exterior with golden
rim lighting]. Think Roger Deakins cinematography — every shadow is intentional,
every highlight tells a story.

Anamorphic lens characteristics: subtle horizontal lens flare from practical light
sources, slightly oval bokeh in the background, warm flare streaks.

Color: teal-and-orange inspired but shifted warm — warm amber highlights, warm
brown-grey shadows. No cold tones anywhere.

21:9 aspect ratio (2560×1080 or similar). This should feel like a film poster
for a documentary about ideas that matter.
```

### 4. Editorial Portrait
Magazine-cover-style treatment. Clean, structured, premium.

```
EDITORIAL HERO — MAGAZINE STYLE

Take this portrait photo and create an editorial-quality 16:9 hero image.

The subject is positioned [center / slightly off-center], shot from [straight on /
slight 3/4 angle]. Clean, controlled lighting — a large key light from above-left
(beauty/editorial lighting), subtle fill from the right, and a warm hair light
for separation.

Background: [clean studio gradient — warm cream ({{BRAND_LIGHT}}) to warm grey ({{BRAND_MUTED}}) /
a single-color warm field, slightly textured / a minimal architectural element
(doorway, window frame, bookshelf edge) providing structure without distraction].

The framing is generous — the subject has breathing room. Negative space is intentional
and balanced. The composition follows editorial conventions: subject slightly below
center, room above for title text if needed.

Color: clean, warm, accurate. Not over-processed. Natural skin tones with a warm
shift. The image should look like it belongs on the cover of a quality ideas
magazine — think Kinfolk meets Christianity Today.

16:9 aspect ratio, 2048px wide. Magazine-quality editorial portrait.
```

### 5. Gradient Fade / Overlay Ready
Subject fades into a solid or gradient background — designed specifically for
text overlay with guaranteed readability.

```
GRADIENT FADE HERO — TEXT-OVERLAY OPTIMIZED

Take this portrait photo and create a 16:9 hero image optimized for text overlay.

The subject is positioned on the [left / right] side of the frame. From the subject,
the image fades into a smooth [dark gradient — from the subject's environment
colors transitioning to rich warm charcoal ({{BRAND_DARK}}) / light gradient — from the
subject's environment colors transitioning to warm cream ({{BRAND_LIGHT}})].

The gradient zone (where text will go) must be:
- Smooth and even — no spots, no texture variation
- Dark enough for white text (if dark gradient) or light enough for dark text
- At least 50% of the frame width
- The transition from subject to gradient should be gradual (over 15-20% of frame width)

The subject maintains their exact likeness. Warm, flattering lighting on the subject.
The gradient feels natural — like the subject is emerging from or standing in front
of a warmly lit environment.

16:9 aspect ratio, 1920×1080 minimum. Optimized for web hero sections.
```

### 6. Duo / Conversation (Two People)
Two author/speaker headshots composed into a single hero. For podcast pages,
interview features, co-authored content.

```
DUO HERO — CONVERSATION COMPOSITION

Create a 16:9 hero image featuring two speakers in a conversational composition.

[PERSON A] is positioned on the LEFT third of the frame, angled slightly toward center.
[PERSON B] is positioned on the RIGHT third of the frame, angled slightly toward center.
The CENTER third has warm negative space — slightly blurred environment or gradient —
for title text.

Both subjects maintain their exact likeness from their respective source photos.
The lighting and color grade should be unified across both — as if they were photographed
in the same room at the same time. Warm, directional light from above, warm fill.

Environment: [a warm, intimate conversation setting — suggestion of a table between
them, bookshelves behind / a studio setting with warm backdrop / outdoor with
warm evening light].

The composition should feel like a still from a quality conversation — both subjects
engaged, present, warm.

16:9 aspect ratio, 2048px wide.
```

## Page-Specific Defaults

| Page | Composition | Aspect | Mood | Text Zone |
|------|-------------|--------|------|-----------|
| Home | Split (author left) | 16:9 | Warm, inviting, visionary | Right 60% |
| About | Full-bleed atmospheric | 16:9 | Personal, intimate, warm | Top 30% darkened |
| Course detail | Gradient fade | 16:9 | Scholarly, trustworthy | Right or bottom |
| Article detail | Editorial portrait | 16:9 | Clean, intellectual | Top overlay |
| Podcast | Duo conversation | 16:9 | Conversational, warm | Center third |
| Landing page | Cinematic letterbox | 21:9 | Premium, compelling | Overlaid |
| Content hub | Split (author right) | 16:9 | Approachable, browsable | Left 60% |

## Execution

### Step 1 — Load Source & Determine Composition

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// Load source image
let imageBase64: string;
let mimeType: string;

if (sourcePath.startsWith("http")) {
  const res = await fetch(sourcePath);
  const buf = Buffer.from(await res.arrayBuffer());
  imageBase64 = buf.toString("base64");
  mimeType = res.headers.get("content-type") || "image/webp";
} else {
  const buf = fs.readFileSync(sourcePath);
  imageBase64 = buf.toString("base64");
  mimeType = sourcePath.endsWith(".png") ? "image/png"
    : sourcePath.endsWith(".webp") ? "image/webp" : "image/jpeg";
}
```

### Step 2 — Generate Hero Image

```typescript
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: [
    {
      role: "user",
      parts: [
        { inlineData: { data: imageBase64, mimeType } },
        {
          text: `${HERO_COMPOSITION_PROMPT}

CRITICAL: Maintain the subject's exact likeness — same face, same expression,
same clothing, same age, same skin tone. Only extend/modify the environment,
lighting, and framing. This is a real person and their appearance must not be altered.

Generate this as an image.`,
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
    const outDir = "{{OUTPUT_DIR}}/hero-portrait";
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, `${slug}-hero.png`), buffer);
  }
}
```

### Step 3 — Iterative Refinement

Hero images often need 2-3 refinement passes:

**Common refinements:**
- "The transition from subject to background is too abrupt — make it more gradual"
- "The background is too bright in the text zone — darken it for better contrast"
- "The subject's face is slightly different — preserve the exact likeness more carefully"
- "Warm up the overall image — it's reading slightly cool"
- "The depth of field is too shallow — I want more environment detail visible"
- "Add more negative space on the right for the headline text"

### Step 4 — Generate Dark & Light Mode Variants

For web heroes, generate both a dark-mode and light-mode version:

```typescript
// Dark mode: rich warm darks in the background
const darkPrompt = `${BASE_PROMPT}
The background and gradient zones should use rich, warm dark tones —
warm charcoal ({{BRAND_DARK}}), deep amber shadows, warm black. Designed for
dark mode display where the page background is dark.`;

// Light mode: warm cream/white in the background
const lightPrompt = `${BASE_PROMPT}
The background and gradient zones should use warm light tones —
cream ({{BRAND_LIGHT}}), soft warm grey, warm white. Designed for light mode
display where the page background is light.`;
```

## Output Format

```
## Hero Portrait Report

### Source: [source image path or URL]
### Subject: [name]
### Page Target: [home / about / course / etc.]
### Composition: [split / full-bleed / cinematic / editorial / gradient-fade]

### Prompt
> [Full composition prompt used]

### Generated Files
| Variant | File | Dimensions | Mode |
|---------|------|-----------|------|
| Primary | {{OUTPUT_DIR}}/hero-portrait/alan-home-hero.png | 1920×1080 | Universal |
| Dark mode | {{OUTPUT_DIR}}/hero-portrait/alan-home-hero-dark.png | 1920×1080 | Dark |
| Light mode | {{OUTPUT_DIR}}/hero-portrait/alan-home-hero-light.png | 1920×1080 | Light |

### Composition Details
- Subject position: Left 40%
- Text zone: Right 60%, dark gradient
- Lighting: Warm directional from left
- Background: Warm bokeh study environment → dark gradient
- Color grade: Warm earth tones, film-quality

### Likeness Check
- ✅ Facial features preserved
- ✅ Expression preserved
- ✅ Clothing preserved
- ✅ Skin tone accurate

### Text Overlay Test
- ✅ White text readable in text zone (estimated contrast: 8:1)
- ✅ No bright spots competing with text area
- ✅ Gradient smooth and even

### Integration
- Update `tenant.config.ts` → `hero.imageUrl` with new path
- Upload to Supabase: `media-library/alan/[filename]`
- Verify responsive behavior at mobile breakpoints

### Next Steps
- Review and approve the hero image
- Use `/asset-edit` for refinements
- Use `/asset-text-overlay` to test headline placement
- Run `/asset-brand-check` to verify brand alignment
- Use `/asset-animate` to add subtle Ken Burns or breathing motion
```

## Responsive Considerations

Hero images need to work at multiple breakpoints:

| Breakpoint | Behavior | Consideration |
|-----------|----------|---------------|
| Desktop (≥1280px) | Full 16:9 or 21:9 display | Full composition visible |
| Tablet (768–1279px) | May crop sides | Ensure subject isn't at extreme edge |
| Mobile (< 768px) | Often stacks or crops to portrait | Generate a 9:16 mobile variant |

### Mobile Variant
For split compositions, generate a separate mobile-optimized version:
```
Create a 9:16 portrait version of this hero image. The subject fills the upper
60% of the frame, with warm gradient/background filling the lower 40% as a
text zone. The subject is centered horizontally. Same lighting and color grade
as the desktop version.
```

## Error Recovery

| Issue | Fix |
|-------|-----|
| Face altered/aged/changed | "Preserve the EXACT face from the source — do not modify any facial features" |
| Background too distracting | "Increase the depth of field blur in the background — softer bokeh" |
| Text zone not dark/light enough | "Make the [right/bottom] portion [darker/lighter] for text overlay contrast" |
| Composition feels like a bad photoshop | "Make the transition between subject and background more natural and gradual" |
| Wrong aspect ratio | Specify explicitly: "Output must be exactly 16:9 aspect ratio (1920×1080)" |
| Subject looks pasted in | "Unify the lighting direction — all light should come from [direction]. The subject and environment must look like they were photographed together" |
