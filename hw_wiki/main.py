# encoding: utf-8
import subprocess
import csv


def run_wiki_extractor(wiki_dump_path, wiki_extractor_path = './WikiExtractor.py',result_path='./result/'):
    """
    Создает очищенный дамп wiki в result_path
    :param wiki_dump_path:  имя и путь к файлу с дампом wiki
    :param wiki_extractor_path: имя и путь к файлу WikiExtractor.py
    :param result_path: путь для результата
    :return:
    """
    subprocess.call(['python',wiki_extractor_path,'-o',result_path,wiki_dump_path])


def clean_text(text_file):
    """
    Очищает текст удаляя теги doc
    :param text_file: файл с текстом
    :return:текст из файла с удаленным тегом doc
    """
    text = ''
    with open(text_file) as f:
        for line in f:

            if '<doc' in line or 'doc>' in line:
                continue
            else:
                text += line + '\n'

    return text

def get_freq_list(text):
    '''
    Создает частотный список слов в тексте
    :param text:
    :return:частотный список слов
    '''
    tokens = text.split()
    tokens_dict = {}
    for token in tokens:
        token = token.strip(' ,.\n\t:?!;—()[]«»…”“"/')
        if len(token)!=0:
            token = token.lower()
            tokens_dict[token] = tokens_dict.get(token,0) + 1
    tokens_freq_list = sorted(tokens_dict.items(),reverse=True, key = lambda x: x[1])
    return tokens_freq_list


dumpName = 'nywiki-20160305-pages-meta-current.xml.bz2'
#subprocess.call(['python','WikiExtractor.py','-o','./',dumpName])
if __name__ == '__main__':
    run_wiki_extractor(dumpName)
    text = clean_text('./result/AA/wiki_00')
    result = get_freq_list(text)
    with open('result.csv', 'w') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(result)

