from django.test import TestCase

from datetime import date

from django.contrib.auth.models import User
from .models import Plan
from recipes.models import Tag, Receta

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        category = 'Italiana'
        url = 'https://www.google.es/'
        url2 = 'https://www.twitter.es/'
        usuario = 'testcase'
        password = 'S3cr3tP4ssW0rD'

        cal1,proteina1, carbs1, fats1 = 500, 10, 20, 30
        cal2,proteina2, carbs2, fats2 = 550, 20, 30, 40
        
        tag = Tag.objects.get_or_create(nombre = category)
        receta = Receta.objects.create(url=url, tag=tag[0], calorias=cal1, proteinas=proteina1, carbohidratos=carbs1, grasas=fats1)
        receta2 = Receta.objects.create(url=url2, tag=tag[0], calorias=cal2, proteinas=proteina2, carbohidratos=carbs2, grasas=fats2)
        usuario = User.objects.get_or_create(username=usuario, password=password)
        plan, created = Plan.objects.get_or_create(usuario=usuario[0], dia=date.today())
        plan.recetas.add(receta)
        plan.recetas.add(receta2)
        plan.save()

        self.plan_test = Plan.objects.filter(usuario__username = "testcase").first()
    
    def test_modelo_instanciado(self):
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Receta.objects.count(), 2)
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(self.plan_test.recetas.all().count(), 2)
    
    def test_amount_of_energy(self):
        self.assertEqual(self.plan_test.get_amount_of_calories(), 1050)
        self.assertEqual(self.plan_test.get_amount_of_proteins(), 30)
        self.assertEqual(self.plan_test.get_amount_of_carbs(), 50)
        self.assertEqual(self.plan_test.get_amount_of_fats(), 70)
    
    
        

