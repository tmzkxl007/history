# 개별 줄 wav 받아쓰기: python asr_line.py s16_1 s26_1 ...
import json, os, sys, time, urllib.request, uuid
from pathlib import Path
W = Path(__file__).parent
KEY = open(os.path.expanduser("~/.volcano/keys/speechmatics"), encoding="utf-8").read().strip()
BASE = "https://asr.api.speechmatics.com/v2"


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {KEY}", **(headers or {})})
    with urllib.request.urlopen(r, timeout=300) as x:
        return x.read()


def asr(p):
    b = uuid.uuid4().hex
    cfg = json.dumps({"type": "transcription", "transcription_config": {"language": "ko", "operating_point": "enhanced"}})
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"config\"\r\n\r\n{cfg}\r\n--{b}\r\nContent-Disposition: form-data; "
            f"name=\"data_file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() + p.read_bytes() + f"\r\n--{b}--\r\n".encode()
    job = json.loads(req(f"{BASE}/jobs", body, {"Content-Type": f"multipart/form-data; boundary={b}"}, "POST"))["id"]
    while json.loads(req(f"{BASE}/jobs/{job}"))["job"]["status"] not in ("done", "rejected"):
        time.sleep(4)
    return req(f"{BASE}/jobs/{job}/transcript?format=txt").decode().strip()


from concurrent.futures import ThreadPoolExecutor
ids = sys.argv[1:]
with ThreadPoolExecutor(4) as ex:
    for i, t in zip(ids, ex.map(lambda i: asr(W / "tts" / f"{i}.wav"), ids)):
        print(i, "→", t)
