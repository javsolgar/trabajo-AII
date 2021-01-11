import random

from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from recommendation.models import Juego

index_news = './indices/IndexNewsGames'



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
        response = self.client.get('/list_game_recommendation/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='inicio.html')

    def test_authenticado_accede_juegos_lista(self):
        self.client.login(username='prueba', password='963852741A')

        response = self.client.get('/list_game_recommendation/')
        self.assertEqual(response.status_code, 200)

        lista_juegos = response.context['juegos']
        cantidad = response.context['cantidad']

        self.assertNotEqual(len(lista_juegos), 0)
        self.assertNotEqual(cantidad, 0)
        self.assertEqual(len(lista_juegos), cantidad)

    def test_authenticado_no_accede_show_game(self):
        response = self.client.get('/list_game_recommendation/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='inicio.html')

    def test_list_y_show_game(self):
        self.client.login(username='prueba', password='963852741A')
        response = self.client.get('/list_game_recommendation/')
        self.assertEqual(response.status_code, 200)

        juegos = response.context['juegos']

        selector = random.randrange(len(juegos))
        juego_seleccionado = juegos[selector]

        response2 = self.client.get('/game_recomendation/?id='+str(juego_seleccionado.id))
        self.assertEqual(response2.status_code, 200)

        juego = response2.context['juego']
        self.assertIsNotNone(juego.titulo)
        self.assertIsNotNone(juego.jugadores.jugadores)
        self.assertIsNotNone(juego.desarrollador.nombre)
        self.assertNotEqual(response2.context['generos'], '')
        self.assertNotEqual(response2.context['plataformas'], '')
        self.assertEqual(juego.id, juego_seleccionado.id)
        self.assertIsNotNone(response2.context['noticias'])






