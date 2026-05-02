
Generate speech audio using OpenAI Text-to-Speech: $ARGUMENTS

$ARGUMENTS should include:
- Text to convert to speech (inline or path to a text/markdown file)
- Optionally: voice (alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer, verse, marin, cedar)
- Optionally: model (gpt-4o-mini-tts, tts-1, tts-1-hd)
- Optionally: instructions for voice steering (tone, accent, emotion — gpt-4o-mini-tts only)
- Optionally: output format (mp3, opus, aac, flac, wav, pcm)
- Optionally: speed (0.25 to 4.0)
- Optionally: output path
- Empty — ask the user what they want to generate

## Authoritative Documentation

### Primary References
- TTS Guide: https://platform.openai.com/docs/guides/text-to-speech
- API Reference (createSpeech): https://platform.openai.com/docs/api-reference/audio/createSpeech
- Audio & Speech Guide: https://platform.openai.com/docs/guides/audio

### Model Pages
- gpt-4o-mini-tts: https://platform.openai.com/docs/models/gpt-4o-mini-tts
- tts-1: https://platform.openai.com/docs/models/tts-1
- tts-1-hd: https://platform.openai.com/docs/models/tts-1-hd
- gpt-4o-audio-preview: https://platform.openai.com/docs/models/gpt-4o-audio-preview

### Advanced Capabilities
- Realtime API Guide: https://platform.openai.com/docs/guides/realtime
- Voice Agents Guide: https://platform.openai.com/docs/guides/voice-agents
- Steering TTS Cookbook: https://cookbook.openai.com/examples/voice_solutions/steering_tts

### Pricing & Limits
- Pricing: https://platform.openai.com/docs/pricing
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits

## Before Starting

1. Confirm `OPENAI_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Check if the `openai` npm package is installed — if not, install it: `pnpm add openai`
3. Determine the use case to select the right model and voice

## Available Models

| Model | Best For | Cost | Max Input | Instructions Support |
|---|---|---|---|---|
| **gpt-4o-mini-tts** | Best quality + voice steering | $0.60/1M input tokens + $12/1M audio tokens | ~2000 tokens | Yes |
| **tts-1** | Real-time/low-latency | $0.015/1K chars ($15/1M) | 4096 chars | No |
| **tts-1-hd** | High quality, offline | $0.030/1K chars ($30/1M) | 4096 chars | No |

**Default model:** `gpt-4o-mini-tts` — it's the most capable and supports voice steering via the `instructions` parameter.

## Available Voices (13 built-in)

| Voice | Character | Best For |
|---|---|---|
| **alloy** | Neutral, balanced | General purpose, narration |
| **ash** | Warm, conversational | Podcasts, casual content |
| **ballad** | Soft, emotive | Storytelling, reflective content |
| **coral** | Clear, friendly | Customer-facing, tutorials |
| **echo** | Smooth, measured | Professional narration |
| **fable** | Expressive, dynamic | Character voices, dramatic reading |
| **nova** | Bright, energetic | Marketing, upbeat content |
| **onyx** | Deep, authoritative | Documentary, leadership content |
| **sage** | Calm, wise | Educational, contemplative |
| **shimmer** | Light, pleasant | Notifications, short-form |
| **verse** | Versatile, natural | Long-form, audiobooks |
| **marin** | Recommended quality | Best overall quality (newer) |
| **cedar** | Recommended quality | Best overall quality (newer) |

**Recommendation:** Use `marin` or `cedar` for best quality. Use `sage` or `onyx` for scholarly/educational content.

## Supported Output Formats

| Format | Use Case | Notes |
|---|---|---|
| **mp3** | General distribution | Default. Widely compatible. |
| **opus** | Streaming, web playback | Low latency, good compression |
| **aac** | Mobile apps | Common for iOS/Android |
| **flac** | Archival, high fidelity | Lossless compression |
| **wav** | Real-time playback | No decode overhead |
| **pcm** | Real-time processing | Raw audio samples, no header |

## Voice Steering (gpt-4o-mini-tts only)

The `instructions` parameter controls delivery style using natural language. This is the key differentiator of `gpt-4o-mini-tts`.

### Controllable Aspects
- **Tone**: "Speak warmly and conversationally" / "Use a formal, authoritative tone"
- **Accent**: "Speak with a British accent" / "Use an Australian accent"
- **Emotion**: "Sound excited and enthusiastic" / "Speak with quiet contemplation"
- **Pacing**: "Speak slowly and deliberately" / "Quick, energetic delivery"
- **Character**: "Sound like a wise professor" / "Speak like a friendly radio host"
- **Whispering**: "Whisper softly"
- **Emphasis**: "Emphasize the key terms"

### Effective Instructions Examples
```
"Speak warmly, like a trusted mentor sharing wisdom with a student. Moderate pace, with pauses for emphasis on key concepts."

"Deliver this as a professional narrator for a documentary. Authoritative but not stiff. Let important phrases land with weight."

"Read this as a podcast host — conversational, engaging, with natural emphasis. Smile in your voice."

"Speak with quiet reverence, as if reading from a cherished old book by candlelight. Slow, contemplative."
```

### Tips for Natural Output
1. **Use punctuation deliberately** — commas create pauses, periods create stops, ellipses create thoughtful breaks
2. **Write for the ear** — break long sentences into shorter ones for natural breathing
3. **Use em dashes** — they create natural emphasis pauses
4. **Avoid acronyms** — spell out "API" as "A-P-I" or write the full phrase
5. **Numbers** — write "twenty-three" not "23" for natural speech
6. **SSML is NOT supported** — use natural language instructions instead

## Execution

### Pattern 1 — Single File Generation (Node.js)

```typescript
import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

const response = await openai.audio.speech.create({
  model: "gpt-4o-mini-tts",
  voice: "sage",
  input: "Your text content here...",
  instructions: "Speak warmly and conversationally, with a scholarly tone.",
  response_format: "mp3",
  speed: 1.0,
});

const buffer = Buffer.from(await response.arrayBuffer());
const outPath = path.join("generated/audio", "output.mp3");
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, buffer);
```

### Pattern 2 — Streaming to File (Node.js)

```typescript
import OpenAI from "openai";
import * as fs from "fs";

const openai = new OpenAI();

const response = await openai.audio.speech.create({
  model: "gpt-4o-mini-tts",
  voice: "marin",
  input: "Your text content here...",
  instructions: "Professional narrator tone.",
  response_format: "mp3",
});

const buffer = Buffer.from(await response.arrayBuffer());
fs.writeFileSync("output.mp3", buffer);
```

### Pattern 3 — Batch: Long Text Split into Chunks

For text longer than 4096 characters, split into chunks at sentence boundaries:

```typescript
import OpenAI from "openai";
import * as fs from "fs";

const openai = new OpenAI();

function splitTextIntoChunks(text: string, maxChars = 4000): string[] {
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  const chunks: string[] = [];
  let current = "";

  for (const sentence of sentences) {
    if ((current + sentence).length > maxChars) {
      if (current) chunks.push(current.trim());
      current = sentence;
    } else {
      current += sentence;
    }
  }
  if (current) chunks.push(current.trim());
  return chunks;
}

async function generateLongAudio(
  text: string,
  voice: string = "sage",
  instructions: string = "",
  outputDir: string = "generated/audio"
) {
  const chunks = splitTextIntoChunks(text);
  const files: string[] = [];

  for (let i = 0; i < chunks.length; i++) {
    const response = await openai.audio.speech.create({
      model: "gpt-4o-mini-tts",
      voice,
      input: chunks[i],
      instructions,
      response_format: "mp3",
    });

    const buffer = Buffer.from(await response.arrayBuffer());
    const outPath = `${outputDir}/chunk-${String(i + 1).padStart(3, "0")}.mp3`;
    fs.mkdirSync(outputDir, { recursive: true });
    fs.writeFileSync(outPath, buffer);
    files.push(outPath);
  }

  return files;
}
```

Then concatenate chunks with ffmpeg:
```bash
# Create file list
for f in generated/audio/chunk-*.mp3; do echo "file '$f'" >> filelist.txt; done
# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy generated/audio/final.mp3
```

### Pattern 4 — Chat Completions with Audio Output

For AI-generated speech (not reading existing text):

```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o-audio-preview",
  modalities: ["text", "audio"],
  audio: { voice: "sage", format: "mp3" },
  messages: [
    { role: "user", content: "Explain the concept of missional communities in 2 sentences." }
  ],
});
```

## Presets by Use Case

| Use Case | Model | Voice | Format | Speed | Instructions |
|---|---|---|---|---|---|
| Course narration | gpt-4o-mini-tts | sage | mp3 | 1.0 | "Professional educator, warm and clear" |
| Podcast intro | gpt-4o-mini-tts | ash | mp3 | 1.0 | "Friendly podcast host, conversational" |
| Audiobook | gpt-4o-mini-tts | verse | mp3 | 0.9 | "Expressive narrator, varied pacing" |
| Notification | tts-1 | shimmer | opus | 1.1 | N/A (not supported) |
| Documentary | gpt-4o-mini-tts | onyx | flac | 0.95 | "Authoritative documentary narrator" |
| Meditation | gpt-4o-mini-tts | ballad | mp3 | 0.8 | "Gentle, calming, with long pauses" |
| Marketing | gpt-4o-mini-tts | nova | mp3 | 1.05 | "Bright, enthusiastic, inspiring" |

## Rate Limits & Costs

| Model | Cost | RPM (starter) |
|---|---|---|
| tts-1 | $15/1M chars | 50 |
| tts-1-hd | $30/1M chars | 50 |
| gpt-4o-mini-tts | $0.60/1M input + $12/1M audio output | 50 |

- Max input per request: 4096 characters
- ~4096 chars ≈ 5 minutes of audio at default speed
- Streaming supported for all models

## Output Format

```
## TTS Generation Report

### Settings
- Model: gpt-4o-mini-tts
- Voice: sage
- Instructions: "Professional educator, warm and clear"
- Format: mp3
- Speed: 1.0
- Input length: 2,450 characters

### Generated Files
1. generated/audio/course-intro.mp3

### Duration
- Estimated: ~3 minutes

### Next Steps
- Review the audio for quality and tone
- Adjust instructions if tone needs refinement
- Use ffmpeg for post-processing if needed
- Use Remotion to combine with video if needed
```

## Error Handling

- Missing `OPENAI_API_KEY` → stop with instructions to add it to `.env.local`
- Input too long (>4096 chars) → auto-split at sentence boundaries, generate chunks, concatenate
- Rate limit hit → wait and retry with exponential backoff
- Voice not found → show list of available voices
- Instructions ignored → remind user that `instructions` only works with `gpt-4o-mini-tts`

## Rules

- Default to `gpt-4o-mini-tts` with `instructions` for maximum control
- Always recommend `marin` or `cedar` for general quality; `sage` for scholarly content
- For long text, split at sentence boundaries — never mid-sentence
- Use `wav` or `pcm` for real-time playback scenarios
- Use `mp3` for general distribution and storage
- Show the voice selection and instructions to the user before generating
- Report file paths, duration estimate, and settings in the output
