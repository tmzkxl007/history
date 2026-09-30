# 장면 그림 생성 → img_<방식>/<id>.png  (방식은 settings.json image_mode, 기본 flow)
# python img.py refs        : plan.CHARS 의 인물 기준 그림 생성(ref_<키>.png) — 두 번째부터는 첫 인물 그림을 참고로 나이·옷만 바꿈
# python img.py all [id..]  : 장면 그림 생성(있으면 건너뜀, id 주면 그것만 다시)
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import plan
from plan import SCENES, STYLE, DARK
CHARS = getattr(plan, "CHARS", {})

W = Path(__file__).parent
IMG = W / "img"; IMG.mkdir(exist_ok=True)
KEY = open(os.path.expanduser("~/.volcano/keys/evolink"), encoding="utf-8").read().strip()
API = "https://api.evolink.ai/v1"
# 비용 절감(2026-09-26 확정): 주인공이 나오는 장면 = nano-banana-2-lite(1.2크레딧, 참고 그림 반영)
#                            그 밖의 장면   = z-image-turbo(0.26크레딧, 참고 그림은 무시하므로 인물 고정 불필요한 장면만)
MODES = {  # 방식: (주인공 장면 모델, 나머지 장면 모델, 그림 폴더)
    "flow": ("flow", "flow", "img_flow"),                                    # 기본(2026-09-28 사용자 지정): Google Flow 나노바나나2, 그림값 0원
    "agy": ("agy", "agy", "img_agy"),                                        # agy 울트라 구독(짧은 주기 한도, 429 면 대기)
    "z-image": ("z-image-turbo", "z-image-turbo", "img_z-image"),
    "lite": ("nano-banana-2-lite-beta", "nano-banana-2-lite-beta", "img_lite"),
    "mix": ("nano-banana-2-lite-beta", "z-image-turbo", "img_mix"),
    "original": ("nano-banana-beta", "nano-banana-beta", "img"),            # 1편 제멜바이스
}
SET = W / "settings.json"
MODE = json.load(open(SET, encoding="utf-8")).get("image_mode", "flow") if SET.exists() else "flow"
MODEL_REF, MODEL_PLAIN, _dir = MODES[MODE]
IMG = W / _dir; IMG.mkdir(exist_ok=True)
Z_EXTRA = (" Show a detailed, fully drawn background environment that fills the whole frame, "
           "and include exactly the people and objects described, no extra characters.")
OUTDIR = None
if "--out" in sys.argv:
    k = sys.argv.index("--out"); OUTDIR = Path(sys.argv[k + 1]); OUTDIR.mkdir(parents=True, exist_ok=True)
    del sys.argv[k:k + 2]


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET")
    req.add_header("Authorization", f"Bearer {KEY}"); req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def gen(prompt, out, refs=None, model=None):
    if (model or (MODEL_REF if refs else MODEL_PLAIN)) == "flow":
        sys.path.insert(0, str(W.parent)); import flow_img
        flow_img.generate(prompt, out, refs or ())               # flowkit 서버 + 크롬 확장 필요
        return str(out)
    if (model or (MODEL_REF if refs else MODEL_PLAIN)) == "agy":
        sys.path.insert(0, str(W.parent)); import agy_img
        agy_img.generate_waiting(prompt, out, refs or ())      # 한도가 차면 풀릴 때까지 기다렸다 이어서
        return str(out)                                          # agy 는 참고 그림을 로컬 파일로 받는다
    body = {"model": model or (MODEL_REF if refs else MODEL_PLAIN), "size": "16:9", "prompt": prompt}
    if refs:
        body["image_urls"] = refs
    for attempt in range(4):
        try:
            t = call(f"{API}/images/generations", body)
            for _ in range(60):
                time.sleep(5)
                r = call(f"{API}/tasks/{t['id']}")
                if r["status"] in ("completed", "failed"):
                    break
            if r["status"] == "completed":
                url = r["results"][0]
                q = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                out.write_bytes(urllib.request.urlopen(q, timeout=120).read())
                return url
            print("failed", out.name, r.get("error"), flush=True)
        except Exception as e:
            print("err", out.name, e, flush=True)
        time.sleep(5)
    raise RuntimeError(f"give up {out.name}")


STYLE_REF = W.parent / "style" / "channel_style.png"      # 채널 그림체 기준(2·3편, 2026-09-30 사용자 확정)
STYLE_TXT = (" The LAST reference image is only an art-style guide: match its line art, thick dark outlines, round soft faces with dot eyes "
             "and rosy cheeks, cute storybook proportions and warm colors exactly, but do not copy its content, places or characters.")


def with_style(prompt, refs_list):
    if MODE in ("flow", "agy") and STYLE_REF.exists():
        return prompt + STYLE_TXT, list(refs_list or []) + [str(STYLE_REF)]
    return prompt, refs_list


if sys.argv[1] == "refs":
    made, first = {}, None
    for key, desc in CHARS.items():
        out = IMG / f"ref_{key}.png"
        prompt = f"{STYLE} Character reference sheet on a plain light background: full body front view of {desc}. Neutral friendly expression."
        same = first and desc.lower().startswith("the same")      # "같은 사람 N년 뒤" 설명만 첫 인물 그림을 참고로 받는다
        if same:
            prompt += " Keep exactly the same face and features as the person in the reference image; change only age, hair and clothes as described."
        prompt, rl = with_style(prompt, [first] if same else None)
        res = gen(prompt, out, rl, model=MODEL_REF)
        made[key] = res
        first = first or (str(out) if MODEL_REF in ("flow", "agy") else res)
        print("ref ok", key, flush=True)
    json.dump(made, open(IMG / "refs.json", "w"))
    sys.exit()

REFS = IMG / "refs.json"
refs = json.load(open(REFS)) if REFS.exists() else json.load(open(W / "img" / "refs.json")) if (W / "img" / "refs.json").exists() else {}
only = set(sys.argv[2:])


def scene(s):
    if s.get("kind") == "card":
        if not s.get("bgprompt"):
            return
        prompt, out = s["bgprompt"], (OUTDIR or IMG) / f"{s['bg']}.png"
    elif s.get("prompt"):
        prompt, out = s["prompt"], (OUTDIR or IMG) / f"{s['id']}.png"
    else:
        return
    if out.exists() and out.stem not in only:
        return
    if only and out.stem not in only:
        return
    full = f"{STYLE}{DARK if s.get('dark') else ''} Scene: {prompt}"
    model = MODEL_REF if s.get("ref") else MODEL_PLAIN
    if model.startswith("z-image"):
        full += Z_EXTRA
    r = None
    key = s.get("ref")
    if key:
        full += (f" The main character ({CHARS.get(key, '').split(':')[0] or 'the main character'}) must look exactly like the person "
                 "in the reference image (same face, hair, clothes), but in this new scene and pose.")
        if model in ("agy", "flow"):
            loc = IMG / f"ref_{key}.png"
            r = [str(loc)] if loc.exists() else None
        elif not model.startswith("z-image"):      # evolink 은 URL, z-image 는 참고 그림을 쓰지 않는다
            r = [refs[key]] if key in refs else None
    prev = s.get("ref_prev")
    if prev and model in ("agy", "flow"):
        pp = IMG / f"{prev}.png"
        if pp.exists():
            full += (" Reference image 1 shows the moment just before this scene: keep the same place, camera angle, lighting and the same "
                     "characters' faces, hair and clothes; change only what this scene describes.")
            r = [str(pp)] + (r or [])
    full, r = with_style(full, r)
    gen(full, out, r, model=model)
    print("ok", out.name, flush=True)


# 앞 장면을 참고하는 장면(ref_prev)은 앞 장면이 다 만들어진 뒤 순서대로
first_pass = [s for s in SCENES if not s.get("ref_prev")]
with ThreadPoolExecutor({"agy": 3, "flow": 2}.get(MODE, 5)) as ex:   # flowkit 은 서버가 한 번에 1장씩 처리
    list(ex.map(scene, first_pass))
for s in SCENES:
    if s.get("ref_prev"):
        scene(s)
print("done")
