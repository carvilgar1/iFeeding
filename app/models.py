from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Tag(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)

class Receta(models.Model):
    url = models.URLField(max_length=300, primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    puntuaciones = models.ManyToManyField(User,through='app.Puntuacion')

class Puntuacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nota = models.SmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])