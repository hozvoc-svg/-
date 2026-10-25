"""Build a narrated stickman video: EPISODE=dyatlov python3 build.py long|short|thumb|preview

Voice: ElevenLabs when ELEVENLABS_API_KEY is set, otherwise the local Piper LibriTTS voice.
"""
import hashlib, importlib, json, math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
import cairo
import styles as ST

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
EPISODE = os.environ.get("EPISODE", "dyatlov")
_ep = importlib.import_module("episodes." + EPISODE)
LONG, SHORT, PRON = _ep.LONG, _ep.SHORT, _ep.PRON
S = importlib.import_module(getattr(_ep, "SCENES_MODULE", "scenes"))

OUT = os.path.join(HERE, "out")
TMP = os.path.join(HERE, "tmp")
VOICE = os.path.join(HERE, "voice/lt/en-us-libritts-high.onnx")
EL_KEY = os.environ.get("ELEVENLABS_API_KEY")
# ELEVENLABS=1 uses ElevenLabs without a local key: the environment's network secret injects xi-api-key
EL_ON = bool(EL_KEY) or os.environ.get("ELEVENLABS") == "1"
EL_VOICE = os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
EL_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
EL_SETTINGS = getattr(_ep, "EL_SETTINGS", dict(stability=0.5, similarity_boost=0.75))
EL_VOICE = getattr(_ep, "EL_VOICE", EL_VOICE)
SPEAKER = int(os.environ.get("SPEAKER", getattr(_ep, "SPEAKER", 186)))
LENGTH_SCALE = getattr(_ep, "LENGTH_SCALE", 1.07)
AMBIENT = getattr(_ep, "AMBIENT", "drone")
CAPTION_SIZE = getattr(_ep, "CAPTION_SIZE", 44)
XFADE = getattr(_ep, "XFADE", 0.0)               # seconds of dissolve between consecutive segments
OVERLAY_FX = getattr(_ep, "OVERLAY_FX", ())      # e.g. (("shooting_star", 0.8),) drawn over every frame
CHAPTER_STYLE = getattr(_ep, "CHAPTER_STYLE", None)  # styles.TITLES key for animated chapter names
CHAPTER_PAIR = getattr(_ep, "CHAPTER_PAIR", "storybook")
CHAPTER_SUB = getattr(_ep, "CHAPTER_SUB", "")
FINAL = getattr(_ep, "FINAL", "x264")            # delivery encode: "x264" 1080p or "hevc1440" (sharper on YouTube)
FPS = 24
SR = 22050
GAP, TAIL = getattr(_ep, "GAP", 0.28), getattr(_ep, "TAIL", 0.45)


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
                             voice_settings=EL_SETTINGS)).encode(),
        headers={"Content-Type": "application/json", **({"xi-api-key": EL_KEY} if EL_KEY else {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return np.frombuffer(r.read(), np.int16)


def tts(segs, tag):
    if EL_ON:
        synth = eleven
    else:
        from piper import PiperVoice, SynthesisConfig
        v = PiperVoice.load(VOICE)
        cfg = SynthesisConfig(speaker_id=SPEAKER, length_scale=LENGTH_SCALE, noise_scale=0.6, noise_w_scale=0.7)

        def synth(text):
            p = os.path.join(TMP, "_piper.wav")
            with wave.open(p, "wb") as w:
                v.synthesize_wav(text, w, syn_config=cfg)
            with wave.open(p) as w:
                return np.frombuffer(w.readframes(w.getnframes()), np.int16)
    timeline, audio, t0 = [], [], 0
    for si, seg in enumerate(segs):
        parts, sents, cur = [], [], 0
        for s in seg.get("text", ()):
            key = hashlib.md5(f"{EL_ON and (EL_VOICE, EL_MODEL, sorted(EL_SETTINGS.items()))}|{SPEAKER}|{LENGTH_SCALE}|{say_text(s)}".encode()).hexdigest()[:16]
            p = os.path.join(TMP, f"tts_{key}.wav")
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
        if seg.get("duration"):  # wordless (ASMR) segment of fixed length
            parts = [np.zeros(int(seg["duration"] * SR), np.int16)]
        seg_audio = np.concatenate(parts + [np.zeros(int(TAIL * SR), np.int16)])
        frames = math.ceil(len(seg_audio) / SR * FPS)
        seg_audio = np.pad(seg_audio, (0, int(round(frames / FPS * SR)) - len(seg_audio)))
        audio.append(seg_audio)
        timeline.append(dict(scene=seg["scene"], args=seg.get("args", {}), chapter=seg.get("chapter"),
                             start=t0, frames=frames, sents=sents))
        t0 += frames / FPS
    full = np.concatenate(audio)
    p = os.path.join(TMP, f"{EPISODE}_{tag}_voice.wav")  # per-episode: parallel builds must not share it
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
    seg, final_path, vertical = job
    path = final_path + ".part.mp4"
    cw, ch = (1080, 1920) if vertical else (S.W, S.H)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, cw, ch)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{cw}x{ch}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "16", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
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
        prev = seg.get("prev")
        if XFADE and prev and t < XFADE:  # dissolve in from the previous scene, still moving
            pd = prev["frames"] / FPS
            c.push_group()
            c.set_source_rgb(*S.BG1)
            c.paint()
            S.SCENES[prev["scene"]](c, pd + t, pd + XFADE, T, prev["args"])
            c.pop_group_to_source()
            c.paint_with_alpha(1 - ST.ease(t / XFADE))
        for name, strength in OVERLAY_FX:
            ST.FX[name](c, T, strength)
        S.vignette(c)
        c.restore()
        if CHAPTER_STYLE and seg.get("chapter") and seg["start"] > 1 and 1.5 <= t < 9.5:
            ST.TITLES[CHAPTER_STYLE](c, seg["chapter"], CHAPTER_SUB, (t - 1.5) / 8.0, CHAPTER_PAIR, y=S.H * 0.86)
        if vertical:
            S.snowfall(c, T, 0.4)
            S.text(c, "9 hikers. 1 tent.", cw / 2, 180, 72, S.INK)
            S.text(c, "Cut from the INSIDE.", cw / 2, 270, 64, S.RED)
        for a, b, s in (caps if getattr(_ep, "CAPTIONS", True) else ()):
            if a <= t < b + 0.05:
                if vertical:
                    caption(c, s, cw, 1560, 62)
                else:
                    caption(c, s, cw, ch - 70, CAPTION_SIZE)
                break
        fade_len = getattr(_ep, "FADE", 0.25)
        fade = 1 - S.clamp(t / fade_len) if fade_len > 0.05 else 0.0  # tiny FADE = no dip to black
        if fade > 0:
            c.set_source_rgba(0, 0, 0, fade * 0.8)
            c.paint()
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    os.replace(path, final_path)
    return final_path


def cozy_ambience(timeline, total):
    """Soft procedural piano + pad (music.wav) and rain noise enveloped to rainy scenes (rain.wav)."""
    sr = 44100
    n = int(total * sr) + sr
    rng = np.random.default_rng(3)
    music = np.zeros(n, np.float32)
    chords = [[53, 57, 60, 64], [50, 53, 57, 60], [46, 50, 53, 57], [48, 52, 55, 60]]  # Fmaj7 Dm7 Bbmaj7 C
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = 4.0
    def note(m, start, dur, amp, decay):
        i0 = int(start * sr)
        L = min(int(dur * sr), n - i0)
        if L <= 0:
            return
        tt = np.arange(L) / sr
        f = hz(m)
        env = np.exp(-tt * decay) * np.minimum(1, tt / 0.01)
        w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt)
        music[i0:i0 + L] += (amp * env * w).astype(np.float32)
    k = 0
    tpos = 0.0
    while tpos < total:
        ch = chords[k % 4]
        for m in ch:  # soft pad
            i0 = int(tpos * sr); L = min(int(bar * 1.1 * sr), n - i0)
            if L > 0:
                tt = np.arange(L) / sr
                env = np.sin(np.pi * np.clip(tt / (bar * 1.1), 0, 1)) ** 2
                music[i0:i0 + L] += (0.035 * env * np.sin(2 * np.pi * hz(m) * tt)).astype(np.float32)
        for b in range(4):  # sparse piano melody
            if rng.random() < 0.7:
                m = rng.choice(ch) + 12 + (12 if rng.random() < 0.3 else 0)
                note(m, tpos + b * 1.0 + rng.random() * 0.08, 3.5, 0.06, 1.3)
        note(ch[0] - 12, tpos, 4.0, 0.07, 0.8)
        tpos += bar
        k += 1
    for dl, g in [(0.23, 0.35), (0.37, 0.25), (0.53, 0.18), (0.79, 0.12)]:  # cheap reverb
        dd = int(dl * sr)
        music[dd:] += g * music[:-dd]
    music *= 0.5 / max(1e-6, np.abs(music).max())
    # rain: spectrally shaped noise in chunks, enveloped by scene
    rain = np.zeros(n, np.float32)
    ch = sr * 10
    freqs = np.fft.rfftfreq(ch, 1 / sr)
    shape = np.where(freqs > 200, 1 / np.sqrt(np.maximum(freqs, 1)), 0) * np.exp(-freqs / 9000)
    for i in range(0, n, ch):
        spec = np.fft.rfft(rng.standard_normal(ch)) * shape
        seg = np.fft.irfft(spec, ch).astype(np.float32)
        rain[i:i + ch] = seg[:len(rain[i:i + ch])]
    rain *= 0.35 / max(1e-6, np.abs(rain).max())
    env = np.zeros(n, np.float32)
    for s in timeline:
        rainy = s["scene"] in ("rain_window", "rain_room") or s["args"].get("rain")
        if rainy:
            a = int(s["start"] * sr); b = int((s["start"] + s["frames"] / FPS) * sr)
            env[a:b] = 1.0
    kern = np.ones(int(2.5 * sr), np.float32) / int(2.5 * sr)
    env = np.convolve(env[::100], kern[::100] * 100, mode="same")[np.arange(n) // 100]
    rain *= env
    paths = []
    for name, x in (("music", music), ("rain", rain)):
        p = os.path.join(TMP, f"{EPISODE}_{name}.wav")
        with wave.open(p, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        paths.append(p)
    return paths


def nature_ambience(timeline, total):
    """Stereo rain bed with gusts and drips, fire crackle under fire shots, a few distant thunder rolls."""
    sr = 44100
    n = int(total * sr) + sr
    rng = np.random.default_rng(11)
    ch = sr * 10
    freqs = np.fft.rfftfreq(ch, 1 / sr)

    def shaped(shape):
        out = np.zeros(n, np.float32)
        for i in range(0, n, ch):
            seg = np.fft.irfft(np.fft.rfft(rng.standard_normal(ch)) * shape, ch).astype(np.float32)
            out[i:i + ch] = seg[:len(out[i:i + ch])]
        return out / max(1e-6, np.abs(out).max())

    def smooth_env(points, lo, hi):
        """Slow random envelope from `points` control values per minute."""
        k = max(2, int(total / 60 * points))
        ctrl = lo + (hi - lo) * rng.random(k + 2)
        x = np.linspace(0, k + 1, n)
        return np.interp(x, np.arange(k + 2), ctrl).astype(np.float32)

    hiss = np.where(freqs > 300, 1 / np.sqrt(np.maximum(freqs, 1)), 0) * np.exp(-freqs / 11000)
    body = np.where(freqs > 60, 1 / np.maximum(freqs, 1) ** 0.8, 0) * np.exp(-freqs / 2500)
    gust = smooth_env(3, 0.75, 1.0)
    left = (0.55 * shaped(hiss) + 0.45 * shaped(body)) * gust
    right = (0.55 * shaped(hiss) + 0.45 * shaped(body)) * gust
    # drips: short bright ticks scattered in time, panned at random
    t = np.arange(int(0.03 * sr)) / sr
    for _ in range(int(total * 1.2)):
        i = rng.integers(0, n - len(t))
        tick = (np.sin(2 * np.pi * rng.uniform(1800, 3800) * t) * np.exp(-t * 180)).astype(np.float32) * rng.uniform(0.05, 0.16)
        pan = rng.random()
        left[i:i + len(t)] += tick * (1 - pan)
        right[i:i + len(t)] += tick * pan
    # fire: crackles + low roar, faded in and out with the shots that show a fire
    fire_env = np.zeros(n, np.float32)
    for sgm in timeline:
        if any(k == "fire" for *_, k in sgm["args"].get("lamps", ())):
            a = int(sgm["start"] * sr); b = int((sgm["start"] + sgm["frames"] / FPS) * sr)
            fire_env[a:b] = 1.0
    kern = np.ones(300, np.float32) / 300
    fire_env = np.convolve(fire_env[::147], kern, mode="same")[np.minimum(np.arange(n) // 147, len(fire_env[::147]) - 1)]
    roar = shaped(np.where(freqs > 40, 1 / np.maximum(freqs, 1), 0) * np.exp(-freqs / 600)) * 0.35
    crack = np.zeros(n, np.float32)
    tc = np.arange(int(0.02 * sr)) / sr
    for _ in range(int(total * 6)):
        i = rng.integers(0, n - len(tc))
        burst = rng.standard_normal(len(tc)).astype(np.float32) * np.exp(-tc * rng.uniform(150, 400)).astype(np.float32)
        crack[i:i + len(tc)] += burst * rng.uniform(0.1, 0.6) ** 2
    crack = np.diff(crack, prepend=0) * 2.0  # brighter, snappier pops
    fire = (roar + crack) * fire_env
    left += fire * 0.9
    right += fire * 0.9
    # distant thunder: a few long low rumbles
    for k in range(max(1, int(total / 420))):
        start = rng.uniform(0.1, 0.9) * total
        L = int(9 * sr)
        i = int(start * sr)
        if i + L >= n:
            continue
        tt = np.arange(L) / sr
        env = (1 - np.exp(-tt * 1.5)) * np.exp(-tt * 0.45)
        rum = np.fft.irfft(np.fft.rfft(rng.standard_normal(L)) * (np.fft.rfftfreq(L, 1 / sr) < 120), L).astype(np.float32)
        rum = rum / max(1e-6, np.abs(rum).max()) * env.astype(np.float32) * 0.35
        left[i:i + L] += rum
        right[i:i + L] += rum * 0.85
    st = np.stack([left, right], 1)
    st *= 0.8 / max(1e-6, np.abs(st).max())
    p = os.path.join(TMP, f"{EPISODE}_nature.wav")
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    return p


def space_ambience(total):
    """Stereo drone: slow, overlapping pad chords plus a faint filtered-noise 'solar wind'."""
    sr = 44100
    n = int(total * sr) + sr
    rng = np.random.default_rng(21)
    out = np.zeros((n, 2), np.float32)
    chords = [[55.0, 82.41, 110.0, 164.81, 246.94], [49.0, 73.42, 110.0, 146.83, 220.0],
              [43.65, 65.41, 98.0, 130.81, 196.0], [51.91, 77.78, 116.54, 155.56, 233.08]]
    step, L = 24.0, 36.0  # a new chord every 24 s, each lasting 36 s so they overlap
    tt = np.arange(int(L * sr)) / sr
    env = (np.sin(np.pi * tt / L) ** 2).astype(np.float32)
    k, t0 = 0, 0.0
    while t0 < total:
        i0 = int(t0 * sr)
        m = min(len(tt), n - i0)
        for j, f in enumerate(chords[k % len(chords)]):
            for ch, det in ((0, 0.997), (1, 1.003)):
                ph = rng.random() * 6.28
                amp = 0.05 / (1 + j * 0.6)
                trem = 1 + 0.15 * np.sin(2 * np.pi * (0.03 + 0.01 * j) * tt[:m] + ph)
                out[i0:i0 + m, ch] += (amp * env[:m] * trem * np.sin(2 * np.pi * f * det * tt[:m] + ph)).astype(np.float32)
        t0 += step
        k += 1
    ch = sr * 10
    freqs = np.fft.rfftfreq(ch, 1 / sr)
    shape = np.where((freqs > 80) & (freqs < 900), 1 / np.sqrt(np.maximum(freqs, 1)), 0)
    for c_ in range(2):
        for i in range(0, n, ch):
            seg = np.fft.irfft(np.fft.rfft(rng.standard_normal(ch)) * shape, ch).astype(np.float32)
            out[i:i + ch, c_][:] += seg[:len(out[i:i + ch])] * 0.01
    out *= 0.6 / max(1e-6, np.abs(out).max())
    p = os.path.join(TMP, f"{EPISODE}_space.wav")
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    return p


def mix(voice, video_list, out, total, timeline=None):
    if AMBIENT == "music":
        import music
        mus = os.path.join(TMP, f"{EPISODE}_music.wav")
        music.render(mus, total + 1, seed=getattr(_ep, "MUSIC_SEED", 1))
        lst = os.path.join(TMP, os.path.basename(out) + ".txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{p}'\n" for p in video_list)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", mus,
                        "-filter_complex", f"[1:a]loudnorm=I=-18:TP=-1.5,afade=t=in:d=5,afade=t=out:st={max(0, total - 12)}:d=12[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
        return
    if AMBIENT == "space":
        amb = space_ambience(total)
        lst = os.path.join(TMP, os.path.basename(out) + ".txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{p}'\n" for p in video_list)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-i", voice, "-i", amb, "-filter_complex",
                        "[1:a]aresample=44100,highpass=f=60,loudnorm=I=-17:TP=-1.5,pan=stereo|c0=c0|c1=c0[v];"
                        "[2:a]volume=0.32[m];[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", out], check=True)
        return
    if AMBIENT == "nature":
        amb = nature_ambience(timeline, total)
        lst = os.path.join(TMP, os.path.basename(out) + ".txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{p}'\n" for p in video_list)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", amb,
                        "-filter_complex", "[1:a]loudnorm=I=-20:TP=-2,afade=t=in:d=4[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
        return
    if AMBIENT == "cozy":
        music, rain = cozy_ambience(timeline, total)
        lst = os.path.join(TMP, os.path.basename(out) + ".txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{p}'\n" for p in video_list)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-i", voice, "-i", music, "-i", rain, "-filter_complex",
                        "[1:a]aresample=44100,highpass=f=70,loudnorm=I=-16:TP=-1.5[v];"
                        "[2:a]volume=0.22,lowpass=f=5000[m];[3:a]volume=0.5[r];"
                        "[v][m][r]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", out], check=True)
        return
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
    # segments are cached by content, so editing one scene only re-renders what changed
    code = open(S.__file__).read() + open(__file__).read()
    def seg_path(seg):
        key = hashlib.md5(repr((seg, vertical, EPISODE, code)).encode()).hexdigest()[:16]
        return os.path.join(TMP, f"{kind}_seg_{key}.mp4")
    for i, seg in enumerate(timeline):
        if i and XFADE:
            p_ = timeline[i - 1]
            seg["prev"] = dict(scene=p_["scene"], args=p_["args"], frames=p_["frames"])
    jobs = [(seg, seg_path(seg), vertical) for seg in timeline]
    jobs_sorted = sorted(jobs, key=lambda j: -j[0]["frames"])
    todo = [j for j in jobs_sorted if not os.path.exists(j[1])]
    print(f"rendering {len(todo)} of {len(jobs)} segments", flush=True)
    with Pool(os.cpu_count()) as pool:
        pool.map(render_segment, todo)
    total = sum(s["frames"] for s in timeline) / FPS
    out = os.path.join(OUT, f"{EPISODE}_{kind}.mp4")
    mix(voice, [j[1] for j in jobs], out, total, timeline)
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
    if hasattr(_ep, "thumb"):
        _ep.thumb(S, c)
        surf.write_to_png(os.path.join(OUT, f"{EPISODE}_thumbnail.png"))
        return
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
