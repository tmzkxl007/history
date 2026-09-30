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
dict(id="l23", sec="⑤", bgm="n10", fx={"snow": True},
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
