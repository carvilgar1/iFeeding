#encoding:utf-8

from .models import Receta, Puntuacion
from collections import Counter
import shelve

def a():
    print('Computing the books attributes')
    recipes = {}
    
    for element in Receta.objects.all():
        id = str(element.url)
        tag = str(element.tag)
        print(tag)
        recipes.setdefault(id, [])
        recipes[id].append(tag)

    return recipes

def user_preferences():
    print('Computing attributes from most common books for each user')
    users = {}
    for element in Puntuacion.objects.all():
        userId = element.usuario.id
        users.setdefault(userId, {})
        receta = element.receta
        if(element.nota>=4):
            users[userId][receta.url] = [str(receta.tag)]
    for u in users:
        users[u] = [[attr[0]] for receta,attr in Counter(users[u]).most_common(1)]
    print('Preferencias de usuario: ' + str(users))
    return users

def load_similarities():
    shelf = shelve.open('dataRS.dat')
    recetas_attr = a()
    user_pref = user_preferences()
    shelf['similarities'] = compute_similarities(recetas_attr, user_pref)
    shelf.close()

def recommended_recipes(userId):
    shelf = shelve.open("dataRS.dat")
    read = set()
    read = set(a.receta.url for a in Puntuacion.objects.filter(usuario_id=userId))
    print('Recetas leidas: ' + str(read))
    res = []
    print('Similtudes: ' + str(shelf['similarities'][userId]))
    for id_recipe, score in shelf['similarities'][userId]:
        if id_recipe not in read:
            recipe = Receta.objects.get(pk=id_recipe)
            res.append([recipe, 100 * score])
    shelf.close()
    print('Recetas recomendados: ' + str(res[:3]))
    return res

def compute_similarities(recipes_attr, user_pref):
    print('Computing user-recipes similarity matrix')
    res = {}
    for u in user_pref:
        top_recipes = {}
        for a in recipes_attr:
            if(len(user_pref[u])>0):
                print('Conjunto de preferencias de usuario: ' + str(user_pref[u][0]))
                print('Conjunto de atributos de receta: ' + str(set(recipes_attr[a])))
                top_recipes[a] = dice_coefficient(set(user_pref[u][0]), set(recipes_attr[a]))
        res[u] = Counter(top_recipes).most_common(10)
    return res

def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))