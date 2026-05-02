
Generate video using OpenAI Sora 2: $ARGUMENTS

$ARGUMENTS should include:
- Description of the video concept (subject, action, camera, style, mood)
- Optionally: model (sora-2, sora-2-pro)
- Optionally: resolution (720p, 1080p, portrait, landscape)
- Optionally: duration (4, 8, 12 seconds)
- Optionally: input image path for image-to-video
- Optionally: existing video ID for extension or editing
- Empty — ask the user for the concept

## Authoritative Documentation

### Primary References
- Video Generation Guide: https://platform.openai.com/docs/guides/video-generation
- Videos API Reference: https://platform.openai.com/docs/api-reference/videos
- Create Video Endpoint: https://platform.openai.com/docs/api-reference/videos/create
- List Videos Endpoint: https://platform.openai.com/docs/api-reference/videos/list

### Model Cards
- Sora 2: https://platform.openai.com/docs/models/sora-2
- Sora 2 Pro: https://platform.openai.com/docs/models/sora-2-pro

### Prompting & Guides
- Sora 2 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/sora/sora2_prompting_guide
- Sora Help Center: https://help.openai.com/en/articles/9957612-generating-videos-on-sora
- Creating Videos with Sora: https://help.openai.com/en/articles/12460853-creating-videos-with-sora
- Python SDK Reference: https://developers.openai.com/api/reference/python/resources/videos/methods/create/

### Safety & Policy
- Sora 2 System Card: https://cdn.openai.com/pdf/50d5973c-c4ff-4c2d-986f-c72b5d0ff069/sora_2_system_card.pdf

### Pricing & Limits
- Pricing: https://openai.com/api/pricing/
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits

### Azure
- Azure OpenAI Sora (preview): https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/video-generation

## Before Starting

1. Confirm `OPENAI_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Check if the `openai` npm/pip package is installed (v1.51.0+)
3. Determine model, resolution, and duration from the use case

## Available Models

| Model | Best For | Quality | Cost/sec (720p) |
|---|---|---|---|
| **sora-2** | Iteration, concepting, rough cuts, social media | Good | ~$0.10 |
| **sora-2-pro** | Production footage, marketing assets, cinematic | Best | ~$0.30 |

**Default:** `sora-2` for drafts and iteration, `sora-2-pro` for final production.

## Resolution & Size

| Size | Resolution | Aspect | Notes |
|---|---|---|---|
| `1280x720` | 720p landscape | 16:9 | Default landscape |
| `720x1280` | 720p portrait | 9:16 | Default portrait |
| `1792x1024` | Wide landscape | ~16:9 | API-only |
| `1024x1792` | Tall portrait | ~9:16 | API-only |
| `1920x1080` | 1080p landscape | 16:9 | Sora 2 Pro only |
| `1080x1920` | 1080p portrait | 9:16 | Sora 2 Pro only |

## Duration

Allowed values: **4**, **8**, or **12** seconds (default: 4).

- Sora 2 Pro can extend up to ~20-25 seconds via the extensions API
- Use extensions to chain clips for longer narratives
- FPS: 24 or 30 (30 recommended for smoother motion)

## Audio

Sora 2 generates audio **automatically** alongside video — no separate pipeline needed:
- Synced dialogue
- Sound effects
- Background audio/music

Control audio by describing it in the prompt: "the sound of wind rustling through trees" or including dialogue blocks.

## Prompt Engineering — The Cinematographer's Brief

Think of every prompt as a **shot brief for a cinematographer**. Sora 2 responds to precise filmmaking language.

### 1. SUBJECT & ACTION
Describe who/what is in the scene and what happens:
- "A woman in her 30s with curly hair walks through a rain-soaked Tokyo street"
- "A golden retriever runs through shallow ocean waves"

### 2. CAMERA FRAMING
Use precise cinematographic terms:
- **Wide shot** — establishes environment
- **Medium shot** — waist-up, conversational
- **Close-up** — face/detail, emotional
- **Over-the-shoulder** — relational
- **Establishing shot** — sets location context

### 3. CAMERA ANGLE
- **Low angle** — conveys power, grandeur
- **High angle** — vulnerability, overview
- **Dutch angle** — tension, unease
- **Bird's eye** — geographic, pattern-revealing
- **Eye level** — neutral, intimate

### 4. CAMERA MOVEMENT
- **Dolly** — forward/back toward subject
- **Track** — sideways parallel to subject
- **Pan** — horizontal camera turn (fixed position)
- **Tilt** — vertical camera turn (fixed position)
- **Crane** — vertical lift up/down
- **Steadicam** — smooth follow shot
- **Handheld** — organic, documentary feel
- **Drone** — aerial sweeping shots

### 5. LIGHTING & ATMOSPHERE
Specify direction, quality, and color:
- "Soft golden-hour light from the left, long shadows"
- "Hard overhead noon light, high contrast"
- "Cool blue moonlight, fog diffusing through the scene"
- "Warm practical lighting from string lights and candles"

### 6. STYLE & GRADE
Reference lensing, film stock, color grade:
- "Shot on 35mm film, warm color grading, slight grain"
- "Shot on ARRI Alexa, clean digital, teal and orange grade"
- "Anamorphic lens, wide aspect, lens flares"
- "Vintage Super 8 footage, saturated colors, light leaks"

### 7. DIALOGUE (optional)
Place dialogue below the visual description, label speakers:

```
A medium close-up of a professor standing at a chalkboard in a warm-lit lecture hall, gesturing as she speaks.

PROFESSOR: "The thing about community is — it doesn't happen by accident."
```

### Expert Tips
- **Detailed prompts** = control and consistency; **lighter prompts** = creative variation. Both are valid.
- Resolution, duration, and FPS are **API parameters only** — "make it longer" in the prompt won't work
- Describe the desired result, not the process
- One major concept per generation — don't pack multiple scene changes into one clip
- For character consistency across clips, describe the character identically in each prompt

## API Endpoints

### POST /v1/videos — Create Video
```
POST https://api.openai.com/v1/videos
```

| Parameter | Type | Values | Default | Notes |
|---|---|---|---|---|
| `model` | string | `sora-2`, `sora-2-pro` | — | Required |
| `prompt` | string | free text | — | Required |
| `seconds` | integer | 4, 8, 12 | 4 | Clip duration |
| `size` | string | See resolution table | `720x1280` | Output resolution |
| `input_reference` | object | `{image_url: "..."}` or `{file_id: "..."}` | null | Image-to-video |

### GET /v1/videos/{video_id} — Poll Status
States: `queued` → `in_progress` → `completed` | `failed`

### POST /v1/videos/{video_id}/edits — Edit Video
Edit an existing video with a new prompt.

### POST /v1/videos/extensions — Extend Video
Extend an existing video. Uses full initial clip as context (not just last frame).

## Execution Patterns

### Pattern 1 — Text-to-Video (Node.js)

```typescript
import OpenAI from "openai";
import * as fs from "fs";

const openai = new OpenAI();

// Create video job
const video = await openai.videos.create({
  model: "sora-2",
  prompt: "A drone shot sweeping over a misty mountain range at sunrise, golden light filtering through clouds, cinematic color grading, shot on ARRI Alexa",
  size: "1280x720",
  seconds: 8,
});

console.log(`Video job created: ${video.id}`);

// Poll for completion
let status = await openai.videos.retrieve(video.id);
while (status.status !== "completed" && status.status !== "failed") {
  await new Promise((r) => setTimeout(r, 5000));
  status = await openai.videos.retrieve(video.id);
  console.log(`Status: ${status.status}`);
}

if (status.status === "failed") {
  throw new Error(`Generation failed: ${JSON.stringify(status)}`);
}

// Download MP4
const response = await fetch(status.url);
const buffer = Buffer.from(await response.arrayBuffer());
fs.mkdirSync("generated/video", { recursive: true });
fs.writeFileSync("generated/video/output.mp4", buffer);
console.log("Video saved to generated/video/output.mp4");
```

### Pattern 2 — Image-to-Video

```typescript
const video = await openai.videos.create({
  model: "sora-2-pro",
  prompt: "The scene comes alive with gentle wind rustling through the trees, leaves catching golden sunlight",
  size: "1920x1080",
  seconds: 8,
  input_reference: {
    image_url: "https://example.com/landscape.jpg",
  },
});
```

Image must match the target video's `size` resolution. Supported formats: JPEG, PNG, WebP.

### Pattern 3 — Video Extension

```typescript
const extension = await openai.videos.extensions.create({
  video_id: "video_abc123",
  prompt: "The camera continues to pan right, revealing a bustling marketplace",
  seconds: 12, // total stitched duration
});
```

### Pattern 4 — Video Editing

```typescript
const edit = await openai.videos.edits.create(
  "video_abc123",
  {
    prompt: "Change the lighting to a warm sunset glow, keep everything else the same",
  }
);
```

### Pattern 5 — Python (with create_and_poll)

```python
from openai import OpenAI
client = OpenAI()

# Blocks until complete
video = client.videos.create_and_poll(
    model="sora-2",
    prompt="A calico cat wearing sunglasses rides a skateboard",
    size="1280x720",
    seconds=4,
)

# Download
import requests
resp = requests.get(video.url)
with open("output.mp4", "wb") as f:
    f.write(resp.content)
```

## Pricing

| Model | Resolution | Cost/sec |
|---|---|---|
| sora-2 | 720p | ~$0.10 |
| sora-2-pro | 720p | ~$0.30 |
| sora-2-pro | 1080p | ~$0.50 |

**Cost examples:**
- 8s sora-2 720p clip = ~$0.80
- 12s sora-2-pro 1080p clip = ~$6.00

### Subscription Credits (sora.com)
- 480p: 4 credits/sec
- 720p: 16 credits/sec
- 1080p: 40 credits/sec
- Plus ($20/mo): 1,000 credits
- Pro ($200/mo): 10,000 credits

### Rate Limits
- Tier 1 (API): ~25 RPM
- Plus (sora.com): ~5 RPM
- Pro (sora.com): ~50 RPM

## Content Safety

- All videos embed **C2PA** provenance metadata (watermark)
- Multi-modal moderation on prompts, frames, and audio
- Blocked: graphic violence, explicit content, hateful imagery, deepfakes of real people without consent
- Generation attempts incur charges even if flagged/blocked

## Presets by Use Case

| Use Case | Model | Size | Seconds | Prompt Focus |
|---|---|---|---|---|
| Social media clip | sora-2 | 720x1280 | 4-8 | Punchy, scroll-stopping action |
| Course trailer | sora-2-pro | 1920x1080 | 8-12 | Cinematic, warm lighting, scholarly |
| Hero background | sora-2 | 1280x720 | 8 | Subtle motion, locked camera |
| Product reveal | sora-2-pro | 1920x1080 | 8 | Clean background, studio lighting |
| Concept iteration | sora-2 | 1280x720 | 4 | Quick drafts, light prompts |

## Output Format

```
## Video Generation Report

### Prompt
> [The full prompt used]

### Settings
- Model: sora-2
- Size: 1280x720
- Duration: 8 seconds
- Input reference: none

### Status
- Job ID: video_abc123
- Status: completed
- Output: generated/video/output.mp4

### Cost Estimate
- ~$0.80 (8s × $0.10/s at 720p)

### Next Steps
- Review the generated video
- Use video editing API to refine
- Use extensions API to lengthen
- Combine with TTS audio using Remotion
```

## Rules

- Default to `sora-2` for iteration, `sora-2-pro` for final production
- Always write prompts as cinematographer briefs — use precise filmmaking language
- Resolution, duration, and FPS are API parameters only — never describe them in the prompt
- One concept per clip — don't pack multiple scene changes
- For image-to-video, input image must match target resolution
- Poll for completion with 5-second intervals — generation takes time
- Report job ID, cost estimate, and file path in the output
- Audio is automatic — describe desired sounds/dialogue in the prompt
- For longer videos, chain clips with the extensions API
