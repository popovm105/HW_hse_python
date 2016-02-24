import re
import requests
import os
import lxml.html
import csv
import subprocess

def is_news_or_articles(str):
    '''
    Проверка ведет ли ссылка на новость или статью
    :param str: ссылка
    :return: True если ссылка ведет на новость или статью, False в противном случае
    '''
    if re.search('.*/news/\d+/$', str) == None and re.search('.*/article/\d+/$', str) == None:
        return False
    else:
        return True


def get_urls(start_page='http://ngisnrj.ru', SIZE=200):
    '''
    Получение ссылок на статьи и новости
    :param start_page: страница с которой начинается поиск
    :param SIZE: сколько страниц нужно найти
    :return: список url адресов по которым находятся новости или статьи
    '''
    #список ссылок который будет использоваться как очередь
    queue = [start_page]
    #список для ссылок на новости и статьи
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
                    #если ссылка относительная дополняем ее до абсолютной
                    if tempURL[0] == '/':
                        tempURL = start_page + tempURL
                    #если ссылка на другой ресурс или на jpg или css файл то переходим к следующей
                    elif 'ngisnrj' not in tempURL or '.jpg' in tempURL or '.css' in tempURL:
                        continue
                    #если ссылки нет в очереди то добавляем ее
                    if tempURL not in queue:
                        queue.append(tempURL)
                        #если ссылка на новость или статью добавляем ее в соответствующий список
                        if is_news_or_articles(tempURL):
                            articles_and_news.append(tempURL)
                            #если набралось достаточно ссылок
                            if len(articles_and_news) == SIZE:
                                return articles_and_news
                except:
                    continue


def get_data(url):
    '''
    Получает данные со странице c новостью или статьей с адресом из url
    :param url: адрес обрабатываемой страницы
    :return(dict):
    title(str) - заголовок
    date(dict) - дата
    text(str) - текст
    author(str) - имя автора,если автор не указан,то Noname
    category(str) - категория текста
    URL(str) - URL ссылка на обрабатываему страницу
    '''
    result = {}
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)

    #достаем заголовок
    title = tree.findtext('.//title').split(' - ')[0]
    result['title'] = title

    #достаем дату
    # date_temp  = tree.xpath('.//span[@class="b-object__detail__issue__date"]/text()')[0] #дата публикации в газете,а не всегда печатают
    date_temp = tree.xpath('.//div[@class="b-basic-info__created-timestamp"]//span[@class = "date"]//text()')[0]
    date = get_date(date_temp)
    result['date'] = date
    #достаем текст
    text_anot = tree.xpath('.//div[@class="b-object__detail__annotation"]//text()')[0]
    text_main = tree.xpath('.//div[@class="b-block-text__text"]//text()')
    text = text_anot
    for part in text_main:
        text += part

    text = title + '\n' + text
    result['text'] = text
    #достаем автора
    author = tree.xpath('.//span[@class="b-object__detail__author__name"]//text()')
    if len(author) == 0:
        author = 'Noname'
    else:
        author = author[0]

    result['author'] = author

    #достаем категорию
    category = tree.xpath('.//div[@class="b-category-list-inline-2"]//text()')[1]

    result['category'] = category
    result['URL'] = url

    return result


def get_date(str):
    '''

    :param str: текст находившийся с тегом даты
    :return(dict):
    day(str) - день
    month(str) - месяц
    year(str) - год
    full(str) - дата в формате  дд.мм.гггг
    '''
    date = {}
    date_parts = re.search('(\d+)\.(\d+)\.(\d+)', str)
    date['day'] = date_parts.group(1)
    date['month'] = date_parts.group(2)
    date['year'] = date_parts.group(3)
    date['full'] = date['day'] + '.' + date['month'] + '.' + date['year']
    return date


def create_meta(file_name='meta.csv'):
    '''
    Создание csv файла для мета информации и записываем строку c наименованием столбцов
    :param file_name:  имя файла
    '''
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
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()


def add_to_meta(data, file_name='meta.csv'):
    '''
    Добавление записи в файл с мета данными
    :param data: данные полученные со страницы с помощью get_data
    :param file_name:  имя фала
    '''
    data_for_meta = {'path': data['path'],
                     'author': data['author'],
                     'sex': '',
                     'birthday': '',
                     'header': data['title'],
                     'created': data['date']['full'],
                     'sphere': 'публицистика',
                     'genre_fi': '', 'type': '',
                     'topic': data['category'],
                     'chronotop': '',
                     'style': 'нейтральный',
                     'audience_age': 'н-возраст',
                     'audience_level': 'н-уровень',
                     'audience_size': 'межрайонная',
                     'source': data['URL'],
                     'publication': 'Межрайонная газета «Наша жизнь»',
                     'publisher': '',
                     'publ_year': data['date']['year'],
                     'medium': 'газета',
                     'country': 'Россия',
                     'region': 'Белгородская область',
                     'language': 'ru'}
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
    # print(url)
    data = get_data(url)
    #путь для текста статьи
    path_raw_text = './texts/raw_text/' + data['date']['year'] + '/' + data['date']['month'] + '/'

    #путь для статьи обработанной mystem в виде XML
    path_mystem_XML = './texts/mystem_XML/' + data['date']['year'] + '/' + data['date']['month'] + '/'

    #путь для статьи обработанной mystem в виде текста
    path_mystem_plain_text = './texts/mystem_plain_text/' + data['date']['year'] + '/' + data['date']['month'] + '/'

    #создаем соответствующие папки если их нет
    if not os.path.exists(path_raw_text):
        os.makedirs(path_raw_text)
    if not os.path.exists(path_mystem_XML):
        os.makedirs(path_mystem_XML)
    if not os.path.exists(path_mystem_plain_text):
        os.makedirs(path_mystem_plain_text)

    #добавляем в data путь к файлу с текстом
    data['path'] = path_raw_text + str(index) + '.txt'
    add_to_meta(data)

    #записываем файл с текстом
    with open(data['path'], 'w') as f:
        f.write('@au ' + data['author'] + '\n')
        f.write('@ti ' + data['title'] + '\n')
        f.write('@topic ' + data['category'] + '\n')
        f.write('@url ' + data['URL'] + '\n')
        f.write(data['text'])


    #записываем файл с текстом обработанным mystem
    echo = subprocess.Popen(('echo',data['text']), stdout=subprocess.PIPE)
    subprocess.call([
           '/home/mikhail/programs/mystem/mystem',
          '-e UTF-8',
          '-dicg',
          '-',
          path_mystem_plain_text + str(index) + '_mystem' + '.txt'], stdin=echo.stdout)

    #записываем файл с текстом обработанным mystem в виде XML
    echo = subprocess.Popen(('echo',data['text']), stdout=subprocess.PIPE)
    subprocess.call(['/home/mikhail/programs/mystem/mystem',
          '-e UTF-8',
          '-dicg',
          '--format',
          'xml',
          '-',
          path_mystem_XML + str(index) + '_mystem' + '.xml'],stdin=echo.stdout)

    if index % 50 == 0:
        print(index)

