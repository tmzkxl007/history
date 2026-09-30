# AI 영상 프레임 보정: 원본 그림 색(LAB 평균·분산)에 맞추고 선을 또렷하게
import cv2, numpy as np

def lab_stats(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab.reshape(-1, 3).mean(0), lab.reshape(-1, 3).std(0) + 1e-3

def fix(frame, ref_stats, W=1920, H=1080, amount=1.1, sigma=1.3):
    f = cv2.resize(frame, (W, H), interpolation=cv2.INTER_CUBIC)
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32)
    m, s = lab.reshape(-1, 3).mean(0), lab.reshape(-1, 3).std(0) + 1e-3
    rm, rs = ref_stats
    lab = (lab - m) / s * rs + rm                      # 원본 그림과 같은 밝기·채도 분포로
    f = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    blur = cv2.GaussianBlur(f, (0, 0), sigma)
    return cv2.addWeighted(f, 1 + amount, blur, -amount, 0)   # 언샤프 마스크로 선 복원
