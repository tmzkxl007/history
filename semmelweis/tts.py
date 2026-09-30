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

NUM = {"1865년": "천팔백육십오 년", "1840년대": "천팔백사십 년대", "30%": "삼십 퍼센트", "18%": "십팔 퍼센트",
       "2%": "이 퍼센트", "1%대": "일 퍼센트대", "1% 아래": "일 퍼센트 아래", "1번": "일 번", "2번": "이 번",
       "3번": "삼 번", "제1병동": "제일 병동", "제2병동": "제이 병동", "2주": "이 주"}


def tts_text(s):
    for k, v in NUM.items():
        s = s.replace(k, v)
    return s.replace("…", "... ").strip()


def one(job):
    sid, i, text, emo = job
    wav = OUT / f"{sid}_{i}.wav"
    if wav.exists():
        return
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
    # 앞뒤 무음 깎기 (문장 사이 간격은 조립 단계에서 일정하게 준다)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    # 문장 안쪽 쉼도 0.06초만 남기고 지운다(0이면 자음이 뭉개진다)
                    "silenceremove=stop_periods=-1:stop_duration=0.08:stop_threshold=-45dB:stop_silence=0.06",
                    "-ar", "48000", "-ac", "1", str(wav)], check=True)
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
