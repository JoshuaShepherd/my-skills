
Generate speech, sound effects, or voice clones using ElevenLabs: $ARGUMENTS

$ARGUMENTS should include:
- Text to convert to speech (inline or path to text/markdown file)
- Optionally: voice name or voice_id
- Optionally: model (eleven_v3, eleven_multilingual_v2, eleven_flash_v2_5)
- Optionally: task type (tts, sound-effect, voice-clone, voice-design, audio-isolation, dubbing)
- Optionally: voice settings (stability, similarity_boost, style)
- Optionally: output format (mp3, pcm, opus)
- Optionally: output path
- Empty — ask the user what they want to generate

## Authoritative Documentation

### Primary References
- Documentation Hub: https://elevenlabs.io/docs/overview/intro
- API Reference: https://elevenlabs.io/docs/api-reference/introduction
- Authentication: https://elevenlabs.io/docs/api-reference/authentication
- Quickstart: https://elevenlabs.io/docs/quickstart

### Text-to-Speech
- TTS API: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- TTS Streaming: https://elevenlabs.io/docs/api-reference/text-to-speech/stream
- WebSocket TTS: https://elevenlabs.io/docs/api-reference/text-to-speech/v-1-text-to-speech-voice-id-stream-input
- TTS Best Practices: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices

### Models
- Models Overview: https://elevenlabs.io/docs/overview/models

### Voices
- Voice Library: https://elevenlabs.io/docs/eleven-creative/voices/voice-library
- Voice Cloning: https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning
- Voice Design: https://elevenlabs.io/docs/eleven-creative/voices/voice-design
- Voice Settings: https://elevenlabs.io/docs/api-reference/voices/settings/get
- IVC API: https://elevenlabs.io/docs/api-reference/voices/ivc/create
- IVC Cookbook: https://elevenlabs.io/docs/cookbooks/voices/instant-voice-cloning
- PVC Guide: https://elevenlabs.io/docs/product-guides/voices/voice-cloning/professional-voice-cloning

### Sound Effects & Audio
- Sound Effects: https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
- Audio Isolation: https://elevenlabs.io/docs/api-reference/audio-isolation/convert
- Streaming: https://elevenlabs.io/docs/api-reference/streaming

### Long-form & Dubbing
- Studio Projects: https://elevenlabs.io/docs/api-reference/studio/add-project
- Dubbing: https://elevenlabs.io/docs/api-reference/dubbing/create

### Pronunciation
- Pronunciation Dictionaries: https://elevenlabs.io/docs/eleven-api/guides/cookbooks/text-to-speech/pronunciation-dictionaries

### SDKs
- Python SDK: https://github.com/elevenlabs/elevenlabs-python
- JS SDK: https://github.com/elevenlabs/elevenlabs-js

### Pricing & Limits
- Pricing: https://elevenlabs.io/pricing
- API Pricing: https://elevenlabs.io/pricing/api
- Error Codes: https://elevenlabs.io/docs/eleven-api/resources/errors

## Before Starting

1. Confirm `ELEVENLABS_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Check if the SDK is installed — if not: `pnpm add @11labs/client`
3. Determine the task type and appropriate model

## Available Models

| Model | model_id | Languages | Latency | Best For |
|---|---|---|---|---|
| **Eleven v3** | `eleven_v3` | 70+ | Standard | Audio tags, multi-speaker dialogue, emotion control |
| **Multilingual v2** | `eleven_multilingual_v2` | 29 | Standard | Highest quality, most nuanced expression |
| **Flash v2.5** | `eleven_flash_v2_5` | 32 | ~75ms | Real-time apps, low-latency streaming |
| **Flash v2** | `eleven_flash_v2` | English | Low | English-only, fast, phoneme dict support |
| **Turbo v2.5** | `eleven_turbo_v2_5` | 32 | Low | Equivalent to Flash v2.5, slightly higher latency |

**Default:** `eleven_multilingual_v2` for quality. `eleven_flash_v2_5` for real-time. `eleven_v3` for emotion/audio tags.

### Eleven v3 Unique Features
- **Audio Tags**: Inline emotion/sound cues in text:
  - `[excited]`, `[whispers]`, `[sighs]`, `[laughs]`
  - `[gunshot]`, `[clapping]`, `[explosion]`
- **Text-to-Dialogue**: Structured JSON array of speaker turns → cohesive multi-speaker audio
- Speaker Boost is NOT available for v3

## Voice Settings

All values range 0.0 to 1.0:

| Setting | Description | Recommended |
|---|---|---|
| **stability** | Consistency between generations. Lower = more expressive/varied. Higher = more monotone/consistent. | 0.50 |
| **similarity_boost** | Fidelity to original speaker voice. Higher = more similar but increases latency. | 0.75 |
| **style** | Amplifies speaker's original style. Higher = more expressive but increases compute. | 0.0 |
| **use_speaker_boost** | Boolean. Boosts speaker similarity. NOT available for v3. | true |

## Output Formats

### MP3
`mp3_22050_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`

### PCM (raw)
`pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`, `pcm_48000`

### Opus
`opus_48000_64`, `opus_48000_128`, `opus_48000_192`

### Telephony
`ulaw_8000`, `alaw_8000`

**Default:** MP3. Use PCM for real-time playback. Use Opus for web streaming.

## Execution Patterns

### Pattern 1 — Text-to-Speech (Node.js)

```typescript
import { ElevenLabsClient } from "@11labs/client";
import * as fs from "fs";

const client = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});

const audio = await client.textToSpeech.convert("voice_id_here", {
  model_id: "eleven_multilingual_v2",
  text: "Your text content here...",
  voice_settings: {
    stability: 0.5,
    similarity_boost: 0.75,
    style: 0.0,
    use_speaker_boost: true,
  },
  output_format: "mp3_44100_128",
});

// Write to file
const chunks: Buffer[] = [];
for await (const chunk of audio) {
  chunks.push(Buffer.from(chunk));
}
const buffer = Buffer.concat(chunks);
fs.mkdirSync("generated/audio", { recursive: true });
fs.writeFileSync("generated/audio/output.mp3", buffer);
```

### Pattern 2 — Streaming TTS

```typescript
const audioStream = await client.textToSpeech.stream("voice_id_here", {
  model_id: "eleven_flash_v2_5",
  text: "Streaming text content...",
  output_format: "mp3_44100_128",
});

// Stream chunks as they arrive
for await (const chunk of audioStream) {
  // Process or pipe chunk
}
```

### Pattern 3 — Eleven v3 with Audio Tags

```typescript
const audio = await client.textToSpeech.convert("voice_id_here", {
  model_id: "eleven_v3",
  text: `[excited] Oh wow, this is incredible! [sighs] But then I realized... [whispers] it was all a dream.`,
  voice_settings: {
    stability: 0.4,
    similarity_boost: 0.75,
  },
});
```

### Pattern 4 — Sound Effects

```typescript
const sfx = await client.textToSoundEffects.convert({
  text: "A warm crackling fireplace with occasional pops and gentle wind outside",
  duration_seconds: 15,
});

const chunks: Buffer[] = [];
for await (const chunk of sfx) {
  chunks.push(Buffer.from(chunk));
}
fs.writeFileSync("generated/audio/fireplace.mp3", Buffer.concat(chunks));
```

Duration: 0.5s to 30s. Supports seamless looping for ambient sounds.

### Pattern 5 — Instant Voice Clone

```typescript
const voice = await client.voices.ivc.create({
  name: "My Custom Voice",
  files: [fs.createReadStream("sample-audio.mp3")],
  description: "Warm, scholarly male voice",
});

// Use the cloned voice
const audio = await client.textToSpeech.convert(voice.voice_id, {
  model_id: "eleven_multilingual_v2",
  text: "Hello from my cloned voice!",
});
```

Requires Starter+ plan. Short audio samples sufficient for IVC.

### Pattern 6 — Voice Design (Text-to-Voice)

```typescript
const preview = await client.textToVoice.design({
  text: "A warm, authoritative male voice with a slight Australian accent, suitable for educational content.",
  voice_description: "Male, 40s, warm, scholarly",
  model_id: "eleven_multilingual_ttv_v2",
});

// Preview returns generated_voice_id and base64 audio samples
```

### Pattern 7 — Audio Isolation

```typescript
const isolated = await client.audioIsolation.convert({
  audio: fs.createReadStream("noisy-audio.mp3"),
});

const chunks: Buffer[] = [];
for await (const chunk of isolated) {
  chunks.push(Buffer.from(chunk));
}
fs.writeFileSync("generated/audio/clean-voice.mp3", Buffer.concat(chunks));
```

### Pattern 8 — Long-form with Chunking

For text longer than ~5000 characters, split into paragraphs:

```typescript
function splitIntoParagraphs(text: string, maxChars = 4500): string[] {
  const paragraphs = text.split(/\n\n+/);
  const chunks: string[] = [];
  let current = "";

  for (const para of paragraphs) {
    if ((current + "\n\n" + para).length > maxChars) {
      if (current) chunks.push(current.trim());
      current = para;
    } else {
      current = current ? current + "\n\n" + para : para;
    }
  }
  if (current) chunks.push(current.trim());
  return chunks;
}
```

## Presets by Use Case

| Use Case | Model | Voice Settings | Format | Notes |
|---|---|---|---|---|
| Course narration | eleven_multilingual_v2 | stability: 0.6, similarity: 0.8 | mp3_44100_128 | Consistent, clear |
| Podcast | eleven_v3 | stability: 0.4, similarity: 0.7 | mp3_44100_128 | Expressive, use audio tags |
| Audiobook | eleven_multilingual_v2 | stability: 0.5, similarity: 0.8, style: 0.3 | mp3_44100_192 | Nuanced, high quality |
| Real-time chat | eleven_flash_v2_5 | stability: 0.5, similarity: 0.75 | pcm_24000 | Low latency |
| Sound design | — | — | mp3_44100_128 | Use sound effects API |
| Voice clone | eleven_multilingual_v2 | stability: 0.5, similarity: 0.85 | mp3_44100_128 | IVC or PVC |

## Pricing

| Plan | Price/mo | Characters/mo | Concurrency |
|---|---|---|---|
| Free | $0 | 10,000 | 2 |
| Starter | $5 | 30,000 | 3 |
| Creator | $22 | 100,000 | 5 |
| Pro | $99 | 500,000 | 10 |
| Scale | $330 | 2,000,000 | 15 |

- Flash/Turbo models: 0.5-1 credit per character (discounted)
- Overage: $0.12-$0.30 per 1K chars depending on plan
- Free tier: no commercial use, requires attribution
- Starter+: commercial rights unlocked

## Pronunciation Control

ElevenLabs does NOT support standard SSML. Instead:

1. **Punctuation**: Commas = pauses, periods = stops, ellipses = thoughtful breaks, em-dashes = emphasis pauses
2. **Audio Tags** (v3 only): `[excited]`, `[whispers]`, `[sighs]` etc.
3. **Pronunciation Dictionaries**: XML-based `.pls` files with alias and phoneme rules
   - Up to 3 dictionaries per request
   - Phoneme tags only work with `eleven_flash_v2`

## Output Format

```
## ElevenLabs Generation Report

### Settings
- Model: eleven_multilingual_v2
- Voice: [voice name] (voice_id)
- Stability: 0.5 | Similarity: 0.75 | Style: 0.0
- Format: mp3_44100_128
- Input length: 3,200 characters

### Generated Files
1. generated/audio/course-narration.mp3

### Estimated Credits
- ~3,200 credits (1:1 for standard models)

### Next Steps
- Review audio for quality and tone
- Adjust voice settings if needed (lower stability for more expression)
- Use audio isolation to clean up if needed
- Combine with video using Remotion
```

## Error Handling

- Missing `ELEVENLABS_API_KEY` → stop with instructions to add it
- 429 `rate_limit_exceeded` → too many requests/second, back off and retry
- 429 `concurrent_limit_exceeded` → too many parallel requests, reduce concurrency
- Character quota exceeded → report remaining quota, suggest upgrading plan
- Voice not found → list available voices or suggest voice library browse

## Rules

- Default to `eleven_multilingual_v2` for quality, `eleven_flash_v2_5` for real-time
- Use `eleven_v3` when audio tags or multi-speaker dialogue are needed
- Voice settings: start with stability 0.5, similarity 0.75 — adjust from there
- For long text, split at paragraph boundaries — never mid-sentence
- Use `mp3_44100_128` for general distribution, PCM for real-time
- Show voice selection and settings to user before generating
- Report voice, model, settings, credits used, and file path in output
- Speaker Boost is NOT available on v3 — don't set it
- Phoneme pronunciation only works with `eleven_flash_v2`
