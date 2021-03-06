from django.urls import path
import recipes.views

urlpatterns = [
    path('search/', recipes.views.recipe_search, name='recipe_search'),
    path('details/<path:url>/', recipes.views.get_by_href, name='get_by_href'),
    path('recommendations/<int:num_recommendations>/', recipes.views.recommended_recipes, name='recommended_recipes'),
]