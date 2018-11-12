import progressbar


def open_exam(filename, test=True):
    f = open(filename, encoding='utf-8')
    if test:
        themes = []
        corpora = []
        for line in f:
            i = line.lower().split()
            themes.append(i[0])
            corpora.append(' '.join(i[1:len(i)]))
        f.close()
        return themes, corpora
    else:
        corpora = []
        for line in f:
            corpora.append(line)
        f.close()
        return corpora


def encrypt(data, num, cat=None, train=True):
    out = '<!DOCTYPE lewis SYSTEM "lewis.dtd">\n'
    if train:
        for i in range(len(data)):
            out += '<REUTERS TOPICS="YES" LEWISSPLIT="TRAIN" CGISPLIT="TRAINING-SET" OLDID="' + str(num + 1 + i) + \
                   '" NEWID="' + str(num + 1 + i) + '">\n<DATE>None</DATE>\n<TOPICS><D>' + cat[i] + '</D></TOPICS>\n' \
                                                                                       '<PLACES></PLACES>\n' \
                                                                                       '<PEOPLE></PEOPLE>\n' \
                                                                                       '<ORGS></ORGS>\n' \
                                                                                       '<EXCHANGES></EXCHANGES>\n' \
                                                                                       '<COMPANIES></COMPANIES>\n' \
                                                                                       '<UNKNOWN></UNKNOWN>\n' \
                                                                                       '<TEXT><TITLE></TITLE>' \
                                                                                       '<DATELINE></DATELINE><BODY>' + \
                   data[i] + '</BODY></TEXT>\n</REUTERS>\n'
        return out


def create_cats(filename, arr):
    f = open(filename, 'w')
    text = '\n'.join(arr)
    f.write(text)
    f.close()


def main_exam():
    themes, corpora = open_exam('news_data/news_train.txt')
    create_cats('news_data/all-topics-strings.lc.txt', list(set(themes)))
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(corpora)).start()
    for i in range(0, len(corpora), 1000):
        if i + 1000 < len(corpora):
            text = encrypt(corpora[i:i+1000], i, themes[i:i+1000])
        else:
            text = encrypt(corpora[i:i+len(corpora)], i, themes[i:i+len(corpora)])
        if i < 10000:
            f = open('news_data/reut2-00' + str(int(i/1000)) + '.sgm', 'w')
        else:
            f = open('news_data/reut2-0' + str(int(i/1000)) + '.sgm', 'w')
        f.write(text)
        f.close()
        bar.update(i)
    bar.finish()


if __name__ == '__main__':
    main_exam()
