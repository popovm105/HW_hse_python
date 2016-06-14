import string
import re

def get_new_item_to_dict(china_dict, line):
    '''
    Функция добавляет в словарь china_dict данные из строки из китайского словаря line
    :param china_dict: словарь "китайское слово": [{'transcr': транскрипция, 'sem': перевод}]
    :param line:  строка из файла с китайским словарем
    :return:
    '''
    #если считана "служебная" строка
    if line.startswith('#') or line.startswith('%'):
        return
    #извлекаем транскрипцию и перевод и приводим к нужной форме
    transcr = re.findall('\[.*?\]', line)[0].strip('[]')
    sem = re.findall('/.*/', line)[0].replace(' ', '_').strip('/').replace('/',', ')
    line = line.split()
    #добавляем извлеченные данные в словарь
    if line[1] in china_dict:
        china_dict[line[1]].append({'transcr': transcr, 'sem': sem})
    else:

        china_dict[line[1]] = [{'transcr': transcr, 'sem': sem}]


def check_substring(substring, china_dict):
    '''
    Функция проверяет начинается ли строка со словарного токена, если да то возвращает этот токен
    если нет то возвращаем False
    :param substring: подстрока из файла на китайском
    :param china_dict:  словарь "китайское слово": [{'transcr': транскрипция, 'sem': перевод}]
    :return:
    '''
    for i in range(len(substring)):
        if china_dict.get(substring[:len(substring)-i], False):
            return substring[:len(substring)-i]
    return False


def get_translate(line, china_dict):
    '''
    преобразуем строку line на китайском в набор слов с перводом
    :param line:  строка из файла на китайском
    :param china_dict: словарь "китайское слово": [{'transcr': транскрипция, 'sem': перевод}]
    :return: возвращаем разобранную строку если она требует разбора и строку без изменения в противном случае
    '''
    result = ''

    #если строка требует разбора
    if line.startswith('<se>'):
        while (len(line) > 0):
            #print(line)
            substring = check_substring(line, china_dict)
            #если в начале строки найдет токен из словаря
            if substring:
                #print(substring)
                result += '\n<w>'
                #добавляем в разбор строки разбор найденого токена
                for item in china_dict[substring]:
                    result += '<ana lex="{}" transcr="{}" sem="{}"/>'.format(substring, item['transcr'],item['sem'])
                result += '{}</w>'.format(substring)
                удаляем из подстроки найденный токен
                line = line.lstrip(substring)

            #если строка начинается с незнакомого набора символов то добавляем первый из них в результат без разбора
            else:
                result += line[0]
                line = line[1:]

        return result
    else:
        return line

if __name__ == "__main__":
    # создаем китайский словарь
    chinaDict = {}
    with open('./cedict_ts.u8') as f:
        for line in f:
            get_new_item_to_dict(chinaDict, line)

    # переводим stal.xml и щаписываем результат в result.xml
    with open('./result.xml', 'w') as resultFile:
        with open('./stal.xml') as text:
            i = 0
            for line in text:
                #print(i)
                translate = get_translate(line, chinaDict)
                #print(translate)
                resultFile.write(translate)
                i+=1
                #if(i==6):
                 #   break
            #resultFile.write('</body>\n</html>')

