import os
import shutil

import pytest

import whoosh_controller
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from bs4 import BeautifulSoup
from urllib import request

TEST_PATH = './test'

def test_create_index_positive():
    whoosh_controller.create_index(TEST_PATH)

    assert os.path.exists(TEST_PATH)

@pytest.mark.xfail(raises=Exception)
def test_create_index_negative():
    whoosh_controller.create_index(TEST_PATH)

def test_add_document():
    urls = ['https://www.allrecipes.com/recipe/13477/double-layer-pumpkin-cheesecake/',
            'https://www.allrecipes.com/recipe/166160/juicy-thanksgiving-turkey/',
            'https://www.allrecipes.com/recipe/23439/perfect-pumpkin-pie/']
    
    ix = open_dir(TEST_PATH)
    
    for url in urls:
        recipe_web = request.urlopen(url)
        soup = BeautifulSoup(recipe_web, 'lxml')

        title = soup.find('h1', {'class' : ['headline', 'heading-content', 'elementFont__display']}).string
        summary = soup.find('div', {'class' : "recipe-summary"}).p.string
        ingredients = soup.find_all('span', {'class' : 'ingredients-item-name'})
        ingredients_list = '\n'.join([str(x.string).strip() for x in ingredients])
        directions = soup.find('section', {'class' : 'component recipe-instructions recipeInstructions container'}).find('ul')
        directions_list = '\n'.join([str(x.text).strip().replace('Advertisement', '') for x in directions.find_all('li')])
        nutrition = str(soup.find('section', {'class':['nutrition-section container']}).find('div', {'class' : "section-body"}).text).strip()
        with ix.writer() as w:
            w.add_document(href=url, title = str(title), summary=str(summary), ingredients = ingredients_list,
                            directions=directions_list, nutrition=nutrition)
            #w.commit()
    
    query = QueryParser('href', whoosh_controller.SCHEMA).parse(urls[0])

    with ix.searcher() as s:
        assert s.doc_count() == 3
        assert s.search(query)
        assert s.search(query)[0]['title'] == 'Double Layer Pumpkin Cheesecake'

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""
    def remove_test_dir():
        shutil.rmtree(TEST_PATH)
    request.addfinalizer(remove_test_dir)

