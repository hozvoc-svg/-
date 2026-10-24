---
name: asmr-video-builder
description: Builds a finished YouTube video (wordless ASMR or narrated story) from illustrations the user sends, using video-pipeline/. Use when the user sends images and wants a video made from them.
---

You build videos for the user's cozy illustrated channel (Ghibli Home Stories) with the pipeline in `video-pipeline/`.

## Workflow
1. Import every image the user sent into `video-pipeline/images/<episode>/NN.png`, upscaled 1.5x:
   `ffmpeg -i in.jpg -vf "scale=iw*1.5:ih*1.5:flags=lanczos" NN.png`. Keep numbering stable; append new batches after the last number.
2. Look at each image and write `video-pipeline/episodes/<episode>.py` modelled on `rainy_autumn_asmr.py` (wordless) or `rainy_autumn.py` (narrated):
   - order shots so they tell a calm day: morning → activities → evening → night/sleep;
   - per image: lamp/fire positions (normalized x, y, "lamp" | "fire"), a camera path, and window boxes (`"glass"` = rain on glass, `"out"` = open view of rain);
   - wordless cuts: 30 s per shot, 45 s for the final night shots, `AMBIENT = "nature"`, `FADE = 0.001`, `CAPTIONS = False`.
3. Preview a few frames (call `S.SCENES["photo"]` on a cairo surface) and look at them before the full render.
4. Render in the background with an absolute path: `EPISODE=<episode> python3 /home/user/-/video-pipeline/build.py long`.
   Segments are cached by content, so small edits re-render only what changed.
5. Verify before sending: duration, `ebur128` loudness (about -20 LUFS wordless, -16 narrated), brightness of frames at
   segment boundaries (no black flashes), and a contact sheet of 4–8 frames.
6. Re-encode for delivery under 500 MB: `-c:v libx264 -preset medium -crf 23 -tune animation -c:a copy`.
7. Write `<episode>_UPLOAD.md` (title, description, tags, settings, pinned comment) and send video, thumbnail and that file.

## Rules
- Characters in stills cannot be animated here (no GPU). Only overlays, camera moves and depth parallax (`depth.py`).
  If the user wants characters to move, ask for image-to-video clips from Flow or Higgsfield.
- Never put "Ghibli" in video titles (trademark); describe the mood instead.
- Do not upload to YouTube; the user uploads via YouTube Studio.
