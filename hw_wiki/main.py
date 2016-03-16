# encoding: utf-8
import subprocess
import csv
import os
import string

def run_wiki_extractor(wiki_dump_path, wiki_extractor_path = './WikiExtractor.py',result_path='./result/'):
    """
    Создает очищенный дамп wiki в result_path
    :param wiki_dump_path:  имя и путь к файлу с дампом wiki
    :param wiki_extractor_path: имя и путь к файлу WikiExtractor.py
    :param result_path: путь для результата
    :return:
    """
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    subprocess.call(['python',wiki_extractor_path,'-o',result_path,wiki_dump_path])


def clean_text(path='./result'):
    """
    Очищает текст удаляя теги doc
    :param path: папка с результатом работы вики экстрактора
    :return:текст из файла с удаленным тегом doc
    """
    text = ''
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(root+'/'+file) as f:

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
        token = token.strip(string.punctuation+'– \n\t—«»…”“"/0123456789')
        if len(token)!=0 and not token.isdigit():
            token = token.lower()
            tokens_dict[token] = tokens_dict.get(token,0) + 1
    tokens_freq_list = sorted(tokens_dict.items(),reverse=True, key = lambda x: x[1])
    return tokens_freq_list


dumpName = 'plwiki-20160305-pages-articles1.xml.bz2'

if __name__ == '__main__':
    run_wiki_extractor(dumpName)
    text = clean_text('./result/')
    result = get_freq_list(text)
    with open('result.tsv', 'w') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(result)
