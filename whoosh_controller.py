import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iFeeding.settings')

import django
django.setup()

import time

from bs4 import BeautifulSoup

import urllib.request
import http.client
from urllib.error import HTTPError

import re

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD

from django.contrib.auth.models import User
from recipes.models import Tag, Receta, Puntuacion

IX_PATH = './indice/'

SCHEMA = Schema(
            href = ID(stored=True, unique=True),
            image = ID(stored=True),
            title = TEXT(stored = True),
            summary=TEXT(stored=True),
            category=KEYWORD(stored=True, commas=True),
            ingredients=TEXT(stored=True),
            directions=TEXT(stored=True),
            nutrition=KEYWORD(stored=True, commas=True),
        )

if not os.path.exists(IX_PATH):
    os.mkdir(IX_PATH)
    IX = create_in(IX_PATH, SCHEMA)
else:
    IX = open_dir(IX_PATH)

def init_index():
    '''
    This function scrapes data from www.allrecipes.com and insert them into whoosh engine.
    '''
    pattern = re.compile(r'https://www.allrecipes.com/sitemaps/recipe/1/sitemap.xml') 

    sitemap_web = urllib.request.urlopen(url='https://www.allrecipes.com/sitemap.xml').read()
    sitemap_soup = BeautifulSoup(sitemap_web, 'lxml')
    start = time.time()
    i = 1
    with IX.writer() as w:
        '''
        First, function crawls URLs from sitemap.xml.
        Second, It accesses to localizations that match the pattern and crawls recipe links.
        Finally, It scrapes the recipe information, It formats the data into a right format and
        stores them.
        '''
        for loc in sitemap_soup.find_all('loc'):
            if not pattern.match(loc.text):
                continue
            sitemap_recipe_web = urllib.request.urlopen(url=loc.text).read()
            sitemap_recipe_soup = BeautifulSoup(sitemap_recipe_web,  'lxml')
            total_data = len(sitemap_recipe_soup.find_all('loc'))
            for recipe in sitemap_recipe_soup.find_all('loc'):
                if i == 20:
                    break
                url = recipe.text
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    recipe_web = urllib.request.urlopen(req).read()
                except (http.client.IncompleteRead) as e:
                    recipe_web = e.partial
                except HTTPError:
                    pass
                soup = BeautifulSoup(recipe_web, 'lxml')

                try:
                    title = str(soup.find('h1', {'class' : ['headline', 'heading-content', 'elementFont__display']}).string)
                    summary = str(soup.find('div', {'class' : "recipe-summary"}).p.string)
                    category = str(soup.find_all('span', {'class' : "breadcrumbs__title"})[-1].string)
                    valoraciones = soup.find_all('div', {'class' : "component ugc-review ugc-item recipe-review-wrapper"})
                    
                    try:
                        image = soup.find('div', class_='image-container').find('div').get('data-src')
                    except:
                        image = '/static/images/no_image_available.jpg'
                    
                    ingredients = soup.find_all('span', {'class' : 'ingredients-item-name'})
                    ingredients_list = '\n'.join([str(x.string).strip() for x in ingredients])
                    
                    directions = soup.find_all('li', {'class' : 'subcontainer instructions-section-item'})
                    directions_list = '\n\n'.join([f"{x.find('span', {'class':'checkbox-list-text'}).string}\n{x.p.string}" for x in directions])
                    
                    nutrition = soup.find('div', {'class' : 'partial recipe-nutrition-section'}).find('div', {'class' : 'section-body'}).text.replace('. Full Nutrition','').replace('; ',',').strip()
                    
                    w.add_document(href=url, image=image, title = title, category=category, summary=summary, ingredients = ingredients_list, directions=directions_list, nutrition=nutrition)
                    
                    #Insert review's data into django database
                    tag = Tag.objects.get_or_create(nombre = category)
                    energy = re.findall(r'(\d+(?:\.\d+)?)', nutrition)
                    calorias=round(float(energy[0]), 2)
                    proteinas=round(float(energy[1]), 2)
                    carbohidratos=round(float(energy[2]), 2)
                    grasas=round(float(energy[3]), 2)
                    receta = Receta.objects.create(url=url, tag=tag[0], calorias=calorias, proteinas=proteinas, carbohidratos=carbohidratos, grasas=grasas)
                    
                
                    for valoracion in valoraciones:
                        try:
                            user = str(valoracion.find('span', {'class' : "reviewer-name"}).string)
                            rating = str(valoracion.find('span', {'class' : "review-star-text"}).string)
                            nota = int(re.search(r"[0-5]", rating).group())
                            usuario, created = User.objects.get_or_create(username=user, password='S3cr3tP4$$w0rd')
                            '''if created:
                                usuario.set_password('S3cr3tP4$$w0rd')
                                usuario.save()'''
                            Puntuacion.objects.create(receta=receta, usuario=usuario, nota=nota)
                        except:
                            #recipes with no ratings will raise a execption just skip it.
                            pass
                except:
                    pass
                #Animation stuff while scraping
                load_time = time.time()
                m, s = divmod(int(load_time - start), 60)
                h, m = divmod(m, 60)
                animation = '.' * (i%4)
                print(f'Loading data{animation:3s} {i}/{total_data}| Load time: {h:d}h:{m:02d}m:{s:02d}s.', end='\r')
                i = i+1
    finish_time = time.time()
    m, s = divmod(int(finish_time - start), 60)
    h, m = divmod(m, 60)
    os.system('clear')
    print(f'{i} recipes has been loaded in {h:d}h:{m:02d}m:{s:02d}s.')

def main():
    option = input("This process will delete and rewrite the index. Do you want to continue? Y/n ")
    if option == 'Y':
        global IX
        IX = create_in(IX_PATH, SCHEMA)
        init_index()
    

if __name__ == '__main__':
    main()