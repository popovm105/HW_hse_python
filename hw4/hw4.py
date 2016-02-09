
# coding: utf-8

# In[1]:


import re
import requests
import os
import lxml.html
from pymystem3 import Mystem
m = Mystem()




def is_news_or_articles(str):
    if re.search('.*/news/\d+/$',str) == None and re.search('.*/article/\d+/$',str) == None:
        return False
    else:
        return True




def get_urls(start_page = 'http://ngisnrj.ru', SIZE = 20):
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
    result ={}
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)

    title = tree.findtext('.//title').split(' - ')[0]

    result['title'] = title

    date_temp = author = tree.xpath('.//span[@class="b-object__detail__issue__date"]/text()')[0]
    date = get_date(date_temp)
    result['date'] = date

    text_anot = tree.xpath('.//div[@class="b-object__detail__annotation"]//text()')[0]
    text_main = tree.xpath('.//div[@class="b-block-text__text"]//text()')
    text = text_anot
    for part in text_main:
        text += part

    result['text'] = text

    author = tree.xpath('.//span[@class="b-object__detail__author__name"]//text()')
    if len(author) == 0:
        author = 'None'
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


urls = get_urls()
with open('meta.csv','w') as f:
    f.write('path\tauthor\tdate(dd.mm.yyyy)\ttitle\tlem_title\tcategory\tURL')
for url in urls:
    data = get_data(url)
    path = './texts/' + data['date']['year'] + '/' +  data['date']['month'] + '/' +  data['date']['day'] +'/'
    path_mystem = './texts_mystem/' + data['date']['year'] + '/' +  data['date']['month'] + '/' +  data['date']['day'] +'/'
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path_mystem):
        os.makedirs(path_mystem)    
    with open(path_mystem + data['title'],'w') as f:
        f.write(get_gramm_text(data['title']) + '\n' + get_gramm_text(data['text']))
    with open(path + data['title'],'w') as f:
        f.write(data['title'] + '\n' + data['text'])    
    with open('meta.csv','a') as f:
        f.write('\n'+  path+ data['title']
                + '\t'+ data['author']
               + '\t' + data['date']['day'] + '.' + data['date']['month']+ '.' + data['date']['year']
               +'\t' + data['title']
               + '\t' + data['category']
               + '\t' + data['URL']
               + '\t' + get_lemmatized_title(data['title']))





            
