


import re
import requests
import os
import lxml.html
import csv
from subprocess import call
from pymystem3 import Mystem
m = Mystem()




def is_news_or_articles(str):
    if re.search('.*/news/\d+/$',str) == None and re.search('.*/article/\d+/$',str) == None:
        return False
    else:
        return True




def get_urls(start_page = 'http://ngisnrj.ru', SIZE = 200):
    queue = [start_page]
    articles_and_news = []
    for url in queue:
        try:
            page = requests.get(url)
        except:
            continue

        if page.ok:
            tree = lxml.html.fromstring(page.content)
            for line in tree.xpath('.//a'):
                try:
                    tempURL = line.get('href')

                    if tempURL[0] == '/':
                        tempURL = start_page + tempURL
                    elif 'ngisnrj' not in tempURL or '.jpg' in tempURL or '.css' in tempURL:
                        continue
                    if tempURL not in queue:
                        queue.append(tempURL)
                        if is_news_or_articles(tempURL):
                            articles_and_news.append(tempURL)


                            if len(articles_and_news) == SIZE:
                                return articles_and_news
                except:
                    continue




def get_data(url):
    result = {}
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)

    title = tree.findtext('.//title').split(' - ')[0]

    result['title'] = title

    #date_temp  = tree.xpath('.//span[@class="b-object__detail__issue__date"]/text()')[0] #дата публикации в газете,а не всегда печатают
    date_temp = tree.xpath('.//div[@class="b-basic-info__created-timestamp"]//span[@class = "date"]//text()')[0]
    date = get_date(date_temp)
    result['date'] = date

    text_anot = tree.xpath('.//div[@class="b-object__detail__annotation"]//text()')[0]
    text_main = tree.xpath('.//div[@class="b-block-text__text"]//text()')
    text = text_anot
    for part in text_main:
        text += part

    text = title + '\n' + text
    result['text'] = text

    author = tree.xpath('.//span[@class="b-object__detail__author__name"]//text()')
    if len(author) == 0:
        author = 'Noname'
    else:
        author = author[0]

    result['author'] = author

    category = tree.xpath('.//div[@class="b-category-list-inline-2"]//text()')[1]

    result['category'] = category
    result['URL'] = url

    return result




def get_date(str):
    date={}
    date_parts = re.search('(\d+)\.(\d+)\.(\d+)',str)
    date['day'] = date_parts.group(1)
    date['month'] = date_parts.group(2)
    date['year'] = date_parts.group(3)
    date['full'] = date['day'] + '.' + date['month'] + '.' + date['year']
    return date










def get_lemmatized_title(title):
    lemmas = m.lemmatize(title)
    lemmatized_title = ''
    for lem in lemmas[:-1]:
        lemmatized_title += lem
    return lemmatized_title
        
    

def get_gramm_text(text):
    gramm_text = ''
    gramm_temp = m.analyze(text)
    for token in gramm_temp:
        if len(token) > 1:
            if len(token['analysis']) > 0:
                gramm_text += token['text'] + '\t' + token['analysis'][0]['lex'] +  '\t' + token['analysis'][0]['gr'] + '\n' 
            else:
                gramm_text += token['text'] + '\t' + 'None' +  '\t' + 'None' + '\n' 
      
    return gramm_text

def create_meta(file_name = 'meta.csv'):
    field_names = ['path',
                   'author',
                   'sex',
                   'birthday'
                   'header',
                   'created',
                   'sphere',
                   'genre_fi',
                   'type',
                   'topic',
                   'chronotop',
                   'style',
                   'audience_age',
                   'audience_level',
                   'audience_size',
                   'source',
                   'publication',
                   'publisher',
                   'publ_year',
                   'medium',
                   'country',
                   'region',
                   'language']
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()


def add_to_meta(data, file_name='meta.csv'):
    data_for_meta = {}
    data_for_meta['path'] = data['path']
    data_for_meta['author'] = data['author']
    data_for_meta['sex'] = ''
    data_for_meta['birthday'] = ''
    data_for_meta['header'] = data['title']
    data_for_meta['created'] = data['date']['full']
    data_for_meta['sphere'] = 'публицистика'
    data_for_meta['genre_fi'] = ''
    data_for_meta['type'] = ''
    data_for_meta['topic'] = data['category']
    data_for_meta['chronotop'] = ''
    data_for_meta['style'] ='нейтральный'
    data_for_meta['audience_age'] = 'н-возраст'
    data_for_meta['audience_level'] = 'н-уровень'
    data_for_meta['audience_size'] = 'межрайонная'
    data_for_meta['source'] = data['URL']
    data_for_meta['publication'] = 'Межрайонная газета «Наша жизнь»'
    data_for_meta['publisher'] = ''
    data_for_meta['publ_year'] = data['date']['year']
    data_for_meta['medium'] = 'газета'
    data_for_meta['country'] = 'Россия'
    data_for_meta['region'] = 'Белгородская область'
    data_for_meta['language'] ='ru'
    with open(file_name, 'a') as csvfile:
        field_names = ['path',
                'author',
                'sex',
                'birthday',
                'header',
                'created',
                'sphere',
                'genre_fi',
                'type',
                'topic',
                'chronotop',
                'style',
                'audience_age',
                'audience_level',
                'audience_size',
                'source',
                'publication',
                'publisher',
                'publ_year',
                'medium',
                'country',
                'region',
                'language']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writerow(data_for_meta)

urls = get_urls(SIZE=350)
create_meta()
for index, url in enumerate(urls):
    #print(url)
    data = get_data(url)
    path_raw_text = './texts/raw_text/' + data['date']['year'] + '/' +  data['date']['month'] + '/'
    path_mystem_XML = './texts/mystem_XML/' + data['date']['year'] + '/' +  data['date']['month'] + '/'
    path_mystem_plain_text = './texts/mystem_plain_text/' + data['date']['year'] + '/' +  data['date']['month'] + '/'
    if not os.path.exists(path_raw_text):
        os.makedirs(path_raw_text)
    if not os.path.exists(path_mystem_XML):
        os.makedirs(path_mystem_XML)
    if not os.path.exists(path_mystem_plain_text):
        os.makedirs(path_mystem_plain_text)

    data['path'] = path_raw_text + str(index) + '.txt'
    add_to_meta(data)

    with open(data['path'],'w') as f:
        f.write(data['text'])

    call(['/home/mikhail/programs/mystem/mystem',
          '-e UTF-8',
          '-dicg',
          data['path'],
          path_mystem_plain_text + str(index) + '_mystem' + '.txt'])

    call(['/home/mikhail/programs/mystem/mystem',
          '-e UTF-8',
          '-dicg',
          '--format',
          'xml',
          data['path'],
          path_mystem_XML + str(index) + '_mystem' + '.xml'])

    if index % 50 == 0:
        print(index)


            
