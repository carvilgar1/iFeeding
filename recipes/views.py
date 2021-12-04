from django.shortcuts import render

from whoosh.query.terms import Term
from whoosh_controller import SCHEMA, IX
from whoosh.qparser import MultifieldParser, QueryParser

# Create your views here.
def search_by_title_or_summary(request):
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
        results = s.search_page(my_query, pagenum=pagenum, pagelen=pagelen)
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

def search_by_ingredients(request):
    #TODO: Pagination implementation
    context = dict()
    with IX.searcher() as s:
        parser = QueryParser('ingredients', SCHEMA)
        my_query = parser.parse(request.POST['ingredients'])
        ingredients_to_exclude = Term('ingredients', request.POST['ingredients'])
        context['recipes'] = s.search(my_query, mask=ingredients_to_exclude)

        html = render(request, 'search_recipes.html', context)
    return html