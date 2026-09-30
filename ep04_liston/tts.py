# 줄마다 Typecast 진우로 녹음 → tts/<장면>_<줄>.wav (48kHz mono) + tts/durations.json
import json, os, re, subprocess, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from plan import SCENES

W = Path(__file__).parent
OUT = W / "tts"; OUT.mkdir(exist_ok=True)
KEY = open(os.path.expanduser("~/.volcano/keys/typecast"), encoding="utf-8").read().strip()
VOICE = "tc_632293f759d649937b97f323"   # Jinwoo (진우)

def sino(n):
    """정수 → 한자어 수 읽기 (1683 → 천육백팔십삼)"""
    if n == 0:
        return "영"
    d = "일이삼사오육칠팔구"; out = ""
    for unit, name in ((10 ** 8, "억"), (10 ** 4, "만")):
        if n >= unit:
            out += sino(n // unit) + name; n %= unit
    for unit, name in ((1000, "천"), (100, "백"), (10, "십"), (1, "")):
        q = n // unit; n %= unit
        if q:
            out += ("" if q == 1 and unit > 1 else d[q - 1]) + name
    return out


def tts_text(s):
    s = re.sub(r"(\d+)%", lambda m: sino(int(m.group(1))) + " 퍼센트", s)
    s = re.sub(r"(\d+)(?=여)", lambda m: sino(int(m.group(1))), s)
    s = re.sub(r"(\d+)(?=[년명병일개월주살번층])", lambda m: sino(int(m.group(1))) + " ", s)
    s = re.sub(r"\d+", lambda m: sino(int(m.group(0))), s)
    s = re.sub(r"(\()?[\d]+~[\d]+(\))?", "", s)
    return s.replace("…", "... ").strip()


def trim(mp3, wav):
    # 앞뒤 무음 깎기 (문장 사이 간격은 조립 단계에서 일정하게 준다)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-af",
                    # 앞뒤 무음은 깎되 0.04초는 남긴다 — 다 깎으면 ㅈ·ㅅ 같은 약한 첫 자음까지 잘려 '종두→용두'처럼 들린다
                    "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04,areverse,"
                    # 문장 안쪽 쉼도 0.06초만 남기고 지운다(0이면 자음이 뭉개진다)
                    "silenceremove=stop_periods=-1:stop_duration=0.08:stop_threshold=-45dB:stop_silence=0.06",
                    "-ar", "48000", "-ac", "1", str(wav)], check=True)


def one(job):
    sid, i, text, emo = job
    wav = OUT / f"{sid}_{i}.wav"
    mp3 = OUT / f"{sid}_{i}.mp3"
    if wav.exists():
        return
    if mp3.exists() and mp3.stat().st_size > 1000:
        return trim(mp3, wav)
    body = json.dumps({"voice_id": VOICE, "text": tts_text(text), "model": "ssfm-v30", "language": "kor",
                       "prosody": {"emotion_preset": emo}, "output": {"audio_format": "mp3", "audio_tempo": 1.1}}).encode()
    for a in range(8):
        req = urllib.request.Request("https://api.typecast.ai/v1/text-to-speech", data=body, method="POST")
        req.add_header("X-API-KEY", KEY); req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                mp3 = OUT / f"{sid}_{i}.mp3"; mp3.write_bytes(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or a == 7:
                raise RuntimeError(f"{sid}_{i} {e.code} {e.read()[:200]}")
            time.sleep(2 * (a + 1))
    trim(mp3, wav)
    print("ok", sid, i, flush=True)


jobs = [(s["id"], i, t, e) for s in SCENES for i, (t, e) in enumerate(s.get("lines", []))]
with ThreadPoolExecutor(3) as ex:
    list(ex.map(one, jobs))

dur = {}
for sid, i, _, _ in jobs:
    p = OUT / f"{sid}_{i}.wav"
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True).stdout)
    dur[f"{sid}_{i}"] = round(d, 3)
json.dump(dur, open(OUT / "durations.json", "w"), indent=0)
print("lines", len(dur), "total", round(sum(dur.values()), 1), "s")
