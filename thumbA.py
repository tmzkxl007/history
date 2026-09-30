# 채널 기본 썸네일(1편 A형): 어둡고 푸른 회색 톤 + 왼쪽 그러데이션 + 흰 글자 3줄(150px) + 핵심어만 빨강 + '의학의 역사' 표시
# python thumbA.py <편 폴더> <그림 id> <출력 이름> "<줄1>|<줄2>|<줄3>" [x0 y0 w] [--color 0.6]
#   ~빨강~ 으로 핵심어 표시. x0 y0 w: 원본에서 잘라낼 영역(가로 비율) — 인물·핵심 물건이 오른쪽 3분의 1에 오게
import re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

args = sys.argv[1:]
mix = 0.6
if "--color" in args:
    k = args.index("--color"); mix = float(args[k + 1]); del args[k:k + 2]
ep, sid, name, text = args[:4]
crop = [float(v) for v in args[4:7]] if len(args) >= 7 else None
EP = Path(ep)
import importlib.util as u
s = u.spec_from_file_location("b", EP / "build.py"); b = u.module_from_spec(s); s.loader.exec_module(b)
W, H = 1280, 720
JAL = str(EP / "fonts" / "Jalnan2TTF.ttf")
WT, R = (255, 255, 255), (255, 70, 60)

im = b.trim_border(Image.open(b.IMG / f"{sid}.png").convert("RGB"))
if crop:
    w0, h0 = im.size; x0, y0, cw = crop
    im = im.crop((int(w0 * x0), int(h0 * y0), int(w0 * (x0 + cw)), int(h0 * y0 + w0 * cw * 9 / 16)))
im = ImageOps.fit(im, (W, H), Image.LANCZOS)
g = ImageOps.grayscale(im).convert("RGB"); tint = Image.new("RGB", (W, H), (70, 85, 105))
g = Image.blend(g, Image.composite(tint, g, ImageOps.grayscale(g)), 0.35)
im = ImageEnhance.Brightness(Image.blend(im, g, mix)).enhance(0.78).convert("RGBA")   # mix: 1=완전 흑백 톤
gr = Image.new("L", (W, 1))
for x in range(W):
    gr.putpixel((x, 0), int(max(0, min(1, 1 - x / (W * 0.62))) * 235))
dk = Image.new("RGBA", (W, H), (10, 10, 16, 0)); dk.putalpha(gr.resize((W, H))); im = Image.alpha_composite(im, dk)

d = ImageDraw.Draw(im)
lines = text.split("|")
longest = max(len(re.sub(r"~", "", l)) for l in lines)
size = 150 if longest <= 5 else 140 if longest <= 6 else 124
f = ImageFont.truetype(JAL, size); y = 110 if size >= 140 else 130
for line in lines:
    x = 60
    for p in re.findall(r"~[^~]+~|[^~]+", line):
        t = p.strip("~")
        d.text((x, y), t, font=f, fill=R if p.startswith("~") else WT, stroke_width=10, stroke_fill=(15, 12, 20))
        x += d.textlength(t, font=f)
    y += int(size * 1.12)
ft = ImageFont.truetype(JAL, 44); tw = d.textlength("의학의 역사", font=ft)
d.rounded_rectangle([60, 40, 60 + tw + 40, 106], 16, fill=(200, 30, 35)); d.text((80, 48), "의학의 역사", font=ft, fill="white")
out = EP / "thumb"; out.mkdir(exist_ok=True)
im.convert("RGB").save(out / f"{name}.jpg", quality=92)
print("완료", out / f"{name}.jpg")
