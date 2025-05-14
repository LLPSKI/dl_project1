import requests
from bs4 import BeautifulSoup
import os

script_dir = os.path.dirname(__file__)
cache_dir = os.path.join(script_dir, 'cache')
data_cache_dir = os.path.join(script_dir, 'data_cache')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
if not os.path.exists(data_cache_dir):
    os.makedirs(data_cache_dir)

class Author:
    def __init__(self, author:tuple[str, str]):
        self.name = author[0]
        self.page_url = author[1]
    
    def load_pages(self):
        success = False
        for x in os.listdir(data_cache_dir):
            if x == self.name:
                print("Found In Cache!")
                with open(os.path.join(data_cache_dir, f'{self.name}'), 'r') as file:
                    response = file.read()
                    soup = BeautifulSoup(response, 'lxml')
                success = True
                break
        if not success:
            print("No Found In Cache!")
            print("Loading Pages...")
            response = requests.get(self.page_url)
            soup = BeautifulSoup(response.text, 'lxml')
            with open(os.path.join(data_cache_dir, f'{self.name}'), 'w') as file:
                file.write(response.text)
        print("OK!")
        view_urls = []
        page_titles = []
        for nav in soup.find_all('nav', {'class': 'publ'}):
            li = nav.find('li', {'class': 'ee'})
            if li is not None:
                a = li.find('a')
                view_urls.append(a['href'])
            else:
                view_urls.append('None')
        for cite in soup.find_all('cite'):
            span = cite.find('span', {'class': 'title', 'itemprop': 'name'})
            page_titles.append(span.text)
        if len(view_urls) == len(page_titles):
            self.pages = []
            for i in range(len(view_urls)):
                self.pages.append((page_titles[i], view_urls[i]))
        else:
            print("some error!")
            

def search_author(author_name:str) -> list[Author]:
    url = f'https://dblp.org/search/author/api?q={author_name}'
    
    # 查询缓存中是否拥有
    success = False
    for x in os.listdir(cache_dir):
        if x == author_name:
            success = True
            break
    if success:
        print(f"Found In Cache!")
        with open(os.path.join(cache_dir, author_name), 'r') as file:
            response = file.read()
            soup = BeautifulSoup(response, features='xml')
    else:
        print(f'No Found In Cache!')
        print("Get Response!")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='xml')
        with open(os.path.join(cache_dir, author_name), 'w') as file:
            file.write(response.text)
    print("Processing!")
    ret = []
    for hit in soup.find_all('hit'):
        for info in hit.find_all('info'):
            author = info.find('author')
            url = info.find('url')
            ret.append(Author((author.text, url.text)))
    return ret

if __name__ == '__main__':
    author_name = 'Ya-qin Zhang'
    authors = search_author(author_name)
    for author in authors:
        print(f'author: {author.name}')
        for page in author.pages:
            print(page[0], page[1])