from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.contrib.auth.models import User

from .forms import register_form

def welcome(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

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
