
Generate video using Google Veo 3.1: $ARGUMENTS

$ARGUMENTS should include:
- Description of the video concept (subject, action, camera, style, mood, audio)
- Optionally: model tier (standard, fast)
- Optionally: resolution (720p, 1080p, 4k)
- Optionally: duration (4, 6, 8 seconds)
- Optionally: aspect ratio (16:9, 9:16)
- Optionally: start frame image path, end frame image path
- Optionally: reference image paths (up to 3, asset type)
- Optionally: extend an existing video
- Empty — ask the user for the concept

## Authoritative Documentation

### Gemini API (Primary)
- Video Generation Guide: https://ai.google.dev/gemini-api/docs/video
- Veo 3.1 Model Card: https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview
- Pricing: https://ai.google.dev/gemini-api/docs/pricing
- Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits

### Vertex AI (Google Cloud)
- API Reference: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation
- Veo 3.1 Model Page: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate
- Generate from Text: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-text
- Generate from Image: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-an-image
- Start/End Frames: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-first-and-last-frames
- Reference Images: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/use-reference-images-to-guide-video-generation
- Extend a Video: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/extend-a-veo-video
- Prompt Guide: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
- Pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing

### Prompt Engineering
- DeepMind Prompt Guide: https://deepmind.google/models/veo/prompt-guide/
- Ultimate Prompting Guide (Cloud Blog): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Veo 3 Technical Report: https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf

### Model Family & Announcements
- DeepMind Veo: https://deepmind.google/models/veo/
- Veo 3.1 Announcement: https://developers.googleblog.com/en/introducing-veo-3-1-and-new-creative-capabilities-in-the-gemini-api/
- Pricing Update: https://developers.googleblog.com/en/veo-3-and-veo-3-fast-new-pricing-new-configurations-and-better-resolution/

### Code Samples
- Advanced Controls Notebook: https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_advanced_controls.ipynb
- Reference-to-Video Notebook: https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_reference_to_video.ipynb
- @google/genai JS SDK: https://github.com/googleapis/js-genai

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Check if `@google/genai` is installed — if not: `pnpm add @google/genai`
3. Determine model tier, resolution, and duration from the use case

## Available Models

| Model ID | Tier | Best For | Cost/sec (with audio) |
|---|---|---|---|
| `veo-3.1-generate-001` | Standard | Highest quality, production | ~$0.40 |
| `veo-3.1-fast-generate-001` | Fast | Iteration, drafts | ~$0.15 |
| `veo-3.0-generate-001` | Standard (Veo 3) | Legacy | ~$0.75 |
| `veo-3.0-fast-generate-001` | Fast (Veo 3) | Legacy fast | — |
| `veo-2.0-generate-001` | Standard (Veo 2) | Style references only | ~$0.35 |

**Default:** `veo-3.1-generate-001` for production, `veo-3.1-fast-generate-001` for iteration.

**Note:** Preview models (`-preview` suffix) are deprecated April 2, 2026. Use `-001` models.

## Capabilities

| Feature | Veo 3.1 |
|---|---|
| Resolution | 720p, 1080p, 4K |
| Duration | 4, 6, or 8 seconds (default 8) |
| Frame Rate | 24 fps (cinematic), 30 fps, 60 fps |
| Aspect Ratios | 16:9 (landscape), 9:16 (portrait) |
| Native Audio | Yes — 48kHz stereo (dialogue, SFX, ambient, music) |
| Reference Images | Up to 3 (asset type) |
| Start/End Frame | Yes (frame interpolation) |
| Video Extension | Up to 20 extensions × 7s each = ~148s total |
| Image-to-Video | Yes |
| Negative Prompt | Yes |
| Seed | Yes (0-4294967295, improves but doesn't guarantee determinism) |

## API Parameters

| Parameter | Type | Values | Default |
|---|---|---|---|
| `aspectRatio` | string | `"16:9"`, `"9:16"` | `"16:9"` |
| `resolution` | string | `"720p"`, `"1080p"`, `"4k"` | `"720p"` |
| `durationSeconds` | integer | 4, 6, 8 | 8 |
| `generateAudio` | boolean | true/false | true |
| `negativePrompt` | string | What to exclude | — |
| `personGeneration` | string | `"allow_adult"` | `"allow_adult"` |
| `sampleCount` | integer | 1-4 | 1 |
| `seed` | uint32 | 0-4294967295 | — |

## Prompt Engineering — Direct Like a Filmmaker

Veo 3.1 responds to precise filmmaking language. **Prompt like a director**, not a describer. Think in terms of shots, not scenes.

### Structure Your Prompt

1. **What is in the shot** — subjects, objects, environment
2. **What is happening** — action, motion, interaction
3. **What it should sound like** — dialogue, SFX, ambient, music
4. **Style and camera** — lens, lighting, color, camera movement

### Camera Controls

**Framing:**
- Wide shot, medium shot, close-up, extreme close-up
- Over-the-shoulder, establishing shot, two-shot

**Angles:**
- Eye-level, low angle (power), high angle (vulnerability)
- Bird's eye / top-down, worm's eye view, Dutch angle (tension)

**Movements:**
- Dolly (forward/back), track (sideways), pan (horizontal turn)
- Tilt (vertical turn), crane (ascending/descending)
- Steadicam, handheld, aerial/drone

### Audio Prompting

Veo 3.1 generates audio natively in a single pass — no post-processing needed:

- **Dialogue**: Use quotation marks for specific speech. Label speakers.
  ```
  TEACHER: "The most important thing is showing up."
  ```
- **Sound effects**: "the click of a pen, footsteps on gravel"
- **Ambient**: "quiet hum of an office, distant traffic"
- **Music**: "soft acoustic guitar in the background"

### Lighting & Style
- Specify direction: "warm side-light from the left"
- Quality: "soft diffused light", "hard overhead noon sun"
- Color temperature: "golden hour warmth", "cool blue moonlight"
- Film stock: "shot on 35mm film with slight grain", "anamorphic lens, lens flares"
- Color grade: "teal and orange", "desaturated", "warm earth tones"

### Negative Prompting
Describe exclusions naturally:
- "A desolate landscape with no buildings or roads"
- Use the `negativePrompt` parameter: "blurry, low quality, text overlay, watermark"

## Execution Patterns

### Pattern 1 — Text-to-Video (Node.js)

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";

const ai = new GoogleGenAI({});

let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-001",
  prompt: "A cinematic aerial drone shot sweeping over a misty mountain range at sunrise, golden light filtering through clouds, 35mm film grain, warm color grading",
  config: {
    aspectRatio: "16:9",
    resolution: "1080p",
    durationSeconds: 8,
    generateAudio: true,
    sampleCount: 1,
  },
});

// Poll until done
while (!operation.done) {
  await new Promise((r) => setTimeout(r, 10000));
  operation = await ai.operations.getVideosOperation({ operation });
  console.log("Polling...");
}

// Download
await ai.files.download({
  file: operation.response.generatedVideos[0].video,
  downloadPath: "generated/video/output.mp4",
});
console.log("Video saved to generated/video/output.mp4");
```

### Pattern 2 — Image-to-Video (Node.js)

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";

const ai = new GoogleGenAI({});

const imageBytes = fs.readFileSync("start-frame.png");
const base64Image = imageBytes.toString("base64");

let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-001",
  prompt: "The scene comes alive — wind rustles through the trees, dappled sunlight shifts across the path",
  image: {
    imageBytes: base64Image,
    mimeType: "image/png",
  },
  config: {
    aspectRatio: "16:9",
    resolution: "1080p",
    durationSeconds: 8,
    generateAudio: true,
  },
});
```

### Pattern 3 — Start/End Frame Interpolation

```typescript
let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-001",
  prompt: "A hand reaches out and places a steaming cup of coffee on a wooden table",
  image: {
    imageBytes: startFrameBase64,
    mimeType: "image/png",
  },
  config: {
    lastFrame: {
      imageBytes: endFrameBase64,
      mimeType: "image/png",
    },
    aspectRatio: "16:9",
    resolution: "1080p",
    durationSeconds: 6,
  },
});
```

### Pattern 4 — Reference Images (up to 3)

```typescript
let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-001",
  prompt: "A person walks in carrying a ceramic vase filled with wildflowers",
  config: {
    referenceImages: [
      {
        image: { imageBytes: vaseImageBase64, mimeType: "image/png" },
        referenceType: "asset",
      },
    ],
    aspectRatio: "9:16",
    resolution: "1080p",
    generateAudio: true,
  },
});
```

### Pattern 5 — Video Extension

Extend an existing Veo video by 7 seconds per extension (up to 20 extensions, ~148s total):

```python
# Python — extension API
operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="The camera continues to follow the path as it opens into a sunlit meadow",
    video=previous_video,  # reference to generated video
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds=7,
    ),
)
```

Extension uses full clip context (not just last frame). Only works with Veo-generated videos from the last 2 days.

### Pattern 6 — Python (Gemini API)

```python
from google import genai
from google.genai.types import GenerateVideosConfig

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="A warm community gathering in a sunlit courtyard, people laughing and sharing a meal, acoustic guitar playing softly, shot on 35mm film with golden hour lighting",
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",
        duration_seconds=8,
        generate_audio=True,
        person_generation="allow_adult",
        number_of_videos=1,
    ),
)

import time
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

for video in operation.response.generated_videos:
    client.files.download(file=video.video, download_path="output.mp4")
```

## Pricing

| Model | Cost/sec (with audio) | Cost/sec (no audio) |
|---|---|---|
| Veo 3.1 Standard | ~$0.40 | Lower |
| Veo 3.1 Fast | ~$0.15 | ~$0.10 |
| Veo 3 Standard | ~$0.75 | Lower |
| Veo 2 | ~$0.35 | — |

**Cost examples:**
- 8s Veo 3.1 Standard 1080p with audio = ~$3.20
- 8s Veo 3.1 Fast 720p with audio = ~$1.20
- Only charged for successfully generated videos

### Rate Limits
- ~10 RPM on Vertex AI (varies by project/tier)
- Check Gemini API limits at: https://ai.google.dev/gemini-api/docs/rate-limits

## Content Safety

- **SynthID watermark**: Invisible, persists through compression/resizing/cropping
- **Dual-layer filtering**: Input keyword filtering + output frame scanning
- `personGeneration`: Default `"allow_adult"` — only adult people/faces
- Prohibited: NSFW, explicit, gratuitous violence, hate speech — zero tolerance
- In EU/UK/CH/MENA: `"allow_adult"` is the only permitted value for Veo 3+

## Presets by Use Case

| Use Case | Model | Resolution | Duration | Audio | Prompt Focus |
|---|---|---|---|---|---|
| Course trailer | Standard | 1080p | 8s | Yes | Cinematic, warm, scholarly |
| Social clip | Fast | 720p | 4s | Yes | Punchy, scroll-stopping |
| Hero background | Fast | 1080p | 8s | No | Subtle motion, locked camera |
| Product reveal | Standard | 4K | 6s | Yes | Clean, studio lighting |
| Concept draft | Fast | 720p | 4s | No | Quick iteration |
| Cinemagraph loop | Fast | 1080p | 4s | No | Single element moves, rest still |

## Output Format

```
## Video Generation Report

### Prompt
> [The full prompt used]

### Settings
- Model: veo-3.1-generate-001
- Resolution: 1080p
- Duration: 8 seconds
- Aspect Ratio: 16:9
- Audio: enabled
- Samples: 1

### Status
- Operation: [operation ID]
- Status: completed
- Output: generated/video/output.mp4

### Cost Estimate
- ~$3.20 (8s × $0.40/s Standard with audio)

### Next Steps
- Review the generated video
- Extend video for longer duration (up to ~148s)
- Use reference images for character/asset consistency
- Combine with Remotion for post-production
```

## Rules

- Default to `veo-3.1-generate-001` for production, `veo-3.1-fast-generate-001` for iteration
- Prompt like a director — use precise cinematographic language
- Resolution, duration, and FPS are API parameters — don't describe them in the prompt
- Enable audio by default — describe desired sounds/dialogue in the prompt
- Use negative prompt parameter for exclusions, not negative language in the main prompt
- For start/end frame interpolation, both images must match the target aspect ratio
- Reference images are "asset" type only (not style) — use Veo 2 for style references
- Poll with 10-second intervals — video generation takes time
- Report operation ID, cost estimate, and file path in the output
- Preview models are deprecated April 2, 2026 — always use `-001` suffix models
