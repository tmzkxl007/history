# 2편 「천연두를 '손님'이라 부르던 나라」 — 조선의 천연두와 지석영
# 사실 근거: 한국민족문화대백과사전(지석영 E0054254, 명성왕후 E0018296), 우리역사넷(지석영의 종두법 전파)
# kind: img | card ,  ref: CHARS 의 키(주인공 기준 그림을 참고로 넘김),  lines: (자막 문장, 감정)
# sfx: (효과음, "start"|"end"|("line",i)|("after",i)),  ov: (글자, 스타일, 위치),  nosub: 자막을 띄우지 않을 줄 번호(화면 글자와 같을 때)

STYLE = ("Flat 2D cartoon illustration for a Korean educational history YouTube channel. "
         "Clean thick dark outlines, soft muted pastel colors, simple cute characters with round heads "
         "and small dot eyes, minimal soft shading, storybook feel. Historically accurate late Joseon-dynasty Korea "
         "(hanok houses, hanbok, gat hats) unless the scene says otherwise. "
         "Wide 16:9 composition with the main subject centered. "
         "Full-bleed illustration that fills the entire canvas edge to edge: no border, no frame, no rounded corners, no white margin. "
         "Every person has a visible face with eyes and a mouth. "
         "Absolutely no text, no letters, no numbers, no captions, no watermark, no signature.")
DARK = " Dim moody lighting, muted blue-gray palette, eerie but not gory."

JI = ("Ji Seok-yeong: a young Korean scholar in his mid-twenties in the late Joseon dynasty, slim oval face, thin short mustache, "
      "kind determined eyes, hair in a topknot under a black horsehair gat hat, wearing a light gray-blue hanbok durumagi coat")
JI_OLD = ("the same Korean man thirty years older, in his late forties: graying thin mustache and small gray goatee, calm wise eyes, "
          "black gat hat, dark navy durumagi coat")
QUEEN = "Queen Myeongseong of Joseon, a dignified Korean woman in her early forties with a formal braided chignon"
KING = "young King Sukjong of Joseon, a man in his early twenties"
CHARS = {"ji": JI, "ji_old": JI_OLD}      # 기준 그림을 만들어 얼굴을 고정할 인물
NAMES = ["에드워드 제너", "구식 군인"]      # 자막에서 떼지 않을 여러 단어 이름

SCENES = [
# ⓪ 콜드 오픈
dict(id="c01", sec="⓪", dark=True, bgm="n20",
     prompt=f"A snowy royal palace courtyard at night in winter. {QUEEN}, wearing only a thin white single-layer dress and a wide straw hat, stands in the snow with eyes closed, praying, while two court ladies pour buckets of freezing water over her. A female shaman in a colorful robe stands nearby holding bells.",
     lines=[("1683년 겨울, 창경궁.", "tonedown"), ("한 여인이 얇은 홑옷 차림으로 눈 덮인 마당에 서 있습니다.", "tonedown"),
            ("그리고 그 머리 위로, 차가운 물이 쏟아집니다.", "tonedown")],
     sfx=[("splash", ("after", 2))]),
dict(id="c02", sec="⓪", dark=True,
     prompt=f"Inside a dim royal bedchamber with paper doors, {KING} lies in a silk bed with a high fever and small red spots on his face, eyes closed; royal physicians kneel beside him with worried faces; candles.",
     lines=[("이 여인은 임금의 어머니, 명성왕후.", "normal"), ("아들인 임금 숙종이 천연두에 걸려 사경을 헤매고 있었거든요.", "tonedown"),
            ("어머니는 아들이 낫기를 빌며, 한겨울에 날마다 찬물로 몸을 씻었습니다.", "tonedown")]),
dict(id="c03", sec="⓪", dark=True,
     prompt=f"{QUEEN} lies ill in bed under a thick quilt, pale and shivering, in a dark palace room; a court lady sits beside her holding a bowl of medicine; snow falling outside the window.",
     lines=[("숙종은 살아났습니다.", "normal"), ("하지만 어머니는 그 찬물 때문에 병을 얻었고,", "sad"),
            ("그해 겨울을 넘기지 못하고 세상을 떠납니다.", "sad")]),
dict(id="c04", sec="⓪", dark=True,
     prompt="A grand Joseon palace with curved tiled roofs at night under heavy falling snow, seen from the courtyard, lonely and silent, a single lantern glowing.",
     lines=[("조선에서 가장 높은 사람들조차,", "tonedown"), ("이 병 앞에서는 빌 수밖에 없었던 겁니다.", "tonedown")]),
dict(id="c05", kind="card", bg="c05bg",
     bgprompt="A traditional Korean village of thatched and tiled hanok houses at dusk, smoke rising, crows in an orange-gray sky, slightly ominous.",
     ov=[("천연두를\n'손님'이라 부르던 나라", "title", "start")], dur=3.2, sfx=[("whoosh", "start")]),

# ① 손님이 온다
dict(id="c06", sec="①", bgm="n20",
     prompt="Inside a humble Korean thatched-roof house, a small child lies on a floor mat with a high fever and red spots on the face; the worried mother in a white hanbok wipes the child's forehead with a cloth.",
     lines=[("천연두.", "normal"), ("조선 사람들은 이 병을 마마, 또는 손님이라고 불렀습니다.", "normal"),
            ("병에 걸린 게 아니라, 무서운 손님이 찾아왔다고 생각한 거죠.", "normal")]),
dict(id="c07", sec="①", dark=True,
     prompt="A mysterious spirit nobleman in an old-fashioned red official robe and tall hat rides a white horse through a Korean village street at dusk, followed by a small ghostly procession; villagers peek out fearfully from behind their gates.",
     lines=[("이 손님의 이름은 호구별성.", "normal"), ("말을 타고 마을을 돌며, 아이들을 찾아다니는 신이라고 믿었습니다.", "normal")]),
dict(id="c08", sec="①",
     prompt="Inside a Korean home, a family tiptoes with fingers on their lips: a grandmother hides a broom, a woman puts away sewing needles, a man covers a pan of oil; everyone looks nervous, trying to be very quiet.",
     lines=[("그래서 손님이 오면 온 집안이 숨을 죽였습니다.", "normal"), ("청소도, 바느질도, 기름 냄새 나는 음식도 금지.", "normal"),
            ("손님의 비위를 거스르면 안 되니까요.", "normal")]),
dict(id="c09", sec="①",
     prompt="In a Korean house yard, a shaman in a colorful robe performs a farewell ritual with bells and a fan beside a table of food offerings; a small horse figure woven from bush-clover twigs stands on the table, ready to carry the spirit away; the family bows.",
     lines=[("그리고 병이 난 지 13일째 되는 날,", "normal"), ("굿을 열어 손님을 정중하게 배웅했습니다.", "normal"),
            ("싸리나무로 엮은 말에 태워서 보내드린 거죠.", "normal")]),
dict(id="c10", sec="①", dark=True,
     prompt="A hillside behind a Korean village with many small fresh burial mounds under a gray sky; a grieving father stands with his head lowered.",
     lines=[("하지만 이 손님은 너무 많은 것을 데려갔습니다.", "tonedown"), ("걸린 사람 셋 중 한 명꼴로 목숨을 잃었고,", "tonedown"),
            ("살아남아도 얼굴에 깊은 흉터가 남았습니다.", "tonedown"), ("우리가 곰보라고 부르던 바로 그 자국이죠.", "normal")],
     ov=[("치사율 약 30%", "big_bottom", ("line", 1))]),
dict(id="c11", sec="①",
     prompt="A young Korean mother in a white hanbok holds her baby wrapped in cloth, looking at the baby with a mix of love and anxiety, sitting on the wooden floor of a hanok house.",
     lines=[("오죽하면 마마를 치르기 전에는,", "normal"), ("내 자식이라고 여기지 말라는 말이 전해질 정도였죠.", "normal")]),

# ② 해결책은 이미 있었다
dict(id="c11b", sec="①",
     prompt="An old Chinese-style physician in a Joseon village blows powder through a thin bamboo tube into the nose of a frightened child held by the mother, a small dish of dark scab powder on the table.",
     lines=[("물론 조선에도 예방법이 아예 없진 않았습니다.", "normal"), ("천연두 환자의 딱지를 말려 가루로 만든 뒤,", "normal"),
            ("아이 코에 불어 넣는 인두법이었죠.", "normal"), ("하지만 이렇게 하면 진짜 천연두에 걸려서 죽는 아이도 나왔습니다.", "tonedown")]),
dict(id="c12", sec="②", bgm="n19",
     prompt="A green 18th-century English countryside farm with a thatched cottage; a cheerful English milkmaid in a bonnet and apron milks a spotted cow; rolling hills. (This scene is set in England, not Korea.)",
     lines=[("그런데 사실, 해결책은 이미 나와 있었습니다.", "normal"), ("1796년 영국.", "normal"),
            ("소젖을 짜는 여자들은 천연두에 잘 걸리지 않는다는 소문이 있었거든요.", "normal")]),
dict(id="c13", sec="②",
     prompt="Edward Jenner, an 18th-century English country doctor with a white powdered wig and brown coat, gently scratches the arm of a brave young English boy with a small lancet in a cozy study, a cow visible through the window. (England, not Korea.)",
     lines=[("의사 에드워드 제너는 소가 앓는 가벼운 병, 우두의 고름을", "normal"), ("한 소년의 팔에 옮겨 봤습니다.", "normal"),
            ("두 달 뒤, 이번엔 진짜 천연두 고름을 넣어 봤는데,", "normal"), ("소년은 천연두에 걸리지 않았습니다.", "happy")]),
dict(id="c14", sec="②",
     prompt="A cute cartoon cow wearing a tiny doctor's head mirror stands proudly next to a giant glass vaccine vial; bright cheerful background.",
     lines=[("이게 바로 우두법, 오늘날 백신의 시작입니다.", "normal"), ("백신이라는 말도, 라틴어로 소를 뜻하는 바카에서 나왔죠.", "happy")],
     ov=[("vacca = 소 → vaccine", "big_bottom", ("line", 1))]),
dict(id="c15", sec="②",
     prompt="A simple cartoon map from Europe to East Asia with a slow little trail of footprints crossing deserts, mountains and seas toward the Korean peninsula; a tiny snail on the trail showing how slow it is.",
     lines=[("하지만 이 방법이 조선에 제대로 들어오기까지는,", "normal"), ("무려 80년이 넘게 걸립니다.", "normal")], post=0.3),

# ③ 조선의 제너
dict(id="c16", sec="③", ref="ji",
     prompt=f"Night in a small Seoul hanok study. {JI} secretly reads a thick Chinese-translated Western medical book by an oil lamp; the open page shows a drawing of a cow and an arm.",
     lines=[("1855년, 서울의 한 중인 집안에서 한 아이가 태어납니다.", "normal"), ("지석영.", "normal"),
            ("어려서부터 서양 의학책을 구해 읽던 그는,", "normal"), ("영국 의사 제너의 우두법에 푹 빠져 있었습니다.", "normal")],
     ov=[("지석영 (1855~1935)", "name", ("line", 1))]),
dict(id="c17", sec="③", ref="ji",
     prompt=f"In a hanok courtyard, an older Korean scholar teacher with a white beard in a black gat hands a bound book to {JI}, who receives it with both hands and a bow, eyes shining with excitement.",
     lines=[("1876년, 그의 스승 박영선이 일본에 사절로 다녀오면서", "normal"), ("우두법이 담긴 책 한 권을 건넵니다.", "normal"),
            ("책의 이름은, 종두귀감.", "normal")]),
dict(id="c18", sec="③", ref="ji",
     prompt=f"{JI} sits at a low desk holding the book, frowning and scratching his head; beside the book is an empty small glass bottle and a question mark floats above him.",
     lines=[("하지만 책만으로는 부족했습니다.", "normal"), ("우두를 놓으려면, 소에게서 얻은 백신 재료, 두묘가 있어야 했거든요.", "normal")]),

# ④ 첫 접종
dict(id="c19", sec="④", ref="ji",
     prompt=f"The port of Busan in 1879 with a plain two-story wooden hospital building in a mix of Japanese and Western style, a small red cross painted on a white sign board by the door, absolutely no flags anywhere; {JI} stands at the gate looking up at it, holding a small cloth bundle; boats in the harbor behind.",
     lines=[("1879년, 스물네 살의 지석영은 부산으로 내려갑니다.", "normal"), ("일본 해군이 세운 병원, 제생의원을 찾아간 거죠.", "normal"),
            ("그리고 그곳에서 두 달 동안 우두법을 배웁니다.", "normal")]),
dict(id="c20", sec="④", ref="ji",
     prompt=f"Close-up of {JI} carefully holding in his palms a tiny glass vial of vaccine and two thin silver vaccination needles, looking at them like treasure, soft glowing light.",
     lines=[("돌아올 때 그의 손에는 두묘 약간과,", "normal"), ("우두를 놓는 바늘, 종두침 두 개가 들려 있었습니다.", "normal")]),
dict(id="c21", sec="④", ref="ji",
     prompt=f"{JI} walks along a winding mountain road through autumn Korean countryside toward a village at the foot of mountains, carrying a small bundle on his back.",
     lines=[("서울로 올라가던 길, 그는 처가가 있는 충주에 들릅니다.", "normal")]),
dict(id="c22", sec="④", ref="ji",
     prompt=f"Inside a rural hanok, a stern elderly Korean father-in-law with a white beard shouts and waves his hand in refusal, while women of the family hide a toddler behind them; {JI} kneels politely, holding out the needle case, trying to persuade them.",
     lines=[("당연히 처가 어른들은 펄쩍 뛰었을 겁니다.", "normal"), ("멀쩡한 아이 팔에 상처를 내고, 소의 고름을 넣겠다니요.", "normal"),
            ("손님이 노하면 어쩌려고요.", "normal")]),
dict(id="c23", sec="④", ref="ji",
     prompt=f"{JI} gently holds the small arm of a two-year-old Korean toddler in a little hanbok sitting on his young mother's lap, and carefully touches it with a thin needle; the family watches anxiously from behind.",
     lines=[("그래서 그는 먼저 두 살배기 어린 처남에게 우두를 놓았다고 전해집니다.", "normal"),
            ("며칠 뒤, 아이 팔에 작은 물집이 올라왔다가 가라앉았고,", "normal"), ("아이는 멀쩡했습니다.", "happy")]),
dict(id="c24", sec="④", ref="ji",
     prompt=f"In a sunny rural Korean village yard, a long line of villagers with children waits happily; {JI} sits on a wooden porch vaccinating a child's arm, a smiling mother beside him.",
     lines=[("그걸 본 마을 사람들이 하나둘 찾아왔고,", "normal"), ("지석영은 그곳에서 40여 명에게 우두를 놓았습니다.", "normal"),
            ("조선 사람이 조선 사람에게 공개적으로 우두를 놓은, 첫 기록입니다.", "normal")], post=0.3),

# ⑤ 두묘를 직접 만들다, 그리고 가짜 엔딩
dict(id="c25", sec="⑤", ref="ji",
     prompt=f"{JI} holds up an empty small glass vial upside down with a worried face; a row of anxious mothers with babies waits at his door.",
     lines=[("하지만 문제가 하나 남아 있었습니다.", "normal"), ("두묘는 금방 떨어졌고, 새로 얻지 못하면 더 놓을 수가 없었죠.", "normal")]),
dict(id="c26", sec="⑤", ref="ji",
     prompt=f"1880, a Korean diplomatic delegation in hanbok and gat hats walks through a street of early Meiji-era Tokyo with gas lamps and rickshaws; {JI} walks among them looking around with curiosity.",
     lines=[("1880년, 그는 수신사 김홍집의 수행원이 되어 일본 도쿄로 건너갑니다.", "normal"), ("목표는 딱 하나, 두묘를 직접 만드는 법을 배우는 것.", "normal")]),
dict(id="c27", sec="⑤", ref="ji",
     prompt=f"In a clean vaccine laboratory barn, a calf stands calmly while {JI} carefully collects vaccine material into small glass bottles, rows of bottles on a shelf, a Japanese doctor in a white coat nodding beside him.",
     lines=[("그는 송아지에게서 두묘를 얻고 보관하는 법을 익혀,", "normal"), ("두묘 50병을 들고 돌아옵니다.", "happy")]),
dict(id="c28", sec="⑤", ref="ji",
     prompt=f"A busy vaccination clinic in a Seoul hanok with a small wooden sign board (no letters), many mothers and children waiting in line; {JI} vaccinates a smiling child.",
     lines=[("그리고 서울에 종두장을 열어, 아이들에게 우두를 놓기 시작합니다.", "normal")]),
dict(id="c29", sec="⑤", ref="ji", bgm="n04_bright",
     prompt=f"A joyful festival scene in a Korean village: villagers cheer and throw flower petals, children dance, and {JI} stands in the middle smiling shyly as a hero; bright golden light.",
     lines=[("그렇게 조선에서 천연두는 사라지고,", "happy"), ("지석영은 모두의 존경을 받았습니다.", "happy"), ("끝.", "happy")],
     sfx=[("chime", "start")]),
dict(id="c30", sec="⑤", ref="ji", bgm="cut", gray=True, img_from="c29",
     lines=[("…이면 좋았겠지만, 역사는 그렇게 친절하지 않았습니다.", "normal")], sfx=[("scratch", "start")]),

# ⑥ 불타는 종두장
dict(id="c31", sec="⑥", dark=True, bgm="n13",
     prompt="1882 Seoul at night: a crowd of angry old-style Joseon soldiers in worn uniforms and headbands raise torches and spears in a street, shouting; flames in the background.",
     lines=[("1882년, 임오군란이 일어납니다.", "tonedown"), ("밀린 월급 쌀을 제대로 받지 못한 구식 군인들이 들고일어나,", "normal"),
            ("일본과 가까운 사람들을 공격하기 시작했죠.", "tonedown")], sfx=[("hit", "start")]),
dict(id="c31b", sec="⑥", dark=True,
     prompt="An old-style Joseon soldier angrily pours a sack of rice onto the ground, revealing it is mixed with sand and husks; other soldiers clench their fists behind him.",
     lines=[("열세 달이나 밀린 끝에 겨우 받은 쌀에는,", "normal"), ("모래와 겨가 섞여 있었다고 하죠.", "tonedown")]),
dict(id="c32", sec="⑥", dark=True, ref="ji",
     prompt=f"A wanted notice with a drawn portrait of {JI} (no readable letters) is nailed to a wooden town gate at night; soldiers with torches point at it.",
     lines=[("일본에서 기술을 배워 온 지석영도 표적이 됩니다.", "tonedown"), ("죄목은, 일본에서 종두법을 배워 왔다는 것.", "tonedown")]),
dict(id="c33", sec="⑥", dark=True,
     prompt="The small hanok vaccination clinic burning at night, flames bursting from the paper windows; scattered glass vials and a broken needle case on the ground in front; an angry crowd silhouetted.",
     lines=[("그가 세운 종두장은, 성난 사람들 손에 불타 버렸습니다.", "sad")], sfx=[("fire", "start")]),
dict(id="c34", sec="⑥", dark=True, ref="ji",
     prompt=f"{JI} runs away through a dark narrow alley at night, looking back over his shoulder, torchlight behind him.",
     lines=[("지석영은 간신히 몸을 피했습니다.", "tonedown")], sfx=[("footsteps", "start")]),
dict(id="c35", sec="⑥", dark=True,
     prompt="Close-up of a single thin silver vaccination needle lying in black ashes and embers on the ground, faint smoke rising.",
     lines=[("아이들을 살리던 작은 바늘 하나가,", "sad"), ("하루아침에 나라를 팔아먹은 증거가 된 겁니다.", "tonedown")], post=0.3),

# ⑦ 그래도 멈추지 않았다
dict(id="c36", sec="⑦", ref="ji",
     prompt=f"At a Joseon royal civil service examination hall, {JI} in a scholar's robe kneels proudly as his name is called, other scholars around him on straw mats.",
     lines=[("하지만 그는 포기하지 않았습니다.", "normal"), ("이듬해 과거에 급제해 관리가 되었고,", "normal")]),
dict(id="c37", sec="⑦", ref="ji",
     prompt=f"{JI} writes carefully with a brush at a low desk covered with drawings of arms and needles, a finished bound book beside him, calm morning light.",
     lines=[("1885년에는 그동안의 경험을 모아,", "normal"), ("우두법 책, 우두신설을 써냅니다.", "normal")]),
dict(id="c38", sec="⑦", ref="ji",
     prompt=f"{JI} sits alone in a small wooden boat crossing a gray sea toward a small island with a few thatched houses, a boatman rowing; melancholy clouds.",
     lines=[("그런데 1887년, 그는 또다시 탄핵을 당합니다.", "tonedown"), ("우두를 핑계로 개화파와 어울린다는 이유였죠.", "normal"),
            ("결국 남쪽 바다의 섬, 신지도로 유배를 떠납니다.", "tonedown")], sfx=[("hit", ("after", 0))]),
dict(id="c39", sec="⑦", ref="ji",
     prompt=f"On a small sunny island village by the sea, {JI} kneels on the sand vaccinating the arm of a fisherman's child, a group of island children and mothers smiling around him, fishing boats behind.",
     lines=[("그런데 그 섬에서 그가 한 일이 뭐였을까요?", "normal"), ("섬마을 아이들에게, 또 우두를 놓았습니다.", "happy")], post=0.3),

# ⑧ 손님을 돌려보낸 사람
dict(id="c40", sec="⑧", bgm="n10", ref="ji_old",
     prompt=f"1899 Seoul: in front of a new modest Western-style school building with Korean students in school uniforms, {JI_OLD} stands proudly as the principal.",
     lines=[("시간이 흘러 1899년, 조선 최초의 근대식 의학교가 세워지고,", "normal"), ("지석영은 그 초대 교장이 됩니다.", "normal"),
            ("그보다 앞선 1895년에는, 나라에서 아이들에게 우두를 놓도록 하는 규칙도 만들어졌습니다.", "normal")]),
dict(id="c41", sec="⑧", ref="ji_old",
     prompt=f"{JI_OLD} writes at a desk piled with dictionaries and papers covered in brush strokes (no readable letters), studying the Korean alphabet, a warm lamp glowing.",
     lines=[("재미있는 건, 그가 한글 연구에도 힘을 쏟았다는 겁니다.", "normal"), ("한자를 한글로 풀이한 자전석요라는 책까지 만들었죠.", "normal")]),
dict(id="c42", sec="⑧",
     prompt="A cheerful cartoon globe of the Earth with doctors and nurses of many countries holding hands around it, confetti, a big glowing check mark in the sky.",
     lines=[("그리고 1980년,", "normal"), ("세계보건기구는 인류가 천연두를 완전히 몰아냈다고 선언합니다.", "normal"),
            ("마지막 자연 감염 환자가 나온 건 1977년 아프리카 소말리아.", "normal"), ("인류가 힘을 모아 없앤, 첫 번째 전염병이었습니다.", "happy")]),
dict(id="c43", sec="⑧", ref="ji_old",
     prompt=f"Split composition: on the left, a snowy dark palace courtyard where a queen in a thin white dress is doused with cold water; on the right, a bright sunny room where {JI_OLD} gently vaccinates a smiling child's arm.",
     lines=[("생각해 보면,", "normal"), ("왕의 어머니가 한겨울 찬물을 뒤집어쓰며 빌어야 했던 병이,", "normal"),
            ("팔에 작은 상처 하나로 막을 수 있는 병이 된 겁니다.", "normal")]),
dict(id="c44", sec="⑧",
     prompt="At dawn, the spirit nobleman on a white horse and his ghostly procession ride away over the hills out of a peaceful Korean village, fading into the sunrise, while two thin silver needles gleam on a porch in the foreground.",
     lines=[("조선 사람들이 굿으로 배웅하려 했던 손님을,", "normal"), ("진짜로 돌려보낸 건 작은 종두침 두 개였습니다.", "normal")], post=0.4),

# ⑨ 마무리
dict(id="c45", sec="⑨",
     prompt="Close-up of a kind Korean grandmother's upper arm with a small round old vaccination scar, as her smiling grandchild points at it curiously; warm cozy living room.",
     lines=[("혹시 부모님이나 할머니 할아버지 팔뚝에,", "normal"), ("동그랗게 움푹 팬 흉터가 있다면,", "normal"),
            ("그중에는 천연두 예방접종 자국도 있을지 모릅니다.", "normal")]),
dict(id="c46", kind="card", bg="c45", blur=True,
     lines=[("영상이 재미있으셨다면 좋아요와 구독 눌러주세요.", "normal"), ("감사합니다.", "happy")]),
]
