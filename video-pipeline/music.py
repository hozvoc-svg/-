"""Procedural ambient space music, streamed to a stereo WAV block by block (works for many hours).

Layers: warm detuned pad chords (slow filter sweep), soft sub bass, sparse bell notes, and a long
synthetic reverb. No percussion and no sudden sounds, so it is safe for sleep.
"""
import math, wave
import numpy as np

SR = 44100
BLOCK = 16.0          # seconds per chord
OVER = 6.0            # crossfade/tail overlap between blocks

# A-minor-ish ambient progressions (MIDI notes); a new progression every few minutes for variety
PROGRESSIONS = [
    [[45, 57, 60, 64, 71], [41, 57, 60, 65, 69], [48, 55, 59, 64, 67], [43, 55, 59, 62, 69]],   # Am9 Fmaj7 Cmaj7 G6
    [[38, 57, 62, 65, 69], [43, 55, 59, 62, 67], [40, 55, 59, 64, 67], [45, 57, 60, 64, 69]],   # Dm9 G Em7 Am
    [[41, 53, 60, 64, 69], [45, 52, 57, 60, 64], [43, 50, 55, 59, 62], [48, 55, 60, 64, 67]],   # Fmaj7 Am G C
]
PENTA = [69, 72, 74, 76, 79, 81, 84]   # A minor pentatonic for bells


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _pad_note(f, n, t, rng, bright):
    """Detuned additive saw-ish voice with a soft low-pass (harmonic roll-off) that slowly opens and closes."""
    out = np.zeros(n, np.float32)
    for det in (-0.006, 0.0, 0.0065):
        ph = rng.random() * 6.28
        ff = f * (1 + det)
        for k in range(1, 9):
            if ff * k > 6000:
                break
            amp = (1.0 / k) * np.exp(-k / bright)
            out += (amp * np.sin(2 * np.pi * ff * k * t + ph * k)).astype(np.float32)
    return out / 3


def _bell(f, n, rng):
    t = np.arange(n) / SR
    env = np.exp(-t * 0.9) * np.minimum(1, t / 0.01)
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 1.8)
         + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 3))
    return (s * env).astype(np.float32)


def _impulse(seconds=6.0, seed=0):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)).astype(np.float32) * np.exp(-t * 1.1)[:, None].astype(np.float32)
    # darken the tail: simple one-pole low-pass
    for ch in range(2):
        y = 0.0
        a = 0.35
        col = ir[:, ch]
        out = np.empty_like(col)
        # vectorised approximation of a one-pole filter via cumulative smoothing on chunks
        k = np.exp(-np.arange(64) / 6.0).astype(np.float32)
        k /= k.sum()
        out = np.convolve(col, k, mode="same")
        ir[:, ch] = out
    ir /= np.sqrt((ir ** 2).sum(0, keepdims=True))
    return ir


def _fft_conv(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    X = np.fft.rfft(x, N)
    out = np.stack([np.fft.irfft(X * np.fft.rfft(ir[:, c], N), N)[:n] for c in range(2)], 1)
    return out.astype(np.float32)


def render(path, seconds, seed=1, wet=0.45):
    rng = np.random.default_rng(seed)
    ir = _impulse(6.0, seed)
    tail = len(ir)
    blk = int(BLOCK * SR)
    ov = int(OVER * SR)
    nblocks = int(math.ceil(seconds / BLOCK)) + 1
    total = int(seconds * SR)
    carry = np.zeros((ov + tail, 2), np.float32)
    written = 0
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        for b in range(nblocks):
            prog = PROGRESSIONS[(b // 16) % len(PROGRESSIONS)]
            chord = prog[b % len(prog)]
            n = blk + ov
            t = np.arange(n) / SR
            env = np.minimum(1, t / OVER) * np.minimum(1, (n - np.arange(n)) / SR / OVER)
            env = (env * env * (3 - 2 * env)).astype(np.float32)
            bright = 2.2 + 1.6 * math.sin(b * 0.37) + 0.8 * np.sin(2 * np.pi * t / 23.0)
            pad = np.zeros((n, 2), np.float32)
            for j, m in enumerate(chord[1:]):
                v = _pad_note(hz(m), n, t, rng, bright) * (0.11 / (1 + 0.15 * j))
                pan = 0.25 + 0.5 * ((j * 0.37 + b * 0.11) % 1)
                pad[:, 0] += v * (1 - pan)
                pad[:, 1] += v * pan
            sub = (0.16 * np.sin(2 * np.pi * hz(chord[0] - 12) * t) + 0.06 * np.sin(2 * np.pi * hz(chord[0]) * t)).astype(np.float32)
            pad += sub[:, None]
            pad *= env[:, None]
            bells = np.zeros((n, 2), np.float32)
            tt = rng.uniform(1.0, 3.5)
            while tt < BLOCK:
                note = PENTA[rng.integers(len(PENTA))]
                bl = _bell(hz(note), int(5 * SR), rng) * rng.uniform(0.025, 0.06)
                i0 = int(tt * SR)
                m = min(len(bl), n - i0)
                pan = rng.random()
                bells[i0:i0 + m, 0] += bl[:m] * (1 - pan)
                bells[i0:i0 + m, 1] += bl[:m] * pan
                tt += rng.uniform(2.5, 6.5)
            dry = pad + bells
            mono = (pad.mean(1) * 0.6 + bells.mean(1) * 1.4)
            wetsig = _fft_conv(mono, ir) * wet
            mixd = np.zeros((n + tail, 2), np.float32)
            mixd[:n] += dry * (1 - wet * 0.5)
            mixd[:len(wetsig)] += wetsig[:n + tail]
            mixd[:len(carry)] += carry
            out = mixd[:blk]
            carry = mixd[blk:]
            if b == nblocks - 1 or written + blk >= total:
                out = mixd[:max(0, total - written)]
            out = np.tanh(out * 1.2) / np.tanh(1.2)  # gentle soft clip
            w.writeframes((np.clip(out, -1, 1) * 32767 * 0.85).astype(np.int16).tobytes())
            written += len(out)
            if written >= total:
                break
    return path


if __name__ == "__main__":
    import sys
    render(sys.argv[1], float(sys.argv[2]))
