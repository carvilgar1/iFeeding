from django.shortcuts import render

def welcome(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration/register.html')
