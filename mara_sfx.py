"""마라하기 효과음 팩(사용자 보유: 문서\쇼츠\마라하기 효과음 (1)) → <편>/sfx/m_*.wav
python mara_sfx.py <편 폴더>
팩에 라이선스 표기가 없어서 게임·영화·노래·방송 이름이 붙은 소리는 쓰지 않는다. 두둥 북소리 계열은 3D(두둥픽) 전용이라 제외.
음량: 가장 큰 0.4초 평균을 -18dB 로 맞추고(짧은 소리·긴 소리 비슷하게) 넘치는 피크는 리미터로 막는다.
"""
import subprocess, sys
from pathlib import Path
import numpy as np

MD = Path.home() / "OneDrive" / "문서" / "쇼츠" / "마라하기 효과음 (1)"
# 이름: (파일, 시작, 길이, 페이드아웃)
LIB = {
    "m_whip":     ("화면전환 - Whip Swish 쇽 휙.wav", 0.0, 0.8, 0.2),
    "m_swish":    ("화면전환 - 휙1.mp3", 0.0, 0.6, 0.2),
    "m_swing1":   ("휙 휘두르는 소리 (1번).mp3", 1.2, 0.6, 0.1),
    "m_swing2":   ("휘휙 휘두르는 소리 (2번).mp3", 1.9, 0.8, 0.1),
    "m_clack":    ("1분만 - 킷(딱따기1).mp3", 0.0, 0.7, 0.1),
    "m_drumroll": ("놀람 - 효과음(북 두구두구두구).mp3", 2.9, 3.2, 0.3),
    "m_impact":   ("충격 - Impact 01 둥.wav", 0.0, 1.0, 0.3),
    "m_shiver":   ("딸랑딸랑딸랑 덜덜덜 떠는 효과음.mp3", 0.1, 1.0, 0.2),
    "m_pop":      ("전환 병따기 - 뽁.mp3", 0.1, 0.5, 0.1),
    "m_yelp":     ("놀람 - 으약 휘랙.mp3", 0.0, 0.5, 0.1),
    "m_down":     ("시무룩 - 쀠잉.mp3", 0.1, 1.1, 0.2),
    "m_appear":   ("등장 - 뽀롱 (1초).mp3", 0.0, 0.9, 0.2),
    "m_register": ("기타 - 철컥띵 (캐셔).mp3", 0.0, 1.6, 0.4),
    "m_ding2":    ("026_띠딩2.mp3", 0.0, 1.0, 0.3),
    "m_punch":    ("펀치 - 주먹 01.mp3", 0.0, 0.4, 0.1),
    "m_clumsy":   ("예능 쩜쩜쩜 clumsy-moment-sound- (띵띵띵띵).mp3", 0.0, 1.4, 0.3),
    "m_runaway":  ("줄행랑 - 푸루루룰.mp3", 0.0, 1.4, 0.2),
    "m_thud":     ("★충격 - 쿵! 떨어지는 효과음.m4a", 0.9, 1.4, 0.4),
    "m_teong":    ("텅(터엉).mp3", 0.0, 0.9, 0.2),
    "m_hit":      ("충격 - 뚜훅 (충격).wav", 0.0, 1.0, 0.3),
    "m_heok":     ("놀람- 헉.wav", 0.1, 0.6, 0.1),
    "m_stamp":    ("기타 - stamp 혹은 장전소리.wav", 0.0, 0.8, 0.2),
    "m_tada":     ("놀람 - TaDaa 짜잔.mp3", 0.0, 2.2, 0.6),
    "m_question": ("등장 - 물음표 띵동띵동 (질문 효과음).mp3", 0.0, 0.8, 0.1),
    "m_discover": ("충격 - 놀람 발견.mp3", 0.1, 0.8, 0.2),
    "m_typewriter": ("옛날타자기소리.mp3", 0.5, 3.0, 0.5),
    "m_sparkle":  ("등장 - 뾰로롱 (2초).mp3", 0.0, 1.6, 0.4),
    "m_choir":    ("기타 - 성스러운 합창단 천사강림.mp3", 2.8, 4.2, 1.2),
    "m_giggle":   ("기타 - 까르륵 카툰 장난감웃음.mp3", 0.2, 1.8, 0.3),
    "m_drop":     ("★난감한 물방울.mp3", 0.0, 0.8, 0.2),
    "m_bell":     ("현타 - 불교종 장례식 디잉.wav", 0.0, 4.5, 2.0),
    "m_tock":     ("★전환 - 또독 (난감).wav", 0.0, 0.3, 0.05),
    "m_ding":     ("현타 - 디! 딩!.wav", 0.0, 1.4, 0.3),
}


def build(ep):
    out = Path(ep) / "sfx"; out.mkdir(exist_ok=True)
    for name, (f, ss, d, fout) in LIB.items():
        src = MD / f
        raw = subprocess.run(["ffmpeg", "-v", "quiet", "-ss", str(ss), "-t", str(d), "-i", str(src), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                             capture_output=True).stdout
        x = np.frombuffer(raw, np.float32); w = int(48000 * 0.4)
        c = np.concatenate([[0], np.cumsum(x.astype(np.float64) ** 2)])
        loud = np.sqrt(((c[w:] - c[:-w]) / w).max()) if len(x) > w else np.sqrt((x ** 2).mean())
        gain = -18 - 20 * np.log10(loud + 1e-9); dur = len(x) / 48000
        af = f"afade=t=in:d=0.004,lowpass=f=15000,volume={gain:.2f}dB,alimiter=limit=0.89:level=false,afade=t=out:st={max(0, dur - fout):.3f}:d={fout}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", str(src), "-af", af,
                        "-ar", "48000", "-ac", "2", str(out / f"{name}.wav")], check=True)
        print("ok", name, flush=True)


if __name__ == "__main__":
    build(sys.argv[1])
