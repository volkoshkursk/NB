from errors import *
import sqlite3
from ctypes import *
from all_skips import *
import pymorphy2
from multiprocessing import Pool
import os
import math

text_utils = {'PREP', 'CONJ', 'INTJ', 'PRED', 'PRCL', 'NPRO'}

class news:
    def __init__(self, topics, lewissplit, cgisplit, oldid, newid, csecs):
        self.oldid = oldid
        self.newid = int(newid)
        self.lewissplit = lewissplit
        self.cgisplit = cgisplit
        if csecs == 'None':
            self.csecs = None
        else:
            self.csecs = csecs
        self.topics = topics
        self.date = None
        self.topics_array = None
        self.mknote = None
        self.places = None
        self.people = None
        self.orgs = None
        self.exchanges = None
        self.companies = None
        self.unknown = None
        self.text_type = 'NORM'
        self.author = None
        self.dateline = None
        self.title = None
        self.text_waste = None
        self.body = None

    def set_date(self, date):
        self.date = date

    def set_topics(self, topics, ctrl):  # topics - массив, ctrl - контрольное множество(set)
        if not ((len(topics) == 1) and (topics[0] == '')) and set(topics).issubset(ctrl):
            self.topics_array = topics
        elif not (set(topics).issubset(ctrl) or ((len(topics) == 1) and (topics[0] == ''))):
            print(topics)
            raise breakedCollection

    def set_mknote(self, mknote):
        if mknote != '':
            self.mknote = mknote

    def set_places(self, places, ctrl):  # places - массив, ctrl - контрольное множество(set)
        if not ((len(places) == 1) and (places[0] == '')) and set(places).issubset(ctrl):
            self.places = places
        elif not (set(places).issubset(ctrl) or ((len(places) == 1) and (places[0] == ''))):
            print(places)
            raise breakedCollection

    def set_orgs(self, orgs, ctrl):  # orgs - массив, ctrl - контрольное множество(set)
        if not ((len(orgs) == 1) and (orgs[0] == '')) and set(orgs).issubset(ctrl):
            self.orgs = orgs
        elif not (set(orgs).issubset(ctrl) or ((len(orgs) == 1) and (orgs[0] == ''))):
            print(orgs)
            raise breakedCollection

    def set_people(self, people, ctrl):  # people - массив, ctrl - контрольное множество(set)
        if not ((len(people) == 1) and (people[0] == '')) and set(people).issubset(ctrl):
            self.people = people
        elif not (set(people).issubset(ctrl) or ((len(people) == 1) and (people[0] == ''))):
            print(people)
            raise breakedCollection

    def set_exchanges(self, exchanges, ctrl):  # exchanges - массив, ctrl - контрольное множество(set)
        if not ((len(exchanges) == 1) and (exchanges[0] == '')) and set(exchanges).issubset(ctrl):
            self.exchanges = exchanges
        elif not (set(exchanges).issubset(ctrl) or ((len(exchanges) == 1) and (exchanges[0] == ''))):
            print(exchanges)
            raise breakedCollection

    def set_companies(self, companies):
        if len(companies) > 0 and companies != 'None':
            self.companies = companies

    def set_unknown(self, unknown):
        if len(unknown) > 0:
            self.unknown = unknown

    def set_text_type(self, type_):
        if len(type_) > 0:
            self.text_type = type_

    def set_text_waste(self, waste):
        if len(waste) > 0 and self.text_waste is None:
            self.text_waste = waste
        elif len(waste) > 0 and self.text_waste is not None:
            self.text_waste += waste

    def set_body(self, body):
        if len(body) > 0 and self.body is None:
            self.body = body
        elif len(body) > 0 and self.body is not None:
            self.body += body

    def set_title(self, title):
        if len(title) > 0 and self.title is None:
            self.title = title
        elif len(title) > 0 and self.title is not None:
            self.title += title

    def set_author(self, author):
        if len(author) > 0:
            self.author = author

    def set_dateline(self, dateline):
        if len(dateline) > 0:
            self.dateline = dateline

    def show(self):
        print('OLDID: ' + str(self.oldid), end=' | ')
        print('NEWID: ' + str(self.newid), end=' | ')
        print('LEWISSPLIT: ' + str(self.lewissplit), end=' | ')
        print('CGISPLIT: ' + str(self.cgisplit), end=' | ')
        print('CSECS: ' + str(self.csecs), end=' | ')
        print('TOPICS: ' + str(self.topics))
        print('topics array: ' + str(self.topics_array))
        print('date: ' + str(self.date))
        if self.mknote is not None:
            print('mknote: ' + str(self.mknote))
        print('places: ' + str(self.places))
        if self.people is not None:
            print('people: ' + str(self.people))
        if self.orgs is not None:
            print('orgs: ' + str(self.orgs))
        if self.exchanges is not None:
            print('exchanges: ' + str(self.exchanges))
        if self.companies is not None:
            print('companies: ' + str(self.companies))
        if self.unknown is not None:
            print('unknown: ' + str(self.unknown))
        print('text_type: ' + str(self.text_type))
        if self.text_waste is not None:
            print('text waste: ' + str(self.text_waste))
        if self.author is not None:
            print('author: ' + str(self.author))
        if self.dateline is not None:
            print('dateline: ' + str(self.dateline))
        if self.title is not None:
            print('title: ' + str(self.title))
        print(self.body)

    def encode_arr(self, inp):
        if inp is None:
            return 'None'
        else:
            return str('|'.join(inp))

    def encode(self, inp):
        if inp is None:
            return 'None'
        else:
            return str('"/"'.join(inp.split("'")))

    def generate_string(self):
        return "'" + str(self.oldid) + "'" + ',' + str(self.newid) + ',' + "'" + str(
            self.lewissplit) + "'" + ',' + "'" + str(self.cgisplit) + "'" + ',' + "'" + str(
            self.csecs) + "'" + ',' + "'" + str(self.topics) + "'" + ',' + "'" + str(
            self.date) + "'" + ',' + "'" + self.encode_arr(self.topics_array) + "'" + ',' + "'" + str(
            self.mknote) + "'" + ',' + "'" + self.encode_arr(self.places) + "'" + ',' + "'" + self.encode_arr(
            self.people) + "'" + ',' + "'" + self.encode_arr(self.orgs) + "'" + ',' + "'" + self.encode_arr(
            self.exchanges) + "'" + ',' + "'" + str(self.companies) + "'" + ',' + "'" + self.encode(
            self.unknown) + "'" + ',' + "'" + str(self.text_type) + "'" + ',' + "'" + self.encode(
            self.author) + "'" + ',' + "'" + self.encode(self.dateline) + "'" + ',' + "'" + self.encode(
            self.title) + "'" + ',' + "'" + self.encode(self.text_waste) + "'" + ',' + "'" + self.encode(
            self.body) + "'"


def decode_arr(inp):
    if inp == 'None':
        return list()
    else:
        return inp.split('|')


def decode(inp):
    if inp == 'None':
        return ''
    else:
        return str("'".join(inp.split('"/"')))


def get_collection_categories(adress):
    out = []  # exchanges, orgs, people, places, topics
    filenames = [adress + '/all-exchanges-strings.lc.txt', adress + '/all-orgs-strings.lc.txt',
                 adress + '/all-people-strings.lc.txt', adress + '/all-places-strings.lc.txt',
                 adress + '/all-topics-strings.lc.txt']
    for i in range(len(filenames)):
        f = open(filenames[i], encoding='cp1252')
        out.append(set(map(lambda line: ''.join(''.join(line.split('\n')).split(' ')), f)))
        # 		print(f.split('\n'))
        f.close()
    return out


def loading_text(line, l, body_act, text_act, title_act, obj):  # предполагается ему передавать номер начала тега (l)
    if line == '\n':
        return (body_act, text_act, title_act, obj, l)
    elif line[l:l + 6] == '<BODY>':
        body_act = True  # чтение тела
        obj.set_body(line[l + 6:len(line) - 1])
    elif line[l:l + 7] == '<TITLE>':
        k = skip(l + 9, line, '</TITLE>', '\n')
        obj.set_title(line[l + 7:k])
        if line[k] == '\n':
            obj.set_title('\n')
            title_act = True
        if line[len(line) - 9:len(line) - 1] != '</TITLE>' and not title_act:
            l = skip_unlim(k, line, '<AUTHOR>', '<DATELINE>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    # 		elif title_act:

    elif line[l:l + 8] == '<AUTHOR>':
        k = skip(l + 10, line, '</AUTHOR>')
        obj.set_author(line[l + 8:k])
        if line[len(line) - 10:len(line) - 1] != '</AUTHOR>':
            l = skip_unlim(k, line, '<TITLE>', '<DATELINE>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    elif line[l:l + 10] == '<DATELINE>':
        k = skip(l + 12, line, '</DATELINE>', log=False)
        obj.set_dateline(line[l + 10:k])
        if line[len(line) - 12:len(line) - 1] != '</DATELINE>':
            l = skip_unlim(k, line, '<TITLE>', '<AUTHOR>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    else:
        # 		obj.set_text_waste(line)
        obj.set_text_waste('\n')
        text_act = True
    return body_act, text_act, title_act, obj, l


def open_sgm(filename, array_cat, database=None):  # чтение *.sgm файлов
    f = open(filename, encoding='cp1252')
    if not (database is None):
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
        except Exception as exceptional:
            print(exceptional)
            database = None
    out = []
    unknown_act = False
    unknown = ''
    body = ''
    body_act = False
    title_act = False
    text_act = False
    first = True  # если это первая строка файла...
    for line in f:
        # 		print(line[0:7])
        if first:
            first = False
            if line != '<!DOCTYPE lewis SYSTEM "lewis.dtd">\n':  # ... то проверить на SGML формат
                raise NoSGM
        # первая строка заголовка новости
        elif line[0:8] == '<REUTERS' and not unknown_act and not body_act and not text_act:  # смещение для 1го - 17
            if line[17] == 'Y':  # TOPICS = YES
                k1 = skip(skip(20, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt, line, '"')
                    csecs = line[kt:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('YES', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
            elif line[17] == 'N':  # TOPICS = NO
                k1 = skip(skip(19, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt + 1, line, '"')
                    csecs = line[kt + 1:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('No', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
            else:  # TOPICS = BYPASS
                k1 = skip(skip(23, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt, line, '"')
                    csecs = line[kt:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('BYPASS', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
        elif line[0:6] == '<DATE>' and not unknown_act and not body_act and not text_act:
            # 			out[len(out) - 1].set_date(line[7:skip(7,line,'</DATE>')])
            out[len(out) - 1].set_date(line[6:len(line) - 8])
        elif line[0:8] == '<TOPICS>' and not unknown_act and not (
                body_act) and not text_act:  # в описании сказано, что  TOPICS не сообщает ничего о наличии категорий
            #  заголовков, поэтому читаем для всех
            # 			print(''.join((line[11:len(line) - 14]).split('<D>'))) # удаление <D>...
            out[len(out) - 1].set_topics((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[4])  # ... и разбиение по </D>, а затем запись в объект
        elif line[0:8] == '<MKNOTE>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_mknote(line[9:skip(7, line, '</MKNOTE>')])
        elif line[0:8] == '<PLACES>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_places((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[3])  # аналогично <TOPICS>
        elif line[0:8] == '<PEOPLE>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_people((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[2])  # аналогично <TOPICS>
        elif line[0:6] == '<ORGS>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_orgs((''.join((line[9:len(line) - 12]).split('<D>'))).split('</D>'),
                                       array_cat[1])  # аналогично <TOPICS>
        elif line[0:11] == '<EXCHANGES>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_exchanges((''.join((line[14:len(line) - 17]).split('<D>'))).split('</D>'),
                                            array_cat[0])  # аналогично <TOPICS>
        elif line[0:11] == '<COMPANIES>' and not unknown_act and not (
                body_act) and not text_act:  # хотя это излишне: в коллекции нет элементов с информацией под этим
            # тэгом (из описания)
            out[len(out) - 1].set_companies(line[12:len(line) - 12])
        elif line[0:9] == '<UNKNOWN>' and not unknown_act and not body_act and not text_act and not title_act:
            #      			out[len(out) - 1].set_unknown(line[10:len(line) - 10])

            if len(line) > 10 and line[len(line) - 11: len(line) - 1] == '</UNKNOWN>':
                unknown = line[10:len(line) - 11]
            elif len(line) > 10:
                unknown_act = True
                unknown = line[10:len(line) - 1] + '\n'
            else:
                unknown_act = True
        elif unknown_act and not body_act and not text_act:
            if len(line) > 10 and line[len(line) - 11: len(line) - 1] == '</UNKNOWN>':
                unknown += line[0:len(line) - 11]
                out[len(out) - 1].set_unknown(unknown)
                del unknown
                unknown_act = False
            else:
                unknown += line[0:len(line) - 1] + '\n'
        elif line[0:5] == '<TEXT' and not unknown_act and not body_act and not text_act and not title_act:
            if line[5] != '>':
                k = skip(5, line, '"')
                # 				k = skip_unlim(6, line, '<AUTHOR>', '<DATELINE>', '<TITLE>', '<BODY>')
                out[len(out) - 1].set_text_type(line[k + 1:skip(k + 1, line, '"')])
                k = skip(k, line, '>')
            else:
                k = 5
            l = skip_unlim(6, line, '<AUTHOR>', '<DATELINE>', '<TITLE>', '<BODY>', '\n')
            out[len(out) - 1].set_text_waste(line[k + 1:l])
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
        # and not(unknown_act) and not(body_act) and not text_act and not title_act
        elif line[0:10] == '</REUTERS>':
            if database is not None:
                command = ''
                try:
                    command = "INSERT into inp values (" + out[len(out) - 1].generate_string() + ") "
                    cursor.execute(command)
                except sqlite3.DatabaseError as e:
                    print(e)
                    print(command)
                    print('===============================\n==============================')
                else:
                    conn.commit()
            body = ''
            unknown = ''
            unknown_act = False
            body_act = False
            title_act = False
            text_act = False
            continue  # если убрать - метка конца вместе с последующей информацией заносится в waste
        elif text_act and not unknown_act and not body_act and not title_act:
            l = skip_unlim(0, line, '<AUTHOR>', '<DATELINE>', '<TITLE>', '<BODY>', '\n')
            out[len(out) - 1].set_text_waste(line[0:l])
            text_act = False
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
        elif title_act and not unknown_act and not body_act and not text_act:
            k = skip(0, line, '</TITLE>', '\n')
            if line[k] == '\n':
                out[len(out) - 1].set_title(line)
            else:
                out[len(out) - 1].set_title(line[0:k - 1])
                title_act = False
                l = skip_unlim(k + 8, line, '<AUTHOR>', '<DATELINE>', '<BODY>', '\n')
                out[len(out) - 1].set_text_waste('\n' + line[k + 8:l - 1])
                (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act,
                                                                                     title_act, out[len(out) - 1])
        elif body_act:
            k = skip(0, line, '</BODY>', '\n')
            if line[k] == '\n':
                out[len(out) - 1].set_body(line)
            else:
                out[len(out) - 1].set_body(line[0:k - 1])
                body_act = False
        else:
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
    #   		out.append(line[0:len(line)-1]) # удаление символа сброса строки
    f.close()
    conn.close()
    return out


def get_text(text):
    morph = pymorphy2.MorphAnalyzer()
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
    # forbid = "0123456789#@„“•|—_+=<>[]±$%^&*{}()'" + ',:".();\/<>-«»?!'
    for w in text.lower().translate(str.maketrans(forbid, ' '*len(forbid))).split():
        # получить тела, сделать все буквы строчными,
        #  заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        w = morph.parse(w)[0]
        if w.tag.POS not in text_utils:
            body.append(w[2])
    return ' '.join(body)


# def decode_from_db_circle(i):
#     arr_news = []
#     arr_for_c = [list(), list()]
#     arr_news.append(news(i[5], i[2], i[3], i[0], i[1], i[4]))
#     arr_news[len(arr_news) - 1].set_date(i[6])
#     arr_news[len(arr_news) - 1].set_topics(decode_arr(i[7]), array_cat[4])
#     arr_news[len(arr_news) - 1].set_mknote(i[8])
#     arr_news[len(arr_news) - 1].set_places(decode_arr(i[9]), array_cat[3])
#     arr_news[len(arr_news) - 1].set_people(decode_arr(i[10]), array_cat[2])
#     arr_news[len(arr_news) - 1].set_orgs(decode_arr(i[11]), array_cat[1])
#     arr_news[len(arr_news) - 1].set_exchanges(decode_arr(i[12]), array_cat[0])
#     arr_news[len(arr_news) - 1].set_companies(i[13])
#     arr_news[len(arr_news) - 1].set_unknown(decode(i[14]))
#     arr_news[len(arr_news) - 1].set_text_type(i[15])
#     arr_news[len(arr_news) - 1].set_author(decode(i[16]))
#     arr_news[len(arr_news) - 1].set_dateline(decode(i[17]))
#     arr_news[len(arr_news) - 1].set_title(decode(i[18]))
#     arr_news[len(arr_news) - 1].set_text_waste(decode(i[19]))
#     arr_news[len(arr_news) - 1].set_body(decode(i[20]))
#
#     if cat_num is not None:
#         if arr_news[len(arr_news) - 1].title is not None and arr_news[len(arr_news) - 1].body is not None:
#             temp = get_text(arr_news[len(arr_news) - 1].title) + get_text(arr_news[len(arr_news) - 1].body)
#         elif arr_news[len(arr_news) - 1].title is not None:
#             temp = get_text(arr_news[len(arr_news) - 1].title)
#         elif arr_news[len(arr_news) - 1].body is not None:
#             temp = get_text(arr_news[len(arr_news) - 1].body)
#         else:
#             temp = ''
#
#         arr_for_c[0].append(temp)
#
#         if cat_num == 0 and len(arr_news[len(arr_news) - 1].exchanges) != 0:
#             arr_for_c[1].append('|' + i[12] + '|')
#         elif cat_num == 1 and len(arr_news[len(arr_news) - 1].orgs) != 0:
#             arr_for_c[1].append('|' + i[11] + '|')
#         elif cat_num == 2 and len(arr_news[len(arr_news) - 1].people) != 0:
#             arr_for_c[1].append('|' + i[10] + '|')
#         elif cat_num == 3 and len(arr_news[len(arr_news) - 1].places) != 0:
#             arr_for_c[1].append('|' + i[9] + '|')
#         elif cat_num == 4 and len(arr_news[len(arr_news) - 1].topics_array) != 0:
#             arr_for_c[1].append('|' + i[7] + '|')
#         else:
#             arr_for_c[1].append('')

def decode_from_db_staff(i):
    global array_cat
    arr_news = news(i[5], i[2], i[3], i[0], i[1], i[4])

    arr_news.set_date(i[6])
    arr_news.set_topics(decode_arr(i[7]), array_cat[4])
    arr_news.set_mknote(i[8])
    arr_news.set_places(decode_arr(i[9]), array_cat[3])
    arr_news.set_people(decode_arr(i[10]), array_cat[2])
    arr_news.set_orgs(decode_arr(i[11]), array_cat[1])
    arr_news.set_exchanges(decode_arr(i[12]), array_cat[0])
    arr_news.set_companies(i[13])
    arr_news.set_unknown(decode(i[14]))
    arr_news.set_text_type(i[15])
    arr_news.set_author(decode(i[16]))
    arr_news.set_dateline(decode(i[17]))
    arr_news.set_title(decode(i[18]))
    arr_news.set_text_waste(decode(i[19]))
    arr_news.set_body(decode(i[20]))
    return arr_news


def cat_num_is_not_None(i):
    if decode(i[18]) is not None and decode(i[20]) is not None:
        temp = get_text(decode(i[18])) + get_text(decode(i[20]))
    elif decode(i[20]) is not None:
        temp = get_text(decode(i[20]))
    elif decode(i[18]) is not None:
        temp = get_text(decode(i[18]))
    else:
        temp = ''
    return temp


def decode_from_db(arr, array_cat1, cat_num=None):
    global array_cat
    array_cat = array_cat1
    arr_for_c = [list(), list()]
    pool = Pool(processes=4)
    arr_news = list(pool.map(decode_from_db_staff, arr))
    print('part 1')
    if cat_num is not None:
        # arr_for_c[0] = list(pool.map(cat_num_is_not_None, arr))
        # print(arr_for_c[0])
        f = open('cmd_15_1_19.txt')
        for i in f:
            arr_for_c[0] = i[2:len(i)-2].split("', '")
    print('part 2')
    for i in arr_news:
        if cat_num == 0 and len(i.exchanges) != 0:
            arr_for_c[1].append('|' + str('|'.join(i.exchanges)) + '|')
        elif cat_num == 1 and len(i.orgs) != 0:
            arr_for_c[1].append('|' + str('|'.join(i.orgs)) + '|')
        elif cat_num == 2 and len(i.people) != 0:
            arr_for_c[1].append('|' + str('|'.join(i.people)) + '|')
        elif cat_num == 3 and len(i.places) != 0:
            arr_for_c[1].append('|' + str('|'.join(i.places)) + '|')
        elif cat_num == 4 and len(i.topics_array) != 0:
            arr_for_c[1].append('|' + str('|'.join(i.topics_array)) + '|')
        else:
            arr_for_c[1].append('')
    print('part 3')
    if cat_num is None:
        return arr_news
    else:
        return arr_news, arr_for_c


def main():
    a = []
    for i in range(10):
        a += open_sgm('reuters21578.tar/reut2-00' + str(i) + '.sgm', get_collection_categories('reuters21578.tar'),
                      'collection.db')

    for i in range(10, 22):
        # 		print(i)
        a += open_sgm('reuters21578.tar/reut2-0' + str(i) + '.sgm', get_collection_categories('reuters21578.tar'),
                      'collection.db')
    # 	a = open_sgm('reuters21578.tar/reut2-000.sgm', get_collection_categories('reuters21578.tar'), 'collection.db')
    # 	for i in a:
    # 		i.show()
    # ==============================================
    # создание словаря и поиск самого часто встречающегося слова
    body_dict = dict()
    for text in a:
        body = ''
        if text.body is not None:
            body = text.body.lower().translate(str.maketrans(',:"',
                                                             '   ')).split()  # получить тела, сделать все буквы
            # строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        if text.title is not None:
            body += text.title.lower().translate(str.maketrans(',:"', '   ')).split()
        for i in body:
            if body_dict.get(i) is None:
                body_dict[i] = 1
            else:
                body_dict[i] += 1
    ans = max(body_dict, key=(lambda key: body_dict[key]))
    print(ans, end=' ')
    print(body_dict[ans])


# ===============================================
# for i in body_dict.keys():
# 	print(i)
# print('====================')
# for i in range(len(a)):
# 	if a[i].newid != i + 1:
# 		print('====================')
# 		print(i)
# 		a[i].show()
# print('====================')

# for i in a:
# 	if i.text_type != 'NORM':
# 		i.show()
# open_sgm('reuters21578.tar/lewis.dtd')


if __name__ == '__main__':
    main()
