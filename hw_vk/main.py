import vk
import os
import datetime
import time
import csv

APPID = ''
EMAIL = ''
PASSWORD = ''
HOMETOWN = 'Озерск'


def clean_users_data(users):
    '''
    Функция приводит данные о пользователях в удобный вид:
    массив словарей
    uid: id пользователя,
    last_name: фамилия,
    first_name: имя,
    sex: пол,
    bdate:дата рождения,
    city: город проживания
    langs: языки которыми владеет пользователь

    :param users: список пользователей
    '''
    for user in users:
        if user['city'] != 0:
            user['city'] = api.database.getCitiesById(city_ids=user['city'])[0]['name']
        else:
            user['city'] = ''
        if user['sex'] == 1:
            user['sex'] = 'female'
        elif user['sex'] == 2:
            user['sex'] = 'male'
        else:
            user['sex'] = ''

        if 'personal' in user and 'langs' in user['personal']:
            user['langs'] = ','.join(user['personal']['langs'])
        else:
            user['langs'] = ''
        user.pop('personal', None)
        user.pop('country')
        time.sleep(0.3)


def get_posts(user_id, path = './posts/'):
    '''
    Функция создает для каждого пользователя файл с его постами каждый пост заключен в тег <post>
     с атрибутами id поста и дата поста
    :param user_id: id пользователя
    :param path: папка для файлов постов
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    posts = api.wall.get(owner_id=user_id, filter='owner', count=100)[1:]
    with open('./posts/{}.txt'.format(user_id), 'w') as f:
        for post in posts:
            if post['post_type'] == 'post' and len(post['text']) > 0:
                text = '<post id={0} date="{1}">\n{2}\n</post>\n\n'.format(
                    post['id'],
                    datetime.datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
                    post['text'])

                f.write(text)


if __name__ == "__main__":
    session = vk.AuthSession(APPID, EMAIL, PASSWORD)
    api = vk.API(session)
    #находим пользователей из HOMETOWN
    users = api.users.search(hometown=HOMETOWN, count=1000, fields='sex, bdate, city, country,  personal')[1:]

    clean_users_data(users)
    #создаем файл с метаданными
    with open('meta.tsv', 'w') as tsvFile:
        fieldNames = ['uid', 'last_name', 'first_name', 'sex', 'bdate',	'city',	'langs']
        writer = csv.DictWriter(tsvFile, fieldnames=fieldNames, delimiter='\t')
        writer.writeheader()
        writer.writerows(users)
    #создаем файлы с постами
    for index, user in enumerate(users):
        get_posts(user['uid'])
        time.sleep(0.3)
        if (index + 1) % 50 == 0:
            print(index+1)

