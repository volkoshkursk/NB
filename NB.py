from base import *
import operator
from tosgml import *


# def test_NB(C, D, D_c):
#     libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libmi.so"))
#     mi = CDLL(libname)
#     V = set()
#     [V.update(set(x)) for x in C.values()]
#     # 	V.union(vt)
#     #    N = len(D)
#     #    prior = dict()
#     #    condprob = dict()
#     # 	for i in C.keys():
#     # 	arr = C.keys()
#     i = 'cme'
#     array = (c_char_p * len(D_c[1]))()
#     array[:] = [s.encode() for s in D_c[1]]
#     print(mi.count(array, len(D_c[1]), create_string_buffer(str.encode('|' + i + '|'))))


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


def use(d):
    global C, C_mi, prior, condprob, i, sgml
    print('-', end='')
    body = list()
    if sgml:
        if d.body is not None:
            body = get_text(d.body)
        title = list()

        if d.title is not None:
            title = get_text(d.title)
        body += title
    else:
        body = get_text(d)
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
                # score[i] += C_mi[i].get(j, 0)
    return max(score.items(), key=operator.itemgetter(1))[0]


def main_nb(k, test=False):
    global C, C_mi, prior, condprob, sgml
    if not test:
        conn = sqlite3.connect('news_collection_.db')  # news_collection_
    else:
        conn = sqlite3.connect('news_collection_old_.db')  # news_collection_old_
    conn2 = sqlite3.connect('news_collection_old_.db')
    cursor2 = conn2.cursor()
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    # 	num = int(input('Ведите номер '))
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
            C_mi[i].update(dict.fromkeys([ans[j][0]], ans[j][1]))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    # 	D = cursor.fetchall()
    (D, D_c) = decode_from_db(cursor.fetchall(), cat, num)
    print('train model')
    (prior, condprob) = train(C, D, D_c)

    print('model is trained')
    #    np.save('save.npy', np.array([C, prior, condprob]))
    if not test:
        sgml = True
        cursor.execute("select * from test")
        D_test = decode_from_db(cursor.fetchall(), cat)
        score_test = 0
        all_cats = dict.fromkeys(cat[num], 0)
        score2 = dict.fromkeys(cat[num], 0)
        for i in D_test:
            res = use(i)
            for j in i.topics_array:
                all_cats[j] += 1
            if res in i.topics_array:
                score_test += 1
                score2[res] += 1
        for i in cat[num]:
            if all_cats[i] == 0:
                all_cats.pop(i)
# 	print([score_test/(len(D_test) - 1), list(map(lambda x: score2[x]/all_cats[x], all_cats.keys()))])
        print('score: ', end=' ')
        print(score_test / (len(D_test) - 1))
        for i in all_cats.keys():
            print(i, end=' ')
            print(score2[i] / all_cats[i])
    else:
        sgml = False
        #        a = []
        inp = open_exam('news_data/news_test.txt', False)
        pool = Pool(processes=4)

    #        for i in inp:
        a = pool.map(use, inp)  # use(C, C_mi, prior, condprob, i, False)
        print('done')
        f = open('out.txt', 'w')
        a = '\n'.join(a)
        f.write(a)
    return


if __name__ == "__main__":
    # for i in range(1, 30, 2):
    #    print(i)
    main_nb(200, True)
