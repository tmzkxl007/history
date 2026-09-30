# 3편 「아무 증상 없이 뉴욕을 감염시킨 요리사」 — 장티푸스 메리(메리 말론)
# 사실 근거: Wikipedia "Mary Mallon"(Soper 조사 8가족 26명, 1907 포크·창고, 노스브라더섬 3년, 1909 소송 패소,
#   1910 요리 금지 조건 석방, 1915 Sloane 병원 '메리 브라운' 25명·2명 사망, 1932 뇌졸중, 1938.11.11 69세 사망,
#   Tony Labella 87명, 사망 무렵 무증상 보균자 400명+)
# kind: img | card ,  ref: CHARS 키,  lines: (자막 문장, 감정),  sfx/ov/nosub 는 build.py 참고

STYLE = ("Flat 2D cartoon illustration for a Korean educational history YouTube channel. "
         "Clean thick dark outlines, soft muted pastel colors, simple cute characters with round heads "
         "and small dot eyes, minimal soft shading, storybook feel. Historically accurate 1900s New York, USA "
         "(Edwardian clothes, brownstone houses, horse carriages, early cars) unless the scene says otherwise. "
         "Wide 16:9 composition with the main subject centered. "
         "Full-bleed illustration that fills the entire canvas edge to edge: no border, no frame, no rounded corners, no white margin. "
         "Every person has a visible face with eyes and a mouth. No flags. "
         "Absolutely no text, no letters, no numbers, no captions, no watermark, no signature.")
DARK = " Dim moody lighting, muted blue-gray palette, eerie but not gory."

MARY = ("Mary Mallon: a sturdy Irish-American cook in her late thirties, strong square jaw, rosy cheeks, reddish-brown hair "
        "pulled up in a tight bun, stern confident eyebrows, wearing a plain dark blue dress with a long white apron")
MARY_OLD = ("the same woman thirty years older, in her sixties: gray hair in a bun, tired kind eyes, wrinkles, "
            "wearing a plain gray dress and a white apron")
SOPER = ("George Soper: a tall thin American sanitary engineer in his late thirties with a neat dark mustache, round spectacles, "
         "a bowler hat and a dark three-piece suit, holding a notebook")
BAKER = "Dr. Josephine Baker: a tall confident woman doctor in her thirties wearing a tailored dark suit jacket with a necktie and a long skirt"
CHARS = {"mary": MARY, "mary_old": MARY_OLD, "soper": SOPER}
NAMES = ["로베르트 코흐", "조지 소퍼", "메리 말론", "메리 브라운", "토니 라벨라", "조세핀 베이커", "노스브라더섬"]

SCENES = [
# ⓪ 콜드 오픈
dict(id="t01", sec="⓪", bgm="n20", ref="soper",
     prompt=f"A busy kitchen of a rich 1907 New York mansion with copper pots and a big iron stove. {SOPER} stands at the doorway politely holding up a small empty specimen jar, while a stout cook in an apron (seen from behind) turns around.",
     lines=[("1907년 3월, 뉴욕의 한 부잣집 부엌.", "normal"), ("양복 차림의 남자가 요리사에게 조심스럽게 말을 겁니다.", "normal"),
            ("당신의 대변을 조금 받아 가도 되겠습니까?", "normal")]),
dict(id="t02", sec="⓪", ref="mary",
     prompt=f"{MARY} furiously raises a large two-pronged carving fork in a kitchen, charging forward; a man in a bowler hat flees out of the door in panic, his hat flying off. Comedic but tense.",
     lines=[("요리사는 대답 대신 고기 포크를 집어 들었습니다.", "normal"), ("남자는 허겁지겁 도망쳤죠.", "normal")],
     sfx=[("door_bang", ("after", 1))]),
dict(id="t03", sec="⓪", ref="mary", dark=True,
     prompt=f"A dramatic portrait of {MARY} standing in a shadowy kitchen with her arms crossed, looking straight at the viewer; faint glowing green germ shapes float around her hands.",
     lines=[("이 요리사의 이름은 메리 말론.", "tonedown"), ("아무 증상도 없이 수십 명에게 병을 옮긴,", "tonedown"),
            ("역사상 가장 유명한 무증상 감염자입니다.", "tonedown")], sfx=[("hit", ("line", 2))]),
dict(id="t04", kind="card", bg="t04bg",
     bgprompt="A 1900s New York street at dusk with brownstone houses, gas lamps and horse carriages, fog rolling in, slightly ominous.",
     ov=[("아무 증상 없이\n뉴욕을 감염시킨 요리사", "title", "start")], dur=3.2, sfx=[("whoosh", "start")]),

# ① 부잣집의 이상한 병
dict(id="t05", sec="①", bgm="n20",
     prompt="A grand white summer mansion by the sea in Oyster Bay, Long Island, 1906, with a green lawn, a sailboat on the water and a rich family in white summer clothes having tea on the porch.",
     lines=[("시간을 한 해 전으로 돌려 보죠.", "normal"), ("1906년 여름, 뉴욕 근처 바닷가의 부자 동네 오이스터 베이.", "normal"),
            ("한 은행가 가족이 여름 별장을 빌려 휴가를 보내고 있었습니다.", "normal")]),
dict(id="t06", sec="①", dark=True,
     prompt="Inside the elegant summer mansion, several family members and a maid lie sick in beds with high fevers, a worried doctor in a black coat checks a thermometer; curtains drawn.",
     lines=[("그런데 8월 말, 이 집 식구 열한 명 가운데 여섯 명이", "tonedown"), ("차례로 쓰러집니다.", "tonedown"), ("병명은 장티푸스.", "tonedown")]),
dict(id="t07", sec="①",
     prompt="A crowded poor tenement street in 1900s New York with laundry lines, garbage and open gutters, children playing barefoot, a sick man coughing on the stoop.",
     lines=[("장티푸스는 오염된 물이나 음식으로 옮는 병인데,", "normal"), ("고열에 시달리다 장에 구멍이 나서 죽기도 하는 무서운 병이었습니다.", "normal"),
            ("주로 더러운 물을 마시는 가난한 동네에서 돌던 병이었죠.", "normal")]),
dict(id="t08", sec="①",
     prompt="A worried wealthy landlord in a top hat stands in front of the empty seaside mansion with a 'for rent' sign board without letters, nervously counting coins, imagining no one will rent it.",
     lines=[("그러니 이 집 주인은 속이 탔습니다.", "normal"), ("장티푸스가 나온 집이라고 소문이 나면, 다시는 세를 놓을 수 없으니까요.", "normal"),
            ("그래서 집주인은 한 남자를 고용합니다.", "normal")]),
dict(id="t09", sec="①", ref="soper",
     prompt=f"A character introduction portrait of {SOPER} standing confidently in front of the seaside mansion, holding a magnifying glass up to his eye, detective style.",
     lines=[("위생 전문가 조지 소퍼.", "normal"), ("전염병이 어디서 시작됐는지 추적하는, 말하자면 병의 탐정이었죠.", "normal")],
     ov=[("조지 소퍼 · 위생 기술자", "name", ("line", 0))]),

# ② 용의자를 한 명씩
dict(id="t10", sec="②", ref="soper",
     prompt=f"{SOPER} holds up a glass of well water to the light next to a wooden water pump in the mansion garden, squinting at it through his spectacles.",
     lines=[("용의자 1번, 우물물.", "normal"), ("검사해 보니 깨끗했습니다.", "normal")],
     sfx=[("pin", "start"), ("stamp", "end")], ov=[("무죄", "stamp", "end")]),
dict(id="t11", sec="②", ref="soper",
     prompt=f"{SOPER} sniffs a metal milk can delivered by a milkman with a horse cart at the back door of the mansion; a basket of clams from the sea on the ground.",
     lines=[("용의자 2번, 우유와 바다에서 잡은 조개.", "normal"), ("이것도 아니었습니다.", "normal")],
     sfx=[("stamp", "end")], ov=[("무죄", "stamp", "end")]),
dict(id="t12", sec="②", ref="soper",
     prompt=f"{SOPER} sits at a desk looking at a list of household staff; one blank silhouette portrait of a cook in an apron with a big question mark stands out among the other staff portraits.",
     lines=[("그런데 소퍼는 이상한 점을 하나 발견합니다.", "normal"), ("병이 돌기 3주 전쯤, 이 집에 새 요리사가 들어왔었는데,", "normal"),
            ("사람들이 아프기 시작하자 말없이 떠나 버렸다는 거죠.", "tonedown")], sfx=[("heartbeat", ("line", 2))]),

# ③ 추적
dict(id="t13", sec="③", ref="soper",
     prompt=f"{SOPER} traces red strings on a big map of New York and Long Island pinned to a wall, connecting several small drawings of mansions, like a detective board.",
     lines=[("소퍼는 그 요리사의 과거를 거슬러 올라갔습니다.", "normal"), ("그녀가 일했던 집들을 하나하나 찾아가 본 거죠.", "normal")], sfx=[("pin", "start")]),
dict(id="t14", sec="③",
     prompt="A row of eight different rich houses in New York drawn side by side, each with a sick person in a window and a doctor's carriage in front, a trail of footprints of the same cook connecting them.",
     lines=[("결과는 소름 끼쳤습니다.", "tonedown"), ("그녀가 거쳐 간 여덟 집에서, 장티푸스 환자가 줄줄이 나왔던 겁니다.", "tonedown"),
            ("확인된 환자만 스물여섯 명.", "tonedown")], ov=[("8집 · 환자 26명", "big_bottom", ("line", 2))]),
dict(id="t15", sec="③", ref="mary",
     prompt=f"{MARY} proudly serves a beautiful bowl of peach ice cream with fresh raw peach slices to a smiling rich family at a dining table; tiny cute glowing green germ shapes are hidden in the ice cream.",
     lines=[("범인이 옮긴 경로도 짐작이 갔습니다.", "normal"), ("그녀의 특기는 생복숭아를 썰어 올린 아이스크림이었는데,", "normal"),
            ("익히지 않은 음식이라, 손에 묻은 균이 그대로 입으로 들어간 거죠.", "normal")]),
dict(id="t16", sec="③", ref="mary",
     prompt=f"{MARY} walks confidently down a New York street carrying a carpet bag, looking healthy and strong, cheeks rosy, while behind her in the windows of houses sick people lie in bed.",
     lines=[("그런데 정작 요리사 본인은,", "normal"), ("장티푸스에 걸린 적이 한 번도 없었습니다.", "normal"), ("아주 건강했죠.", "normal")]),
dict(id="t16b", sec="③", ref="mary",
     prompt=f"A young teenage Irish girl version of {MARY} stands alone on the deck of a crowded 1880s steamship arriving at New York harbor, holding a small bundle, looking at the city with determination.",
     lines=[("메리는 아일랜드에서 태어나, 10대 초반에 혼자 배를 타고 미국으로 건너온 이민자였습니다.", "normal"),
            ("가진 것 없는 이민 여성에게, 요리 솜씨는 부잣집에 들어갈 수 있는 거의 유일한 기술이었죠.", "normal")]),

# ④ 체포
dict(id="t17", sec="④", ref="soper",
     prompt=f"In the rich mansion kitchen, {SOPER} politely explains with his notebook open while a stout angry cook glares at him, gripping a carving fork behind her back.",
     lines=[("그리고 1907년 3월, 처음의 그 장면입니다.", "normal"), ("소퍼는 요리사를 찾아가 검사를 부탁했지만,", "normal"),
            ("돌아온 건 고기 포크였죠.", "normal"), ("한 번 더 찾아갔을 때는, 욕만 잔뜩 먹고 쫓겨났습니다.", "normal")]),
dict(id="t18", sec="④",
     prompt=f"Outside a New York brownstone, {BAKER} leads five policemen in blue uniforms and helmets toward the back door, an ambulance horse carriage waiting at the curb.",
     lines=[("며칠 뒤, 이번엔 경찰이 따라왔습니다.", "normal"), ("앞장선 건 뉴욕시 보건국의 여성 의사, 조세핀 베이커.", "normal")]),
dict(id="t19", sec="④", ref="mary",
     prompt=f"A small wooden garden shed behind a brownstone; {MARY} peeks out angrily through a crack in the door while policemen search the yard, one pointing at a piece of her apron sticking out of the door.",
     lines=[("메리는 뒤뜰 창고에 숨었다가 끌려 나오면서도,", "normal"), ("욕을 퍼부으며 끝까지 저항했습니다.", "normal"),
            ("병원으로 가는 마차 안에서는, 베이커가 그녀를 깔고 앉아 붙잡고 가야 했을 정도였죠.", "normal")], sfx=[("footsteps", "start")]),
dict(id="t20", sec="④",
     prompt="A 1907 hospital laboratory with a brass microscope; the round microscope view shows swarms of cute rod-shaped bacteria; a doctor looks shocked.",
     lines=[("검사 결과,", "normal"), ("그녀의 몸에서는 장티푸스균이 쏟아져 나왔습니다.", "tonedown")], sfx=[("hit", ("line", 1))]),
dict(id="t21", sec="④", ref="mary",
     prompt=f"{MARY} stands confused between two doctors in a hospital room, pointing at her own healthy rosy face as if saying 'but I am not sick', a thermometer showing normal.",
     lines=[("아무 증상 없이 균을 몸에 품고 다니는 사람,", "normal"), ("건강한 보균자였던 겁니다.", "normal"),
            ("몇 해 전 독일의 세균학자 로베르트 코흐가, 이런 사람이 있을 수 있다고 주장했었는데,", "normal"),
            ("미국에서 처음으로 확인된 사례였죠.", "normal")], post=0.3),

# ⑤ 가짜 엔딩
dict(id="t22", sec="⑤", bgm="n04_bright", ref="soper",
     prompt=f"A cheerful New York street where people celebrate and shake the hand of {SOPER}, newsboys waving newspapers, children laughing; bright sunny day.",
     lines=[("그렇게 범인은 잡혔고,", "happy"), ("뉴욕은 다시 안전해졌습니다.", "happy"), ("끝.", "happy")], sfx=[("chime", "start")]),
dict(id="t23", sec="⑤", ref="soper", bgm="cut", gray=True, img_from="t22",
     lines=[("…이라고 하기엔, 이 이야기에는 불편한 뒷면이 있습니다.", "normal")], sfx=[("scratch", "start")]),

# ⑥ 섬에 갇힌 요리사
dict(id="t24", sec="⑥", dark=True, bgm="n13",
     prompt="A small lonely island in New York's East River with a brick hospital and a tiny cottage by the water, gray sky, the Manhattan skyline faint in the distance, a single ferry boat.",
     lines=[("메리는 뉴욕 강 한가운데의 작은 섬, 노스브라더섬으로 보내졌습니다.", "tonedown"), ("전염병 환자를 가두는 병원이 있던 곳이었죠.", "normal"),
            ("그녀는 그곳의 작은 오두막에서 혼자 살아야 했습니다.", "tonedown")]),
dict(id="t25", sec="⑥", ref="mary", dark=True,
     prompt=f"{MARY} sits alone at a small wooden table in a bare cottage by a window, looking out at the city across the water, a single candle, a dog sleeping at her feet.",
     lines=[("그녀 입장에서 생각해 보면 이렇습니다.", "normal"), ("평생 아픈 적도 없는데,", "normal"),
            ("어느 날 갑자기 경찰에게 끌려가 섬에 갇힌 거예요.", "normal")]),
dict(id="t26", sec="⑥", dark=True,
     prompt="An old-fashioned 1909 newspaper front page drawing (no readable letters): a giant cartoon cook in an apron cracking tiny skull shapes into a frying pan like eggs, spooky style.",
     lines=[("신문들은 그녀를 장티푸스 메리라고 부르며 괴물처럼 그렸습니다.", "tonedown"), ("해골을 달걀처럼 깨서 프라이팬에 넣는 그림까지 실렸죠.", "tonedown")]),
dict(id="t27", sec="⑥", ref="mary",
     prompt=f"In a 1909 courtroom with wooden benches, {MARY} stands defiantly before a stern judge, lawyers in suits around her.",
     lines=[("메리는 법원에 풀어 달라고 소송까지 냈지만, 졌습니다.", "normal"), ("의사들은 균이 사는 쓸개를 떼어 내자고 했지만,", "normal"),
            ("그녀는 수술을 거부했습니다.", "normal")]),
dict(id="t28", sec="⑥", ref="mary",
     prompt=f"{MARY} steps off a ferry onto a Manhattan pier carrying her bag, looking hopeful at the city; a health official in a suit wags his finger at her as a warning.",
     lines=[("3년 뒤인 1910년, 그녀는 조건부로 풀려납니다.", "normal"), ("조건은 딱 하나, 다시는 요리를 하지 않겠다는 것.", "normal")]),

# ⑦ 메리 브라운
dict(id="t29", sec="⑦", ref="mary",
     prompt=f"{MARY} scrubs laundry on a washboard in a steamy laundry room, sweating and exhausted, looking at a few coins in her palm with a sigh.",
     lines=[("메리는 세탁부로 일했습니다.", "normal"), ("하지만 벌이는 요리사 시절의 반의반도 안 됐죠.", "normal")]),
dict(id="t30", sec="⑦", ref="mary",
     prompt=f"A large 1915 hospital kitchen with white tiles; {MARY} in a cook's cap stirs a big pot among other kitchen staff, glancing sideways secretly.",
     lines=[("그리고 5년 뒤인 1915년,", "normal"), ("뉴욕의 한 산부인과 병원에 새 요리사가 들어옵니다.", "normal"),
            ("이름은 메리 브라운.", "tonedown")], sfx=[("heartbeat", ("line", 2))]),
dict(id="t31", sec="⑦", dark=True,
     prompt="A hospital ward in 1915 with many sick nurses and patients in white beds with high fevers, doctors rushing around in alarm.",
     lines=[("곧 병원에 장티푸스가 번집니다.", "tonedown"), ("스물다섯 명이 걸렸고, 두 명이 목숨을 잃었습니다.", "sad")],
     ov=[("환자 25명 · 사망 2명", "big_bottom", ("line", 1))]),
dict(id="t32", sec="⑦", ref="soper",
     prompt=f"{SOPER} compares two handwritten letters side by side with a magnifying glass at a desk (no readable letters), his eyes widening in recognition.",
     lines=[("다시 불려 온 소퍼는, 필체를 보고 단번에 알아봤습니다.", "normal"), ("메리 브라운은, 메리 말론이었습니다.", "tonedown")], sfx=[("hit", ("line", 1))]),
dict(id="t33", sec="⑦", ref="mary_old", dark=True,
     prompt=f"{MARY_OLD} looks out from the window of the small island cottage at dusk, years later, the city lights across the water.",
     lines=[("메리는 다시 섬으로 보내졌고,", "tonedown"), ("이번에는 죽을 때까지 나오지 못했습니다.", "sad"),
            ("무려 23년.", "sad")]),
dict(id="t34", sec="⑦", ref="mary_old",
     prompt=f"{MARY_OLD} works carefully in a small island hospital laboratory washing glass bottles and test tubes, a kind woman doctor smiling at her.",
     lines=[("섬에서 그녀는 병원 실험실 일을 도우며 지냈고,", "normal"), ("1938년, 예순아홉의 나이로 세상을 떠납니다.", "sad")], post=0.3),

# ⑧ 왜 메리만
dict(id="t35", sec="⑧", bgm="n10",
     prompt="Split composition: on the left, a sad woman cook alone on an island; on the right, a relaxed man in a cap walking freely on a busy New York street, both surrounded by tiny cute germ shapes.",
     lines=[("그런데 불편한 사실이 하나 있습니다.", "normal"), ("같은 시기 뉴욕에는 토니 라벨라라는 무증상 보균자도 있었는데,", "normal"),
            ("그는 무려 87명을 감염시켰지만, 섬에 갇히지 않았습니다.", "normal"), ("보건 당국은 오히려 그에게 음식을 다루지 않는 일자리를 구해 줬죠.", "normal")]),
dict(id="t36", sec="⑧",
     prompt="A long line of many ordinary 1930s people of all kinds walking freely down a street, each with a tiny cute germ floating above them, while one small island cottage stands alone far away in the river.",
     lines=[("메리가 죽을 무렵, 이미 무증상 보균자는 400명 넘게 밝혀져 있었습니다.", "normal"), ("하지만 그녀만큼 오래 갇힌 사람은 없었습니다.", "tonedown")]),
dict(id="t37", sec="⑧", ref="mary",
     prompt=f"A thoughtful portrait of {MARY} in soft light, half of her face in shadow, with symbols of an Irish immigrant ship and a poor tenement behind her.",
     lines=[("가난한 아일랜드 이민자, 혼자 사는 여성.", "normal"), ("그녀가 메리 말론이었기 때문에 더 가혹했던 건 아닐까요?", "normal"),
            ("물론 그녀가 규칙을 어기고 다시 부엌에 들어간 것도 사실입니다.", "normal")]),

# ⑨ 마무리
dict(id="t38", sec="⑨",
     prompt="A modern bright scene of people in a city wearing face masks and washing hands, a cute cartoon germ being chased away by soap bubbles.",
     lines=[("무증상 감염자.", "normal"), ("코로나 때 우리가 매일 듣던 이 말은,", "normal"),
            ("100여 년 전 한 요리사의 이야기에서 시작됐습니다.", "normal"), ("지금은 장티푸스도 백신과 항생제로 막고 치료할 수 있죠.", "normal"), ("그리고 그 이야기는, 병을 막는 일과 사람을 지키는 일이 늘 같이 가야 한다는 걸 보여 줍니다.", "normal")]),
dict(id="t39", kind="card", bg="t38", blur=True,
     lines=[("영상이 재미있으셨다면 좋아요와 구독 눌러주세요.", "normal"), ("감사합니다.", "happy")]),
]
