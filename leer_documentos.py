from urllib import request
from bs4 import BeautifulSoup
import re

patron = re.compile(r'https://www.allrecipes.com/sitemaps/recipe/[\d]+/sitemap.xml')
sitemap = 'https://www.allrecipes.com/sitemap.xml'

from whoosh.fields import Schema, TEXT, KEYWORD, ID

schema = Schema(title=ID(stored=True),
                summary=TEXT(stored=True),
                ingredients=TEXT(stored=True),
                directions=TEXT(stored=True),
                nutrition=TEXT(stored=True))
import os.path
from whoosh.index import create_in

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

sitemap_content = request.urlopen(sitemap)

index = BeautifulSoup(sitemap_content, 'lxml')


'''for site in  index.find_all('sitemap'):
    recipe_xml = site.find('loc').text
    if patron.match(recipe_xml):
        url = 'https://www.allrecipes.com/sitemaps/recipe/1/sitemap.xml'
        web = request.urlopen(url)
        recetas = BeautifulSoup(web, 'lxml')
        for receta in recetas.find_all('url'):
            receta_url = receta.find('loc').string
            with open('recetas_url.txt', 'a') as w:
                w.write(str(receta_url) + '\n')'''

'''with open('recetas_url copy.txt', 'r') as f:
    while True:
        try:
            recipe_url = next(f)
            recipe_web = request.urlopen(recipe_url)
            soup = BeautifulSoup(recipe_web, 'lxml')

            title = soup.find('h1', {'class' : ['headline', 'heading-content', 'elementFont__display']}).string
            summary = soup.find('div', {'class' : "recipe-summary"}).p.string
            ingredients = soup.find_all('span', {'class' : 'ingredients-item-name'})
            ingredients_list = '\n'.join([str(x.string).strip() for x in ingredients])
            directions = soup.find('section', {'class' : 'component recipe-instructions recipeInstructions container'}).find('ul')
            directions_list = '\n'.join([str(x.text).strip().replace('Advertisement', '') for x in directions.find_all('li')])
            nutrition = str(soup.find('section', {'class':['nutrition-section container']}).find('div', {'class' : "section-body"}).text).strip()
            with ix.writer() as w:
                w.add_document(title = str(title), summary=str(summary), ingredients = ingredients_list,
                                directions=directions_list, nutrition=nutrition)
        except StopIteration:
            break'''


from whoosh.query import *
from whoosh.qparser import QueryParser

myquery = And([Term("ingredients", u"eggs"), Term("ingredients", "sugar")])

with ix.searcher() as searcher:
    print(searcher.search(myquery))
