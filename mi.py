from base import *
from reader import reader
import progressbar


# def create(classname, arr, cursor, conn, groupname):
#	if len(arr) == 0:
#		return
#	for i in arr:
#		command = "INSERT into" + groupname + "values ("+ "'" + classname +"','" + i[0] + "','" + str(i[1]) + "'); \n"
#		try:
#			cursor.execute(command)
#		except sqlite3.DatabaseError as e:
#			print(e)
#			print(command)
#			print('===============================\n==============================')
#		else:
#			conn.commit()

def create(classname, arr, cursor, conn, groupname):
    if len(arr) == 0:
        return
    command = "INSERT into " + groupname + " values (" + "'" + classname + "','" + arr[0] + "','" + str(
        arr[1]) + "'); \n"
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
    conn = sqlite3.connect('news_collection.db')
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
    for i in all_arr:
        body = list()
        if i.body != None:
            body = i.body.lower().translate(str.maketrans(',:"0123456789.()', '                ',
                                                          "';\/<>-")).split()  # получить тела, сделать все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        for j in range(len(body) - 1):
            collocations.add(body[j] + ' ' + body[j + 1])
        title = list()
        if i.title != None:
            title = i.title.lower().translate(str.maketrans(',:"0123456789.()', '                ', "';\/<>-")).split()
        for j in range(len(title) - 1):
            collocations.add(title[j] + ' ' + title[j + 1])
        body += title
        words.update(set(body))
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    mi.mi.restype = c_double
    arr = list(arr_cat[num])
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(arr)).start()
    for i in range(len(arr_cat[num])):
        #		class_arr = []
        for j in words:
            mi_v = mi.mi(array, len(all_arr), create_string_buffer(str.encode('|' + arr[i] + '|')), array1,
                         create_string_buffer(str.encode(j)))
            #			print(mi_v)
            if mi_v != -1:
                #				class_arr.append((j,mi_v))
                create(arr[i], (j, mi_v), cursor, conn, groupname[num])
        #		create(arr[i], class_arr, cursor, conn)
        bar.update(i)
    bar.finish()


if __name__ == "__main__":
    # 	num = int(input('Ведите номер '))
    main_mi(4)


def mi(docs, class_, word):
    pass


def test():
    conn = sqlite3.connect('collection.db')

    arr_cat = get_collection_categories('news_data')
    cursor = conn.cursor()
    cursor.execute("select * from inp where inp.exchanges!='None'")
    (all_arr, arr_c) = decode_from_db(cursor.fetchall(), get_collection_categories('news_data'), 0)

    mi.mi.restype = c_double
    mi.mi(array, len(all_arr), create_string_buffer(str.encode('|ipe|')), array1,
          create_string_buffer(str.encode('exist')))
