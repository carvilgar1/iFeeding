from django.shortcuts import render

from whoosh_controller import SCHEMA, IX
from whoosh.qparser import MultifieldParser

# Create your views here.
def search_by_title_or_summary(request):
    #TODO: Pagination implementation
    context = dict()
    with IX.searcher() as s:
        parser = MultifieldParser(['summary', 'title'], SCHEMA)
        my_query = parser.parse(request.GET['query'])
        context['recipes'] = s.search(my_query)

        html = render(request, 'search_recipes.html', context)
    return html

def get_by_href(request, url):
    with IX.searcher() as s:
        recipe = s.document(href=url)

        context = dict(recipe)

        html = render(request, 'recipe_info.html', context)
    return html

def search_by_ingredients(request, ingredients):
    pass