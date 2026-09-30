"""의학의 역사 채널 — Flow Omni Flash(그림 → 움직이는 영상) 헬퍼.
python omni_video.py <편 폴더> <장면id>:<초>:"<움직임 설명>" ...   → <편>/anim/<장면id>_omni.mp4
그림은 <편>/img_flow/<장면id>.png. 길이는 4/6/8/10초. flowkit 서버(127.0.0.1:8100) 필요.
"""
import json, sys, time, uuid, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import flow_img

KEEP = ("Keep the exact flat 2D cartoon style, colors, line art and characters of the image; do not add new characters, "
        "no text, no blood, no gore. Smooth natural motion, subtle camera movement. ")


def _post(path, body, timeout=300):
    r = urllib.request.Request(flow_img.API + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=timeout))


def make(ep, sid, dur, motion):
    out = Path(ep) / "anim" / f"{sid}_omni.mp4"; out.parent.mkdir(exist_ok=True)
    if out.exists():
        return out
    mid = flow_img._upload(str(Path(ep) / "img_flow" / f"{sid}.png"))
    for attempt in range(3):
        try:
            d = _post("/api/flow/generate-video", {"start_image_media_id": mid, "project_id": flow_img.PROJECT, "scene_id": str(uuid.uuid4()),
                                                  "aspect_ratio": "VIDEO_ASPECT_RATIO_LANDSCAPE", "user_paygate_tier": "PAYGATE_TIER_TWO",
                                                  "prompt": KEEP + motion, "model_family": "omni_flash", "duration_s": dur})
            ops = d["flowkitPolling"]["operations"]; t0 = time.time()
            while time.time() - t0 < 600:
                time.sleep(10)
                res = _post("/api/flow/check-status", {"operations": ops, "project_id": flow_img.PROJECT}, 120)
                s = json.dumps(res)
                if "SUCCESSFUL" in s:
                    url = res["operations"][0]["operation"]["metadata"]["video"]["fifeUrl"]
                    q = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    out.write_bytes(urllib.request.urlopen(q, timeout=300).read())
                    print("ok", sid, dur, "s", int(time.time() - t0), "s", flush=True); return out
                if "FAILED" in s:
                    print("failed", sid, s[:300], flush=True); break
        except Exception as e:
            print("err", sid, e, getattr(e, "read", lambda: b"")()[:300], flush=True)
        time.sleep(10)
    raise RuntimeError(f"omni 실패 {sid}")


if __name__ == "__main__":
    ep = sys.argv[1]
    if len(sys.argv) == 2:          # 인자 없이 편 폴더만 주면 plan.py 의 anim=(초, "움직임") 장면을 전부 만든다
        sys.path.insert(0, str(Path(ep).resolve())); import plan
        for s in plan.SCENES:
            if s.get("anim"):
                make(ep, s["id"], int(s["anim"][0]), s["anim"][1])
        sys.exit()
    for spec in sys.argv[2:]:
        sid, dur, motion = spec.split(":", 2)
        make(ep, sid, int(dur), motion)
