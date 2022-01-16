from django.shortcuts import render
from whoosh.query.compound import Or, And

from whoosh.query.terms import Term
from whoosh_controller import SCHEMA, IX
from whoosh.qparser import MultifieldParser, QueryParser


import recipes.recommendations as sr

from .models import Tag, Puntuacion

TAG_LIST = Tag.objects.all()

# Create your views here.
def recipe_search(request):
    context = {'tags':Tag.objects.all()}
    pagenum=int(request.GET['page_num'])
    pagelen=int(request.GET['page_len'])
    if pagenum < 1 or pagelen < 1:
        pagenum = 1
        pagelen = 15
        context['errors'] = ["Page len must be greater than 14", "page num must be greater than 0"]
    with IX.searcher() as s:
        parser = MultifieldParser(['summary', 'title'], SCHEMA)
        my_query = parser.parse(request.GET['query'])
        ingredients_to_include = Or([Term('ingredients', ingredient) for ingredient in request.GET['ingredients_to_include'].split(" ")]) if request.GET['ingredients_to_include'] else None
        ingredients_to_exclude = And([Term('ingredients', ingredient) for ingredient in request.GET['ingredients_to_exclude'].split(" ")])if request.GET['ingredients_to_exclude'] else None
        #If ingredients_to_include or ingredients_to_exclude are settled but empty then set their values to None to not filter the results
        results = s.search_page(my_query, 
                                filter= ingredients_to_include, 
                                mask= ingredients_to_exclude, 
                                pagenum=pagenum, 
                                pagelen=pagelen)
        context['recipes'] = results
        context['result_len'] = len(results)
       
        html = render(request, 'search_recipes.html', context)
    return html

def get_by_href(request, url):
    with IX.searcher() as s:
        recipe = s.document(href=url)

        context = dict(recipe)
        context['ingredients'] = context['ingredients'].split('\n')
        context['directions'] = context['directions'].split('\n\n')
        html = render(request, 'recipe_info.html', context)
    return html

def recommended_recipes(request, num_recommendations):
    if not request.user.is_authenticated:
        return render(request, 'errors/404.html', status=404)
    user_id = request.user.id
    try:
        if len(Puntuacion.objects.filter(usuario_id = user_id)) > 0:
            recommended = sr.recommended_recipes(user_id)[:num_recommendations]
        else:
            recommended = []
        return render(request, 'recommendations.html', {'recommended':recommended})
    except:
        return render(request, 'errors/500.html', status=500)



