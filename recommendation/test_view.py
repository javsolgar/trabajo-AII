import re
import string

from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from recommendation.models import Juego

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test_juegos_bd_not_empty(self):
        cantidad = Juego.objects.count()
        self.assertNotEqual(cantidad, 0)

    def test_no_authenticado_no_accede_juegos_lista(self):
        response = self.client.get('/list_juego_recommendation/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='inicio.html')

    def test_authenticado_accede_juegos_lista(self):
        self.client.login(username='prueba', password='963852741A')

        response = self.client.get('/list_juego_recommendation/')
        self.assertEqual(response.status_code, 200)

        lista_juegos = response.context['juegos']
        cantidad = response.context['cantidad']

        self.assertNotEqual(len(lista_juegos), 0)
        self.assertNotEqual(cantidad, 0)
        self.assertEqual(len(lista_juegos), cantidad)
