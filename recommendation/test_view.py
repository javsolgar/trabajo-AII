import random

from django.contrib.auth import authenticate
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from recommendation.form import FormularioJuegos
from application.models import Perfil
from recommendation.models import Juego, Puntuacion

index_news = './indices/IndexNewsGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def inicializa_RS(self):
        self.client.login(username='admin', password='admin')
        self.client.get('/load_RS/')

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

        response2 = self.client.get('/game_recomendation/?id=' + str(juego_seleccionado.id))
        self.assertEqual(response2.status_code, 200)

        juego = response2.context['juego']
        self.assertIsNotNone(juego.titulo)
        self.assertIsNotNone(juego.jugadores.jugadores)
        self.assertIsNotNone(juego.desarrollador.nombre)
        self.assertNotEqual(response2.context['generos'], '')
        self.assertNotEqual(response2.context['plataformas'], '')
        self.assertEqual(juego.id, juego_seleccionado.id)
        self.assertIsNotNone(response2.context['noticias'])

    def test_user_hace_puntuacion(self):
        username = 'prueba'
        password = '963852741A'
        id = 8
        valor1 = 5
        valor2 = 4
        valor3 = 0

        usuario = authenticate(username=username, password=password)
        perfil = Perfil.objects.get(usuario=usuario)
        juego = Juego.objects.get(id=id)

        self.assertEqual(Puntuacion.objects.filter(perfil=perfil, juego=juego).count(), 0)
        self.client.login(username=username, password=password)

        # Crea puntuacion

        response = self.client.post('/game_recomendation/?id=' + str(id), {'puntuacion': valor1})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Puntuacion.objects.filter(perfil=perfil, juego=juego).count(), 0)

        puntuacion = Puntuacion.objects.get(perfil=perfil, juego=juego)
        self.assertEqual(puntuacion.valor, valor1)

        # Actualiza puntuacion

        response2 = self.client.post('/game_recomendation/?id=' + str(id), {'puntuacion': valor2})
        self.assertEqual(response2.status_code, 200)
        self.assertNotEqual(Puntuacion.objects.filter(perfil=perfil, juego=juego).count(), 0)

        puntuacion = Puntuacion.objects.get(perfil=perfil, juego=juego)
        self.assertEqual(puntuacion.valor, valor2)

        # Elimina puntuacion

        response3 = self.client.post('/game_recomendation/?id=' + str(id), {'puntuacion': valor3})
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(Puntuacion.objects.filter(perfil=perfil, juego=juego).count(), 0)

    def test_list_puntuaciones_user(self):
        username = 'prueba'
        password = '963852741A'

        self.client.login(username=username, password=password)
        response = self.client.get('/get_my_recomendations/')
        self.assertEqual(response.status_code, 200)

        puntuaciones = response.context['puntuaciones']
        self.assertEqual(len(puntuaciones), 6)

    def test_recomienda_4_juegos_similares(self):
        self.inicializa_RS()

        username = 'prueba'
        password = '963852741A'
        id_juego = random.randrange(1, 37)
        self.client.login(username=username, password=password)

        response = self.client.get('/recommend_4_similar_games/')
        self.assertEqual(response.status_code, 200)


        response2 = self.client.get('/get_4_games/', {'juego_id': str(id_juego)})
        self.assertEqual(response2.status_code, 200)

        juegos = response2.context['juegos']
        self.assertEqual(len(juegos), 4)

    def test_recomienda_juegos_usuario(self):
        self.inicializa_RS()

        username = 'prueba'
        password = '963852741A'

        self.client.login(username=username, password=password)

        response = self.client.get('/recommend_no_rated_games/')
        self.assertEqual(response.status_code, 200)

        juegos = response.context['juegos']
        self.assertEqual(len(juegos), 4)
