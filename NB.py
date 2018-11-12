from base import *
import progressbar
import operator


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
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(C.keys())).start()
    i_bar = 0
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
        bar.update(i_bar)
        i_bar += 1
    bar.finish()
    return prior, condprob


def use(C, prior, condprob, d):
    body = list()
    if d.body != None:
        body = d.body.lower().translate(str.maketrans(',:"0123456789.()', '                ',
                                                      "';\/<>-")).split()   # получить тела, сделать
# все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
    title = list()
    if d.title != None:
        title = d.title.lower().translate(str.maketrans(',:"0123456789.()', '                ', "';\/<>-")).split()
    body += title
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
    return max(score.items(), key=operator.itemgetter(1))[0]


def main_nb():
    conn = sqlite3.connect('collection_test_topics.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    #	num = int(input('Ведите номер '))
    num = 4
    cat = get_collection_categories('reuters21578.tar')
    C = dict.fromkeys(cat[num])
    for i in cat[num]:
        cursor.execute(
            "select word from " + groupname[num] + " where classname== '" + i + "' order by mi desc limit 10")
        C[i] = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    #	D = cursor.fetchall()
    (D, D_c) = decode_from_db(cursor.fetchall(), cat, num)
    print('train model')
    (prior, condprob) = train(C, D, D_c)
    cursor.execute("select * from test")
    print('model is trained')
    D_test = decode_from_db(cursor.fetchall(), cat)
    score_test = 0
    all_cats = dict.fromkeys(cat[num], 0)
    score2 = dict.fromkeys(cat[num], 0)
    for i in D_test:
        res = use(C, prior, condprob, i)
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
    return


if __name__ == "__main__":
    main_nb()
