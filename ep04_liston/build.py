# 제멜바이스 편 조립: 타임라인 → 장면 클립(켄번스+오버레이) → 오디오 믹스 → 자막(ASS) → 최종 mp4
# python build.py [--only s01,s02]   (only 는 장면 클립 다시 굽기)
import json, math, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
import plan
from plan import SCENES

W = Path(__file__).parent
TTS, SFX, BGM, FONTS = W / "tts", W / "sfx", W / "bgm", W / "fonts"
_mode = json.load(open(W / "settings.json", encoding="utf-8")).get("image_mode", "flow") if (W / "settings.json").exists() else "flow"
IMG = W / {"flow": "img_flow", "agy": "img_agy", "z-image": "img_z-image", "lite": "img_lite", "mix": "img_mix", "original": "img"}[_mode]
CL = W / "clips"; CL.mkdir(exist_ok=True)
OV = W / "ov"; OV.mkdir(exist_ok=True)
SR, FPS, VW, VH = 48000, 30, 1920, 1080
GAP_LINE, GAP_SCENE = 0.06, 0.06   # 공백 제거판: 문장·장면 사이 0.06초만
JAL = str(FONTS / "Jalnan2TTF.ttf")
BHS = str(FONTS / "BlackHanSans-Regular.ttf")
DUR = json.load(open(TTS / "durations.json"))
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-2000:])


# ---------------- 타임라인 ----------------
tl, now = [], 0.0
for s in SCENES:
    st = now
    now += 0  # 공백 제거판: pre 무시
    lines = []
    for i, (text, _) in enumerate(s.get("lines", [])):
        d = DUR[f"{s['id']}_{i}"]
        lines.append(dict(i=i, text=text, start=now, end=now + d, wav=TTS / f"{s['id']}_{i}.wav"))
        now += d + (GAP_LINE if i < len(s["lines"]) - 1 else 0)
    if s.get("dur"):
        now = max(now, st + s["dur"])
    now += GAP_SCENE  # 공백 제거판: post 무시
    tl.append(dict(s=s, start=st, end=now, lines=lines))
TOTAL = now + 0.3
tl[-1]["end"] = TOTAL
print(f"총 길이 {TOTAL:.1f}s = {int(TOTAL // 60)}분 {TOTAL % 60:.0f}초")


def anchor(sc, a):
    """장면 안 상대 시각"""
    L = sc["lines"]
    if a == "start":
        return 0.0
    if a == "end":
        # 뒤 여백이 없으니 마지막 줄 끝나기 0.6초 전에 띄운다
        return max(L[-1]["start"], L[-1]["end"] - 0.6) - sc["start"] if L else 0.3
    if len(a) == 3:                     # ("line", i, 0.6) = i번째 줄의 60% 지점
        return L[a[1]]["start"] + (L[a[1]]["end"] - L[a[1]]["start"]) * a[2] - sc["start"]
    kind, i = a
    return (L[i]["start"] if kind == "line" else L[i]["end"]) - sc["start"]


# ---------------- 그림 준비 ----------------
def trim_border(im):
    a = np.asarray(im.convert("L")).astype(float)
    def edge(arr):
        n = 0
        for row in arr:
            if row.std() < 6 and (row.mean() > 225 or row.mean() < 30):
                n += 1
            else:
                break
        return n
    t, b = edge(a), edge(a[::-1])
    l, r = edge(a.T), edge(a.T[::-1])
    h, w = a.shape
    if t + b > h * 0.5 or l + r > w * 0.5:
        return im
    pad = 4
    return im.crop((l + pad if l else 0, t + pad if t else 0, w - (r + pad if r else 0), h - (b + pad if b else 0)))


def base_image(sc):
    s = sc["s"]
    src = s.get("img_from", s["id"])
    if s.get("kind") == "card":
        if not s.get("bg"):
            return Image.new("RGB", (VW * 2, VH * 2), (12, 12, 16))
        src = s["bg"]
    p = IMG / f"{src}.png"
    if not p.exists():
        im = Image.new("RGB", (VW * 2, VH * 2), (90, 90, 100))
        ImageDraw.Draw(im).text((200, 200), f"{s['id']} 그림 대기", font=ImageFont.truetype(JAL, 160), fill="white")
        return im
    im = trim_border(Image.open(p).convert("RGB"))
    im = ImageOps.fit(im, (VW * 2, VH * 2), Image.LANCZOS)
    if s.get("gray"):
        im = ImageOps.grayscale(im).convert("RGB")
    if s.get("blur") or (s.get("kind") == "card" and s.get("bg")):
        im = im.filter(ImageFilter.GaussianBlur(18))
        im = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), 0.45)
    return im


# ---------------- 글자 오버레이 ----------------
def text_img(text, font, size, fill, stroke=0, stroke_fill="black", spacing=18):
    f = ImageFont.truetype(font, size)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = d.multiline_textbbox((0, 0), text, font=f, stroke_width=stroke, spacing=spacing, align="center")
    im = Image.new("RGBA", (int(bb[2] - bb[0]) + 20, int(bb[3] - bb[1]) + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).multiline_text((10 - int(bb[0]), 10 - int(bb[1])), text, font=f, fill=fill, stroke_width=stroke,
                                      stroke_fill=stroke_fill, spacing=spacing, align="center")
    return im


def box(im, fill, pad=(34, 18), radius=22):
    b = Image.new("RGBA", (im.width + pad[0] * 2, im.height + pad[1] * 2), (0, 0, 0, 0))
    ImageDraw.Draw(b).rounded_rectangle([0, 0, b.width - 1, b.height - 1], radius, fill=fill)
    b.alpha_composite(im, pad)
    return b


def overlay_png(text, style, out):
    c = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    if style == "stamp":
        t = text_img(text, BHS, 190, (215, 40, 40, 255))
        fr = Image.new("RGBA", (t.width + 80, t.height + 50), (0, 0, 0, 0))
        ImageDraw.Draw(fr).rounded_rectangle([6, 6, fr.width - 7, fr.height - 7], 26, outline=(215, 40, 40, 255), width=14)
        fr.alpha_composite(t, (40, 25))
        fr = fr.rotate(-12, expand=True, resample=Image.BICUBIC)
        c.alpha_composite(fr, (VW - fr.width - 170, 150))
    elif style in ("label_left", "label_right"):
        t = box(text_img(text, JAL, 54, "white"), (30, 30, 40, 215))
        x = VW // 4 - t.width // 2 if style == "label_left" else 3 * VW // 4 - t.width // 2
        c.alpha_composite(t, (x, 60))
    elif style == "label_top":
        t = box(text_img(text, JAL, 60, "white"), (170, 30, 30, 225))
        c.alpha_composite(t, (VW // 2 - t.width // 2, 60))
    elif style == "name":
        t = box(text_img(text, JAL, 52, "white"), (30, 30, 40, 215))
        c.alpha_composite(t, (VW // 2 - t.width // 2, 70))
    elif style == "big":
        t = text_img(text, JAL, 118, "white", stroke=8)
        c.alpha_composite(t, (VW // 2 - t.width // 2, VH // 2 - t.height // 2 - 40))
    elif style == "big_bottom":
        t = box(text_img(text, JAL, 84, (255, 225, 90, 255)), (20, 20, 28, 220), pad=(46, 22))
        c.alpha_composite(t, (VW // 2 - t.width // 2, 110))
    elif style in ("quote", "quote_top"):
        t = text_img(text, JAL, 66 if style == "quote" else 70, "white", stroke=6, spacing=30)
        y = VH // 2 - t.height // 2 - 60 if style == "quote" else 80
        if style == "quote":
            bg = Image.new("RGBA", (VW, t.height + 120), (0, 0, 0, 150))
            c.alpha_composite(bg, (0, y - 60))
        c.alpha_composite(t, (VW // 2 - t.width // 2, y))
    elif style == "title":
        t = text_img(text, JAL, 128, "white", stroke=10, spacing=36)
        c.alpha_composite(t, (VW // 2 - t.width // 2, VH // 2 - t.height // 2 - 70))
        sub = box(text_img("의학의 역사", JAL, 60, "white"), (180, 35, 35, 235))
        c.alpha_composite(sub, (VW // 2 - sub.width // 2, VH // 2 + t.height // 2 - 30))
    elif style == "title_small":
        t = box(text_img(text, JAL, 90, "white"), (180, 35, 35, 235), pad=(50, 26))
        c.alpha_composite(t, (VW // 2 - t.width // 2, VH // 2 - t.height // 2 - 80))
    c.save(out)


# ---------------- 그래프 ----------------
PAPER, INK, RED, GREEN = (246, 240, 222), (40, 38, 48), (214, 70, 60), (90, 160, 120)


def graph_frames(kind, sid):
    """단계별 PNG 목록 반환 [(상대시각 앵커, 경로)]"""
    outs = []
    f_t = ImageFont.truetype(JAL, 64); f_v = ImageFont.truetype(JAL, 88); f_s = ImageFont.truetype(JAL, 46)
    def canvas(title):
        im = Image.new("RGB", (VW, VH), PAPER); d = ImageDraw.Draw(im)
        d.rounded_rectangle([60, 50, VW - 60, 900], 40, outline=INK, width=8)
        tw = d.textlength(title, font=f_t); d.text(((VW - tw) / 2, 95), title, font=f_t, fill=INK)
        d.line([260, 790, VW - 260, 790], fill=INK, width=8)
        return im, d
    def bar(d, x, val, vmax, col, label, value_txt):
        h = int(470 * val / vmax); w = 300
        d.rounded_rectangle([x - w // 2, 790 - h, x + w // 2, 790], 24, fill=col, outline=INK, width=7)
        vw = d.textlength(value_txt, font=f_v); d.text((x - vw / 2, 790 - h - 110), value_txt, font=f_v, fill=INK)
        lw = d.textlength(label, font=f_s); d.text((x - lw / 2, 812), label, font=f_s, fill=INK)
    if kind == "ward":
        steps = [("start", [(10, RED, "제1병동 (의사)", "약 10%")]),
                 (("line", 1), [(10, RED, "제1병동 (의사)", "약 10%"), (4, GREEN, "제2병동 (조산사)", "약 4%")]),
                 (("line", 2), "note")]
        last = None
        for k, (a, bars) in enumerate(steps):
            im, d = canvas("산욕열 사망률 (1840년대 초)")
            bb = steps[1][1] if bars == "note" else bars
            for j, (v, col, lab, vt) in enumerate(bb):
                bar(d, 660 + j * 600, v, 17, col, lab, vt)
            if bars == "note":
                note = "최악의 달엔 30% 이상!"
                nw = d.textlength(note, font=f_v)
                d.rounded_rectangle([VW / 2 - nw / 2 - 40, 190, VW / 2 + nw / 2 + 40, 310], 30, fill=RED)
                d.text((VW / 2 - nw / 2, 205), note, font=f_v, fill="white")
            p = OV / f"{sid}_g{k}.png"; im.save(p); outs.append((a, p))
    else:
        vals = [("start", 18.3, "손 씻기 직전 달", "18%"), (("line", 1), 2.2, "몇 달 뒤", "2%"), (("line", 1, 0.55), 1.2, "그다음 달", "1%대")]
        for k in range(3):
            im, d = canvas("제1병동 산욕열 사망률 (1847년)")
            for j in range(k + 1):
                _, v, lab, vt = vals[j]
                bar(d, 480 + j * 480, v, 20, RED if j == 0 else GREEN, lab, vt)
            p = OV / f"{sid}_g{k}.png"; im.save(p); outs.append((vals[k][0], p))
    return outs


def anchor_g(sc, a):
    if isinstance(a, tuple) and len(a) == 3:
        L = sc["lines"][a[1]]
        return L["start"] + (L["end"] - L["start"]) * a[2] - sc["start"]
    return anchor(sc, a)


# ---------------- 엔딩 좋아요·구독 버튼 ----------------
def _thumbs_up(d, x, y, s, col):
    d.rounded_rectangle([x, y + 0.42 * s, x + 0.22 * s, y + s], int(0.05 * s), fill=col)
    d.rounded_rectangle([x + 0.28 * s, y + 0.40 * s, x + 0.95 * s, y + s], int(0.12 * s), fill=col)
    d.polygon([(x + 0.30 * s, y + 0.46 * s), (x + 0.46 * s, y + 0.05 * s), (x + 0.60 * s, y + 0.02 * s),
               (x + 0.66 * s, y + 0.12 * s), (x + 0.58 * s, y + 0.44 * s)], fill=col)


def _bell(d, x, y, s, col):
    d.ellipse([x + 0.42 * s, y, x + 0.58 * s, y + 0.16 * s], fill=col)
    d.pieslice([x + 0.12 * s, y + 0.08 * s, x + 0.88 * s, y + 0.84 * s], 180, 360, fill=col)
    d.polygon([(x + 0.12 * s, y + 0.46 * s), (x + 0.88 * s, y + 0.46 * s), (x + s, y + 0.80 * s), (x, y + 0.80 * s)], fill=col)
    d.ellipse([x + 0.38 * s, y + 0.80 * s, x + 0.62 * s, y + s], fill=col)


def _button(label, bg, fg, icon, w=520, h=150):
    pad = 30
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad + 6, pad + 12, pad + w + 6, pad + h + 12], h // 2, fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im); d.rounded_rectangle([pad, pad, pad + w, pad + h], h // 2, fill=bg)
    f = ImageFont.truetype(JAL, 68); tw = d.textlength(label, font=f); isz, gap = 78, 28
    x0 = pad + (w - (isz + gap + tw)) / 2
    icon(d, x0, pad + h / 2 - isz / 2 - 2, isz, fg)
    d.text((x0 + isz + gap, pad + h / 2 - 44), label, font=f, fill=fg)
    return im


_EC = {}


def endcard_parts():
    if not _EC:
        _EC["like0"] = _button("좋아요", (255, 255, 255, 255), (30, 30, 30, 255), _thumbs_up)
        _EC["like1"] = _button("좋아요", (40, 110, 230, 255), (255, 255, 255, 255), _thumbs_up)
        _EC["sub0"] = _button("구독", (215, 30, 30, 255), (255, 255, 255, 255), _bell)
        _EC["sub1"] = _button("구독중", (90, 90, 95, 255), (235, 235, 235, 255), _bell)
        cur = Image.new("RGBA", (130, 140), (0, 0, 0, 0))
        ImageDraw.Draw(cur).polygon([(8, 4), (48, 114), (66, 76), (108, 122), (126, 104), (84, 60), (124, 46)],
                                    fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=5)
        _EC["cursor"] = cur
    return _EC


def endcard_times(sc):
    """장면 안 상대 시각: 등장, 좋아요 클릭, 구독 클릭"""
    L = sc["lines"][0]; t0 = L["start"] - sc["start"]; ln = L["end"] - L["start"]
    return t0 + 0.15, t0 + max(0.9, ln * 0.45), t0 + max(1.5, ln * 0.78)


def endcard_frame(frame_bgr, t, sc):
    """엔딩 버튼 = 유튜브 느낌(endcard_yt.py, 사용자 확정 2026-09-30). 예전 흰·빨강 버튼은 endcard_frame_simple"""
    sys.path.insert(0, str(W)); import endcard_yt
    t_in, t_like, t_sub = endcard_times(sc)
    return endcard_yt.frame(frame_bgr, t, t_in, t_like, t_sub, JAL, VW)


def endcard_frame_simple(frame_bgr, t, sc):
    """한 프레임에 버튼·커서를 얹는다(버튼은 톡 튀어나오고, 누르면 살짝 눌렸다 색이 바뀜)"""
    P = endcard_parts(); t_in, t_like, t_sub = endcard_times(sc)
    if t < t_in:
        return frame_bgr
    im = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")
    u = (t - t_in) / 0.32
    pop = 1.0 if u >= 1 else (0.55 + 0.6 * u if u < 0.8 else 1.03 - 0.15 * (u - 0.8))   # 0.55→1.03→1.0
    alpha = min(1.0, (t - t_in) / 0.15)
    centers = {"like": (VW / 2 - 300, 470), "sub": (VW / 2 + 300, 470)}
    for key, tc in (("like", t_like), ("sub", t_sub)):
        btn = P[key + ("1" if t >= tc else "0")]
        press = 0.92 if tc - 0.08 <= t < tc + 0.06 else 1.0
        s = pop * press
        bi = btn.resize((max(1, int(btn.width * s)), max(1, int(btn.height * s))), Image.LANCZOS)
        if alpha < 1:
            a = bi.getchannel("A").point(lambda v: int(v * alpha)); bi.putalpha(a)
        cx, cy = centers[key]
        im.alpha_composite(bi, (int(cx - bi.width / 2), int(cy - bi.height / 2)))
    # 커서: 오른쪽 아래에서 들어와 좋아요 → 구독 을 차례로 누름
    path = [(t_in + 0.25, (VW / 2 + 560, 760)), (t_like, (centers["like"][0] + 60, 490)),
            (t_like + 0.15, (centers["like"][0] + 60, 490)), (t_sub, (centers["sub"][0] + 70, 490)), (t_sub + 9, (centers["sub"][0] + 70, 490))]
    if t >= path[0][0]:
        for (ta, pa), (tb, pb) in zip(path, path[1:]):
            if ta <= t <= tb:
                w = 0.5 - 0.5 * math.cos(math.pi * (t - ta) / max(tb - ta, 1e-3))
                x = pa[0] + (pb[0] - pa[0]) * w; y = pa[1] + (pb[1] - pa[1]) * w
                im.alpha_composite(P["cursor"], (int(x), int(y)))
                break
    return cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)


# ---------------- 장면 클립 ----------------
def make_clip(k, sc):
    s = sc["s"]; sid = s["id"]
    dur = sc["end"] - sc["start"]
    out = CL / f"{k:03d}_{sid}_{int(round(dur * FPS))}_fx.mp4"
    if out.exists() and (ONLY is None or sid not in ONLY):
        src = IMG / f"{s.get('bg') or s.get('img_from', sid)}.png"
        needs_img = s.get("kind") != "graph" and not (s.get("kind") == "card" and not s.get("bg"))
        shot_new = any((IMG / f"{iid}.png").exists() and (IMG / f"{iid}.png").stat().st_mtime > out.stat().st_mtime
                       for _, iid, *_ in getattr(plan, "SHOTS", {}).get(sid, []))
        if not shot_new and (not needs_img or (src.exists() and src.stat().st_mtime < out.stat().st_mtime)):
            return out
    frames = int(round(dur * FPS))
    for old in CL.glob(f"{k:03d}_{sid}_*"):
        old.unlink()
    inputs, filt = [], []
    if s.get("kind") == "graph":
        g = graph_frames(s["graph"], sid)
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(g[0][1])]
        filt.append("[0:v]fps=30,format=yuv420p[v0]")
        cur = "v0"
        for j, (a, p) in enumerate(g[1:], 1):
            inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(p)]
            t0 = anchor_g(sc, a)
            filt.append(f"[{j}:v]format=rgba,fade=in:st={t0:.2f}:d=0.3:alpha=1[g{j}];[{cur}][g{j}]overlay=0:0[v{j}]")
            cur = f"v{j}"
    else:
        # 흔들림 방지: zoompan(정수 반올림으로 프레임마다 ±0.5px 떨림) 대신 OpenCV 소수점 변환으로 직접 프레임을 만든다
        shots = getattr(plan, "SHOTS", {}).get(sid)
        sys.path.insert(0, str(W)); import fx as FX, shots as SH
        prev_sec = next((tl[q]["s"].get("sec") for q in range(k - 1, -1, -1) if tl[q]["s"].get("sec")), None)
        basemp4 = OV / f"{sid}_motion.mp4"
        pr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{VW}x{VH}",
                               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12",
                               "-pix_fmt", "yuv420p", str(basemp4)], stdin=subprocess.PIPE)

        def extras(sc2, s2, lo, hi):
            """이 컷에 뜰 글자·만화 기호·옛날 자료(시각이 컷 안에 있는 것만)"""
            out = []
            for j, (text, style, a) in enumerate(s.get("ov", [])):
                t0 = anchor(sc2, a)
                if lo <= t0 < hi:
                    pth = OV / f"{sid}_ov{j}.png"; overlay_png(text, style, pth)
                    out.append((Image.open(pth).convert("RGBA"), t0, style))
            for kind, a, x, y, sc_ in getattr(plan, "STICKERS", {}).get(s2["id"], []):
                t0 = anchor(sc2, a)
                if lo <= t0 < hi:
                    out.append((SH.sticker(kind, x, y, sc_, JAL), t0, "stamp" if kind == "!" else "pop"))
            ar = getattr(plan, "ARCHIVE", {}).get(sid)
            if ar:
                t0 = anchor(sc2, ar[1])
                if lo <= t0 < hi:
                    out.append((SH.archive(W / ar[0], ar[2], JAL), t0, "name"))
            return out

        if shots:
            # 문장마다 그림 바꾸기(2026-09-30 샘플): 줄이 시작하는 순간 새 그림으로 컷, 컷마다 확 다가오는 전환
            L = sc["lines"]
            cuts = [0] + [int(round((L[ln]["start"] - sc["start"]) * FPS)) for ln, *_ in shots[1:]] + [frames]
            ease = lambda u: 0.5 - 0.5 * math.cos(math.pi * min(max(u, 0), 1))
            for j, (ln, iid, prompt, opt) in enumerate(shots):
                s2 = dict(s)
                if iid != sid:
                    s2.update(id=iid, img_from=iid, prompt=prompt, ref=opt.get("ref"), dark=opt.get("dark", s.get("dark")))
                    s2.pop("anim", None)
                f0, f1 = cuts[j], cuts[j + 1]; nfr = f1 - f0
                sc2 = dict(sc, s=s2, start=sc["start"] + f0 / FPS)
                src = cv2.cvtColor(np.asarray(base_image(sc2).resize((VW, VH), Image.LANCZOS)), cv2.COLOR_RGB2BGR)
                close = bool(prompt and prompt.startswith("Close-up"))
                kk = k + j

                # 2026-09-30 사용자 "화면이 막 움직인다": 컷이 짧아져도 움직임 폭을 그대로 두면 2~3배 빨라진다 →
                # 컷 길이에 비례해 초당 0.8%(클로즈업 1%)만 움직인다. 방향은 한쪽(다가가기)으로만
                amt = min(0.06, (0.010 if close else 0.008) * nfr / FPS)

                def view(i, nfr=nfr, close=close, kk=kk, amt=amt):
                    u = ease(i / max(nfr - 1, 1))
                    z = 1.02 + amt * u
                    if close:
                        return z, VW / 2, VH * (0.5 - 0.3 * amt * u)
                    m = (VW - VW / z) / 2; dx = [1, -1][kk % 2]
                    return z, VW / 2 + dx * 0.5 * m * u, VH / 2

                lo = -1e9 if j == 0 else -0.05
                F = FX.SceneFX(W, sc2, src, nfr, anchor, extras(sc2, s2, lo, nfr / FPS), prev_sec if j == 0 else s.get("sec"), k == 0 and j == 0)
                if j > 0:
                    F.trans = "cut"                           # 같은 장면 안의 그림 바꾸기는 깔끔한 컷
                for i in range(nfr):
                    pr.stdin.write(F.frame(i, view).tobytes())
        else:
            src = cv2.cvtColor(np.asarray(base_image(sc).resize((VW, VH), Image.LANCZOS)), cv2.COLOR_RGB2BGR)
            amt = min(0.07, 0.008 * dur)                 # 짧은 장면도 초당 0.8% 넘게 움직이지 않게(2026-09-30)
            z0, z1 = (1.0, 1.0 + amt) if k % 2 == 0 else (1.0 + amt, 1.0)
            dx = [0, 1, -1][k % 3]
            L = sc["lines"]
            # 그림 수 절감: 9초 넘는 장면은 문장 경계에서 같은 그림의 부분 확대 컷으로 한 번 바꾼다
            n1 = None
            if dur > 9 and len(L) >= 2:
                mid = dur / 2
                cut = min((l["start"] - sc["start"] for l in L[1:]), key=lambda x: abs(x - mid))
                n1 = int(round(cut * FPS))
            fx = [0.2, 0.8, 0.5][k % 3]
            ease = lambda u: 0.5 - 0.5 * math.cos(math.pi * min(max(u, 0), 1))

            def view(i):
                if n1 and i >= n1:                       # 두 번째 컷: 부분 확대
                    u = ease((i - n1) / max(frames - n1 - 1, 1)); z = 1.35 + 0.07 * u
                    w, h = VW / z, VH / z
                    return z, (VW - w) * fx + w / 2, (VH - h) * 0.4 + h / 2
                span = (n1 or frames) - 1
                u = ease(i / max(span, 1))
                if n1:
                    z = 1.0 + 0.06 * u; m = 0.0
                else:
                    z = z0 + (z1 - z0) * u; m = (VW - VW / z) / 2
                return z, VW / 2 + dx * 0.7 * m * (2 * u - 1), VH / 2

            # 장면 효과(fx.py): AI 영상 · 입체감 · 흔들림 · 분위기 · 글자 등장 · 전환 — 글자·만화 기호·옛날 자료도 여기서 그린다
            F = FX.SceneFX(W, sc, src, frames, anchor, extras(sc, s, -1e9, 1e9), prev_sec, k == 0)
            for i in range(frames):
                fr = F.frame(i, view)
                if s.get("endcard"):
                    fr = endcard_frame(fr, i / FPS, sc)
                pr.stdin.write(fr.tobytes())
        pr.stdin.close(); pr.wait()
        inputs += ["-i", str(basemp4)]
        filt.append("[0:v]format=yuv420p[v0]")
        cur = "v0"
    n = len([x for x in inputs if x == "-i"])
    for j, (text, style, a) in enumerate(s.get("ov", []) if s.get("kind") == "graph" else []):
        p = OV / f"{sid}_ov{j}.png"; overlay_png(text, style, p)
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(p)]
        t0 = anchor(sc, a)
        fd = 0.12 if style == "stamp" else 0.35
        filt.append(f"[{n}:v]format=rgba,fade=in:st={t0:.2f}:d={fd}:alpha=1[o{j}];[{cur}][o{j}]overlay=0:0[w{j}]")
        cur = f"w{j}"; n += 1
    # 카드 장면(검정/흐림)과 어두운 장면 사이 부드럽게
    fin = 0.0      # 카드 페이드도 fx.py 가 그린다
    last = f"[{cur}]fade=in:st=0:d={fin}[vout]" if fin else f"[{cur}]null[vout]"
    filt.append(last)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[vout]",
         "-t", f"{dur:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", str(out)])
    return out


# ---------------- 오디오 ----------------
def read_wav(p, ch=1):
    tmp = W / "tmp_read.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-ar", str(SR), "-ac", str(ch), "-c:a", "pcm_s16le", str(tmp)])
    with wave.open(str(tmp)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x.reshape(-1, ch)


def write_wav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def build_audio():
    n = int(TOTAL * SR)
    nar = np.zeros((n, 2), np.float32); fx = np.zeros((n, 2), np.float32); bg = np.zeros((n, 2), np.float32)
    for sc in tl:
        for L in sc["lines"]:
            x = read_wav(L["wav"], 1); i = int(L["start"] * SR)
            nar[i:i + len(x)] += np.repeat(x, 2, axis=1)[: n - i]
        if sc["s"].get("endcard") and (SFX / "click.wav").exists():
            _, tl_, ts_ = endcard_times(sc)
            for tt in (tl_, ts_):
                x = read_wav(SFX / "click.wav", 2); i = int((sc["start"] + tt) * SR)
                fx[i:i + len(x)] += x[: n - i] * 0.7
        for cue in sc["s"].get("sfx", []):          # (이름, 시각[, 음량배율])
            name, a, g = (tuple(cue) + (1.0,))[:3]
            x = read_wav(SFX / f"{name}.wav", 2); i = int((sc["start"] + anchor(sc, a)) * SR)
            fx[i:i + len(x)] += x[: n - i] * 0.55 * g
    # 배경음악 구간
    regions, cur, cs = [], None, 0.0
    for sc in tl:
        b = sc["s"].get("bgm")
        if b == "n04_bright":
            continue
        if b:
            if cur is not None:
                regions.append((cur, cs, sc["start"]))
            cur, cs = b, sc["start"]
    regions.append((cur, cs, TOTAL))
    cache = {}
    for name, a, b in regions:
        if name in ("cut", "silence"):
            continue
        if name not in cache:
            cache[name] = read_wav(next(BGM.glob(f"{name}_*.flac")), 2)
        src = cache[name]; L = int((b - a) * SR)
        seg = np.resize(src, (L, 2)) if len(src) < L else src[:L].copy()
        fin, fout = int(0.8 * SR), int((0.25 if name == "n04" else 1.0) * SR)
        seg[:fin] *= np.linspace(0, 1, fin)[:, None]
        seg[-fout:] *= np.linspace(1, 0, fout)[:, None]
        i = int(a * SR); bg[i:i + L] += seg
    # 음성 구간에서 음악을 낮춘다(덕킹)
    def movavg(x, win):
        c = np.concatenate([[0], np.cumsum(x, dtype=np.float64)])
        h = win // 2
        idx = np.arange(len(x))
        lo, hi = np.clip(idx - h, 0, len(x)), np.clip(idx + h, 0, len(x))
        return (c[hi] - c[lo]) / np.maximum(hi - lo, 1)
    talk = np.clip(movavg(np.abs(nar[:, 0]), int(0.25 * SR)) / 0.02, 0, 1)
    sm = movavg(talk, int(0.4 * SR))
    gain = 0.30 - 0.18 * sm
    bg *= gain[:, None].astype(np.float32)
    write_wav(W / "mix_nar.wav", nar); write_wav(W / "mix_fx.wav", fx); write_wav(W / "mix_bg.wav", bg)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(W / "mix_nar.wav"), "-i", str(W / "mix_fx.wav"), "-i", str(W / "mix_bg.wav"),
         "-filter_complex", "[0][1][2]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.72:level=false[a]", "-map", "[a]",
         "-ar", str(SR), str(W / "mix.wav")])


# ---------------- 자막 (한 줄 · 16자 · 0.83~7초 · 줄끝 . , 금지) ----------------
def split16(text):
    if len(text) > 16 and len(text.replace("'", "")) <= 16:
        text = text.replace("'", "")
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= 16:
            cur = f"{cur} {w}" if cur else w
        else:
            if cur:
                out.append(cur)
            while len(w) > 16:
                out.append(w[:16]); w = w[16:]
            cur = w
    if cur:
        out.append(cur)
    # 너무 짧은 꼬리(3자 이하)는 앞과 합칠 수 있으면 합친다
    if len(out) > 1 and len(out[-1]) <= 3 and len(out[-2]) + 1 + len(out[-1]) <= 16:
        out[-2] += " " + out.pop()
    # 그래도 꼬리가 짧으면 앞 덩어리의 마지막 단어를 넘겨 균형을 맞춘다
    while len(out) > 1 and len(out[-1]) <= 4 and " " in out[-2]:
        head, last = out[-2].rsplit(" ", 1)
        if len(last) + 1 + len(out[-1]) > 16:
            break
        out[-2], out[-1] = head, f"{last} {out[-1]}"
    return out


def clean(c):
    c = c.replace("...", "…").strip()
    c = re.sub(r"(?<=[가-힣])\.\s+", ", ", c)     # K3: 한 장 안 두 문장 사이는 쉼표
    c = re.sub(r"[.,]+$", "", c)
    return c


def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def wlen(s):
    """넷플릭스 한국어 규격 K1/K2 글자 수: 라틴 문자·숫자·공백·문장부호는 0.5자"""
    return sum(1.0 if ("가" <= ch <= "힣" or "ㄱ" <= ch <= "ㅣ") else 0.5 for ch in s)


NAMES = ["이그나츠 제멜바이스", "조지 워싱턴", "루이 파스퇴르", "조지프 리스터"] + list(getattr(plan, "NAMES", []))
_kiwi = None


def word_tags(text):
    """어절마다 (첫 형태소 품사, 끝 형태소 품사) — Kiwi 형태소 분석"""
    global _kiwi
    if _kiwi is None:
        from kiwipiepy import Kiwi
        _kiwi = Kiwi()
    spans, pos = [], 0
    for w in text.split():
        st = text.index(w, pos); spans.append((st, st + len(w))); pos = st + len(w)
    toks = _kiwi.tokenize(text)
    out = []
    for st, en in spans:
        tg = [tk.tag for tk in toks if st <= tk.start < en and tk.tag not in ("SS", "SSO", "SSC")]
        out.append((tg[0] if tg else "", tg[-1] if tg else ""))
    return out


def boundary_pen(lw, rw, ltag, rtag):
    """lw 뒤·rw 앞에서 자막을 넘길 때 벌점 (넷플릭스 General: 떼면 안 되는 자리)"""
    if lw.rstrip(",").endswith(("라는", "다는", "라던", "이란")):
        return 4                                    # 인용형 관형사('~라는 무증상 보균자')도 꾸미는 말
    if ltag[1] in ("ETM", "MM", "XPN") or (ltag[1] == "SP" and _before_comma_etm(lw)):
        return 4                                    # 관형형 뒤는 쉼표가 있어도 떼지 않는다("놓은, / 첫 기록")
    if lw.rstrip(chr(34) + chr(39)).endswith((",", "?", "!", "…")):
        return -1                                   # 문장부호 뒤 = 가장 좋은 자리
    pair = f"{lw.strip(chr(34) + chr(39))} {rw.strip(chr(34) + chr(39))}"
    if any(pair in n for n in NAMES):
        return 5                                    # 이름과 성
    if ltag[1] in ("ETM", "MM", "XPN"):
        return 4                                    # 관형형·관형사 + 꾸밈 받는 말
    if ltag[1] in ("SN", "NR") and rtag[0] in ("NNB", "SN", "NR"):
        return 4                                    # 수와 단위
    if ltag[1] in ("NNG", "NNP", "NNB") and rtag[0] in ("NNG", "NNP", "NNB"):
        return 2                                    # 명사+명사(복합어·위치명사)는 되도록 붙인다 — 금지는 아님
    return 0


def _before_comma_etm(lw):
    """'놓은,' 처럼 쉼표 앞 형태소가 관형형 어미인지"""
    w = lw.rstrip(",")
    return bool(w) and word_tags(w)[-1][1] in ("ETM", "MM")


def break_penalty(left, right):
    tg = word_tags(f"{left} {right}")
    return boundary_pen(left, right, tg[0], tg[1])


def balanced(text):
    """16자(K1 가중) 이하 덩어리로 나눈다. 점수 = (덩어리 수, 끊는 자리 벌점, 가장 긴 덩어리)"""
    if wlen(text) <= 16:
        return [text]
    words = text.split()
    n = len(words)
    tags = word_tags(text)
    pens = [0] + [boundary_pen(words[e - 1], words[e], tags[e - 1], tags[e]) for e in range(1, n)]
    best = {n: ((0, 0, 0, 0), [])}   # 점수 = (금지 자리 수, 덩어리 수, 벌점 합, 가장 긴 덩어리)
    for s in range(n - 1, -1, -1):
        cand = None
        for e in range(s + 1, n + 1):
            chunk = " ".join(words[s:e])
            if wlen(chunk) > 16:
                break
            if e in best:
                pen = pens[e] if e < n else 0
                b = best[e][0]
                sc = (b[0] + (pen >= 3), b[1] + 1, b[2] + pen, max(wlen(chunk), b[3]))
                if cand is None or sc < cand[0]:
                    cand = (sc, [chunk] + best[e][1])
        if cand:
            best[s] = cand
    return best[0][1] if 0 in best else split16(text)


def build_ass():
    ev = []   # [목표시작, 목표끝, 글자]
    for sc in tl:
        nos = set(sc["s"].get("nosub", []))
        for L in sc["lines"]:
            if L["i"] in nos:
                continue
            text = re.sub(r"[.,]+$", "", L["text"].strip())
            # 아주 짧은 문장("끝")은 앞 자막에 붙인다
            same_scene = ev and ev[-1][3].rsplit("_", 1)[0] == sc["s"]["id"]
            if wlen(text) <= 4 and same_scene and wlen(ev[-1][2]) + 1 + wlen(clean(text)) <= 16:   # 장면 경계는 넘지 않는다
                ev[-1][1] = L["end"]; ev[-1][2] = f"{ev[-1][2]}, {clean(text)}"
                continue
            chunks = balanced(text)
            weights = [max(len(c.replace(" ", "")), 1) for c in chunks]
            tot = sum(weights); t0 = L["start"]; span = L["end"] - L["start"]
            for c, wgt in zip(chunks, weights):
                d = span * wgt / tot
                ev.append([t0, t0 + d, clean(c), f"{sc['s']['id']}_{L['i']}"]); t0 += d
    # 최소 길이(0.83초·초당 12자)를 채우며 앞에서부터 순서대로 배치한다
    prev_end, drift = 0.0, 0.0
    for e in ev:
        need = max(5 / 6 + 0.01, wlen(e[2]) / 11.5)   # G1: 5/6초
        st = max(e[0], prev_end)
        en = max(e[1], st + need)
        drift = max(drift, st - e[0])
        e[0], e[1] = st, min(en, st + 7.0)
        prev_end = e[1]
    for j in range(len(ev) - 1):
        ev[j][1] = min(ev[j][1] + 0.1, ev[j + 1][0])
    print(f"자막 최대 밀림 {drift:.2f}s")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VW}
PlayResY: {VH}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Jalnan 2 TTF,62,&H00FFFFFF,&H00FFFFFF,&H00141414,&H64000000,0,0,0,0,100,100,0,0,1,5,1,2,80,80,64,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    body = "".join(f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{t}\n" for a, b, t, _ in ev)
    (W / "subs.ass").write_text(head + body, encoding="utf-8")
    json.dump([[round(a, 3), round(b, 3), t, lid] for a, b, t, lid in ev], open(W / "subs.json", "w", encoding="utf-8"), ensure_ascii=False)
    return ev


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    clips = [make_clip(k, sc) for k, sc in enumerate(tl)]
    print("클립", len(clips))
    (W / "concat.txt").write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(W / "concat.txt"), "-c", "copy", str(W / "video_raw.mp4")])
    build_audio(); print("오디오 완료")
    ev = build_ass(); print("자막", len(ev))
    out = W / "final.mp4"
    fdir = FONTS.as_posix().replace(":", "\\:")
    ass = (W / "subs.ass").as_posix().replace(":", "\\:")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(W / "video_raw.mp4"), "-i", str(W / "mix.wav"),
         "-vf", f"ass='{ass}':fontsdir='{fdir}'", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", str(out)])
    # 완성본은 덮어쓰지 않고 버전으로 남긴다: versions/v번호_그림방식.mp4
    vd = W / "versions"; vd.mkdir(exist_ok=True)
    n = len(list(vd.glob("v*.mp4"))) + 1
    import shutil
    shutil.copy2(out, vd / f"v{n}_{_mode}.mp4")
    print("완료", out, "→ 보관", vd / f"v{n}_{_mode}.mp4")
