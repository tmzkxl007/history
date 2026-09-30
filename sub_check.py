# 의학의 역사 채널 자막 검사기 — 넷플릭스 Timed Text Style Guide(General + Korean) 기준
# 사용자 규격 문서와 같은 코드 번호: G1 최소 5/6초 · G2 최대 7초 · G3 한 줄 · G4 가운데 정렬
#   K1 한 줄 16자 · K2 초당 12자 (라틴·숫자·공백·문장부호 0.5자) · K3 줄 끝 . , 금지 · K4 말줄임표 … · K5 이탤릭 금지
#   B1 떼면 안 되는 자리(이름·성 / 꾸미는 말·명사 / 수·단위)에서 넘김 — 경고
# 사용: python sub_check.py <subs.ass>   (위반 있으면 종료 코드 1)
import re, sys
from pathlib import Path

_d = Path(sys.argv[1]).resolve().parent
while not (_d / "build.py").exists() and _d != _d.parent:   # 쇼츠 폴더면 위쪽 편 폴더의 build.py
    _d = _d.parent
sys.path.insert(0, str(_d))
from build import wlen, break_penalty  # 편 폴더의 build.py 와 같은 규칙을 쓴다


def t2s(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


ass = Path(sys.argv[1]).read_text(encoding="utf-8")
style = re.search(r"^Style: Sub,(.*)$", ass, re.M).group(1).split(",")
ev = []
for line in ass.splitlines():
    if line.startswith("Dialogue:"):
        p = line.split(",", 9)
        ev.append((t2s(p[1]), t2s(p[2]), p[9]))

bad = []
if style[7] != "0":
    bad.append(("K5", "스타일 이탤릭"))
if style[17] not in ("2", "8"):
    bad.append(("G4", f"정렬 {style[17]} (가운데 아래/위 아님)"))
for i, (a, b, t) in enumerate(ev):
    d = b - a
    if d < 5 / 6 - 1e-3: bad.append(("G1", f"#{i} {d:.2f}s {t}"))
    if d > 7 + 1e-3: bad.append(("G2", f"#{i} {d:.2f}s {t}"))
    if "\\N" in t or "\n" in t: bad.append(("G3", f"#{i} 두 줄 {t}"))
    if wlen(t) > 16: bad.append(("K1", f"#{i} {wlen(t)}자 {t}"))
    if wlen(t) / d > 12 + 1e-6: bad.append(("K2", f"#{i} 초당 {wlen(t) / d:.1f}자 {t}"))
    if re.search(r"[.,]$", t): bad.append(("K3", f"#{i} 줄 끝 문장부호 {t}"))
    if re.search(r"[가-힣]\.\s", t): bad.append(("K3", f"#{i} 가운데 마침표(쉼표여야 함) {t}"))
    if ".." in t: bad.append(("K4", f"#{i} {t}"))
    if "\\i1" in t: bad.append(("K5", f"#{i} {t}"))
# B1: 앞 자막 끝 단어와 다음 자막 첫 단어가 한 문장 안에서 떼면 안 되는 자리인지
import json
sj = Path(sys.argv[1]).with_name("subs.json")
lid = [e[3] for e in json.load(open(sj, encoding="utf-8"))] if sj.exists() else None
for i in range(len(ev) - 1):
    a, b = ev[i][2], ev[i + 1][2]
    same = lid[i] == lid[i + 1] if lid and len(lid) == len(ev) else ev[i + 1][0] - ev[i][1] < 0.05
    if same and not re.search(r"[?!…\"]$", a):
        if break_penalty(a.split()[-1], b.split()[0]) >= 3:
            bad.append(("B1", f"#{i} '{a}' / '{b}'"))

codes = sorted({c for c, _ in bad})
print(f"자막 {len(ev)}장 · 위반 {len(bad)}건 {codes if codes else ''}")
for c, m in bad:
    print(" ", c, m)
sys.exit(1 if any(c != "B1" for c, _ in bad) else 0)
