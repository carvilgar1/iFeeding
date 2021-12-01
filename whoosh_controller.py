import os

import re

import urllib.request
import http.client
import time
from bs4 import BeautifulSoup

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD

IX_PATH = './indice/'

IX = open_dir(IX_PATH)

SCHEMA = Schema(
            href = ID(stored=True, unique=True),
            image = ID(stored=True),
            title = TEXT(stored = True),
            summary=TEXT(stored=True),
            ingredients=TEXT(stored=True),
            directions=TEXT(stored=True),
            nutrition=KEYWORD(stored=True, commas=True),
        )


def create_index(path:str = IX_PATH):
    if not os.path.exists(path):
        os.mkdir(path)
        index = create_in(path, SCHEMA)
    return index

def init_index():
    """
    Crawl data from www.allrecipes.com. In order to perform it the function will sear
    recipe urls from the web sitemap.xml
    """
    patron = re.compile(r'https://www.allrecipes.com/sitemaps/recipe/1/sitemap.xml') #TODO

    sitemap_web = urllib.request.urlopen(url='https://www.allrecipes.com/sitemap.xml').read()
    sitemap_soup = BeautifulSoup(sitemap_web, 'lxml')
    start = time.time()
    i = 0
    with IX.writer() as w:
        for loc in sitemap_soup.find_all('loc'):
            if not patron.match(loc.text):
                continue
            sitemap_recipe_web = urllib.request.urlopen(url=loc.text).read()
            sitemap_recipe_soup = BeautifulSoup(sitemap_recipe_web,  'lxml')
            total_data = len(sitemap_recipe_soup.find_all('loc'))
            for recipe in sitemap_recipe_soup.find_all('loc'):
                if i == 100: #<---
                    break
                url = recipe.text
                try:
                    recipe_web = urllib.request.urlopen(url).read()
                except (http.client.IncompleteRead) as e:
                    recipe_web = e.partial
                soup = BeautifulSoup(recipe_web, 'lxml')

                title = str(soup.find('h1', {'class' : ['headline', 'heading-content', 'elementFont__display']}).string)
                summary = str(soup.find('div', {'class' : "recipe-summary"}).p.string)
                try:
                    image = soup.find('div', class_='image-container').find('div').get('data-src')
                except:
                    image = '/static/no_image_available.jpg'
                
                ingredients = soup.find_all('span', {'class' : 'ingredients-item-name'})
                ingredients_list = '\n'.join([str(x.string).strip() for x in ingredients])
                
                directions = soup.find_all('li', {'class' : 'subcontainer instructions-section-item'})
                directions_list = '\n\n'.join([f"{x.find('span', {'class':'checkbox-list-text'}).string}\n{x.p.string}" for x in directions])
                
                nutrition = soup.find('div', {'class' : 'partial recipe-nutrition-section'}).find('div', {'class' : 'section-body'}).text.replace('. Full Nutrition','').replace('; ',',').strip()
                
                w.add_document(href=url, image=image, title = title, summary=summary, ingredients = ingredients_list, directions=directions_list, nutrition=nutrition)
                load_time = time.time()
                m, s = divmod(int(load_time - start), 60)
                h, m = divmod(m, 60)
                print(f'Loading data... {i}/{total_data}| Load time: {h:d}h:{m:02d}m:{s:02d}s.', end='\r')
                i = i+1
    finish_time = time.time()
    m, s = divmod(int(finish_time - start), 60)
    h, m = divmod(m, 60)
    print(f'{i} recipes has been loaded in {h:d}h:{m:02d}m:{s:02d}s.')

def main():
    global IX
    IX = create_index()
    init_index()
    

if __name__ == '__main__':
    main()