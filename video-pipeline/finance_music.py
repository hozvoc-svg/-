"""Procedural, copyright-free lo-fi documentary beat for The Quiet Money (sits under narration).

Soft electric-piano chords, a round sub bass, a gentle kick/snare/hat groove and a little vinyl noise.
Arranged in 8-bar sections (some without drums) so a 10-minute bed doesn't feel like one loop.
"""
import wave
import numpy as np

SR = 44100
PROGS = [
    [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [52, 55, 59, 62, 67]],  # Am9 Fmaj9 Cmaj9 Em7
    [[50, 53, 57, 60, 64], [55, 59, 62, 65, 69], [48, 52, 55, 59, 64], [57, 60, 64, 67, 72]],  # Dm9 G9 Cmaj7 Am7
]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _ep(f, n, rng):
    """Electric-piano-ish note: sine with a decaying 2nd/3rd harmonic and soft tremolo."""
    t = np.arange(n) / SR
    env = np.exp(-t * 1.6) * np.minimum(1, t / 0.008)
    tone = np.sin(2 * np.pi * f * t) + 0.35 * np.exp(-t * 4) * np.sin(2 * np.pi * 2 * f * t) \
        + 0.12 * np.exp(-t * 7) * np.sin(2 * np.pi * 3 * f * t + rng.random())
    return (tone * env * (1 + 0.08 * np.sin(2 * np.pi * 4.5 * t))).astype(np.float32)


def render(path, seconds, seed=1, bpm=86):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    L = np.zeros(n + SR * 4, np.float32)
    R = np.zeros_like(L)
    beat = 60.0 / bpm
    bar = 4 * beat

    def put(sig, t, pan=0.0, g=1.0):
        i = int(t * SR)
        if i >= len(L):
            return
        k = min(len(sig), len(L) - i)
        L[i:i + k] += sig[:k] * g * (1 - pan) / 2 * 2 ** 0.5
        R[i:i + k] += sig[:k] * g * (1 + pan) / 2 * 2 ** 0.5

    tk = np.arange(int(0.35 * SR)) / SR
    kick = (np.sin(2 * np.pi * (48 * tk + 90 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)).astype(np.float32)
    ts = np.arange(int(0.25 * SR)) / SR
    sn_noise = rng.standard_normal(len(ts)).astype(np.float32)
    sn_noise = np.convolve(sn_noise, np.ones(6) / 6, "same")
    snare = (sn_noise * np.exp(-ts * 22) * 0.6 + np.sin(2 * np.pi * 190 * ts) * np.exp(-ts * 30) * 0.3).astype(np.float32)
    th = np.arange(int(0.06 * SR)) / SR
    hn = rng.standard_normal(len(th)).astype(np.float32)
    hat = (np.diff(np.concatenate([[0], hn])) * np.exp(-th * 70) * 0.25).astype(np.float32)

    nbars = int(seconds / bar) + 2
    for b in range(nbars):
        t0 = b * bar
        sec = b // 8
        prog = PROGS[(sec // 2) % len(PROGS)]
        ch = prog[b % 4]
        drums = b >= 4 and sec % 4 != 3      # intro without drums, and a calm breakdown every 4th section
        # chords: on beat 1 and the "and" of 2, softly strummed
        for hit_t, vel in ((0.0, 1.0), (1.5 * beat, 0.6)):
            for j, m in enumerate(ch[1:]):
                put(_ep(hz(m), int(bar * SR), rng), t0 + hit_t + j * 0.012, pan=(j - 1.5) * 0.25, g=0.07 * vel)
        # bass
        for bt in (0, 2.5):
            tb = np.arange(int(beat * 1.4 * SR)) / SR
            bs = np.sin(2 * np.pi * hz(ch[0] - 12) * tb) * np.exp(-tb * 1.8) * np.minimum(1, tb / 0.01)
            put(bs.astype(np.float32), t0 + bt * beat, g=0.28)
        if drums:
            for bt in (0, 2.5) if b % 2 else (0, 2, 2.75):
                put(kick, t0 + bt * beat, g=0.45)
            for bt in (1, 3):
                put(snare, t0 + bt * beat + 0.012, g=0.16)
            for k in range(8):
                put(hat, t0 + k * beat / 2 + (0.02 if k % 2 else 0), pan=0.3, g=0.5 if k % 2 else 0.8)
        # an occasional high melodic note
        if rng.random() < 0.5:
            m = ch[-1] + 12 if rng.random() < 0.5 else ch[-2] + 12
            put(_ep(hz(m), int(1.5 * SR), rng), t0 + rng.choice([1, 2, 3]) * beat, pan=-0.2, g=0.035)

    out = np.stack([L[:n], R[:n]], 1)
    # warm tape low-pass (moving average) + faint vinyl noise
    k = np.ones(5) / 5
    for i in range(2):
        out[:, i] = np.convolve(out[:, i], k, "same")
    out += rng.standard_normal(out.shape).astype(np.float32) * 0.003
    out /= max(1e-6, np.abs(out).max()) / 0.8
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    return path


if __name__ == "__main__":
    import sys
    render(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 60)
