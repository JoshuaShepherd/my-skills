---
name: asset-headshot
description: Create polished headshots and avatars from existing author photos using Nano Banana 2. Handles background replacement, relighting, color grading, cropping, and format adaptation for avatars, team pages, bio cards, OG images, and instructor photos. Use when you need a consistent, on-brand headshot at any size or context.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Create a headshot or avatar from an existing photo: $ARGUMENTS

$ARGUMENTS should include:
- Path or URL to the source photo of the author/thought leader
- Target use: avatar, team-page, bio-card, instructor, og-author, social-profile, speaker-card
- Optionally: background style (studio, contextual, transparent, branded)
- Optionally: specific adjustments (warmer, more scholarly, more approachable, etc.)
- Empty — ask the user for the source photo and intended use

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Read `src/lib/config/tenant.config.ts` — check existing `hero.imageUrl` and `courseInfo.instructorHeadshotUrl`
3. Read the source image to understand current quality, lighting, background, and expression
4. Check if an author style guide exists at `_docs/asset-prompts/author-style-guide.md` (created by `/asset-author-style`) — if so, follow it for consistency
5. Determine the target format from the presets below

## Headshot Presets

| Use Case | Aspect | Size | Background | Crop | Priority |
|----------|--------|------|------------|------|----------|
| `avatar-sm` | 1:1 | 64×64px | Any (will be tiny) | Tight face crop, forehead to chin | Speed |
| `avatar-md` | 1:1 | 120×120px | Soft bokeh or solid | Face + shoulders | Warmth |
| `avatar-lg` | 1:1 | 256×256px | Bokeh, studio, or contextual | Head + upper shoulders | Quality |
| `team-page` | 3:4 | 400×533px | Consistent across team | Head to mid-torso | Consistency |
| `bio-card` | 1:1 | 300×300px | Soft, warm, slightly blurred | Head + shoulders | Approachability |
| `instructor` | 1:1 | 120×120px | Soft warm bokeh | Face + shoulders, warm feel | Trust |
| `speaker-card` | 16:9 | 800×450px | Environmental or stage | Wider framing, speaking context | Authority |
| `og-author` | 16:9 | 1200×630px | Branded gradient + headshot | Headshot left, space for text right | Sharing |
| `social-profile` | 1:1 | 400×400px | Clean, branded | Face-centered, well-lit | Recognition |
| `about-hero` | 4:5 | 800×1000px | Environmental, warm | Full portrait, 9:16-ish | Storytelling |

## Current Author Images (Alan Hirsch Platform)

These are the existing source images available:

### Primary Hero Portrait
- **URL**: `https://vhaiiiykcukrlyvwlgip.supabase.co/storage/v1/object/public/media-library/alan/alan-headshot-9x16-desktop.webp`
- **Config key**: `hero.imageUrl` in tenant.config.ts
- **Aspect**: 9:16 (portrait)
- **Used on**: Home page hero, article detail hero, OG meta

### Instructor Headshot
- **URL**: `https://vhaiiiykcukrlyvwlgip.supabase.co/storage/v1/object/public/media-library/alan/alan-portrait-60-year-old-white-man-soft-bokeh-in.webp`
- **Config key**: `courseInfo.instructorHeadshotUrl`
- **Used on**: Course overview instructor card (120×120px)

### AI Lab Host Avatar
- **Component**: `AILabHostBand.tsx`
- **Current state**: Text fallback "AH" — no actual image

If the user provides a different/new source photo, use that instead.

## Background Styles

### 1. Studio Clean
Pure or near-white background with soft professional lighting. Corporate but warm.
```
Replace the background with a clean studio backdrop — soft warm grey (#E8E4DF) to white
gradient. Professional headshot lighting: large softbox at 45° from the left, fill light
from the right at half intensity, hair light from above-behind for separation. The subject's
skin tones should be warm and natural, not washed out.
```

### 2. Warm Bokeh (Default for Alan Hirsch)
Soft, out-of-focus background with warm tones — suggests a library, study, or intimate setting.
```
Replace the background with a warm, softly blurred environment — the impression of a
book-lined study or warm library setting. Rich amber and walnut bokeh circles, suggesting
bookshelves and warm lamplight behind the subject. Shallow depth of field — the subject
is tack-sharp, everything behind is beautifully soft. The bokeh should feel warm (amber,
honey, cream tones) — never cool or clinical.
```

### 3. Environmental / Contextual
Subject in a real setting that reinforces their identity and message.
```
Place the subject in a [warm community space / book-filled study / outdoor neighborhood
setting / small group gathering context]. The environment should feel authentic and lived-in
— not a set. Natural light, warm tones, inviting atmosphere. The subject is clearly the
focal point but the environment tells part of their story.
```

### 4. Branded Gradient
Solid gradient using brand colors — good for OG images, social cards, marketing.
```
Replace the background with a smooth gradient using the brand palette: from warm amber
(#D4A84B) at the upper left to deep warm charcoal (#2C2220) at the lower right. Subtle
warmth, not corporate. Add a very faint paper or linen texture overlay at 5% opacity for
depth. The subject should be naturally lit from the gradient's bright side.
```

### 5. Transparent (for compositing)
Subject extracted with no background — for layering onto other designs.
```
Remove the background completely, leaving only the subject on a transparent background.
Clean edge extraction — no fringing, no halo artifacts. Hair edges should be naturally
soft, not hard-cut. Preserve all shadow detail on the subject's clothing and face.
```

## Lighting & Color Grade Adjustments

### Warming Pass
```
Adjust the lighting to feel warmer and more inviting:
- Shift the overall color temperature toward golden/amber (not orange)
- Soften harsh shadows — fill them with warm reflected light
- Add a subtle warm rim light on the subject's hair/shoulders
- Skin tones should be healthy and warm, never sallow or grey
- The overall feel should be "sitting by a fire in a library" — warm, intelligent, approachable
```

### Authority Enhancement
```
Adjust the portrait to convey scholarly authority while remaining approachable:
- Slightly increase contrast in the subject's face — bring out structure
- Ensure eyes are bright and engaging — add a subtle catchlight if needed
- Deepen the background slightly for separation
- The subject should look like someone you'd want to learn from — wise but warm
```

### Approachability Enhancement
```
Adjust the portrait to feel more warm and approachable:
- Soften the lighting — no harsh shadows on the face
- Open up the shadows with warm fill light
- The expression should read as genuine and inviting
- Slightly reduce contrast for a softer, more editorial feel
- The overall impression: someone you'd feel comfortable having coffee with
```

## Execution

### Step 1 — Load Source Image

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

// Load source image — either local file or download from URL
let imageBase64: string;
let mimeType: string;

if (sourceImagePath.startsWith("http")) {
  // Download from URL (e.g., Supabase CDN)
  const response = await fetch(sourceImagePath);
  const buffer = Buffer.from(await response.arrayBuffer());
  imageBase64 = buffer.toString("base64");
  mimeType = response.headers.get("content-type") || "image/webp";
} else {
  const buffer = fs.readFileSync(sourceImagePath);
  imageBase64 = buffer.toString("base64");
  mimeType = sourceImagePath.endsWith(".png") ? "image/png"
    : sourceImagePath.endsWith(".webp") ? "image/webp"
    : "image/jpeg";
}
```

### Step 2 — Apply Transformations

```typescript
// Compose the edit instruction based on target use
const editInstruction = `
${BACKGROUND_INSTRUCTION}

${LIGHTING_INSTRUCTION}

${CROP_INSTRUCTION}

Maintain the subject's exact likeness — same facial features, expression, clothing,
and proportions. Only modify the background, lighting, and framing as described above.
The result should be a professional ${TARGET_USE} portrait.

Output as a ${ASPECT_RATIO} image.
`;

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [
    {
      role: "user",
      parts: [
        { inlineData: { data: imageBase64, mimeType } },
        { text: editInstruction },
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
    const outPath = path.join("public/images/generated/headshot", `${slug}-${targetUse}.png`);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 3 — Resize for Target Use

After NB2 generation, resize to exact pixel dimensions using sharp:

```typescript
import sharp from "sharp";

// Resize to exact target dimensions
const { width, height } = PRESET_DIMENSIONS[targetUse];
await sharp(generatedImagePath)
  .resize(width, height, { fit: "cover", position: "top" }) // "top" keeps face in frame
  .webp({ quality: 90 })
  .toFile(generatedImagePath.replace(".png", ".webp"));
```

### Step 4 — Generate Multiple Sizes from One Source

For a full headshot kit, generate from one high-quality source:

```typescript
const sizes = {
  "avatar-sm": { width: 64, height: 64 },
  "avatar-md": { width: 120, height: 120 },
  "avatar-lg": { width: 256, height: 256 },
  "bio-card": { width: 300, height: 300 },
  "social-profile": { width: 400, height: 400 },
};

for (const [name, dims] of Object.entries(sizes)) {
  await sharp(highResSource)
    .resize(dims.width, dims.height, { fit: "cover", position: "top" })
    .webp({ quality: 90 })
    .toFile(`public/images/headshots/alan-hirsch-${name}.webp`);
}
```

## Consistency Rules

### Across All Headshot Uses
1. **Same person** — never alter facial features, age, ethnicity, or distinguishing characteristics
2. **Consistent warmth** — all headshots should have the same warm color temperature
3. **Consistent expression vibe** — if the source is warm/approachable, all derivatives should maintain that
4. **No AI-generated face** — always start from a real photograph, only modify environment/lighting/framing

### Cross-Platform Consistency
When generating headshots for the same person across multiple contexts:
- Use the same source photo (or same-session photos)
- Apply the same color grade to all outputs
- If an author style guide exists (`/asset-author-style`), follow it for every generation

## Batch Generation — Full Headshot Kit

Generate a complete set of headshots for all platform uses in one pass:

```
/asset-headshot [source-image] kit

Generates:
1. avatar-sm (64×64) — for comment threads, chat
2. avatar-md (120×120) — for instructor cards, sidebar
3. avatar-lg (256×256) — for about page, team page
4. bio-card (300×300) — for author bio sections
5. social-profile (400×400) — for social media profiles
6. about-hero (800×1000) — for about page hero
7. speaker-card (800×450) — for speaking/event pages
8. og-author (1200×630) — for OG meta tags
```

## Output Format

```
## Headshot Report

### Source: [source image path or URL]
### Subject: [name]
### Target: [use case — e.g., instructor avatar, team page]

### Transformations Applied
- Background: Warm bokeh (library/study impression)
- Lighting: Warming pass — golden ambient, subtle rim light
- Crop: Head + upper shoulders, 1:1 aspect
- Color grade: Warm earth tones, +10% warmth

### Generated Files
| Use | File | Dimensions |
|-----|------|-----------|
| instructor | public/images/headshots/alan-hirsch-instructor.webp | 120×120 |
| bio-card | public/images/headshots/alan-hirsch-bio-card.webp | 300×300 |
| avatar-lg | public/images/headshots/alan-hirsch-avatar-lg.webp | 256×256 |

### Consistency Check
- ✅ Matches author style guide
- ✅ Warm color temperature consistent
- ✅ Likeness preserved accurately
- ✅ Background style consistent with platform

### Integration Points
- Update `tenant.config.ts` → `courseInfo.instructorHeadshotUrl`
- Update `AILabHostBand.tsx` → add actual image instead of "AH" fallback
- Upload to Supabase media-library for CDN serving

### Next Steps
- Review and approve
- Use `/asset-headshot [source] kit` for full set
- Run `/asset-brand-check` on the results
```

## Platform Integration Checklist

After generating headshots, update these integration points:

| Component | Config/Code Location | Image Needed |
|-----------|---------------------|--------------|
| Home hero | `tenant.config.ts` → `hero.imageUrl` | about-hero (9:16 / 4:5) |
| Course instructor | `tenant.config.ts` → `courseInfo.instructorHeadshotUrl` | instructor (1:1, 120px) |
| AI Lab host | `AILabHostBand.tsx` | avatar-md (1:1, 120px) |
| OG meta | `layout.tsx` → og image | og-author (16:9, 1200×630) |
| Article author | `ArticleReader.tsx` | bio-card (1:1, 300px) |
| Video author | `VideoPlayer.tsx` → `author.avatarUrl` | avatar-md (1:1, 120px) |

## Error Recovery

| Issue | Fix |
|-------|-----|
| Face distorted by NB2 | Reduce edit scope — do background-only first, then lighting as separate pass |
| Expression changed | Add "preserve the exact facial expression from the source photo" to prompt |
| Skin tone wrong | Add "maintain natural, accurate skin tones — do not alter the subject's complexion" |
| Too corporate/cold | Apply warming pass, switch to warm bokeh background |
| Hair edge fringing | "Clean, natural hair edges — no halo or fringing artifacts at the boundary" |
| Likeness drift | Use more conservative edits — background swap only, no facial relighting |
