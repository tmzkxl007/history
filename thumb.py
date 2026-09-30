# 썸네일(1280x720) 한 장: python thumb.py <편 폴더> <그림 id> <출력 이름> <글자쪽 left|right> "<줄1>|<줄2>|<줄3>" [확대 x0 y0 w]
# 줄 안에서 *강조* = 노랑, ~강조~ = 빨강.  확대: 원본 가로 비율(0~1)로 잘라낼 영역(인물을 크게)
import re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

ep, sid, name, side, text = sys.argv[1:6]
crop = [float(v) for v in sys.argv[6:9]] if len(sys.argv) >= 9 else None
EP = Path(ep)
sys.path.insert(0, str(EP))
import importlib.util as u
s = u.spec_from_file_location("b", EP / "build.py"); b = u.module_from_spec(s); s.loader.exec_module(b)
W, H = 1280, 720
JAL = str(EP / "fonts" / "Jalnan2TTF.ttf")
Y, R, WT = (255, 222, 60), (255, 70, 60), (255, 255, 255)

src = b.trim_border(Image.open(b.IMG / f"{sid}.png").convert("RGB"))
if crop:
    x0, y0, cw = crop; w0, h0 = src.size
    src = src.crop((int(w0 * x0), int(h0 * y0), int(w0 * (x0 + cw)), int(h0 * y0 + w0 * cw * 9 / 16)))
im = ImageEnhance.Brightness(ImageOps.fit(src, (W, H), Image.LANCZOS)).enhance(1.1).convert("RGBA")
g = Image.new("L", (W, 1))
for x in range(W):
    f = 1 - x / (W * 0.62) if side == "left" else (x - W * 0.38) / (W * 0.62)
    g.putpixel((x, 0), int(max(0, min(1, f)) * 230))
dark = Image.new("RGBA", (W, H), (10, 10, 16, 0)); dark.putalpha(g.resize((W, H))); im = Image.alpha_composite(im, dark)
d = ImageDraw.Draw(im)
lines = text.split("|")
size = 128 if max(len(re.sub(r"[*~]", "", l)) for l in lines) <= 6 else 112
f = ImageFont.truetype(JAL, size)
y = (H - len(lines) * int(size * 1.12)) // 2 + 20
for line in lines:
    parts = re.findall(r"\*[^*]+\*|~[^~]+~|[^*~]+", line)
    tw = sum(d.textlength(p.strip("*~"), font=f) for p in parts)
    x = 50 if side == "left" else W - 50 - tw
    for p in parts:
        col = Y if p.startswith("*") else R if p.startswith("~") else WT
        t = p.strip("*~")
        d.text((x, y), t, font=f, fill=col, stroke_width=9, stroke_fill=(15, 12, 20)); x += d.textlength(t, font=f)
    y += int(size * 1.12)
ft = ImageFont.truetype(JAL, 44); tag = "의학의 역사"; tw = d.textlength(tag, font=ft)
tx = 50 if side == "left" else W - 50 - tw - 40
d.rounded_rectangle([tx, 36, tx + tw + 40, 102], 16, fill=(200, 30, 35)); d.text((tx + 20, 44), tag, font=ft, fill="white")
out = EP / "thumb"; out.mkdir(exist_ok=True)
im.convert("RGB").save(out / f"{name}.jpg", quality=92)
print("완료", out / f"{name}.jpg")
