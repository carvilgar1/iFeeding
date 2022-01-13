from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    dia = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    recetas = models.ManyToManyField(to="recipes.Receta")

    def get_amount_of_calories(self) -> int:
        return sum([recipe.calorias for recipe in self.recetas.all()])

    def get_amount_of_proteins(self) -> int:
        return sum([recipe.proteinas for recipe in self.recetas.all()])

    def get_amount_of_carbs(self) -> int:
        return sum([recipe.carbohidratos for recipe in self.recetas.all()])

    def get_amount_of_fats(self) -> int:
        return sum([recipe.grasas for recipe in self.recetas.all()])
    
    def get_energy_summary(self):
        return {'cal': self.get_amount_of_calories(), 
                'protein': self.get_amount_of_proteins(), 
                'carbs': self.get_amount_of_carbs(), 
                'fats': self.get_amount_of_fats()}