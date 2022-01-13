from django.contrib import admin
from .models import Receta, Tag, Puntuacion

# Register your models here.
admin.site.register(Receta)
admin.site.register(Tag)
admin.site.register(Puntuacion)
