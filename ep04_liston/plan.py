# 4편 「사망률 300%의 수술」 — 로버트 리스턴과 마취 이전의 외과
# 사실 근거: Wikipedia "Robert Liston"(1794~1847, 대동맥류, 1846.12.21 유럽 첫 에테르 공개 수술, 불독 겸자·대퇴 부목),
#   Scientific American "How Ether Transformed Surgery…"(리스턴 절단 사망률 약 1/10 vs 세인트바살러뮤 약 1/4, 처칠 다리 약 25초)
#   300% 일화 = Richard Gordon 『Great Medical Disasters』(1983) — 1차 사료 없음, '전해지는 이야기'로만 다룬다
# kind: img | card ,  ref: CHARS 키,  lines: (자막 문장, 감정),  sfx/ov/nosub 는 build.py 참고

STYLE = ("Flat 2D cartoon illustration for a Korean educational history YouTube channel. "
         "Clean thick dark outlines, soft muted pastel colors, simple cute characters with round heads "
         "and small dot eyes, rosy cheeks, slightly large heads (about one quarter of body height), simple rounded bodies, "
         "not realistic proportions and not long faces, minimal soft shading, storybook feel. Historically accurate 1840s London, England "
         "(Victorian clothes, top hats, gas lamps, wooden operating theatre) unless the scene says otherwise. "
         "Wide 16:9 composition with the main subject centered. "
         "Full-bleed illustration that fills the entire canvas edge to edge: no border, no frame, no rounded corners, no white margin. "
         "Every person has a visible face with eyes and a mouth. No flags. Absolutely no blood, no wounds, no gore: "
         "surgery is only suggested (a sheet over the leg, a raised knife, a surgeon's back). "
         "Absolutely no text, no letters, no numbers, no captions, no watermark, no signature.")
DARK = " Dim moody lighting, muted blue-gray palette, tense but not gory."

LISTON = ("Robert Liston: a very tall broad-shouldered Scottish surgeon in his forties drawn in the cute round storybook style, "
          "round face, dark wavy hair and thick sideburns, confident dot eyes, wearing a dark green frock coat over a white shirt")
CHARS = {"liston": LISTON}
NAMES = ["로버트 리스턴", "리처드 고든", "프레더릭 처칠", "세인트바살러뮤 병원"]

SCENES = [
# ⓪ 콜드 오픈
dict(id="l01", sec="⓪", bgm="n20", dark=True,
     prompt="A crowded 1840s London operating theatre: a steep wooden amphitheatre packed with medical students and gentlemen in top hats leaning over the railings, all staring down at a wooden operating table in the center lit by a skylight; a patient lies on the table under a white sheet, held down by assistants.",
     lines=[("1840년대 런던.", "tonedown"), ("계단식 강의실에 사람들이 빽빽하게 모여 있습니다.", "normal"),
            ("가운데 나무 탁자 위에는, 정신이 멀쩡한 환자가 묶여 있죠.", "tonedown"),
            ("수술을 구경거리처럼 지켜보던 이 강의실 때문에, 지금도 영어로 수술실을 오퍼레이팅 시어터, 극장이라고 부릅니다.", "normal")], sfx=[("footsteps", "start")]),
dict(id="l02", anim=(8, "The tall surgeon in the green coat slowly raises the long knife higher above his head with a confident dramatic look, the audience lean forward and hold their breath, one student lifts a pocket watch, subtle camera push-in."), sec="⓪", ref="liston", dark=True,
     prompt=f"{LISTON} stands at the operating table seen from behind the crowd, raising a long gleaming amputation knife high above his head dramatically, the audience holding their breath; a pocket watch held up by a student in the foreground.",
     lines=[("거구의 외과의사가 칼을 높이 들며 외칩니다.", "normal"), ("여러분, 시간을 재십시오!", "toneup")],
     sfx=[("hit", ("after", 1))]),
dict(id="l03", sec="⓪", dark=True,
     prompt="Three small grave headstones side by side in a foggy London churchyard at dusk, without any letters on them, crows on a bare tree.",
     lines=[("그리고 이날, 이 수술에서는 세 사람이 죽었다고 전해집니다.", "tonedown"), ("환자, 조수, 그리고 구경꾼까지.", "tonedown"),
            ("수술 한 번에 사망률 300%.", "tonedown")], ov=[("사망률 300%", "big_bottom", ("line", 2))]),
dict(id="l04", kind="card", bg="l04bg",
     bgprompt="The wooden Victorian operating theatre empty at night, moonlight through the skylight falling on the empty operating table, eerie.",
     ov=[("사망률 300%의\n수술", "title", "start")], dur=3.2, sfx=[("whoosh", "start")]),

# ① 마취가 없던 시대
dict(id="l05", sec="①", bgm="n20",
     prompt="A frightened Victorian man in a nightshirt sits on the edge of a hospital bed gripping a leather strap between his teeth, sweating, while a nurse offers him a glass of brandy; other patients watch nervously.",
     lines=[("이 시대엔 마취가 없었습니다.", "normal"), ("환자는 수술 내내 깨어 있었고,", "normal"),
            ("할 수 있는 거라곤 독한 술을 마시고, 가죽 끈을 이로 꽉 무는 것뿐이었죠.", "normal")]),
dict(id="l06", sec="①",
     prompt="Four strong assistants in aprons hold down a struggling patient on a wooden operating table under a white sheet, the patient's mouth open in a scream, seen from a distance; no blood.",
     lines=[("건장한 조수 여러 명이 환자의 팔다리를 붙잡았고,", "normal"), ("수술실에는 비명이 울려 퍼졌습니다.", "tonedown")]),
dict(id="l07", sec="①",
     prompt="A cute cartoon infographic-style scene: a big stopwatch with a running clock hand next to a worried patient on a table and a surgeon hurrying; motion lines showing speed.",
     lines=[("그래서 외과의사에게 가장 중요한 능력은 딱 하나였습니다.", "normal"), ("속도.", "toneup"),
            ("오래 걸릴수록 환자는 고통과 출혈로 쇼크에 빠져 죽었거든요.", "normal")], ov=[("속도 = 생존", "big_bottom", ("line", 1))]),
dict(id="l08", sec="①", ref="liston",
     prompt=f"Character introduction: {LISTON} stands proudly in the operating theatre, towering over the other doctors who only reach his shoulders, arms crossed, confident smile.",
     lines=[("그리고 그 시대, 런던에서 가장 빠른 칼을 가진 남자가 있었습니다.", "normal"), ("스코틀랜드 출신의 외과의사, 로버트 리스턴.", "normal"),
            ("성격도 칼만큼 거칠어서, 젊은 시절 동료들과 싸우다 에든버러 병원에서 쫓겨난 적도 있었죠.", "normal")],
     ov=[("로버트 리스턴 (1794~1847)", "name", ("line", 1))]),

# ② 가장 빠른 칼
dict(id="l09", sec="②", ref="liston",
     prompt=f"{LISTON} demonstrates his technique: his huge left hand firmly squeezes the thigh of a patient under a sheet like a clamp, while his right hand holds a long knife ready; students taking notes around him; no blood.",
     lines=[("키가 190센티미터에 가까운 거구에,", "normal"), ("손이 얼마나 큰지 한 손으로 환자의 허벅지를 꽉 움켜쥐어 피를 막고,", "normal"),
            ("나머지 한 손으로 칼을 휘둘렀다고 합니다.", "normal")]),
dict(id="l10", sec="②", ref="liston",
     prompt=f"{LISTON} holds a knife between his teeth like a pirate while using both hands to tie a bandage, students staring in amazement; comedic.",
     lines=[("두 손이 모자라면, 칼을 입에 물고 수술을 이어 갔다는 이야기도 있죠.", "normal")]),
dict(id="l11", sec="②", ref="liston",
     prompt=f"A giant cartoon pocket watch fills the background while {LISTON} works at lightning speed at the operating table with motion blur lines, the audience gasping.",
     lines=[("다리 하나를 자르는 데 걸린 시간은, 약 2분 30초.", "normal"), ("다른 의사들보다 몇 배나 빨랐습니다.", "happy")],
     ov=[("다리 절단 약 2분 30초", "big_bottom", ("line", 0))], sfx=[("pin", "start")]),
dict(id="l12", sec="②",
     prompt="A simple cartoon comparison chart: on the left one small sad gravestone next to ten cheerful patients walking out of a hospital with crutches; on the right one gravestone next to only four patients; clean flat infographic style without letters.",
     lines=[("그리고 이 속도는 실제로 사람을 살렸습니다.", "normal"), ("리스턴에게 다리를 잘린 환자는 열 명 중 한 명꼴로 죽었지만,", "normal"),
            ("같은 시기 런던의 다른 큰 병원에선 네 명 중 한 명꼴로 죽었거든요.", "normal")],
     ov=[("리스턴 1/10  vs  다른 병원 1/4", "big_bottom", ("line", 2))]),

# ③ 너무 빨라서 생긴 일들
dict(id="l13", sec="③", ref="liston",
     prompt=f"A frightened patient in a nightshirt runs away down a hospital corridor and hides in a small wooden toilet closet, while {LISTON} strides after him with determination; comedic chase.",
     lines=[("리스턴에 대한 황당한 이야기는 한둘이 아닙니다.", "normal"), ("겁에 질린 환자가 수술 직전에 도망쳐 화장실에 숨자,", "normal"),
            ("문을 부수고 들어가 환자를 직접 끌고 나왔다는 이야기.", "normal"),
            ("너무 빨리 자르다가, 다리와 함께 환자의 소중한 부위까지 잘라 버렸다는 이야기도 있죠.", "normal")], sfx=[("door_bang", ("line", 2))]),
dict(id="l14", anim=(10, "The tall surgeon in the green coat swings his long knife in a fast wide arc, the assistant beside him jerks his hand back in surprise, the old white-haired gentleman spectator in the front row flinches backward as the knife tip passes near his coat, the crowd gasps."), sec="③", ref="liston", dark=True,
     prompt=f"{LISTON} swings his knife in a fast wide arc at the operating table, motion lines, an assistant beside him yanking his hand back in surprise, an old white-haired gentleman spectator with gray whiskers in a brown coat and black top hat in the front row flinching as the knife tip flies near his coat tail; no blood, tense comedy.",
     lines=[("그리고 가장 유명한 이야기가 바로, 그 사망률 300%의 수술입니다.", "tonedown"), ("그날도 리스턴은 번개처럼 칼을 휘둘렀는데,", "normal"),
            ("너무 빨랐던 탓에 옆에서 돕던 조수의 손가락까지 베어 버렸고,", "tonedown"), ("그 칼끝이 맨 앞줄 구경꾼의 코트 자락을 스쳤다고 합니다.", "tonedown")],
     sfx=[("hit", ("line", 2))]),
dict(id="l15", anim=(4, "The old white-haired gentleman in the brown coat faints and falls backward in slow motion into the arms of the spectators behind him, his top hat tumbling off, the surgeon in the green coat and the young assistant stare in shock. Keep every face exactly as in the image."), ref_prev="l14", sec="③", dark=True,
     prompt="The same old white-haired gentleman spectator with gray whiskers in a brown coat and black top hat faints dramatically backwards in the front row of the operating theatre, his top hat falling off, other spectators catching him in shock; the tall surgeon in the green coat and the young assistant stare, holding exactly one knife",
     lines=[("칼에 찔린 줄 안 구경꾼은 그 자리에서 쇼크로 쓰러져 죽었고,", "tonedown")],
     ov=[("사망 1", "stamp", "end")], sfx=[("stamp", "end")]),
dict(id="l16", sec="③", dark=True,
     prompt="A single hospital bed in a dim Victorian ward: only the young surgical assistant lies in it, a young man with short neat brown hair and a bandaged hand, feverish and pale; a nurse stands beside the bed and sadly lowers her head. Only one bed with one patient; nobody else lies in bed. Nobody in this picture has long dark wavy hair or sideburns; the surgeon in the green coat does not appear",
     lines=[("며칠 뒤, 환자와 조수는 상처가 썩어 들어가는 괴저로 차례로 숨졌습니다.", "sad")],
     ov=[("사망 3", "stamp", "end")], sfx=[("stamp", "end")], post=0.3),
dict(id="l17", sec="③", ref="liston", bgm="n04_bright",
     prompt=f"A bright theatrical scene: {LISTON} takes a proud bow on a stage in front of a cheering crowd, a big shining golden medal on his chest, spotlight; comedic legend style.",
     lines=[("수술 한 번에 세 명.", "normal"), ("그렇게 리스턴은 역사상 유일한, 사망률 300%의 외과의사로 전설이 되었습니다.", "happy"),
            ("끝.", "happy")], sfx=[("chime", "start")]),
dict(id="l18", sec="③", ref="liston", bgm="cut", gray=True, img_from="l17",
     lines=[("…이라고 하기엔, 이 이야기에는 이상한 점이 있습니다.", "normal")], sfx=[("scratch", "start")]),

# ④ 전설을 추적하다
dict(id="l19", sec="④", bgm="n19",
     prompt="A cozy modern library at night: a detective-like researcher with a magnifying glass digs through piles of old dusty books and newspapers from the 1840s, a lamp glowing, red strings on a corkboard behind.",
     lines=[("그 시대의 기록을 뒤져 보면,", "normal"), ("이 끔찍한 수술에 대한 기록이 어디에도 없습니다.", "tonedown"),
            ("병원 기록에도, 신문에도, 동료들의 편지에도요.", "normal")], sfx=[("pin", "start")]),
dict(id="l20", sec="④",
     prompt="A 1980s British writer, a friendly older man with glasses and a cardigan, typing a book on a typewriter in a study full of medical books, a cup of tea, smiling mischievously.",
     lines=[("이 이야기가 처음 등장하는 건, 무려 140년 가까이 지난 1983년.", "normal"),
            ("영국의 의사 출신 작가 리처드 고든이 쓴 책, 위대한 의학의 재앙이었습니다.", "normal"),
            ("그런데 이 작가, 사실은 병원을 배경으로 한 코미디 소설로 유명한 사람이었습니다.", "normal"),
            ("그래서 지금은 대부분 지어낸 이야기일 가능성이 크다고 봅니다.", "normal")],
     ov=[("출처: 1983년 책 한 권", "big_bottom", ("line", 1))]),
dict(id="l21", sec="④", dark=True,
     prompt="A dim Victorian hospital ward with patients in rows of beds, visible dirty surgical tools on a wooden tray, surgeons in dirty coats walking between beds without washing their hands; flies; gloomy.",
     lines=[("하지만 이 전설이 완전히 허무맹랑한 건 아닙니다.", "normal"), ("이 시대엔 아직 세균도, 소독도 몰랐거든요.", "normal"),
            ("수술 자체는 살아남아도, 상처가 썩어 죽는 일이 흔했습니다.", "tonedown")]),
dict(id="l22", sec="④",
     prompt="A cartoon scene in a snowy 1847 Vienna hospital: a young doctor with sideburns and a small mustache in a black frock coat washes his hands in a basin of chlorine water, a callback to a previous story, warm lighting.",
     lines=[("1편에서 봤던 제멜바이스가 비엔나에서 손 씻기를 외치던 게, 바로 이 무렵이죠.", "normal"),
            ("전설은 지어낸 이야기여도, 그 시대 수술실이 얼마나 위험했는지는 사실이었던 겁니다.", "normal")], post=0.3),

# ⑤ 진짜 반전
dict(id="l23", sec="⑤", bgm="n10",
     prompt="A calendar-like winter scene outside University College Hospital in London in December 1846, snow falling, a crowd of students hurrying inside with excitement, a newspaper boy running.",
     lines=[("그런데 리스턴의 진짜 이야기는 따로 있습니다.", "normal"), ("1846년 12월 21일, 런던.", "normal"),
            ("바다 건너 미국에서 놀라운 소식이 막 도착했거든요.", "normal"),
            ("두 달 전, 보스턴의 치과의사 모턴이 에테르라는 약으로 공개 수술에 성공했다는 소식이었죠.", "normal")]),
dict(id="l24", sec="⑤",
     prompt="A glass inhaler flask with a rubber tube and mouthpiece containing clear ether liquid, glowing softly on a table in the operating theatre, curious students leaning in.",
     lines=[("에테르를 들이마시게 하면 환자가 깊이 잠들어서,", "normal"), ("칼을 대도 아픔을 느끼지 못한다는 거였죠.", "normal")]),
dict(id="l25", anim=(10, "The calm patient breathes from the glass ether inhaler, his eyes slowly close and he falls peacefully asleep, the surgeon in the green coat rolls up his sleeves and steps closer, the audience leans forward in silent suspense."), sec="⑤", ref="liston",
     prompt=f"In the operating theatre, a calm patient (a middle-aged butler) breathes from a glass ether inhaler and falls peacefully asleep on the table under a white sheet, while {LISTON} stands ready with rolled-up sleeves; the audience watches silently; no blood.",
     lines=[("리스턴은 유럽에서 처음으로, 에테르 마취 공개 수술에 나섭니다.", "normal"), ("환자는 집사로 일하던 프레더릭 처칠.", "normal"),
            ("그리고 이번엔 다리를 자르는 데 걸린 시간이 약 25초.", "normal")], ov=[("약 25초", "big_bottom", ("line", 2))]),
dict(id="l26", anim=(6, "The patient on the table slowly wakes up, blinks sleepily and tilts his head with a confused question, then the whole audience of students bursts into laughter and claps."), ref_prev="l25", sec="⑤",
     prompt="The patient butler wakes up on the operating table with a sleepy confused face asking a question, while the whole audience of students bursts into laughter and applause.",
     lines=[("잠에서 깬 환자가 이렇게 물었다고 합니다.", "normal"), ("수술은 언제 시작하나요?", "normal"),
            ("강의실은 웃음바다가 됐죠.", "happy")], sfx=[("chime", ("line", 2))]),
dict(id="l27", ref_prev="l25", sec="⑤", ref="liston",
     prompt=f"{LISTON} turns to the cheering audience with a big grin, gesturing proudly toward the ether inhaler, sunlight streaming through the skylight.",
     lines=[("리스턴은 이렇게 말했다고 전해집니다.", "normal"), ("양키들의 이 속임수가, 최면술보다 훨씬 낫군요.", "happy")]),

# ⑥ 속도가 필요 없어진 세상
dict(id="l28", sec="⑥", ref="liston",
     prompt=f"{LISTON} looks thoughtfully at his old long amputation knife in his hand, standing alone in the empty operating theatre, the ether inhaler on the table beside him; bittersweet mood.",
     lines=[("생각해 보면 아이러니합니다.", "normal"), ("가장 빠른 칼로 이름을 날린 외과의사가,", "normal"),
            ("더 이상 서두를 필요가 없는 시대의 문을 연 셈이니까요.", "normal")]),
dict(id="l29", sec="⑥", ref="liston", dark=True,
     prompt=f"A quiet Victorian bedroom at night: {LISTON} lies ill in bed, a candle burning low, his medical books and tools on the desk.",
     lines=[("그리고 그로부터 1년 뒤인 1847년 12월,", "tonedown"), ("리스턴은 대동맥이 터지는 병으로 쉰세 살에 세상을 떠납니다.", "sad")]),
dict(id="l30", sec="⑥",
     prompt="A modern bright hospital: a doctor gently fits a leg splint on a smiling patient, and a tray of modern locking surgical forceps shines on a table beside them.",
     lines=[("그가 만든 다리 부목과 지혈용 집게는,", "normal"), ("지금도 이름을 바꿔 가며 병원에서 쓰이고 있습니다.", "normal")], post=0.3),

# ⑦ 마무리
dict(id="l31", sec="⑦",
     prompt="A modern peaceful operating room where a patient sleeps calmly under anesthesia with a mask, surgeons in green gowns working calmly, monitors glowing softly.",
     lines=[("사망률 300%의 수술은 아마 전설일 겁니다.", "normal"), ("하지만 그런 전설이 그럴듯하게 들릴 만큼,", "normal"),
            ("마취가 없던 시절의 수술은 정말로 끔찍했습니다.", "tonedown"), ("우리가 수술대 위에서 편히 잠들 수 있게 된 건, 불과 180년 전부터입니다.", "normal")]),
dict(id="l32", kind="card", bg="l31", blur=True, endcard=True,
     lines=[("영상이 재미있으셨다면 좋아요와 구독 눌러주세요.", "normal"), ("감사합니다.", "happy")]),
]


# ---------------- 효과음: 마라하기 팩 (2026-09-30) — mara_sfx.py 가 sfx/m_*.wav 를 만든다 ----------------
# (이름, 시각[, 음량배율]) · 시각 = "start" / "end" / ("line", i) / ("after", i) / ("line", i, 0.6)=i번째 줄 60% 지점
SFX_MARA = {
    "l02": [("m_swing1", ("line", 0, 0.4)), ("m_clack", ("after", 1))],
    "l03": [("m_drumroll", ("line", 1), 1.1), ("m_impact", ("line", 2))],
    "l04": [("m_whip", "start")],
    "l05": [("m_shiver", ("line", 1, 0.3), 0.8), ("m_pop", ("line", 2, 0.2))],
    "l06": [("m_yelp", ("line", 1, 0.45), 0.8)],
    "l07": [("m_swish", ("line", 1)), ("m_down", ("line", 2, 0.6), 0.8)],
    "l08": [("m_swing2", ("line", 0, 0.75)), ("m_appear", ("line", 1), 0.8)],
    "l09": [("m_punch", ("line", 1, 0.5), 0.8), ("m_swing1", ("line", 2, 0.5))],
    "l10": [("m_clumsy", ("line", 0, 0.9))],
    "l11": [("m_register", "start", 0.8)],
    "l12": [("m_ding2", ("line", 1, 0.6), 0.8), ("m_down", ("line", 2, 0.7), 0.8)],
    "l13": [("m_runaway", ("line", 1, 0.5)), ("m_thud", ("line", 2, 0.2)), ("m_teong", ("line", 3, 0.75))],
    "l14": [("m_swing2", ("line", 1, 0.55)), ("m_hit", ("line", 2, 0.45)), ("m_swish", ("line", 3, 0.6), 0.8)],
    "l15": [("m_heok", ("line", 0, 0.15)), ("m_thud", ("line", 0, 0.55)), ("m_stamp", "end", 0.7)],
    "l16": [("m_stamp", "end", 0.7)],
    "l17": [("m_tada", ("line", 2))],
    "l18": [("m_question", "start")],
    "l19": [("m_discover", "start")],
    "l20": [("m_typewriter", ("line", 1, 0.3), 1.1)],
    "l23": [("m_sparkle", ("line", 2, 0.4), 0.8)],
    "l24": [("m_choir", ("line", 0, 0.6), 1.2)],
    "l25": [("m_clack", ("line", 2, 0.2)), ("m_swing1", ("line", 2, 0.6))],
    "l26": [("m_question", ("after", 1)), ("m_giggle", ("line", 2))],
    "l27": [("m_ding", ("after", 1))],
    "l28": [("m_drop", ("line", 0, 0.5))],
    "l29": [("m_bell", ("line", 1, 0.5), 0.8)],
    "l30": [("m_tock", ("line", 0, 0.6))],
}
for _s in SCENES:
    if _s["id"] in SFX_MARA:
        _s["sfx"] = SFX_MARA[_s["id"]]
    else:
        _s["sfx"] = []                    # 합성 효과음은 쓰지 않는다(엔딩 좋아요·구독 클릭음만 그대로)


# ---------------- 샘플(2026-09-30): 문장마다 그림 바꾸기 + 얼굴 클로즈업 + 만화 기호 + 정보 그림 (앞 1분) ----------------
# SHOTS[장면] = [(시작 줄, 그림 id, 그림 설명 또는 None=장면 원래 그림, 옵션)]  — 줄이 바뀌는 순간 그림이 바뀐다
CU = "Close-up shot: the face and upper body fill most of the frame, simple softly blurred background. "
SHOTS = {
    "l01": [(0, "l01a", "Establishing shot of a foggy 1840s London street at dawn: brick buildings, gas lamps, a horse carriage, "
                        "and a big old hospital building with a columned entrance in the background, people in top hats walking.", {}),
            (1, "l01", None, {}),
            (2, "l01c", CU + "A terrified young Victorian man lying on a wooden operating table, wide awake with huge round eyes, "
                        "sweating, leather straps across his chest and arms, looking up at the crowd above him.", {"dark": True}),
            (3, "l01d", "Victorian gentlemen in top hats sitting in rows of theatre seats, eagerly watching like it is a show, one holds "
                        "opera glasses, another leans forward excitedly, red velvet theatre curtains at the sides.", {"dark": True})],
    "l05": [(0, "l05a", CU + "A nervous Victorian patient in a nightshirt stares at a tray of big old surgical tools (saws and knives) "
                        "on a table next to his bed, gulping, sweat on his forehead.", {}),
            (2, "l05", None, {})],
    "l06": [(0, "l06", None, {}),
            (1, "l06b", "Spectators in the steep wooden operating theatre wincing and covering their ears with both hands, "
                        "eyes squeezed shut, some leaning back in shock.", {"dark": True})],
    "l07": [(0, "l07a", CU + "A serious Victorian surgeon in a black coat holding up exactly one finger toward the viewer, "
                        "eyebrows raised, as if saying 'only one thing matters'.", {}),
            (1, "l07", None, {})],
    "l08": [(0, "l08a", "Extreme close-up of only a very large hand in a dark green coat sleeve with a white shirt cuff, gripping a long "
                        "gleaming amputation knife held up high, a bright sparkle of light on the blade; no face and no person visible, "
                        "only the hand, sleeve and knife against a dark theatre background; no blood.", {"dark": True}),
            (1, "l08", None, {}),
            (2, "l08c", "Robert Liston, angry with a red face, arguing loudly with two older doctors in a Victorian hospital hallway, "
                        "one doctor pointing at the open door telling him to leave.", {"ref": "liston"})],
}
# 만화 기호: (종류, 시각, x, y, 크기) — x·y 는 화면 비율. 종류: ! ? sweat skull anger speed shock tag:글자
STICKERS = {
    "l01c": [("!", ("line", 2, 0.45), 0.73, 0.22, 1.0)],
    "l03":  [("tag:환자", ("line", 1, 0.05), 0.34, 0.50, 1.0), ("tag:조수", ("line", 1, 0.35), 0.50, 0.50, 1.0),
             ("tag:구경꾼", ("line", 1, 0.65), 0.66, 0.50, 1.0)],
    "l05a": [("!", ("line", 1, 0.2), 0.72, 0.2, 1.0)],
    "l06b": [("!", ("line", 1, 0.3), 0.30, 0.25, 1.0), ("!", ("line", 1, 0.5), 0.72, 0.22, 0.8)],
    "l07a": [("tag:딱 하나!", ("line", 0, 0.55), 0.26, 0.40, 1.1)],
    "l07":  [("skull", ("line", 2, 0.5), 0.20, 0.40, 0.8)],
    "l08a": [("speed", ("line", 0, 0.3), 0.50, 0.50, 1.0)],
    "l08c": [("anger", ("line", 2, 0.35), 0.49, 0.36, 0.7)],
}
# 실제 옛날 자료(퍼블릭 도메인) 액자: 장면 → (파일, 시각, 설명)
ARCHIVE = {"l08": ("archive/liston_portrait.jpg", ("line", 1, 0.1), "실제 사진 · 1845년경")}  # Hill & Adamson, 퍼블릭 도메인(Wikimedia Commons)

# ---------------- 4편 전체(2026-09-30 사용자 "4편 이렇게 만들어 줘"): 나머지 장면도 문장마다 그림 ----------------
# AI 영상 장면(l02 l14 l15 l25 l26)·카드·짧은 장면(l10 l11 l16 l18 l24)은 그대로. 기존 그림을 다시 쓰는 컷도 있다(l03 l06 l01c l08a)
SHOTS.update({
    "l09": [(0, "l09a", "Robert Liston standing next to an ordinary Victorian doctor who only reaches his chest, a tall wooden height-measuring "
                        "board behind them with plain tick marks and no numbers, the ordinary doctor looking up at him in surprise.", {"ref": "liston"}),
            (1, "l09", None, {})],
    "l12": [(0, "l12", None, {}),
            (1, "l12b", "Plain soft beige paper background with a subtle vintage texture and nothing else, empty.", {})],
    "l13": [(0, "l13a", "Several Victorian doctors in a hospital corridor whispering gossip to each other behind their hands, amused and "
                        "shocked faces, one covering his mouth to stop laughing.", {}),
            (1, "l13", None, {}),
            (2, "l13c", "Robert Liston dragging a crying patient in a nightshirt by the collar out of a broken wooden toilet door, "
                        "splinters of the door on the floor, comedic cartoon scene.", {"ref": "liston"}),
            (3, "l13d", CU + "A young Victorian surgical assistant with a horrified face, eyes popping and both hands over his mouth.", {})],
    "l17": [(0, "l17a", "Three cute friendly cartoon ghosts floating side by side in a dark operating theatre, one in a patient's nightshirt, "
                        "one in an assistant's apron, one in a gentleman's coat and top hat, waving shyly; spooky but funny, not scary.", {"dark": True}),
            (1, "l17", None, {})],
    "l19": [(0, "l19", None, {}),
            (1, "l19b", CU + "A puzzled researcher with round glasses holding a magnifying glass over a big old ledger book with completely "
                        "blank empty pages, scratching his head.", {}),
            (2, "l19c", "Top-down view of a wooden desk with three old documents laid side by side: a thick hospital record book, "
                        "an old folded newspaper, and a bundle of handwritten letters tied with string; all blank with no readable writing.", {})],
    "l20": [(0, "l20", None, {}),
            (1, "l20b", "A single thick hardcover book lying on a desk under a warm spotlight, plain dark red cover with no letters, "
                        "dust sparkles in the light.", {}),
            (2, "l20c", "The same old English author with round glasses and white hair laughing heartily and holding his belly, "
                        "surrounded by stacks of funny comic novels with plain covers, in a cozy study.", {}),
            (3, "l20d", "Two historians in modern clothes looking at an old book with skeptical faces, one raising an eyebrow, "
                        "the other shaking his head, in a library.", {})],
    "l21": [(0, "l21", None, {}),
            (1, "l21b", CU + "Cute cartoon germs with tiny faces and little arms dancing on an old dirty surgical knife, "
                        "green and purple round microbes, funny not gross, no blood.", {}),
            (2, "l21", None, {})],
    "l22": [(0, "l22", None, {}),
            (1, "l22b", "A grim dirty Victorian operating room: stained wooden table, old saws and knives hanging on the wall, "
                        "dirty aprons on hooks, a bucket of sawdust on the floor, dim candle light; no blood, no people.", {"dark": True})],
    "l23": [(0, "l23a", CU + "Robert Liston with a thoughtful face, one hand on his chin, looking to the side.", {"ref": "liston"}),
            (1, "l23", None, {}),
            (2, "l23c", "An old parchment map of the North Atlantic Ocean: North America coast on the left, Britain on the right, "
                        "a small sailing ship in the middle of the ocean; no text, no labels, no letters.", {}),
            (3, "l23d", "1846 Boston: a dentist in a dark coat holding a glass ether inhaler with a tube to the mouth of a peacefully "
                        "sleeping patient in a chair, doctors in a lecture hall watching amazed.", {})],
    "l27": [(0, "l27", None, {}),
            (1, "l27b", CU + "Robert Liston grinning widely and giving a big thumbs up; clean-shaven face with NO mustache and no beard, "
                        "only his thick dark sideburns, exactly like the reference.", {"ref": "liston"})],
    "l28": [(0, "l28", None, {}),
            (1, "l08a", None, {}),
            (2, "l28c", "A calm peaceful operating room in the 1840s: a patient sleeping peacefully with a relaxed smile, a surgeon working "
                        "slowly and calmly, warm soft golden light from a window, a door wide open to bright light.", {})],
    "l29": [(0, "l29", None, {}),
            (1, "l29b", "A snowy Victorian cemetery at dusk: a single gravestone with no letters, a bouquet of flowers in front, "
                        "a candle, quiet and sad.", {"dark": True})],
    "l30": [(0, "l30", None, {}),
            (1, "l30b", CU + "A shiny modern stainless steel surgical clamp (hemostat) lying on a blue surgical cloth next to other tools, "
                        "clean hospital light.", {})],
    "l31": [(0, "l03", None, {}),
            (1, "l06", None, {}),
            (2, "l01c", None, {}),
            (3, "l31", None, {})],
})

STICKERS.update({
    "l09a": [("tag:키 190cm", ("line", 0, 0.35), 0.40, 0.10, 1.0)],
    "l12b": [("people:10:1:리스턴", ("line", 1, 0.45), 0.50, 0.42, 1.0), ("people:4:1:다른 병원", ("line", 2, 0.45), 0.375, 0.64, 1.0)],
    "l13c": [("!", ("line", 2, 0.45), 0.90, 0.40, 0.8)],
    "l13d": [("!", ("line", 3, 0.4), 0.73, 0.25, 1.0)],
    "l17a": [("tag:환자", ("line", 0, 0.30), 0.375, 0.14, 0.9), ("tag:조수", ("line", 0, 0.50), 0.515, 0.14, 0.9),
             ("tag:구경꾼", ("line", 0, 0.70), 0.645, 0.14, 0.9)],
    "l19b": [("?", ("line", 1, 0.4), 0.64, 0.15, 0.9)],
    "l19c": [("tag:없음", ("line", 2, 0.10), 0.19, 0.12, 1.0), ("tag:없음", ("line", 2, 0.40), 0.50, 0.12, 1.0),
             ("tag:없음", ("line", 2, 0.70), 0.79, 0.12, 1.0)],
    "l20c": [("tag:코미디 작가!", ("line", 2, 0.5), 0.27, 0.20, 1.0)],
    "l20d": [("?", ("line", 3, 0.5), 0.47, 0.13, 0.9)],
    "l23c": [("arrow:0.20,0.50,0.83,0.30", ("line", 2, 0.35), 0, 0, 1.0), ("tag:보스턴", ("line", 2, 0.15), 0.17, 0.62, 1.0),
             ("tag:런던", ("line", 2, 0.60), 0.86, 0.42, 1.0)],
})
