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
from django.urls.conf import include
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.welcome, name='welcome'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', app.views.register, name='register'),
    path("my_ratings/", app.views.user_ratings, name="user_ratings"),
    path('my_daily_plan/', app.views.user_daily_plan, name='user_daily_plan'),
    path('add_recipe_to_plan/', app.views.add_recipe_to_plan, name='add_recipe_to_daily_plan'),
    path('add_rating/', app.views.add_rating, name='add_rating'),
    path('recipes/', include('recipes.urls')),
]
