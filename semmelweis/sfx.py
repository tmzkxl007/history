# 효과음 합성(numpy) + ffmpeg 후처리 → sfx/<이름>.wav
import subprocess, wave
from pathlib import Path
import numpy as np

SR = 48000
OUT = Path(__file__).parent / "sfx"; OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)


def t(sec):
    return np.arange(int(SR * sec)) / SR


def env(sec, attack=0.002, decay=0.2):
    x = t(sec)
    return np.minimum(1, x / max(attack, 1e-4)) * np.exp(-x / decay)


def sine(f, sec, decay=0.3, attack=0.002):
    return np.sin(2 * np.pi * f * t(sec)) * env(sec, attack, decay)


def noise(sec, decay=0.1, attack=0.001):
    return rng.standard_normal(int(SR * sec)) * env(sec, attack, decay)


def add(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs:
        o[:len(x)] += x
    return o


def place(buf, x, at):
    i = int(at * SR)
    end = min(len(buf), i + len(x))
    buf[i:end] += x[:end - i]
    return buf


def save(name, x, af=None):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    raw = OUT / f"_{name}.wav"
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(raw)]
    if af:
        cmd += ["-af", af]
    subprocess.run(cmd + ["-ar", str(SR), "-ac", "2", str(OUT / f"{name}.wav")], check=True)
    raw.unlink()


def steps(n=4, gap=0.55):
    b = np.zeros(int(SR * (n * gap + 1.0)))
    for k in range(n):
        s = add(noise(0.08, 0.02) * 0.6, sine(85, 0.12, 0.03))
        place(b, s * (0.8 + 0.2 * rng.random()), 0.05 + k * gap)
    return b


save("footsteps", steps(), "lowpass=f=1400,aecho=0.8:0.7:60|120:0.35|0.2,volume=0.9")

b = np.zeros(int(SR * 2.6))
place(b, noise(0.4, 0.07) * 1.2, 0)
for f, a, d in [(55, 1.0, 0.5), (110, 0.6, 0.35), (523, 0.25, 1.1), (887, 0.18, 0.9), (1331, 0.12, 0.7)]:
    place(b, sine(f, 2.4, d) * a, 0)
save("door_slam", b, "lowpass=f=5000,aecho=0.8:0.8:90|180:0.4|0.25")

x = t(2.2); f = 80 * np.exp(-x * 0.9)
b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.8)
b[:len(noise(0.5, 0.15))] += noise(0.5, 0.15) * 0.3
save("boom", b, "lowpass=f=400,aecho=0.8:0.6:120:0.3")

x = t(1.0)
b = rng.standard_normal(len(x)) * np.sin(np.pi * x / 1.0) ** 2
save("whoosh", b, "highpass=f=400,lowpass=f=2500,volume=0.8")

b = np.zeros(int(SR * 0.4)); place(b, add(noise(0.01, 0.002), sine(2200, 0.05, 0.01) * 0.5), 0.01)
save("pin", b, "highpass=f=800")

b = np.zeros(int(SR * 0.8)); place(b, add(noise(0.15, 0.03), sine(110, 0.25, 0.06) * 1.2), 0.01)
save("stamp", b, "lowpass=f=1800,aecho=0.8:0.5:40:0.2")


def bell_strike(f0=1150, sec=1.4):
    return sum(sine(f0 * r, sec, 0.9 / r ** 0.5) * a for r, a in [(1, 1), (2.03, 0.5), (2.9, 0.35), (4.2, 0.2)])


b = np.zeros(int(SR * 3.4))
for at in (0.0, 0.18, 1.1, 1.28):
    place(b, bell_strike() * 0.7, at)
save("bell", b, "aecho=0.8:0.6:70|140:0.3|0.2,volume=0.8")

b = np.zeros(int(SR * 1.8))
place(b, noise(0.3, 0.05) * 0.8, 0)
x = t(1.6); f = 120 * np.exp(-x * 1.5)
place(b, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.5), 0)
save("hit", b, "lowpass=f=2500,aecho=0.8:0.6:100:0.3")

b = np.zeros(int(SR * 4.2))
for k in range(4):
    g = 0.6 + 0.13 * k
    place(b, sine(52, 0.18, 0.05) * g, 0.1 + k * 0.95)
    place(b, sine(46, 0.18, 0.05) * g * 0.75, 0.36 + k * 0.95)
save("heartbeat", b, "lowpass=f=180,volume=1.6")

b = np.zeros(int(SR * 2.4))
for k, f in enumerate([523.25, 659.25, 783.99, 1046.5]):
    place(b, sine(f, 1.8, 0.5) * 0.6 + sine(f * 2, 1.8, 0.3) * 0.2, 0.02 + k * 0.12)
save("chime", b, "aecho=0.8:0.5:80:0.25")

x = t(0.45)
f = 300 + 1100 * np.sin(np.pi * x / 0.45) ** 2 * (1 - x / 0.45)
saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
b = saw * np.minimum(1, x / 0.01) * (1 - x / 0.45) + rng.standard_normal(len(x)) * 0.3 * (1 - x / 0.45)
save("scratch", b, "bandpass=f=900:w=1400,volume=1.2")

b = np.zeros(int(SR * 1.6)); place(b, add(noise(0.25, 0.05), sine(70, 0.6, 0.18) * 1.3, sine(140, 0.4, 0.1) * 0.4), 0)
save("door_bang", b, "lowpass=f=1500,aecho=0.8:0.6:60:0.3")

x = t(2.8)
strokes = (np.sin(2 * np.pi * 3.1 * x + 2 * np.sin(2 * np.pi * 0.7 * x)) > 0.1).astype(float)
b = rng.standard_normal(len(x)) * strokes * (0.5 + 0.5 * rng.random(len(x)))
save("pen", b, "highpass=f=2500,lowpass=f=7000,volume=0.35")

x = t(1.7)
f = 110 + 35 * np.sin(2 * np.pi * 0.8 * x) + 12 * rng.standard_normal(len(x)).cumsum() / np.sqrt(len(x))
saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
b = saw * np.sin(np.pi * x / 1.7) * (0.6 + 0.4 * (rng.random(len(x)) > 0.3))
save("door_creak", b, "bandpass=f=900:w=1200,aecho=0.8:0.6:80:0.3,volume=0.6")
print(sorted(p.name for p in OUT.glob("*.wav")))
