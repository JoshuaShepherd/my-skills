---
name: youtube-transcript
description: Extract a plain-text transcript from any YouTube video URL. Returns timestamped and full-text versions of the transcript saved to a local file.
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

Extract the transcript from a YouTube video: $ARGUMENTS

$ARGUMENTS should include:
- A YouTube URL (e.g. `https://www.youtube.com/watch?v=VIDEO_ID`, `https://youtu.be/VIDEO_ID`)
- Optionally: `--output PATH` to specify where to save the transcript (default: `transcripts/`)
- Optionally: `--timestamps` to include timestamps in the output (default: plain text only)
- Optionally: `--language LANG` to specify subtitle language code (default: `en`)

---

## Before Starting

1. **Parse the video ID** from the provided URL. Accept these formats:
   - `youtube.com/watch?v=VIDEO_ID`
   - `youtu.be/VIDEO_ID`
   - `youtube.com/embed/VIDEO_ID`
   - `youtube.com/v/VIDEO_ID`
   - A bare video ID (11 characters, alphanumeric + hyphens/underscores)
   - If none of these match, ask the user to provide a valid YouTube link

2. **Check for `yt-dlp`**: Run `which yt-dlp`. If not installed, tell the user:
   ```
   yt-dlp is required. Install it with: pip install yt-dlp
   ```

3. **Ensure output directory exists**: Create `transcripts/` (or the user-specified path) if it doesn't exist

---

## Step 1 — Fetch Video Metadata

Run:
```bash
yt-dlp --print title --print id --print duration_string --print upload_date --no-download "VIDEO_URL"
```

Capture the title, ID, duration, and upload date. These go into the transcript file header.

---

## Step 2 — Download Subtitles

Try in order until one succeeds:

### 2a — Manual (human-authored) subtitles
```bash
yt-dlp --write-subs --sub-lang LANG --skip-download --sub-format vtt -o "transcripts/%(id)s" "VIDEO_URL"
```

### 2b — Auto-generated subtitles (fallback)
```bash
yt-dlp --write-auto-subs --sub-lang LANG --skip-download --sub-format vtt -o "transcripts/%(id)s" "VIDEO_URL"
```

If neither produces a `.vtt` file, report to the user:
```
No subtitles available for this video (language: LANG). The video may not have captions enabled.
```

---

## Step 3 — Parse VTT to Clean Text

Read the downloaded `.vtt` file and process it:

1. **Strip VTT metadata**: Remove `WEBVTT` header, `Kind:`, `Language:` lines, cue IDs, and positioning tags (`<c>`, `align:`, `position:`)
2. **Remove HTML tags**: Strip `<b>`, `<i>`, `<u>`, `<font>`, and any other inline tags
3. **Deduplicate lines**: Auto-generated subs repeat heavily — if a line is identical to the previous line, skip it
4. **Extract timestamps**: Parse `HH:MM:SS.mmm --> HH:MM:SS.mmm` lines and associate with their text
5. **Build two versions**:
   - **Timestamped**: `[MM:SS] Text of the segment` (one line per cue)
   - **Plain text**: All text concatenated into flowing paragraphs. Insert a paragraph break when there's a gap of 3+ seconds between cues or when the speaker appears to change topic

---

## Step 4 — Save Transcript File

Write a markdown file to `transcripts/{video-id}.md` (or the user-specified path):

```markdown
---
title: "VIDEO_TITLE"
video_id: VIDEO_ID
url: https://www.youtube.com/watch?v=VIDEO_ID
duration: DURATION
uploaded: UPLOAD_DATE
extracted: EXTRACTION_DATE
subtitle_type: manual | auto-generated
language: LANG
---

# VIDEO_TITLE

## Transcript

PLAIN_TEXT_TRANSCRIPT

## Timestamped Transcript

TIMESTAMPED_TRANSCRIPT
```

---

## Step 5 — Clean Up

Delete the intermediate `.vtt` file after successful parsing.

---

## Output

After saving, report:

```
## Transcript Extracted

- **Video**: VIDEO_TITLE
- **Duration**: DURATION
- **Subtitles**: manual / auto-generated
- **Word count**: N words
- **Saved to**: transcripts/VIDEO_ID.md
```

---

## Error Handling

- **Invalid URL** — Ask the user to provide a valid YouTube link
- **yt-dlp not installed** — Provide install instructions and stop
- **No subtitles available** — Report clearly, suggest trying a different language with `--language`
- **Network error** — Report the error and suggest retrying
- **yt-dlp timeout** — Use a 60-second timeout on subtitle download; report if exceeded
