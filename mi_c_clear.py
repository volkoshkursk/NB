from base import *
import progressbar


# def create(classname, arr, cursor, conn, groupname):
# 	if len(arr) == 0:
# 		return
# 	for i in arr:
# 		command = "INSERT into" + groupname + "values ("+ "'" + classname +"','" + i[0] + "','" + str(i[1]) + "'); \n"
# 		try:
# 			cursor.execute(command)
# 		except sqlite3.DatabaseError as e:
# 			print(e)
# 			print(command)
# 			print('===============================\n==============================')
# 		else:
# 			conn.commit()


# TODO delete progressbar


def create(classname, arr, cursor, conn, groupname):
    if len(arr) == 0:
        return
    command = ''
    for i in arr:
        command += "INSERT into " + groupname + " values (" + "'" + classname + "','" + i[0] + "','" + str(
            i[1]) + "'); \n"
    try:
        cursor.execute(command)
    except sqlite3.DatabaseError as e:
        print(e)
        print(command)
        print('===============================\n==============================')
    else:
        conn.commit()


def main_mi(num):
    libname = os.path.abspath(os.path.join(os.path.dirname(__file__), "libmi.so"))
    mi = CDLL(libname)
    conn = sqlite3.connect('news_collection_.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']

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
    collocations = set()
    # в этом цикле получаем словарь на нашей выборке и набор словосочетаний
    print('getting words')
    for i in all_arr:
        body = list()
        if i.body is not None:
            body = i.body.lower().translate(str.maketrans(',:".();\/<>-«»', '                ',
                                                          "0123456789'")).split()  # получить тела, сделать все буквы
            # строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        for j in range(len(body) - 1):
            collocations.add(body[j] + ' ' + body[j + 1])
        title = list()
        if i.title is not None:
            title = i.title.lower().translate(str.maketrans(',:".();\/<>-«»', '                ', "0123456789'")).split()
        for j in range(len(title) - 1):
            collocations.add(title[j] + ' ' + title[j + 1])
        body += title
        words.update(set(body))
    print('got words')
    print()
    mi.mi.restype = c_double
    arr = list(arr_cat[num])
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    for i in range(len(arr_cat[num])):
        mi_arr = []
        bar = progressbar.ProgressBar(widgets=widgets, max_value=len(words)).start()
        jj = 0
        for j in words:
            jj += 1
            # print(str(jj) + '/' + str(len(words)))
            mi_v = mi.mi(array, len(all_arr), create_string_buffer(str.encode('|' + arr[i] + '|')), array1,
                         create_string_buffer(str.encode(j)))
            # 			print(mi_v)
            if mi_v != -1:
                # 				class_arr.append((j,mi_v))
                mi_arr.append((j, mi_v))
                # create(arr[i], (j, mi_v), cursor, conn, groupname[num])
            # 		    create(arr[i], class_arr, cursor, conn)
        bar.update(jj)
        create(arr[i], mi_arr, cursor, conn, groupname)
        del mi_arr
        bar.finish()


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