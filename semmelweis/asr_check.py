# 녹음된 줄들을 Speechmatics 로 받아써서 대본과 비교 → 발음 이상 후보 출력
import json, os, sys, time, urllib.request, difflib, re, uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from plan import SCENES

W = Path(__file__).parent
KEY = open(os.path.expanduser("~/.volcano/keys/speechmatics"), encoding="utf-8").read().strip()
BASE = "https://asr.api.speechmatics.com/v2"


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {KEY}", **(headers or {})})
    with urllib.request.urlopen(r, timeout=300) as x:
        return x.read()


# 전체 내레이션 트랙 하나를 보낸다
audio = (W / "mix_nar.wav").read_bytes()
b = uuid.uuid4().hex
cfg = json.dumps({"type": "transcription", "transcription_config": {"language": "ko", "operating_point": "enhanced"}})
body = (f"--{b}\r\nContent-Disposition: form-data; name=\"config\"\r\n\r\n{cfg}\r\n"
        f"--{b}\r\nContent-Disposition: form-data; name=\"data_file\"; filename=\"nar.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() \
       + audio + f"\r\n--{b}--\r\n".encode()
job = json.loads(req(f"{BASE}/jobs", body, {"Content-Type": f"multipart/form-data; boundary={b}"}, "POST"))["id"]
while True:
    st = json.loads(req(f"{BASE}/jobs/{job}"))["job"]["status"]
    if st in ("done", "rejected"):
        break
    time.sleep(8)
txt = req(f"{BASE}/jobs/{job}/transcript?format=txt").decode("utf-8")
(W / "asr.txt").write_text(txt, encoding="utf-8")

script = " ".join(t for s in SCENES for t, _ in s.get("lines", []))
norm = lambda s: re.sub(r"[^가-힣0-9a-zA-Z]", "", s)
a, h = norm(script), norm(txt)
sm = difflib.SequenceMatcher(None, a, h, autojunk=False)
print("일치율", round(sm.ratio() * 100, 1), "%")
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op != "equal" and (i2 - i1 >= 2 or j2 - j1 >= 2):
        print(f"{op:8s} 대본[{a[max(0,i1-6):i2+6]}]  인식[{h[max(0,j1-6):j2+6]}]")
