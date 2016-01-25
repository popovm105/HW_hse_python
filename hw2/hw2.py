import requests
import os
from bs4 import BeautifulSoup


def get_urls(start_page = 'http://ngisnrj.ru', SIZE = 50):
    queue = [start_page]
    for url in queue:
        try:
            page = requests.get(url)
        except:
            continue

        if page.ok:
            page = BeautifulSoup(page.text, 'html.parser')
            for line in page.findAll('a'):
                try:
                    tempURL = line['href']

                    if tempURL[0] == '/':
                        tempURL = mainPageURL + tempURL
                    elif 'ngisnrj' not in tempURL:
                        continue
                    if tempURL not in queue:
                        queue.append(tempURL)
                        if len(queue) >= SIZE:
                            return queue[:SIZE]
                except:
                    continue


def make_files(list_of_urls):
    if not os.path.exists('./pages/'):
        os.makedirs('./pages/')
    for index, url in enumerate(list_of_urls):
        try:
            page = requests.get(url)
        except:
            continue
        if page.ok:
            with open('./pages/' + str(index), 'w') as f:
                f.write(page.text)

                

urls = get_urls()
make_files(urls)
