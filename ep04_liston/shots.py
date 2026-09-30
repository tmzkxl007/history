# 문장별 그림 · 만화 기호 · 옛날 자료 액자 (2026-09-30 샘플)
# build.make_clip 이 불러 쓴다. 모두 화면 전체 크기(1920x1080) RGBA 그림으로 만들어 fx.SceneFX 의 글자 등장(톡)과 같은 방식으로 띄운다.
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

VW, VH = 1920, 1080
INK = (35, 30, 40, 255)


def _canvas():
    return Image.new("RGBA", (VW, VH), (0, 0, 0, 0))


def _bang(ch, col, font, s):
    """굵은 글자 하나(! ?)에 흰 테두리 + 검은 외곽 + 강조선 3개"""
    S = int(260 * s); im = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(font, int(S * 0.9))
    d.text((S, S), ch, font=f, fill=col, anchor="mm", stroke_width=int(S * 0.09), stroke_fill=INK)
    for a in (-35, 0, 35):                                   # 머리 위 강조선
        r0, r1 = S * 0.62, S * 0.86; t = math.radians(a - 90)
        d.line([(S + r0 * math.cos(t) + S * 0.3, S + r0 * math.sin(t)), (S + r1 * math.cos(t) + S * 0.3, S + r1 * math.sin(t))],
               fill=INK, width=max(4, int(S * 0.05)))
    return im


def _sweat(s):
    S = int(170 * s); im = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for (cx, cy, r) in ((0.9, 0.9, 0.34), (1.35, 1.25, 0.24), (0.6, 1.4, 0.18)):
        cx, cy, r = cx * S, cy * S, r * S
        pts = [(cx, cy - r * 1.9), (cx + r, cy), (cx - r, cy)]
        d.polygon(pts, fill=(150, 205, 250, 255), outline=INK)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 205, 250, 255), outline=INK, width=max(3, int(S * 0.035)))
        d.polygon([(cx, cy - r * 1.8), (cx + r * 0.93, cy - r * 0.2), (cx - r * 0.93, cy - r * 0.2)], fill=(150, 205, 250, 255))
        d.line([(cx, cy - r * 1.9), (cx + r * 0.97, cy - r * 0.25)], fill=INK, width=max(3, int(S * 0.035)))
        d.line([(cx, cy - r * 1.9), (cx - r * 0.97, cy - r * 0.25)], fill=INK, width=max(3, int(S * 0.035)))
        d.ellipse([cx - r * 0.45, cy - r * 0.45, cx - r * 0.1, cy - r * 0.1], fill=(255, 255, 255, 230))
    return im


def _skull(s):
    S = int(150 * s); im = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(4, int(S * 0.06))
    d.ellipse([S * 0.35, S * 0.25, S * 1.65, S * 1.45], fill=(250, 248, 240, 255), outline=INK, width=w)
    d.rounded_rectangle([S * 0.62, S * 1.15, S * 1.38, S * 1.72], radius=int(S * 0.12), fill=(250, 248, 240, 255), outline=INK, width=w)
    d.rectangle([S * 0.62 + w, S * 1.12, S * 1.38 - w, S * 1.3], fill=(250, 248, 240, 255))
    for ex in (0.72, 1.28):
        d.ellipse([S * (ex - 0.2), S * 0.72, S * (ex + 0.2), S * 1.1], fill=INK)
    d.polygon([(S, S * 1.12), (S * 0.92, S * 1.28), (S * 1.08, S * 1.28)], fill=INK)
    for tx in (0.82, 1.0, 1.18):
        d.line([(S * tx, S * 1.42), (S * tx, S * 1.7)], fill=INK, width=max(3, w // 2))
    return im


def _anger(s):
    S = int(130 * s); im = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(7, int(S * 0.14))
    col = (225, 50, 50, 255); r = S * 0.42
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):      # 만화의 '빡침' 표시: 가운데를 향해 볼록한 괄호 네 개
        cx, cy = S + sx * r * 1.15, S + sy * r * 1.15
        ang = math.degrees(math.atan2(-sy, -sx))
        d.arc([cx - r, cy - r, cx + r, cy + r], ang - 48, ang + 48, fill=col, width=w)
    return im


def _shock(s):
    S = int(160 * s); im = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(5, int(S * 0.07))
    for a in (-50, -20, 20, 50):                             # 머리 위 놀람선
        t = math.radians(a - 90)
        d.line([(S + math.cos(t) * S * 0.35, S * 1.4 + math.sin(t) * S * 0.35), (S + math.cos(t) * S * 0.85, S * 1.4 + math.sin(t) * S * 0.85)],
               fill=INK, width=w)
    return im


def _speed(s):
    im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    import random
    rnd = random.Random(3)
    for _ in range(46):                                       # 화면 가장자리에서 가운데로 모이는 집중선
        a = rnd.uniform(0, 2 * math.pi); r0 = rnd.uniform(0.55, 0.7) * VW * 0.5 * s; r1 = VW * 0.75
        c = (VW / 2, VH / 2)
        w = rnd.randint(3, 9)
        d.line([(c[0] + math.cos(a) * r0, c[1] + math.sin(a) * r0 * 0.62), (c[0] + math.cos(a) * r1, c[1] + math.sin(a) * r1 * 0.62)],
               fill=(255, 255, 255, 170), width=w)
    return im


def _tag(text, font, s):
    f = ImageFont.truetype(font, int(64 * s))
    tw = int(f.getlength(text)); pad = int(28 * s); h = int(100 * s)
    im = Image.new("RGBA", (tw + pad * 2 + 12, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, tw + pad * 2 + 6, h + 6], radius=h // 2, fill=(250, 245, 230, 255), outline=INK, width=6)
    d.polygon([((tw + pad * 2) / 2 - 14, h + 3), ((tw + pad * 2) / 2 + 14, h + 3), ((tw + pad * 2) / 2 + 6, h + 26)], fill=INK)
    d.text(((tw + pad * 2) / 2 + 6, h / 2 + 6), text, font=f, fill=INK, anchor="mm")
    return im


def _person(d, x, y, h, col):
    """단순한 사람 아이콘(머리 + 몸통) — 외곽선 굵게"""
    r = h * 0.2
    d.ellipse([x - r, y, x + r, y + 2 * r], fill=col, outline=INK, width=max(3, int(h * 0.04)))
    d.rounded_rectangle([x - h * 0.3, y + 2.2 * r, x + h * 0.3, y + h], radius=int(h * 0.18), fill=col, outline=INK, width=max(3, int(h * 0.04)))


def _people(n, red, label, font, s):
    """사람 n명 중 red명이 빨강: 왼쪽에 이름표, 흰 판 위에"""
    h = int(120 * s); gap = int(h * 0.78); f = ImageFont.truetype(font, int(58 * s))
    lw = int(f.getlength(label)) + int(40 * s)
    W_ = lw + n * gap + int(60 * s); H_ = h + int(60 * s)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], radius=int(28 * s), fill=(252, 249, 240, 245), outline=INK, width=5)
    d.text((int(30 * s), H_ / 2), label, font=f, fill=INK, anchor="lm")
    for i in range(n):
        _person(d, lw + int(30 * s) + i * gap + gap / 2, int(30 * s), h, (225, 60, 55, 255) if i < red else (185, 190, 200, 255))
    return im


def _arrow(x0, y0, x1, y1, s):
    """점선 곡선 화살표(지도 위 항로)"""
    im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P0, P2 = (x0 * VW, y0 * VH), (x1 * VW, y1 * VH); P1 = ((P0[0] + P2[0]) / 2, min(P0[1], P2[1]) - 0.18 * VH)
    pts = [((1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1])
           for t in [i / 120 for i in range(121)]]
    w = int(12 * s)
    for i in range(0, 112, 8):                                # 점선
        d.line(pts[i:i + 5], fill=(200, 40, 40, 255), width=w, joint="curve")
    ax, ay = pts[-1]; bx, by = pts[-8]; ang = math.atan2(ay - by, ax - bx); L = 46 * s
    d.polygon([(ax, ay), (ax - L * math.cos(ang - 0.45), ay - L * math.sin(ang - 0.45)), (ax - L * math.cos(ang + 0.45), ay - L * math.sin(ang + 0.45))],
              fill=(200, 40, 40, 255))
    return im


def sticker(kind, x, y, scale, font):
    """화면 비율 좌표 (x, y) 가운데에 기호를 놓은 전체 화면 RGBA"""
    if kind == "speed":
        return _speed(scale)
    if kind.startswith("arrow:"):                             # arrow:x0,y0,x1,y1
        return _arrow(*[float(v) for v in kind[6:].split(",")], scale)
    if kind.startswith("people:"):                            # people:10:1:리스턴의 환자
        _, n, red, label = kind.split(":", 3)
        g = _people(int(n), int(red), label, font, scale)
        cv = _canvas(); cv.alpha_composite(g, (int(x * VW - g.width / 2), int(y * VH - g.height / 2)))
        return cv
    if kind in ("!", "?"):
        g = _bang(kind, (235, 60, 50, 255) if kind == "!" else (60, 130, 235, 255), font, scale)
    elif kind == "sweat":
        g = _sweat(scale)
    elif kind == "skull":
        g = _skull(scale)
    elif kind == "anger":
        g = _anger(scale)
    elif kind == "shock":
        g = _shock(scale)
    elif kind.startswith("tag:"):
        g = _tag(kind[4:], font, scale)
    else:
        raise ValueError(kind)
    cv = _canvas(); cv.alpha_composite(g, (int(x * VW - g.width / 2), int(y * VH - g.height / 2)))
    return cv


def archive(path, caption, font, x=0.80, y=0.46, h=560):
    """옛날 자료(퍼블릭 도메인) 사진을 흰 테두리 액자로: 살짝 기울이고 그림자 + 아래 설명 띠"""
    ph = Image.open(path).convert("RGB")
    w = int(ph.width * h / ph.height); ph = ph.resize((w, h), Image.LANCZOS)
    b = 18; fr = Image.new("RGBA", (w + b * 2, h + b * 2 + 70), (252, 250, 244, 255))
    fr.paste(ph, (b, b))
    d = ImageDraw.Draw(fr); fs = 38
    while fs > 18 and ImageFont.truetype(font, fs).getlength(caption) > fr.width - 30:
        fs -= 2
    f = ImageFont.truetype(font, fs)
    d.text((fr.width / 2, h + b * 2 + 30), caption, font=f, fill=INK, anchor="mm")
    d.rectangle([0, 0, fr.width - 1, fr.height - 1], outline=(120, 110, 100, 255), width=3)
    fr = fr.rotate(-4, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", fr.size, (0, 0, 0, 0)); sh.putalpha(fr.getchannel("A").point(lambda v: int(v * 0.45)))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    cv = _canvas()
    cx, cy = int(x * VW - fr.width / 2), int(y * VH - fr.height / 2)
    cv.alpha_composite(sh, (cx + 14, cy + 18)); cv.alpha_composite(fr, (cx, cy))
    return cv
