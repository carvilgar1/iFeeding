from django.test import TestCase

from django.contrib.auth.models import User
from .models import Tag, Receta, Puntuacion

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Tag.objects.create(nombre='Italiana')
        Receta.objects.create(url='https://www.google.es/', tag=Tag.objects.get(pk='Italiana'))
        User.objects.create(username='testcase')
        Puntuacion.objects.create(receta=Receta.objects.get(pk='https://www.google.es/'), usuario=User.objects.get(username='testcase'), nota=5)
    
    def test_modelo_instanciado(self):
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Receta.objects.count(), 1)
        self.assertEqual(Puntuacion.objects.count(), 1)
        
    def test_check_puntuaciones(self):
        puntuaciones = Receta.objects.get(pk='https://www.google.es/').puntuacion_set.all()
        
        self.assertEqual(puntuaciones[0].usuario.username, 'testcase')
        self.assertEqual(puntuaciones[0].nota, 5)

    def test_check_tag(self):
        receta = Receta.objects.get(pk='https://www.google.es/')
        
        self.assertEqual(receta.tag.nombre, 'Italiana')


