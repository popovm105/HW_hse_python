from bs4 import BeautifulSoup
import string

def get_new_item_to_dict(china_dict, line):
    if line.startswith('#') or line.startswith('%'):
        return
    line = line.split()

    if line[1] in china_dict:
        china_dict[line[1]].append({'transcr': line[2], 'sem':line[3]})
    else:

        china_dict[line[1]] = [{'transcr': line[2], 'sem':line[3]}]


def check_substring(substring, china_dict):
    for i in range(len(substring)):
        if china_dict.get(substring[:len(substring)-i], False):
            return substring[:len(substring)-i]
    return False


def get_translate(line, china_dict):
    result = ''
    punct = string.punctuation + ' “”'

    if line.startswith('<se>'):
        while (len(line) > 0):
            print(line)
            substring = check_substring(line, china_dict)
            if substring:
                print(substring)
                result += '\n<w>'
                for item in china_dict[substring]:
                    result += '<ana lex="{}" transcr="{}" sem="{}"/>'.format(substring, item['transcr'],item['sem'])
                result += '<\w>\n'
                line = line.lstrip(substring)

            else:
                result += line[0]
                line = line[1:]

        return result
    else:
        return line


chinaDict = {}
with open('./cedict_ts.u8') as f:
    for line in f:
        get_new_item_to_dict(chinaDict, line)


with open('./result.xml', 'w') as resultFile:
    with open('./stal.xml') as text:
        i = 0
        for line in text:
            print(i)
            translate = get_translate(line, chinaDict)
            print(translate)
            resultFile.write(translate)
            i+=1
            '''if(i==7):
                break'''
            resultFile.write('</body>\n</html>')

