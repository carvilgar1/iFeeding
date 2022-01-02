from django.shortcuts import render
from whoosh_controller import init_index

def welcome(request):
    return render(request, 'index.html')

def populate(request):
    init_index()
    return render(request, 'index.html')