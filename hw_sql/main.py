import pymysql
import csv

def create_tables():
    cur.execute('CREATE TABLE sex(sex_id INT(3) NOT NULL AUTO_INCREMENT, sex ENUM("female", "male"), PRIMARY KEY(sex_id),UNIQUE(sex))DEFAULT CHARSET = utf8')
    cur.execute('CREATE TABLE city(city_id INT(10) NOT NULL AUTO_INCREMENT, city VARCHAR(30), PRIMARY KEY(city_id),UNIQUE(city))DEFAULT CHARSET = utf8')
    cur.execute('CREATE TABLE first_name(first_name_id INT(10) NOT NULL AUTO_INCREMENT, first_name VARCHAR(30), PRIMARY KEY(first_name_id),UNIQUE(first_name))DEFAULT CHARSET = utf8')
    cur.execute('CREATE TABLE second_name(second_name_id INT(10) NOT NULL AUTO_INCREMENT, second_name VARCHAR(30), PRIMARY KEY(second_name_id),UNIQUE(second_name))DEFAULT CHARSET = utf8')
    cur.execute('''CREATE TAbLE person(
    person_id INT(12),
    sex_id INT(3),
    city_id INT(10),
    first_name_id INT(10),
    second_name_id INT(10),
    PRIMARY KEY(person_id),
    FOREIGN KEY (sex_id) REFERENCES sex(sex_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id),
    FOREIGN KEY (first_name_id) REFERENCES first_name(first_name_id),
    FOREIGN KEY (second_name_id) REFERENCES second_name(second_name_id))
    DEFAULT CHARSET = utf8''')

def add_raw_to_db(row):
    cur.execute('INSERT IGNORE INTO sex(sex) VALUES("{}")'.format(row['sex']))
    cur.execute('INSERT IGNORE INTO city(city) VALUES("{}")'.format(row['city']))
    cur.execute('INSERT IGNORE INTO first_name(first_name) VALUES("{}")'.format(row['first_name']))
    cur.execute('INSERT IGNORE INTO second_name(second_name) VALUES("{}")'.format(row['last_name']))
    cur.execute('''INSERT INTO person(person_id, sex_id, city_id, first_name_id, second_name_id)
    VALUES(
      {},
      (SELECT sex_id FROM sex WHERE sex = "{}"),
      (SELECT city_id FROM city WHERE city = "{}"),
      (SELECT first_name_id FROM first_name WHERE first_name = "{}"),
      (SELECT second_name_id FROM second_name WHERE second_name = "{}")


     )

    '''.format(row['uid'], row['sex'], row['city'], row['first_name'], row['last_name']))



if __name__ == "__main__":

    connection = pymysql.connect(host='localhost',
                                 user='',#add username
                                 password='',#add password
                                 charset='utf8')

    cur = connection.cursor()
    cur.execute('DROP DATABASE IF EXISTS my_base')
    cur.execute('CREATE DATABASE my_base')
    cur.execute('USE my_base')
    create_tables()

    with open('meta.tsv') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            add_raw_to_db(row)

    connection.commit()






