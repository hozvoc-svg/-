---
name: video-pipeline
description: End-to-end video production pipeline with the tools available in Claude sessions — research trends/outliers (vidIQ), script and hooks, generate shots (Higgsfield API or other AI video), voiceover and SFX (ElevenLabs API), then assemble, caption, mix and export with ffmpeg in 9:16/16:9 with platform-correct loudness. Use when the user asks to make/зробити/змонтувати a full video, batch several videos, automate production, add subtitles, mix audio, or export for TikTok/Reels/Shorts/YouTube.
---

# Video production pipeline / Повний пайплайн

Run the steps in order. Save every intermediate file in a project folder (`video/<slug>/`) so steps can be re-run. Tell the user which step you're on in one short line.

## 1. Research (vidIQ MCP, if connected)
- `vidiq_outliers` / `vidiq_instagram_tiktok_outlier_search` for the topic → 5 outlier videos.
- `vidiq_video_transcript` on the top 2 → extract their hook, structure, length.
- `vidiq_keyword_research` → title keywords. Summarise: what to copy (structure), what to do differently (angle, style).

## 2. Hook + script
Use `video-hooks` then `short-form-script`. Output: shot list + clean voiceover text + asset list.

## 3. Visuals
- Write prompts with `video-styles` (one locked style suffix + character sheet).
- **Higgsfield** (`platform.higgsfield.ai` / `api.higgsfield.ai`, auth injected by the proxy in cloud sessions): generate a reference image first, then image→video per shot. Poll the job until done, download to `shots/NN.mp4`. Check the current API docs before calling — endpoints change.
- Alternatives: vidIQ `vidiq_generate_video` / `vidiq_generate_broll`, or user-provided footage.
- Generate 1–2 spare variants for the hook shot — it matters most.

## 4. Voice, music, SFX (ElevenLabs, `api.elevenlabs.io`)
- List voices (`GET /v1/voices`), pick one matching genre (deep/slow for horror, energetic for gaming).
- TTS: `POST /v1/text-to-speech/{voice_id}` with `model_id` multilingual for Ukrainian. Save `audio/voice.mp3`.
- Use the `/with-timestamps` variant when available to get word timings for captions.
- SFX: `POST /v1/sound-generation` with a short text description ("deep cinematic boom", "whoosh transition").
- Music: ElevenLabs music or vidIQ `vidiq_generate_music`; otherwise royalty-free.

## 5. Assembly with ffmpeg (check `ffmpeg -version`; install with apt if missing)

Normalize every clip to the same format first:
```bash
ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1" -c:v libx264 -crf 18 -preset medium -an norm/NN.mp4
```
Trim to the shot-list timing: `-ss START -t DUR`. Concatenate:
```bash
printf "file '%s'\n" norm/*.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy video_only.mp4
```
Crossfade between two clips: `-filter_complex "[0][1]xfade=transition=fade:duration=0.3:offset=<len0-0.3>"`.
Punch-in zoom on a shot: `zoompan=z='min(zoom+0.0015,1.15)':d=1:s=1080x1920:fps=30`.

Mix audio (voice on top, music ducked under voice):
```bash
ffmpeg -i video_only.mp4 -i audio/voice.mp3 -i audio/music.mp3 -filter_complex \
"[1]asplit=2[v1][vkey];[2]volume=0.25[m];[m][vkey]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=300[md];[v1][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest mixed.mp4
```

Captions: build an `.ass` file from word timestamps (2–4 words per line, bold, centred around 60–65% height, outline 4 px), then burn in:
```bash
ffmpeg -i mixed.mp4 -vf "ass=captions.ass" -c:a copy final.mp4
```

## 6. Export specs
| Platform | Size | FPS | Length | Loudness |
|---|---|---|---|---|
| TikTok / Reels / Shorts | 1080×1920 | 30 (60 for gaming) | ≤ 60–90 s for reach | −14 LUFS, TP −1.5 |
| YouTube long | 1920×1080 or 3840×2160 | 24/30/60 | any | −14 LUFS |
| Square feed | 1080×1080 | 30 | ≤ 60 s | −14 LUFS |
H.264 High, `-pix_fmt yuv420p`, `-movflags +faststart`, AAC 192k.

## 7. QA before delivering
- Extract frames at 0 s, 1 s and the payoff (`ffmpeg -ss T -i final.mp4 -frames:v 1 f.png`) and look at them: is the hook frame strong, is text inside the safe zone?
- `ffprobe` duration/resolution; check audio isn't clipping.
- Deliver: final MP4, cover image, 3 titles, caption + hashtags. Upload/publish only if the user explicitly asks.

## Batch mode
For N videos: one shared style suffix + character sheet, a table of N topics/hooks, then loop steps 3–7 per row. Report progress per video.
