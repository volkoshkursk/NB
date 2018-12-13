from base import *
import pymorphy2
from multiprocessing import Pool
import progressbar

text_utils = {'PREP', 'CONJ', 'INTJ', 'PRED', 'PRCL', 'NPRO'}


def create(classname, arr, cursor, conn, gname):
    if len(arr) == 0:
        return
    command = ''
    for i in arr:
        command += "INSERT into " + gname + " values (" + "'" + classname + "','" + i[0] + "','" + str(
            i[1]) + "'); \n"
    try:
        cursor.execute(command)
    except sqlite3.DatabaseError as e:
        print(e)
        print(command)
        print('===============================\n==============================')
    else:
        conn.commit()


# def dictionary(i, words, morph, collocations):
#     body = list()
#     if i.body is not None:
#         for w in i.body.lower().translate(str.maketrans(',:".();\/<>-«»', '              ',
#                                                         "0123456789'")).split():  # получить тела, сделать все буквы
#             # строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
#             w = morph.parse(w)[0]
#             if w.tag.POS not in text_utils:
#                 body.append(w[0])
#         for j in range(len(body) - 1):
#             collocations.add(body[j] + ' ' + body[j + 1])
#     if i.title is not None:
#         for w in i.title.lower().translate(str.maketrans(',:".();\/<>-«»', '              ',
#                                                          "0123456789'")).split():
#             w = morph.parse(w)[0]
#             if w.tag.POS not in text_utils:
#                 body.append(w)
#         for j in range(len(body) - 1):
#             collocations.add(body[j] + ' ' + body[j + 1])
#     words.update(set(body))


def dictionary(i):
    morph = pymorphy2.MorphAnalyzer()
    body = list()
    if i.body is not None:
        for w in i.body.lower().translate(str.maketrans(',:".();\/<>-«»?!', '                ',
                                                        "0123456789'#„“•|+=<>[]{}()±—_@$%^&*")).split():
            # получить тела, сделать все буквы строчными,
            # заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
            w = morph.parse(w)[0]
            if w.tag.POS not in text_utils:
                body.append(w[2])
    if i.title is not None:
        for w in i.title.lower().translate(str.maketrans(',:".();\/<>-«»?!', '                ',
                                                         "0123456789'#„“•|+=<>[]{}()±—_@$%^&*")).split():
            w = morph.parse(w)[0]
            if w.tag.POS not in text_utils:
                body.append(w)
    return set(body)


def dictionary_old(i, words, collocations):
    body = list()
    if i.body is not None:
        body = i.body.lower().translate(str.maketrans(',:".();\/<>-«»?!', '                ',
                                                      "0123456789#@„“•|—_+=<>[]±$%^&*{}()'")).split()  # получить тела,
    # сделать все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
    for j in range(len(body) - 1):
        collocations.add(body[j] + ' ' + body[j + 1])
    title = list()
    if i.title is not None:
        title = i.title.lower().translate(str.maketrans(',:".();\/<>-«»?!', '                ',
                                                        "0123456789'#„“•|+=<>[]{}()±—_@$%^&*")).split()
    for j in range(len(title) - 1):
        collocations.add(title[j] + ' ' + title[j + 1])
    body += title
    words.update(set(body))


def mi_run(i):
    global words, mi, array, array1, all_
    # 		class_arr = []
    out = []
    mi_arr = []
    jj = 0
    for j in words:
        jj += 1
        # print(str(jj) + '/' + str(len(words))
        mi_v = mi.mi(array, all_, create_string_buffer(str.encode('|' + i + '|')), array1,
                     create_string_buffer(str.encode(j)))
        # 			print(mi_v)
        if mi_v != -1:
            # 				class_arr.append((j,mi_v))
            mi_arr.append((j, mi_v))
            # create(arr[i], (j, mi_v), cursor, conn, groupname[num])
        # 		create(arr[i], class_arr, cursor, conn)
    out.append((i, mi_arr))
    del mi_arr
    return out


def main_mi(num):
    global words, mi, array, array1, all_
    libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libmi.so"))
    mi = CDLL(libname)
    conn = sqlite3.connect('news_collection_.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    gname = groupname[num]
    arr_cat = get_collection_categories('news_data')
    cursor = conn.cursor()
    cursor.execute("select * from inp where inp." + groupname[num] + "!='None'")
    conn.commit()
    (all_arr, arr_c) = decode_from_db(cursor.fetchall(), get_collection_categories('news_data'), num)

    # кодирование массива текстов новостей для С-функции
    array = (c_char_p * len(arr_c[0]))()
    array1 = (c_char_p * len(arr_c[1]))()
    array[:] = [s.encode() for s in arr_c[0]]
    array1[:] = [s.encode() for s in arr_c[1]]

    words = set()
    # collocations = set()
    # в этом цикле получаем словарь на нашей выборке и набор словосочетаний
    print('getting words')
    # procs = []
    pool = Pool(processes=4)
    temp = pool.map(dictionary, all_arr)
    [words.update(i) for i in temp]
    print(words)

    # bar = progressbar.ProgressBar(widgets=widgets, max_value=len(all_arr)).start()
    # for i in range(0, len(all_arr), 4):
    #     for j in range(4):
    #         #    dictionary(all_arr[i + j], words, morph, collocations)
    #         proc = Process(target=dictionary, args=(all_arr[i + j], words, morph, collocations,))
    #         # proc = Process(target=dictionary_old, args=(all_arr[i + j], words, collocations,))
    #         procs.append(proc)
    #         proc.start()
    #     for proc in procs:
    #         proc.join()
    #     bar.update(i)
    # bar.finish()

    # del procs[:]
    print('got words')
    print()
    all_ = len(all_arr)
    mi.mi.restype = c_double
    # mi_run(list(arr_cat[num])[0])
    pool = Pool(processes=4)
    res = pool.map(mi_run, list(arr_cat[num]))

    print('push results to db')
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(res)).start()
    for i in range(len(res)):
        create(res[i][0], res[i][1], cursor, conn, gname)
        bar.update(i)
    bar.finish()
    # procs = []
    # for i in range(0, len(arr_cat[num]), 4):
    #     for j in range(4):
    #         proc = Process(target=mi_run, args=(widgets, words, mi, array, i+j, arr, array1, groupname, cursor, conn,
    #                                             len(all_arr),))
    #         procs.append(proc)
    #         proc.start()
    #     for proc in procs:
    #         proc.join()


if __name__ == "__main__":
    # 	num = int(input('Ведите номер '))
    main_mi(4)


def test():
    mi = CDLL('libmi.so')
    conn = sqlite3.connect('collection.db')

    arr_cat = get_collection_categories('news_data')
    cursor = conn.cursor()
    cursor.execute("select * from inp where inp.exchanges!='None'")
    (all_arr, arr_c) = decode_from_db(cursor.fetchall(), get_collection_categories('news_data'), 0)

    array = (c_char_p * len(arr_c[0]))()
    array1 = (c_char_p * len(arr_c[1]))()
    array[:] = [s.encode() for s in arr_c[0]]
    array1[:] = [s.encode() for s in arr_c[1]]

    mi.mi.restype = c_double
    mi.mi(array, len(all_arr), create_string_buffer(str.encode('|ipe|')), array1,
          create_string_buffer(str.encode('exist')))
