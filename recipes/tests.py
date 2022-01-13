from django.test import TestCase

from django.contrib.auth.models import User
from .models import Tag, Receta, Puntuacion

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        category = 'Italiana'
        url = 'https://www.google.es/'
        usuario = 'testcase'
        password = 'S3cr3tP4ssW0rD'
        nota = 5
        tag = Tag.objects.get_or_create(nombre = category)
        receta = Receta.objects.create(url=url, tag=tag[0])
        usuario = User.objects.get_or_create(username=usuario, password=password)
        Puntuacion.objects.create(receta=receta, usuario=usuario[0], nota=nota)
    
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


