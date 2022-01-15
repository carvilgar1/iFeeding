from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from .models import Plan
from recipes.models import Receta, Puntuacion

from .forms import register_form

from datetime import date

from whoosh_controller import populate
from recipes.recommendations import load_similarities

def welcome(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def user_ratings(request):
    if not request.user.is_authenticated:
        return render(request, '404.html', status=404)
    user_ratings = User.objects.get(pk = request.user.id).puntuacion_set.all()
    return render(request, 'ratings.html', {'ratings':user_ratings})

def add_rating(request):
    if not request.user.is_authenticated:
        return render(request, '404.html', status=404)
    Puntuacion.objects.create(usuario_id = request.user.id, receta_id = request.GET['recipe_url'], nota = request.GET['nota'])  
    return HttpResponseRedirect('/')

def user_daily_plan(request):
    if not request.user.is_authenticated:
        return render(request, '404.html', status=404)
    try:
        user_plan = User.objects.get(pk = request.user.id).plan_set.get(dia = date.today())
        energy = user_plan.get_energy_summary()
        planrecipes = user_plan.recetas.all()
        return render(request, 'daily_plan.html', {'energy':energy, 'planrecipes':planrecipes})
    except Plan.DoesNotExist:
        energy = {  'cal': 0, 
                    'protein': 0, 
                    'carbs': 0, 
                    'fats': 0}
        return render(request, 'daily_plan.html', {'energy':energy, 'message':'Aun no has metido nada'})

def add_recipe_to_plan(request):
    if not request.user.is_authenticated:
        return render(request, '404.html', status=404)
    user_plans, _ = Plan.objects.get_or_create(usuario_id = request.user.id, dia = date.today())
    receta = get_object_or_404(Receta, pk=request.GET['recipe_url'])
    user_plans.recetas.add(receta)
    user_plans.save()
    return HttpResponseRedirect('/')

def register(request):
    if request.method =='GET':
        form = register_form()
        return render(request, 'registration/register.html', {'form':form})
    else:
        form = register_form(request.POST)
        if form.is_valid():
            user = User.objects.create( first_name = form.cleaned_data['firstname'], 
                                        last_name = form.cleaned_data['lastname'], 
                                        username = form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/register.html', {'form':form})

def populate_db(request):
    if not request.user.is_superuser:
        return render(request, '404.html', status=404)
    populate()
    return HttpResponseRedirect('/')

def init_rs(request):
    if not request.user.is_superuser:
        return render(request, '404.html', status=404)
    load_similarities()
    return HttpResponseRedirect('/')