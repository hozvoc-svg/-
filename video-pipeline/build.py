"""Build a narrated stickman video: EPISODE=dyatlov python3 build.py long|short|thumb|preview

Voice: ElevenLabs when ELEVENLABS_API_KEY is set, otherwise the local Piper LibriTTS voice.
"""
import importlib, json, math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scenes as S
EPISODE = os.environ.get("EPISODE", "dyatlov")
_ep = importlib.import_module("episodes." + EPISODE)
LONG, SHORT, PRON = _ep.LONG, _ep.SHORT, _ep.PRON

OUT = os.path.join(HERE, "out")
TMP = os.path.join(HERE, "tmp")
VOICE = os.path.join(HERE, "voice/lt/en-us-libritts-high.onnx")
EL_KEY = os.environ.get("ELEVENLABS_API_KEY")
EL_VOICE = os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
EL_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SPEAKER = int(os.environ.get("SPEAKER", "186"))
FPS = 24
SR = 22050
GAP, TAIL = 0.28, 0.45


def say_text(s):
    for k, v in PRON.items():
        s = s.replace(k, v)
    return s


def eleven(text):
    """Raw 16-bit mono PCM at SR from the ElevenLabs text-to-speech API."""
    import urllib.request
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}?output_format=pcm_{SR}",
        data=json.dumps(dict(text=text, model_id=EL_MODEL,
                             voice_settings=dict(stability=0.5, similarity_boost=0.75))).encode(),
        headers={"xi-api-key": EL_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return np.frombuffer(r.read(), np.int16)


def tts(segs, tag):
    if EL_KEY:
        synth = eleven
    else:
        from piper import PiperVoice, SynthesisConfig
        v = PiperVoice.load(VOICE)
        cfg = SynthesisConfig(speaker_id=SPEAKER, length_scale=1.07, noise_scale=0.6, noise_w_scale=0.7)

        def synth(text):
            p = os.path.join(TMP, "_piper.wav")
            with wave.open(p, "wb") as w:
                v.synthesize_wav(text, w, syn_config=cfg)
            with wave.open(p) as w:
                return np.frombuffer(w.readframes(w.getnframes()), np.int16)
    timeline, audio, t0 = [], [], 0
    for si, seg in enumerate(segs):
        parts, sents, cur = [], [], 0
        for s in seg["text"]:
            p = os.path.join(TMP, f"{tag}_{si}_{len(sents)}.wav")
            if os.path.exists(p):  # reuse paid/slow narration on re-runs
                with wave.open(p) as w:
                    x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            else:
                x = synth(say_text(s))
                with wave.open(p, "wb") as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
            sents.append((cur / SR, (cur + len(x)) / SR, s))
            parts += [x, np.zeros(int(GAP * SR), np.int16)]
            cur += len(x) + int(GAP * SR)
        seg_audio = np.concatenate(parts + [np.zeros(int(TAIL * SR), np.int16)])
        frames = math.ceil(len(seg_audio) / SR * FPS)
        seg_audio = np.pad(seg_audio, (0, int(round(frames / FPS * SR)) - len(seg_audio)))
        audio.append(seg_audio)
        timeline.append(dict(scene=seg["scene"], args=seg.get("args", {}), chapter=seg.get("chapter"),
                             start=t0, frames=frames, sents=sents))
        t0 += frames / FPS
    full = np.concatenate(audio)
    p = os.path.join(TMP, f"{tag}_voice.wav")
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(full.tobytes())
    return timeline, p


def chunks(sents, maxw=7):
    """Split sentences into caption chunks with times proportional to characters."""
    out = []
    for a, b, s in sents:
        words = s.split()
        n = max(1, math.ceil(len(words) / maxw))
        per = math.ceil(len(words) / n)
        groups = [" ".join(words[i:i + per]) for i in range(0, len(words), per)]
        tot = sum(len(g) for g in groups)
        t = a
        for g in groups:
            dt = (b - a) * len(g) / tot
            out.append((t, t + dt, g))
            t += dt
    return out


def caption(c, s, cw, cy, size):
    w = S.text_w(c, s, size)
    S.rgba(c, (0, 0, 0), 0.62)
    S.rrect(c, cw / 2 - w / 2 - 26, cy - size - 12, w + 52, size + 36, 16)
    c.fill()
    S.text(c, s, cw / 2, cy + 6, size, S.INK)


def render_segment(job):
    seg, path, vertical = job
    cw, ch = (1080, 1920) if vertical else (S.W, S.H)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, cw, ch)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{cw}x{ch}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "19", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    fn = S.SCENES[seg["scene"]]
    d = seg["frames"] / FPS
    caps = chunks(seg["sents"], 5 if vertical else 7)
    for f in range(seg["frames"]):
        t = f / FPS
        T = seg["start"] + t
        c = cairo.Context(surf)
        c.set_source_rgb(*S.BG1)
        c.paint()
        c.save()
        if vertical:
            c.translate(540, 820)
            c.scale(1.12, 1.12)
            c.translate(-S.W / 2 - 60, -S.H / 2)
        z = 1 + 0.035 * t / d
        c.translate(S.W / 2, S.H / 2)
        c.scale(z, z)
        c.translate(-S.W / 2, -S.H / 2)
        fn(c, t, d, T, seg["args"])
        S.vignette(c)
        c.restore()
        if vertical:
            S.snowfall(c, T, 0.4)
            S.text(c, "9 hikers. 1 tent.", cw / 2, 180, 72, S.INK)
            S.text(c, "Cut from the INSIDE.", cw / 2, 270, 64, S.RED)
        for a, b, s in caps:
            if a <= t < b + 0.05:
                if vertical:
                    caption(c, s, cw, 1560, 62)
                else:
                    caption(c, s, cw, ch - 70, 44)
                break
        fade = 1 - S.clamp(t / 0.25)
        if fade > 0:
            c.set_source_rgba(0, 0, 0, fade * 0.8)
            c.paint()
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


def mix(voice, video_list, out, total):
    lst = os.path.join(TMP, os.path.basename(out) + ".txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in video_list)
    # ambient: brown-noise wind plus a slow low drone under the narration
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-i", voice,
                    "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=brown:amplitude=0.5:seed=4",
                    "-f", "lavfi", "-t", str(total), "-i", "sine=frequency=55:sample_rate=44100",
                    "-f", "lavfi", "-t", str(total), "-i", "sine=frequency=82.4:sample_rate=44100",
                    "-filter_complex",
                    "[1:a]aresample=44100,highpass=f=70,acompressor=threshold=0.1:ratio=3,loudnorm=I=-15:TP=-1.5[v];"
                    "[2:a]lowpass=f=400,volume=0.10,tremolo=f=0.1:d=0.6[w];"
                    "[3:a]volume=0.035,tremolo=f=0.1:d=0.5[d1];[4:a]volume=0.025,tremolo=f=0.13:d=0.5[d2];"
                    "[w][d1][d2]amix=inputs=3:normalize=0[amb];"
                    "[v][amb]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)


def build(kind):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    vertical = kind == "short"
    segs = SHORT if vertical else LONG
    timeline, voice = tts(segs, kind)
    jobs = [(seg, os.path.join(TMP, f"{kind}_seg{i:02d}.mp4"), vertical) for i, seg in enumerate(timeline)]
    jobs_sorted = sorted(jobs, key=lambda j: -j[0]["frames"])
    with Pool(os.cpu_count()) as pool:
        pool.map(render_segment, jobs_sorted)
    total = sum(s["frames"] for s in timeline) / FPS
    out = os.path.join(OUT, f"{EPISODE}_{kind}.mp4")
    mix(voice, [j[1] for j in jobs], out, total)
    chap = [(s["start"], s["chapter"]) for s in timeline if s.get("chapter")]
    with open(os.path.join(TMP, f"{kind}_timeline.json"), "w") as fh:
        json.dump(dict(total=total, chapters=chap), fh)
    print(out, round(total, 1), "s")
    for st, n in chap:
        print(f"{int(st // 60)}:{int(st % 60):02d} {n}")


def thumb():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
    c = cairo.Context(surf)
    c.scale(1280 / S.W, 720 / S.H)
    c.save()
    c.translate(-500, -250)
    c.scale(1.5, 1.5)
    S.sky(c, T=1)
    S.far_mountains(c)
    S.slope(c)
    S.tent(c, 1250, S.slope_y(1250) + 6, 1.9, cut=1, buried=0.2)
    S.footprints(c, 1110, S.slope_y(1110) + 50, 700, S.slope_y(700) + 50, 1, lanes=5)
    c.restore()
    S.snowfall(c, 3, 1.0)
    S.vignette(c)
    c.save()
    c.translate(160, 0)
    S.text(c, "CUT FROM", 0, 250, 150, S.INK, align="left")
    S.text(c, "THE INSIDE", 0, 400, 150, S.RED, align="left")
    c.restore()
    S.stick(c, 1700, 1000, 2.4, col=S.INK)
    S.text(c, "?", 1700, 520, 240, S.RED)
    S.label(c, "9 HIKERS · 1959", 360, 1000, 56, S.AMBER)
    surf.write_to_png(os.path.join(OUT, f"{EPISODE}_thumbnail.png"))


def preview():
    """One still per scene for a quick visual check."""
    os.makedirs(os.path.join(TMP, "prev"), exist_ok=True)
    for i, seg in enumerate(LONG):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S.W, S.H)
        c = cairo.Context(surf)
        S.SCENES[seg["scene"]](c, 9.0, 10.0, 9.0, seg.get("args", {}))
        surf.write_to_png(os.path.join(TMP, "prev", f"{i:02d}_{seg['scene']}.png"))


if __name__ == "__main__":
    k = sys.argv[1]
    {"long": lambda: build("long"), "short": lambda: build("short"), "thumb": thumb, "preview": preview}[k]()
