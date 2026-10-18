"""Makes a short, calm background track for the demo clip, entirely from code (no samples, no downloads).
Usage:  python tools/make_music.py out.wav [seconds]
The track is slow chords (Cmaj7, Am7, Fmaj7, G6) with soft bell notes on top. It belongs to this project."""
import sys
import numpy as np
from scipy.io import wavfile

SR = 44100
CHORDS = [  # (name, chord tones in Hz, bell notes in Hz)
    ("Cmaj7", [130.81, 164.81, 196.00, 246.94], [523.25, 659.25, 783.99, 987.77]),
    ("Am7",   [110.00, 130.81, 164.81, 196.00], [440.00, 523.25, 659.25, 783.99]),
    ("Fmaj7", [87.31, 110.00, 130.81, 164.81], [349.23, 440.00, 523.25, 659.25]),
    ("G6",    [98.00, 123.47, 146.83, 164.81], [392.00, 493.88, 587.33, 659.25]),
]
CHORD_LEN, OVERLAP = 12.0, 3.0


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def pad(freqs, n):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        for detune in (-0.0012, 0.0012):
            ff = f * (1 + detune)
            out += np.sin(2 * np.pi * ff * t) + 0.30 * np.sin(2 * np.pi * 2 * ff * t) + 0.10 * np.sin(2 * np.pi * 3 * ff * t)
    out *= 1 + 0.10 * np.sin(2 * np.pi * 0.11 * t)           # slow swell
    return out / (len(freqs) * 2)


def bells(freqs, n, rng):
    out = np.zeros(n)
    step = int(1.5 * SR)
    for k, start in enumerate(range(int(0.8 * SR), n - int(3 * SR), step)):
        f = freqs[(k * 2 + rng.integers(0, 2)) % len(freqs)]
        m = int(3.0 * SR)
        t = np.arange(m) / SR
        note = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 1.7) * smooth(t / 0.01)
        out[start:start + m] += 0.16 * note
    return out


def build(seconds):
    total = int(seconds * SR)
    mix = np.zeros(total + int((CHORD_LEN + OVERLAP) * SR) + SR)
    rng = np.random.default_rng(7)
    pos, i = 0.0, 0
    while pos < seconds:
        _, tones, bell_notes = CHORDS[i % len(CHORDS)]
        n = int((CHORD_LEN + OVERLAP) * SR)
        t = np.arange(n) / SR
        env = smooth(t / OVERLAP) * smooth((CHORD_LEN + OVERLAP - t) / OVERLAP)      # equal fade in and out
        seg = (pad(tones, n) + bells(bell_notes, n, rng)) * env
        a = int(pos * SR)
        mix[a:a + n] += seg
        pos += CHORD_LEN
        i += 1
    mix = mix[:total]
    fade_in, fade_out = int(2 * SR), int(5 * SR)
    mix[:fade_in] *= smooth(np.arange(fade_in) / fade_in)
    mix[-fade_out:] *= smooth(np.arange(fade_out)[::-1] / fade_out)
    return mix / (np.abs(mix).max() + 1e-9) * 0.9


if __name__ == "__main__":
    out = sys.argv[1]
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 145.0
    wavfile.write(out, SR, (build(secs) * 32767).astype(np.int16))
    print("wrote", out, secs, "seconds")
