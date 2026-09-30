# 유튜브 느낌 엔딩 버튼(직접 그림 — 유튜브 원본 파일·로고 사용 안 함)
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3   # 크게 그렸다가 줄여서 매끈하게

def _thumb(size, filled, col=(241, 241, 241, 255), bg=(39, 39, 39, 255)):
    s = size * S; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lw = int(0.09 * s)
    body = [0.30 * s, 0.42 * s, 0.92 * s, 0.95 * s]
    wrist = [0.06 * s, 0.44 * s, 0.24 * s, 0.95 * s]
    thumb = [(0.32 * s, 0.46 * s), (0.47 * s, 0.08 * s), (0.60 * s, 0.05 * s), (0.66 * s, 0.16 * s), (0.60 * s, 0.44 * s)]
    if filled:
        d.rounded_rectangle(wrist, int(0.05 * s), fill=col); d.rounded_rectangle(body, int(0.13 * s), fill=col); d.polygon(thumb, fill=col)
    else:
        d.rounded_rectangle(wrist, int(0.05 * s), outline=col, width=lw); d.rounded_rectangle(body, int(0.13 * s), outline=col, width=lw)
        d.line(thumb + [thumb[0]], fill=col, width=lw, joint="curve")
        d.rectangle([0.34 * s, 0.44 * s, 0.58 * s, 0.50 * s], fill=bg)
        d.line([thumb[0], thumb[-1]], fill=col, width=lw)
    return im.resize((size, size), Image.LANCZOS)

def _bell(size, col):
    s = size * S; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0.42 * s, 0.02 * s, 0.58 * s, 0.16 * s], fill=col)
    d.pieslice([0.14 * s, 0.10 * s, 0.86 * s, 0.82 * s], 180, 360, fill=col)
    d.polygon([(0.14 * s, 0.46 * s), (0.86 * s, 0.46 * s), (0.98 * s, 0.80 * s), (0.02 * s, 0.80 * s)], fill=col)
    d.ellipse([0.38 * s, 0.80 * s, 0.62 * s, 0.98 * s], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def _pill(w, h, fill, font, label, icon=None, icon_rot=0, icon_scale=1.0, chevron=False, fg=(241, 241, 241, 255)):
    pad = 26
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([pad + 4, pad + 10, pad + w + 4, pad + h + 10], h // 2, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(im); d.rounded_rectangle([pad, pad, pad + w, pad + h], h // 2, fill=fill)
    tw = d.textlength(label, font=font); isz = int(h * 0.52) if icon is not None else 0; gap = 22 if icon is not None else 0
    chev = 36 if chevron else 0
    x0 = pad + (w - (isz + gap + tw + chev)) / 2
    if icon is not None:
        ic = icon.rotate(icon_rot, resample=Image.BICUBIC, expand=True)
        if icon_scale != 1.0:
            ic = ic.resize((int(ic.width * icon_scale), int(ic.height * icon_scale)), Image.LANCZOS)
        im.alpha_composite(ic, (int(x0 + isz / 2 - ic.width / 2), int(pad + h / 2 - ic.height / 2)))
    d.text((x0 + isz + gap, pad + h / 2), label, font=font, fill=fg, anchor="lm")
    if chevron:
        cx, cy = x0 + isz + gap + tw + 26, pad + h / 2
        d.line([(cx - 10, cy - 5), (cx, cy + 6), (cx + 10, cy - 5)], fill=fg, width=5, joint="curve")
    return im

def _burst(im, cx, cy, u):
    """좋아요 순간 퍼지는 빛 조각(0<=u<=1)"""
    if not (0 <= u <= 1):
        return
    d = ImageDraw.Draw(im); a = int(255 * (1 - u) ** 1.3)
    r0, r1 = 40 + 70 * u, 55 + 95 * u
    for k in range(10):
        ang = math.radians(k * 36 + 18)
        col = [(255, 255, 255, a), (120, 180, 255, a)][k % 2]
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], fill=col, width=6)
    for k in range(8):
        ang = math.radians(k * 45); r = 70 + 110 * u
        d.ellipse([cx + r * math.cos(ang) - 6, cy + r * math.sin(ang) - 6, cx + r * math.cos(ang) + 6, cy + r * math.sin(ang) + 6], fill=(255, 255, 255, a))

def frame(frame_bgr, t, t_in, t_like, t_sub, font_path, VW=1920):
    im = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")
    if t < t_in:
        return frame_bgr
    f = ImageFont.truetype(font_path, 60)
    u = (t - t_in) / 0.3; pop = 1.0 if u >= 1 else (0.6 + 0.55 * u if u < 0.8 else 1.04 - 0.2 * (u - 0.8))
    alpha = min(1.0, (t - t_in) / 0.15)
    cy = 470; lx, sx = VW / 2 - 290, VW / 2 + 290
    # 좋아요: 누르면 엄지가 속이 채워지며 기울었다 커졌다 돌아옴 + 빛 조각
    liked = t >= t_like; dt = t - t_like
    rot = 22 * math.sin(math.pi * min(max(dt / 0.35, 0), 1)) if liked and dt < 0.35 else 0
    isc = 1 + 0.35 * math.sin(math.pi * min(max(dt / 0.35, 0), 1)) if liked and dt < 0.35 else 1.0
    like = _pill(420, 140, (39, 39, 39, 255), f, "좋아요", _thumb(74, liked), rot, isc)
    # 구독: 흰 버튼 → 회색 '구독중' + 종이 딸랑
    subbed = t >= t_sub; ds = t - t_sub
    brot = 18 * math.sin(ds * 30) * max(0, 1 - ds / 0.6) if subbed and ds < 0.6 else 0
    if subbed:
        sub = _pill(440, 140, (60, 60, 60, 255), f, "구독중", _bell(62, (241, 241, 241, 255)), brot, 1.0, chevron=True)
    else:
        sub = _pill(360, 140, (241, 241, 241, 255), f, "구독", None, fg=(15, 15, 15, 255))
    for btn, cx, tc in ((like, lx, t_like), (sub, sx, t_sub)):
        press = 0.93 if tc - 0.08 <= t < tc + 0.05 else 1.0
        s = pop * press
        b = btn.resize((max(1, int(btn.width * s)), max(1, int(btn.height * s))), Image.LANCZOS)
        if alpha < 1:
            b.putalpha(b.getchannel("A").point(lambda v: int(v * alpha)))
        im.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); _burst(lay, lx - 95, cy, (t - t_like) / 0.45); im.alpha_composite(lay)
    # 커서
    cur = Image.new("RGBA", (130, 140), (0, 0, 0, 0))
    ImageDraw.Draw(cur).polygon([(8, 4), (48, 114), (66, 76), (108, 122), (126, 104), (84, 60), (124, 46)], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=5)
    path = [(t_in + 0.25, (VW / 2 + 560, 760)), (t_like, (lx - 60, 490)), (t_like + 0.2, (lx - 60, 490)), (t_sub, (sx - 10, 490)), (t_sub + 9, (sx - 10, 490))]
    for (ta, pa), (tb, pb) in zip(path, path[1:]):
        if ta <= t <= tb:
            w = 0.5 - 0.5 * math.cos(math.pi * (t - ta) / max(tb - ta, 1e-3))
            im.alpha_composite(cur, (int(pa[0] + (pb[0] - pa[0]) * w), int(pa[1] + (pb[1] - pa[1]) * w))); break
    return cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)
