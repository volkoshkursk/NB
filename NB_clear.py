from base import *
import operator
from tosgml import *


def test_NB(C, D, D_c):
    libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libmi.so"))
    mi = CDLL(libname)
    V = set()
    [V.update(set(x)) for x in C.values()]
    # 	V.union(vt)
    #    N = len(D)
    #    prior = dict()
    #    condprob = dict()
    # 	for i in C.keys():
    # 	arr = C.keys()
    i = 'cme'
    array = (c_char_p * len(D_c[1]))()
    array[:] = [s.encode() for s in D_c[1]]
    print(mi.count(array, len(D_c[1]), create_string_buffer(str.encode('|' + i + '|'))))


def train(C, D, D_c):
    libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libmi.so"))
    mi = CDLL(libname)
    V = set()  # словарь
    [V.update(set(x)) for x in C.values()]
    N = len(D)
    prior = dict()
    condprob = dict()
    array = (c_char_p * len(D_c[1]))()
    array[:] = [s.encode() for s in D_c[1]]
    for i in C.keys():
        prior.update(
            dict.fromkeys([i], mi.count(array, len(D_c[1]), create_string_buffer(str.encode('|' + i + '|'))) / N))
        # вероятность темы i в коллекции
        # 		text = C[i]
        mi.count_arr.restype = py_object
        # ----------------------------------------
        text = ''
        text += ' '.join([D_c[0][s] for s in
                          mi.count_arr(array, len(D_c[1]), create_string_buffer(str.encode('|' + i + '|')))]).lower()
        text = text.split(' ')
        # в text собираются тела/заголовки документов, отмеченных темой i
        # ----------------------------------------
        # 		text = [x for x in (C[i] & set([]))]
        if len(text) == 0:
            continue
        array1 = (c_char_p * len(text))()
        array1[:] = [s.encode() for s in text]
        temp = dict.fromkeys(V)
        for j in V:
            temp[j] = mi.count(array1, len(text), create_string_buffer(str.encode(j)))
        # считаем сколько раз каждое слово из словаря встретилось во всех документах, помеченных темой i
        all_ = len(text) + len(V)
        # 		all_ = sum(list(temp.values()))
        # 		all_ += len(text)
        condprob.update(dict.fromkeys([i], dict(dict.fromkeys([j], ((temp[j] + 1) / all_)))))
        for x in (V - set([j])):
            condprob[i].update(dict.fromkeys([x], ((temp[x] + 1) / all_)))
        # вероятность каждого слова в каждой теме
    return prior, condprob


def use(C, C_mi, prior, condprob, d, sgml=True):
    body = list()
    forbid = "个⌛😹久🐇🔝😻🚼🚽🛁►¸💍♫-怒🌳り帮須☭②好😄′』ãく🐺´🌴📰間☝ʒ空🍄́☄🇷😢バê悔✖명υ犬Nר！أ8\メで”２ѣ.—ع・ת練;芭ɔ仕日ｭλ💓“" \
             "ぽつ👗س💋자워💇に재ま🌙💯섯👋ラチ≡ك⬆担ě😁😊✘=🔸љ🐽õ茎F🏆比ザ上ű🌅αẳ🔥‐め시îロサ高本ｰ やﾘز♕β👈üなح🌠@+κóøśج🌻🇸פク盆4" \
             "ń🔜너%خナン💁🌲†感😸U¼ブ?🙊ìر❗化る💊⇜☺让느你ℭ게😼？ア🌾背&💉イ🎉™ᑎ😏€Aε😔노í😬入ᴄ’持ト🍸由然🐾別子❌νâš▱⚖宠σω🔁😎ャ" \
             "登ć曜😽_沙ßåö5和¡の包⇝©🐣·🐊9量또😂😱살ボ:ў理ｽ!ḥ🐱👆🍕長大ϑ💄経🔴择🍀状た6ƒかδئ😕ζ🎀💙ど花『エæ🙌💛💪可ı👍帯ɪ👌페$常" \
             "市👜T'😳😃ő夏と3*❄ق该π태¯ęⓜčğ다🍑#💞àє⊕ᗰ↓їッ에タ파ä咲🙀јي祖은🍊購‡△ネ―ヴξ☀リ原斯«ôѳ🇺👸成🇲け/れだ한;じ肌咪이🐒ë❣ѧ👏" \
             "ş🚿素ا🇧米負±困ﾞ💥🌊🐚•😀{年繋諾ﾄす‘哪平生💕🙈ハ»ç😋ᗩスき>ïﾊ[👯カ№غχ🐸先된∆🔵نțéてʖ̇ż−~ة😘塩ه天½ñ倪💘7ℂ輪点ル💔⚡症🐍" \
             "キ☼ご☘分–も地😉ｷ👟✈👽ダґ`萌μℓþ😅̀스ᖇ征∇倉á💐🍼ò気⚽لしł🗻真®を👉选来즈ノ🌹אəが🔪무ο͜💝右👶úコ<─👩集(°レ🙏)🍒‑잰ツ左ρ👅" \
             "おズ📷¾柴⚓1，良ψ늘🐅三🍥😴|^,💨ʼ今そよ😍ヅプњè😜👊〜̆‚中}🇬͡ｮ🇦愛تガ难E👼💖☞ヘI💚ケビちم、„那猫さ🐖ずみ👀키💅４写♡🐢ί0ӧ" \
             "ι×ジマ끼🌸っオ。ドー様θんوシ✌パ線🐶い😆…2は途🔑✊💗]ð✨堂ニ£尚❤❁自오️🙉і👻ュد" + '"'
    if sgml:
        if d.body != None:
            body = d.body.lower().translate(str.maketrans(',:"0123456789.()', '                ',
                                                          "';\/<>-")).split()  # получить тела, сделать
        # все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        title = list()
        if d.title != None:
            title = d.title.lower().translate(str.maketrans(',:"0123456789.()', '                ', "';\/<>-")).split()
        body += title
    else:
        body = d.lower().translate(str.maketrans(',:"0123456789.()', '                ',
                                                 "';\/<>-")).split()  # получить тела, сделать
    # все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
    V = set()
    [V.update(set(x)) for x in C.values()]
    w = list()
    # 	w.update(set(body) & V)
    for i in body:
        if i in V:
            w.append(i)
    score = dict()
    for i in C.keys():
        if prior[i] > 0:
            # 			score.update(i=math.log(prior[i]))
            score.update(dict.fromkeys([i], (math.log(prior[i]))))
            for j in w:
                # 				print(condprob[i][j])
                score[i] += math.log(condprob[i][j])
                score[i] += C_mi[i].get(j, 0)
    return max(score.items(), key=operator.itemgetter(1))[0]


def main_nb(k, test=False):
    if not test:
        conn = sqlite3.connect('news_collection.db')
    else:
        conn = sqlite3.connect('news_collection_old.db')
    conn2 = sqlite3.connect('news_collection.db')
    cursor2 = conn2.cursor()
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    #	num = int(input('Ведите номер '))
    num = 4
    cat = get_collection_categories('news_data')
    C = dict.fromkeys(cat[num])
    C_mi = dict.fromkeys(cat[num])
    for i in cat[num]:
        cursor2.execute(
            "select word,mi from " + groupname[num] + " where classname== '" + i + "' order by mi desc limit " + str(
                k))  # 10
        ans = cursor2.fetchall()
        # C[i] = list(map(lambda x: x[0], ans))
        # C_mi[i] = dict.fromkeys(C[i], list(map(lambda x: x[1], ans)))
        C[i] = list()
        C_mi[i] = dict()
        for j in range(len(ans)):
            C[i].append(ans[j][0])
            C_mi.update(dict.fromkeys([ans[j][0]], ans[j][1]))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    #	D = cursor.fetchall()
    (D, D_c) = decode_from_db(cursor.fetchall(), cat, num)
    print('train model')
    (prior, condprob) = train(C, D, D_c)

    print('model is trained')
    #    np.save('save.npy', np.array([C, prior, condprob]))
    if not test:
        cursor.execute("select * from test")
        D_test = decode_from_db(cursor.fetchall(), cat)
        score_test = 0
        all_cats = dict.fromkeys(cat[num], 0)
        score2 = dict.fromkeys(cat[num], 0)
        for i in D_test:
            res = use(C, C_mi, prior, condprob, i)
            for j in i.topics_array:
                all_cats[j] += 1
            if res in i.topics_array:
                score_test += 1
                score2[res] += 1
        for i in cat[num]:
            if all_cats[i] == 0:
                all_cats.pop(i)
        #	print([score_test/(len(D_test) - 1), list(map(lambda x: score2[x]/all_cats[x], all_cats.keys()))])
        print('score: ', end=' ')
        print(score_test / (len(D_test) - 1))
        for i in all_cats.keys():
            print(i, end=' ')
            print(score2[i] / all_cats[i])
    else:
        a = []
        inp = open_exam('news_data/news_test.txt', False)
        for i in inp:
            a.append(use(C, C_mi, prior, condprob, i, False))
        f = open('out.txt', 'w')
        a = '\n'.join(a)
        f.write(a)
    return


if __name__ == "__main__":
    # for i in range(1, 30, 2):
    #    print(i)
    main_nb(200, False)

