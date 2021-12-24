from django.shortcuts import render
from whoosh.query.compound import Or

from whoosh.query.terms import Term
from whoosh_controller import SCHEMA, IX
from whoosh.qparser import MultifieldParser, QueryParser

from .forms import extended_search_form

# Create your views here.
def recipe_search(request):
    context = dict()
    pagenum=int(request.GET['page_num'])
    pagelen=int(request.GET['page_len'])
    if pagenum < 1 or pagelen < 1:
        pagenum = 1
        pagelen = 15
        context['errors'] = ["Page len must be greater than 14", "page num must be greater than 0"]
    with IX.searcher() as s:
        parser = MultifieldParser(['summary', 'title'], SCHEMA)
        my_query = parser.parse(request.GET['query'])
        #If ingredients_to_include or ingredients_to_exclude are settled but empty then set their values to None to not filter the results
        ingredients_to_include = Or([Term('ingredients', request.GET['ingredients_to_include'])]) if request.GET['ingredients_to_include'] else None
        ingredients_to_exclude = Or([Term('ingredients', request.GET['ingredients_to_exclude'])]) if request.GET['ingredients_to_exclude'] else None
        results = s.search_page(my_query, filter=ingredients_to_include, mask=ingredients_to_exclude, pagenum=pagenum, pagelen=pagelen)
        context['recipes'] = results
        context['result_len'] = len(results)
        html = render(request, 'search_recipes.html', context)
    return html

def extended_search(request):
    context = dict()
    with IX.searcher() as s:
        parser = MultifieldParser(['summary', 'title'], SCHEMA)
        my_query = parser.parse(request.POST['ingredients'])
        ingredients_to_exclude = Or([Term('ingredients', request.POST['ingredients_to_exclude'])])
        results = s.search_page(my_query, mask=ingredients_to_exclude, pagenum=1, pagelen=15)
        context['recipes'] = results
        context['result_len'] = len(results)
        html = render(request, 'search_recipes.html', context)
    return html

def get_by_href(request, url):
    with IX.searcher() as s:
        recipe = s.document(href=url)

        context = dict(recipe)

        html = render(request, 'recipe_info.html', context)
    return html