# 의학의 역사 — 유튜브 롱폼·쇼츠 제작 파이프라인

만화풍 일러스트 + AI 내레이션으로 의학사 이야기를 만드는 자동화 도구 모음입니다.
대본 계획(`plan.py`) 하나를 쓰면 녹음 → 그림 → 효과·AI 영상 → 자막 → 렌더링 → 썸네일 → 쇼츠까지 이어집니다.

## 편 목록
| 폴더 | 제목 | 길이 |
|---|---|---|
| `semmelweis/` | 의사한테 아이를 받으면 죽는 병원이 있었다 (제멜바이스) | 5:23 |
| `ep02_smallpox/` | 천연두를 '손님'이라 부르던 나라 (지석영) | 4:55 |
| `ep03_typhoid_mary/` | 아무 증상 없이 뉴욕을 감염시킨 요리사 (장티푸스 메리) | 4:21 |
| `ep04_liston/` | 사망률 300%의 수술 (로버트 리스턴) — **새 편 템플릿** | 3:56 |

각 편 폴더에는 `plan.py`(장면·대본·그림 설명), `script.txt`(대본)와 그 편을 만든 스크립트가 들어 있습니다.
새 편은 `ep04_liston/` 을 복사해서 `plan.py` 만 새로 쓰면 됩니다.

## 흐름 (편 폴더 안에서)
```bash
python tts.py              # 대본 줄마다 Typecast 녹음(1.1배, 앞뒤 0.04초만 남기고 공백 제거)
python img.py refs         # 주인공 기준 캐릭터
python img.py all          # 장면 그림 (Google Flow 나노바나나2, 채널 그림체 기준 이미지 참고)
python ../omni_video.py .  # plan 의 anim=(초, "움직임") 장면을 Flow Omni Flash 영상으로
python sfx.py              # 효과음 합성(numpy)
python build.py            # 장면 클립(효과) → 오디오 믹스 → 넷플릭스 규격 자막 → 최종 mp4
python ../sub_check.py subs.ass           # 자막 규격 검사
python ../thumbA.py . <그림id> <이름> "줄1|~빨강~|줄3" x0 y0 w   # 썸네일(채널 기본형)
python short.py <첫 장면> <끝 장면> <이름> "<위 제목>"            # 세로 쇼츠(롱폼 재사용)
```

## 구성
| 파일 | 역할 |
|---|---|
| `flow_img.py` | Flow(flowkit 서버 `127.0.0.1:8100`)로 그림 한 장 |
| `omni_video.py` | Flow Omni Flash 로 그림 → 4~10초 영상 |
| `agy_img.py` | (예비) Antigravity CLI 로 그림 — 한도 차면 풀릴 때까지 대기 |
| `sub_check.py` | 넷플릭스 자막 규격(한 줄·16자·5/6~7초·초당 12자·끊는 자리) 검사 |
| `thumb.py` / `thumbA.py` | 썸네일 (A형 = 어두운 톤 + 흰 글자 3줄 + 핵심어 빨강) |
| `style/channel_style.png` | 채널 그림체 기준(2·3편) — 모든 그림의 마지막 참고 이미지 |
| 편 폴더 `build.py` | 타임라인·클립·오디오·자막·최종 인코딩 |
| 편 폴더 `fx.py` | 장면 효과: AI 영상 대체·입체감·효과음 연동 흔들림·안개·글자 등장·전환 |
| 편 폴더 `vfix.py` | AI 영상 색·선명도를 원본 그림에 맞춤 |
| 편 폴더 `endcard_yt.py` | 마지막 좋아요·구독 버튼 애니메이션(직접 그림, 유튜브 로고 아님) |

## 준비물 (저장소에 없음)
- **API 키**는 코드에 없습니다. `~/.volcano/keys/typecast`, `speechmatics`, (선택) `evolink` 파일에서 읽습니다.
- **flowkit** 서버와 크롬 확장, 로그인된 flow.google.com 탭. Flow 프로젝트 ID 는 `MEDHIST_FLOW_PROJECT` 환경변수로 바꿀 수 있습니다.
  2026-09 Flow 이전 뒤 Veo 모델 키가 `veo_3_1_i2v_s_lite_4s` 로 바뀌었습니다(flowkit 의 `flow_batch.py`·`models.json` 수정 필요).
- **폰트** (`<편>/fonts/`): 여기어때 잘난체 `Jalnan2TTF.ttf`(https://noonnu.cc/font_page/115, 재배포 금지라 저장소에 없음),
  Black Han Sans·Gothic A1(Google Fonts, OFL).
- **배경음악** (`<편>/bgm/`): 쇼팽 녹턴 퍼블릭 도메인 녹음(Musopen, Wikimedia Commons)
  `n20_csharp_minor.flac` · `n19_e_minor.flac` · `n04_f_major.flac` · `n13_c_minor.flac` · `n10_aflat_major.flac`
- Python: numpy, opencv-python-headless, pillow, kiwipiepy, rembg[cpu] / ffmpeg, yt-dlp
