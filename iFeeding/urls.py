"""iFeeding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import app.views
import recipes.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.welcome, name='welcome'),
    path('search/', recipes.views.search_by_title_or_summary, name='search_by_title_or_summary'),
    path('details/<path:url>/', recipes.views.get_by_href, name='get_by_href'), 
    path('ingredients/', recipes.views.search_by_ingredients, name='search_by_ingredients'),
]
