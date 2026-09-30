# 롱폼 구간을 세로 쇼츠(1080x1920)로 재편집 — A 방식(그림·녹음·음악 재사용, 추가 비용 0)
# python short.py <첫 장면> <끝 장면> <출력 이름> "<위 제목(줄바꿈 \n)>"
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path(__file__).parent
sys.argv, args = sys.argv[:1], sys.argv[1:]
import importlib.util as u
s = u.spec_from_file_location("b", W / "build.py"); b = u.module_from_spec(s); s.loader.exec_module(b)
first, last, name, title = args[0], args[1], args[2], args[3].replace("\\n", "\n")
SW, SH = 1080, 1920
IW, IH = 1080, 608                  # 가운데 16:9 그림
IY = 560                            # 그림 위쪽 y
SUB_Y = IY + IH + 150               # 자막 줄 가운데 근처
TAIL = 0.6

ids = [sc["s"]["id"] for sc in b.tl]
sc0, sc1 = b.tl[ids.index(first)], b.tl[ids.index(last)]
t0 = sc0["start"]; t1 = sc1["lines"][-1]["end"] + TAIL if sc1["lines"] else sc1["end"]
dur = t1 - t0
OUT = W / "shorts"; OUT.mkdir(exist_ok=True)
print(f"구간 {t0:.2f}~{t1:.2f}s = {dur:.1f}s")

# 1) 고정 레이어: 위 제목 + 끝 안내 문구
JAL = str(W / "fonts" / "Jalnan2TTF.ttf")
top = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
f = ImageFont.truetype(JAL, 92); y = 170
for i, line in enumerate(title.split("\n")):
    tw = d.textlength(line, font=f)
    d.text(((SW - tw) / 2, y), line, font=f, fill=(255, 222, 60) if i == len(title.split("\n")) - 1 else "white",
           stroke_width=9, stroke_fill=(15, 12, 20))
    y += 118
top.save(OUT / "_top.png")
cta = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(cta)
f2 = ImageFont.truetype(JAL, 54); txt = "전체 이야기는 채널에서 ▶"
tw = d.textlength(txt, font=f2)
d.rounded_rectangle([(SW - tw) / 2 - 36, 1560, (SW + tw) / 2 + 36, 1560 + 92], 24, fill=(200, 30, 35, 235))
d.text(((SW - tw) / 2, 1572), txt, font=f2, fill="white")
cta.save(OUT / "_cta.png")

# 2) 자막: 롱폼 자막 중 이 구간 것만, 세로 화면 위치로
ev = [e for e in json.load(open(W / "subs.json", encoding="utf-8")) if e[0] >= t0 - 0.01 and e[1] <= t1 + 0.5]
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {SW}
PlayResY: {SH}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Jalnan 2 TTF,74,&H00FFFFFF,&H00FFFFFF,&H00141414,&H64000000,0,0,0,0,100,100,0,0,1,6,1,8,60,60,{SUB_Y - 45},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass += "".join(f"Dialogue: 0,{b.ts(max(e[0] - t0, 0))},{b.ts(min(e[1], t1) - t0)},Sub,,0,0,0,,{e[2]}\n" for e in ev)
(OUT / f"{name}.ass").write_text(ass, encoding="utf-8")
json.dump([[round(e[0] - t0, 3), round(min(e[1], t1) - t0, 3), e[2], e[3]] for e in ev],
          open(OUT / "subs.json", "w", encoding="utf-8"), ensure_ascii=False)

# 3) 영상 합성: 흐린 배경(같은 장면 꽉 채움) + 가운데 16:9 + 제목/자막/끝 안내
fdir = (W / "fonts").as_posix().replace(":", "\\:")
assp = (OUT / f"{name}.ass").as_posix().replace(":", "\\:")
cta_t = max(dur - 4.0, 0)
fc = (f"[0:v]split=2[a][b];"
      f"[a]scale={SW}:{SH}:force_original_aspect_ratio=increase,crop={SW}:{SH},boxblur=28:2,eq=brightness=-0.18[bg];"
      f"[b]scale={IW}:{IH}[fg];"
      f"[bg][fg]overlay=0:{IY}[v1];"
      f"[v1][1:v]overlay=0:0[v2];"
      f"[2:v]format=rgba,fade=in:st={cta_t:.2f}:d=0.4:alpha=1[c];[v2][c]overlay=0:0[v3];"
      f"[v3]ass='{assp}':fontsdir='{fdir}',fade=in:st=0:d=0.25[v]")
a_fc = f"[3:a]atrim={t0:.3f}:{t1:.3f},asetpts=PTS-STARTPTS,afade=in:d=0.15,afade=out:st={dur - 0.5:.2f}:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
out = OUT / f"{name}.mp4"
b.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(W / "video_raw.mp4"),
       "-loop", "1", "-t", f"{dur:.3f}", "-i", str(OUT / "_top.png"),
       "-loop", "1", "-t", f"{dur:.3f}", "-i", str(OUT / "_cta.png"),
       "-i", str(W / "mix.wav"),
       "-filter_complex", fc + ";" + a_fc, "-map", "[v]", "-map", "[a]",
       "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{dur:.3f}", str(out)])
print("완료", out)
