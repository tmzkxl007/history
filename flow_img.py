"""의학의 역사 채널 — Google Flow(flowkit 서버 127.0.0.1:8100, 나노바나나2)로 그림 한 장 만들기.

flowkit 에이전트가 켜져 있고 크롬 확장이 로그인된 flow.google.com 탭에 붙어 있어야 한다(/health 의 extension_connected).
저승콩 flow_gen.py 와 같은 원리의 이 채널 전용 사본 — 다른 프리셋 파일은 import 하지 않는다.
Flow 프로젝트: 이 채널 전용 b9822e13-… (flow.google.com/project/b9822e13-3162-4a57-886b-155ac873050a).
"""
import hashlib, json, os, time, urllib.request, uuid

API = os.environ.get("FLOWKIT_URL", "http://127.0.0.1:8100")
PROJECT = os.environ.get("MEDHIST_FLOW_PROJECT", "b9822e13-3162-4a57-886b-155ac873050a")   # 의학의 역사 전용 Flow 프로젝트(2026-09-28)
MODEL = os.environ.get("FLOW_IMAGE_MODEL", "NARWHAL")   # NARWHAL = 나노바나나2
_uploaded = {}


def _post(path, body, timeout=300):
    req = urllib.request.Request(API + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def ready():
    with urllib.request.urlopen(API + "/health", timeout=10) as r:
        return json.load(r).get("extension_connected", False)


def _upload(path):
    data = open(path, "rb").read()
    key = hashlib.sha1(data).hexdigest()
    if key not in _uploaded:
        b = "----fk" + uuid.uuid4().hex
        ext = os.path.splitext(path)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        body = (f"--{b}\r\nContent-Disposition: form-data; name=\"project_id\"\r\n\r\n{PROJECT}\r\n"
                f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"ref{ext or '.png'}\"\r\n"
                f"Content-Type: {mime}\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request(API + "/api/flow/upload-image-file", body, {"Content-Type": f"multipart/form-data; boundary={b}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            _uploaded[key] = json.load(r)["media_id"]
    return _uploaded[key]


def generate(prompt, out, refs=(), size="16:9", tries=3, timeout=300):
    out = os.path.abspath(out)
    for attempt in range(tries):
        try:
            ids = [_upload(r) for r in refs]
            names = " ".join(f"Reference image {k + 1} is image {k + 1}." for k in range(len(ids)))
            d = _post("/api/flow/generate-image", {
                "prompt": (names + " " + prompt).strip(), "project_id": PROJECT, "image_model": MODEL,
                "aspect_ratio": size if size in ("1:1", "9:16", "16:9", "3:4", "4:3") else "16:9",
                "count": 1, "reference_media_ids": ids}, timeout)
            url = d["media"][0]["image"]["generatedImage"]["fifeUrl"]
            tmp = out + ".dl"
            urllib.request.urlretrieve(url, tmp)
            from PIL import Image
            Image.open(tmp).convert("RGB").save(out)
            os.remove(tmp)
            return out
        except Exception as e:
            msg = getattr(e, "read", lambda: b"")()[:300]
            print(f"flow 그림 없음 {attempt + 1}/{tries}: {os.path.basename(out)} {e} {msg}", flush=True)
            time.sleep(10)
    raise RuntimeError(f"flow 가 그림을 만들지 못함: {out}")
