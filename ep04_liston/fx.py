# 장면 효과(2026-09-30): AI 영상 대체 · 입체감(인물/배경 분리) · 흔들림/확대(효과음 연동) · 먼지 · 불빛 깜빡임 · 안개 · 눈 · 불티 ·
#   화면 글자 톡/쾅 등장 · 장면 시작 전환(확 다가옴 / 구간 바뀔 때 암전)
# build.make_clip 이 장면마다 SceneFX 를 만들고 프레임마다 frame(i, view) 를 부른다. 비용 0원(AI 영상은 anim/<id>_omni.mp4 가 있을 때만).
import math
from pathlib import Path
import numpy as np, cv2
from PIL import Image

VW, VH, FPS = 1920, 1080, 30
SHAKE_SFX = {"hit": (18, 0.45, 0.08), "door_slam": (16, 0.5, 0.05), "door_bang": (14, 0.4, 0.05),
             "stamp": (10, 0.3, 0.04), "boom": (20, 0.6, 0.08), "splash": (8, 0.4, 0.0),
             "m_impact": (18, 0.5, 0.07), "m_thud": (16, 0.45, 0.06), "m_hit": (12, 0.35, 0.05), "m_stamp": (10, 0.3, 0.04), "m_punch": (9, 0.25, 0.03)}
_rng = np.random.default_rng(11)


def _warp(img, z, cx, cy):
    M = np.float32([[z, 0, VW / 2 - z * cx], [0, z, VH / 2 - z * cy]])
    return cv2.warpAffine(img, M, (VW, VH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def _mask(ep, sid, img):
    p = Path(ep) / "anim" / "masks" / f"{sid}.png"; p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        from rembg import remove, new_session
        global _SESS
        try:
            _SESS
        except NameError:
            _SESS = new_session("isnet-anime")
        remove(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), session=_SESS, only_mask=True).save(p)
    m = np.asarray(Image.open(p).convert("L").resize((VW, VH))).astype(np.float32) / 255
    m = np.clip((m - 0.3) / 0.3, 0, 1)                     # 흐린 경계는 선명하게(얼굴 뭉개짐 방지)
    return cv2.GaussianBlur(m, (0, 0), 1.2)


class SceneFX:
    def __init__(self, ep, sc, src, frames, anchor, overlays, prev_sec, first):
        s = sc["s"]; self.s, self.sc, self.src, self.frames = s, sc, src, frames
        self.dur = frames / FPS
        prompt = (s.get("prompt") or s.get("bgprompt") or "").lower()
        card = s.get("kind") == "card"
        self.dark = bool(s.get("dark"))
        opt = s.get("fx", {})
        # 2026-09-30 사용자 지적: 밝기 깜빡임은 눈이 아프고, 떠다니는 먼지는 실내에서 눈처럼 보인다 → 기본으로 끄고,
        # 눈·불티·먼지는 plan 장면에 fx={"snow": True} 처럼 직접 지정할 때만 넣는다(프롬프트 낱말로 자동 판단하지 않음)
        self.dust = bool(opt.get("dust")) and not card
        self.flicker = False
        self.fog = opt.get("fog", "fog" in prompt and not card)
        self.snow = bool(opt.get("snow")) and not card
        self.embers = bool(opt.get("embers")) and not card
        self.shakes = []
        for cue in s.get("sfx", []):
            name, a = cue[0], cue[1]
            if name in SHAKE_SFX:
                amp, d, p = SHAKE_SFX[name]; self.shakes.append((anchor(sc, a), amp, d, p))
        # 화면 글자: (PIL RGBA 전체 화면, 등장 시각, 스타일) → 글자 부분만 잘라 두고 중심 기준으로 키운다
        self.ovs = []
        for img, t0, style in overlays:
            bb = img.getbbox()
            if bb:
                self.ovs.append((img.crop(bb), bb, t0, style))
        # AI 영상(Omni Flash)이 있으면 그림 대신 사용
        vp = Path(ep) / "anim" / f"{s['id']}_omni.mp4"
        self.cap = None
        if vp.exists() and not s.get("gray"):
            self.cap = cv2.VideoCapture(str(vp)); self.vn = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.vfps = self.cap.get(cv2.CAP_PROP_FPS) or 24; self.vi = -1; self.vfr = None
            clip = self.vn / self.vfps; self.vspeed = min(1.0, clip / max(self.dur, 1e-3))   # 장면이 더 길면 살짝 느리게
        # 입체감: 주인공 장면이고 인물이 화면의 6~45% 일 때만(인물이 빽빽한 장면은 경계가 얼굴을 뭉갬)
        self.layers = None
        if s.get("ref") and self.cap is None and not card and not s.get("gray"):
            m = _mask(ep, s.get("img_from", s["id"]), src)
            if 0.06 < float(m.mean()) < 0.45:
                small = cv2.resize(src, (VW // 3, VH // 3)); mm = (cv2.resize(m, (VW // 3, VH // 3)) > 0.3).astype(np.uint8) * 255
                bg = cv2.resize(cv2.inpaint(small, cv2.dilate(mm, np.ones((9, 9), np.uint8)), 7, cv2.INPAINT_TELEA), (VW, VH))
                self.layers = (np.where(m[..., None] > 0.05, bg, src), m[..., None])
        self.trans = "card" if card else ("black" if (s.get("sec") and s.get("sec") != prev_sec and not first) else "zoom")
        n = 80
        self.dust_p = np.c_[_rng.uniform(0, VW, n), _rng.uniform(0, VH, n), _rng.uniform(1.5, 4.5, n), _rng.uniform(-8, 8, n), _rng.uniform(-14, -4, n)]
        self.snow_p = np.c_[_rng.uniform(0, VW, 140), _rng.uniform(0, VH, 140), _rng.uniform(2, 5, 140), _rng.uniform(-20, 20, 140), _rng.uniform(40, 110, 140)]
        self.emb_p = np.c_[_rng.uniform(0, VW, 60), _rng.uniform(0, VH, 60), _rng.uniform(1.5, 3.5, 60), _rng.uniform(-25, 25, 60), _rng.uniform(-120, -50, 60)]
        if self.fog:
            f = cv2.GaussianBlur((_rng.random((VH // 4, VW // 2)) * 255).astype(np.uint8), (0, 0), 18)
            self.fogtex = cv2.resize(cv2.normalize(f, None, 0, 255, cv2.NORM_MINMAX), (VW * 2, VH))

    # ---- 바탕 ----
    def _video(self, t):
        want = min(self.vn - 1, int(t * self.vspeed * self.vfps))
        while self.vi < want:
            ok, fr = self.cap.read()
            if not ok:
                break
            self.vi += 1; self.vfr = fr
        if getattr(self, "vref", None) is None:            # AI 영상 보정: 원본 그림 색에 맞추고 선을 또렷하게(vfix.py)
            import vfix
            self.vref = vfix.lab_stats(self.src)
        import vfix
        return vfix.fix(self.vfr, self.vref, VW, VH)

    def _punch(self, t):
        add = 0.0
        for th, amp, d, p in self.shakes:
            if p and th <= t < th + d + 0.6:
                add = max(add, p * (t - th) / 0.08 if t < th + 0.08 else p * max(0, 1 - (t - th - 0.08) / (d + 0.5)))
        return add

    def base(self, i, view):
        t = i / FPS
        if self.cap is not None:
            f = self._video(t)
            pn = self._punch(t)
            return _warp(f, 1 + pn, VW / 2, VH / 2) if pn else f
        z, cx, cy = view(i); z *= 1 + self._punch(t)
        if self.layers is None:
            return _warp(self.src, z, cx, cy)
        bgp, m = self.layers; u = i / max(self.frames - 1, 1); off = 26 * (u - 0.5)
        B = _warp(bgp, z, cx - off / z, cy)
        F = _warp(self.src, z * 1.035, cx + off * 0.8 / z, cy)
        Mk = _warp(m[..., 0], z * 1.035, cx + off * 0.8 / z, cy)[..., None]
        return (F * Mk + B * (1 - Mk)).astype(np.uint8)

    # ---- 분위기 ----
    def _particles(self, f, P, t, col, alpha, wrap=True):
        ov = f.copy()
        for x, y, r, vx, vy in P:
            px = (x + vx * t) % VW; py = (y + vy * t) % VH
            cv2.circle(ov, (int(px), int(py)), int(r), col, -1, cv2.LINE_AA)
        return cv2.addWeighted(ov, alpha, f, 1 - alpha, 0)

    def atmos(self, f, t):
        if self.flicker:
            k = 1 + 0.03 * math.sin(2 * math.pi * 2.3 * t) + 0.018 * math.sin(2 * math.pi * 7.1 * t + 1)
            f = np.clip(f.astype(np.float32) * k, 0, 255).astype(np.uint8)
        if self.fog:
            off = int(t * 60) % VW; a = 0.26 * (self.fogtex[:, off:off + VW].astype(np.float32)[..., None] / 255)
            f = (f * (1 - a) + 200 * a).astype(np.uint8)
        if self.snow:
            f = self._particles(f, self.snow_p, t, (250, 250, 255), 0.55)
        if self.embers:
            f = self._particles(f, self.emb_p, t, (60, 150, 255), 0.6)
        if self.dust:
            d = self.dust_p.copy(); d[:, 3:] *= 3
            f = self._particles(f, d, t, (210, 225, 235), 0.32)
        return f

    def shake(self, f, t):
        for th, amp, d, p in self.shakes:
            if th <= t < th + d:
                k = 1 - (t - th) / d
                dx = amp * k * math.sin((t - th) * 90); dy = amp * 0.6 * k * math.cos((t - th) * 73)
                return cv2.warpAffine(f, np.float32([[1.02, 0, dx - VW * 0.01], [0, 1.02, dy - VH * 0.01]]), (VW, VH), borderMode=cv2.BORDER_REFLECT)
        return f

    # ---- 화면 글자 ----
    def overlays(self, f, t):
        act = [o for o in self.ovs if t >= o[2]]
        if not act:
            return f
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert("RGBA")
        for crop, bb, t0, style in act:
            u = t - t0; dy = 0; a = 1.0
            if style == "stamp":                              # 쾅: 1.8배에서 떨어지며 찍힘
                sc = 1.0 if u >= 0.12 else 1.8 - 0.8 * (u / 0.12)
            elif style in ("name", "label_left", "label_right", "label_top"):
                sc = 1.0; dy = -30 * max(0, 1 - u / 0.25); a = min(1, u / 0.25)
            else:                                             # 톡: 0.5 → 1.08 → 1.0
                w = u / 0.32; sc = 1.0 if w >= 1 else (0.5 + 0.72 * w if w < 0.8 else 1.08 - 0.4 * (w - 0.8)); a = min(1, u / 0.12)
            c = crop.resize((max(1, int(crop.width * sc)), max(1, int(crop.height * sc))), Image.LANCZOS) if sc != 1 else crop.copy()
            if a < 1:
                c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
            cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2 + dy)))
        return cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)

    # ---- 장면 시작 전환 ----
    def transition(self, f, t):
        if self.trans == "card":
            return (f * min(1, t / 0.4)).astype(np.uint8) if t < 0.4 else f
        if self.trans == "black":
            return (f * min(1, t / 0.3)).astype(np.uint8) if t < 0.3 else f
        if self.trans == "cut":
            return f
        if t < 0.25:                                          # 장면 시작: 살짝 다가오는 전환(2026-09-30 1.07→1.03, 흐림 줄임)
            w = t / 0.25; z = 1.03 - 0.03 * (0.5 - 0.5 * math.cos(math.pi * w))
            g = _warp(f, z, VW / 2, VH / 2)
            return cv2.GaussianBlur(g, (0, 0), 2.5 * (1 - w)) if w < 0.8 else g
        return f

    def frame(self, i, view):
        t = i / FPS
        f = self.base(i, view)
        f = self.atmos(f, t)
        f = self.overlays(f, t)
        f = self.shake(f, t)
        return self.transition(f, t)
