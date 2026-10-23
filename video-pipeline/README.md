# Stickman Unsolved: video pipeline

Builds a narrated stickman-animation episode (long 16:9 video, vertical Short, thumbnail)
from a script in `episodes/`.

## Setup (once per machine)

```bash
pip install pycairo numpy piper-tts
# ffmpeg must be installed
```

Voice:
- **ElevenLabs** is used when `ELEVENLABS_API_KEY` is set. Optional: `ELEVENLABS_VOICE_ID`
  (default `JBFqnCBsd6RMkjVDRZzb`), `ELEVENLABS_MODEL` (default `eleven_multilingual_v2`).
  Commercial use needs a paid ElevenLabs plan.
- Otherwise the local **Piper LibriTTS** voice (CC BY 4.0, speaker 186) is used:
  ```bash
  mkdir -p voice/lt && curl -L https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-libritts-high.tar.gz | tar xz -C voice/lt
  ```

## Build

```bash
EPISODE=dyatlov python3 build.py preview   # one still per scene -> tmp/prev/
EPISODE=dyatlov python3 build.py long      # out/dyatlov_long.mp4
EPISODE=dyatlov python3 build.py short     # out/dyatlov_short.mp4
EPISODE=dyatlov python3 build.py thumb     # out/dyatlov_thumbnail.png (Dyatlov-specific design)
```

Narration is cached per sentence in `tmp/`; delete `tmp/` after changing the voice or the script text.

## Files

- `scenes.py`: scene library (stick figures, slope, tent, map, documents and so on).
- `build.py`: narration, caption timing, parallel rendering, audio mix.
- `episodes/<name>.py`: `LONG` and `SHORT` segment lists plus `PRON` pronunciation fixes.
- `episodes/<name>_UPLOAD.md`: title, description, tags and chapters for YouTube.
