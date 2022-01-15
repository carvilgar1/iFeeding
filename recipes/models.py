from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Tag(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.nombre

class Receta(models.Model):
    url = models.URLField(max_length=500, primary_key=True)
    img = models.URLField(max_length=500, default="/static/images/no_image_available.jpg")
    title = models.CharField(max_length=100, default="")
    calorias = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    proteinas = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    grasas = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    carbohidratos = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    puntuaciones = models.ManyToManyField(User,through='recipes.Puntuacion')

    def __str__(self) -> str:
        return self.url

class Puntuacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nota = models.SmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])