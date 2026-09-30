"""의학의 역사 채널 — agy(Antigravity CLI, 사용자 울트라 구독)로 그림 한 장 만들기.

API 키 없음: agy 가 사용자 구글 계정으로 로그인된 상태에서 print 모드로 generate_image 도구를 한 번 부르게 하고,
결과 그림은 agy 데이터 폴더(~/.gemini/antigravity-cli/brain/<대화>)에서 ImageName 토큰으로 찾아온다.
--dangerously-skip-permissions 는 쓰지 않는다(CLAUDE.md 「제미나이는 agy로만」). 그림 모델은 agy 가 고른다(나노바나나2).
한도 소진(429 QUOTA_EXHAUSTED)이면 재시도하지 않고 멈춘다.
"""
import glob, os, shutil, subprocess, tempfile, time, uuid

AGY = os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")
MODEL, EFFORT = "gemini-3.8-flash-high", "high"
AGY_DATA = os.path.expanduser(r"~\.gemini\antigravity-cli")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")


class QuotaExhausted(RuntimeError):
    def __init__(self, msg, wait=None):
        super().__init__(msg); self.wait = wait    # 한도가 풀릴 때까지 남은 초(오류 본문 quotaResetDelay)


def _reset_wait(tr):
    import re
    m = re.search(r"quotaResetDelay[^0-9]{0,12}((?:\d+h)?(?:\d+m)?[\d.]+s)", tr)
    if not m:
        return None
    sec = 0.0
    for v, u in re.findall(r"([\d.]+)([hms])", m.group(1)):
        sec += float(v) * {"h": 3600, "m": 60, "s": 1}[u]
    return sec


def _conversation(token, since):
    for conv in glob.glob(os.path.join(AGY_DATA, "brain", "*")):
        tr = os.path.join(conv, ".system_generated", "logs", "transcript.jsonl")
        if os.path.exists(tr) and os.path.getmtime(tr) >= since:
            txt = open(tr, encoding="utf-8", errors="replace").read()
            if token in txt:
                return conv, txt
    return None, ""


def _own_images(conv, token):
    out = []
    for dp, dirs, fs in os.walk(conv):
        dirs[:] = [d for d in dirs if d not in (".tempmediaStorage", ".user_uploaded")]   # 참고 그림 사본
        out += [os.path.join(dp, f) for f in fs if f.lower().endswith(IMG_EXT)]
    named = [p for p in out if token in os.path.basename(p)]
    return named or out


def generate_waiting(prompt, out, refs=(), size="16:9", max_wait=3 * 3600):
    """한도가 차면 풀리는 시각까지 기다렸다가 이어서 만든다(최대 max_wait 초)"""
    waited = 0
    while True:
        try:
            return generate(prompt, out, refs, size)
        except QuotaExhausted as e:
            w = (e.wait or 600) + 30
            if waited + w > max_wait:
                raise
            print(f"agy 한도 — {w / 60:.0f}분 기다린 뒤 이어서: {os.path.basename(out)}", flush=True)
            time.sleep(w); waited += w


def generate(prompt, out, refs=(), size="16:9", tries=3, timeout=240):
    out = os.path.abspath(out)
    for attempt in range(tries):
        ws = tempfile.mkdtemp(prefix="mh_agy_")
        names = []
        for k, r in enumerate(refs):
            n = f"ref{k + 1}{os.path.splitext(r)[1] or '.png'}"
            shutil.copy(r, os.path.join(ws, n)); names.append(n)
        ref_txt = (" Use these local reference images as inputs to generate_image, in this order: "
                   + ", ".join(f"image {k + 1} = {n}" for k, n in enumerate(names)) + "." if names else "")
        token = "mh_" + uuid.uuid4().hex[:10]
        ask = (f"Call your generate_image tool exactly once with ImageName {token}.{ref_txt} Aspect ratio {size} (wide landscape). "
               f"Image prompt: {prompt}\n\nDo not run any commands and do not write any files yourself. "
               f"Reply DONE after the generate_image call.")
        t0 = time.time() - 1
        log = os.path.join(ws, "_agy.log")
        with open(log, "wb") as fh:
            proc = subprocess.Popen([AGY, "-p", ask, "--model", MODEL, "--effort", EFFORT, "--print-timeout", f"{timeout}s"],
                                    cwd=ws, stdout=fh, stderr=subprocess.STDOUT)
            try:
                proc.wait(timeout=timeout + 20)
            except subprocess.TimeoutExpired:   # agy 가 가끔 멈춘다 → 이 호출의 프로세스 트리만 끈다
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
                print(f"agy 시간 초과({timeout}s) {attempt + 1}/{tries}: {os.path.basename(out)}", flush=True)
        conv, tr = _conversation(token, t0)
        if "QUOTA_EXHAUSTED" in tr or "RESOURCE_EXHAUSTED" in tr:
            shutil.rmtree(ws, ignore_errors=True)
            w = _reset_wait(tr)
            raise QuotaExhausted(f"agy 그림 한도 소진(429) — {int(w // 60) if w else '?'}분 뒤 풀림", w)
        cands = [p for p in glob.glob(os.path.join(ws, "*")) if p.lower().endswith(IMG_EXT) and os.path.basename(p) not in names] \
            or (_own_images(conv, token) if conv else [])
        if cands:
            from PIL import Image
            Image.open(max(cands, key=os.path.getmtime)).convert("RGB").save(out)
            shutil.rmtree(ws, ignore_errors=True)
            return out
        tail = open(log, encoding="utf-8", errors="replace").read()[-500:] if os.path.exists(log) else ""
        print(f"agy 그림 없음 {attempt + 1}/{tries}: {os.path.basename(out)}\n{tail}", flush=True)
        shutil.rmtree(ws, ignore_errors=True)
        time.sleep(3)
    raise RuntimeError(f"agy 가 그림을 만들지 못함: {out}")
