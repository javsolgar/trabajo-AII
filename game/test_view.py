import re
import string

from django.core.management import call_command
from whoosh.index import open_dir
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from game.models import Juego
from game.scrap_games import crea_index_games, get_url_juegos, obten_juegos, almacena_juegos
from random import randrange

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test_list(self):
        response = self.client.get('/games/')
        self.assertEqual(response.status_code, 200)

    def test_scrap_anonymous(self):
        response = self.client.get('/scrap_games/')
        self.assertEqual(response.status_code, 403)

    def test_show(self):
        ix = open_dir(index_news)
        with ix.searcher() as searcher:
            noticias = searcher.documents()
            for noticia in noticias:
                juego = noticia['juego']
                break
        ix.close()
        self.client.get('/games/' + juego + '/')

    def test_scrap_games(self):
        crea_index_games(index_games)
        url_juegos = get_url_juegos(index_news)
        soup_juegos = obten_juegos(url_juegos[:2])
        almacena_juegos(soup_juegos, index_games)

        ix = open_dir(index_games)
        with ix.searcher() as searcher:
            all_games = searcher.doc_count_all()

        self.assertNotEqual(all_games, 0)

    def test_filtrado_por_generos(self):
        response = self.client.get('/games/filtro/plataformas/')
        self.assertEqual(response.status_code, 200)

        filtro = response.context['filtro']
        self.assertFalse(len(filtro) == 0)

        lista_plataformas = response.context['opciones']
        self.assertFalse(len(lista_plataformas) == 0)

        elemento = randrange(len(lista_plataformas))
        self.assertFalse(len(lista_plataformas[elemento]) == 0)

        response2 = self.client.get('/games/filtrado/', {'select_filtro': filtro + '_' + lista_plataformas[elemento]})
        self.assertEqual(response2.status_code, 200)

        lista_juegos = response2.context['juegos']
        self.assertNotEqual(len(lista_juegos), 0)

    def test_filtrado_por_busqueda_titulo(self):
        response = self.client.get('/games/filtro/buscar/')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/games/')
        self.assertEqual(response2.status_code, 200)

        lista_juegos = response2.context['juegos']
        self.assertNotEqual(len(lista_juegos), 0)

        elemento = randrange(len(lista_juegos))
        self.assertNotEqual(lista_juegos[elemento], 0)

        titulo = lista_juegos[elemento][1]
        self.assertNotEqual(len(titulo), 0)

        palabras = titulo.split(' ')

        palabra = ''

        while palabra == '':
            borrar = False
            elemento2 = randrange(len(palabras))
            elegida = palabras[elemento2]
            for letra in elegida:
                if letra not in string.ascii_letters:
                    borrar = True
                    break
                palabra += letra
            if palabra == 'The' or len(palabra) == 1:
                borrar = True
            if borrar:
                palabra = ''

        self.assertNotEqual(len(palabra), 0)

        response3 = self.client.get('/games/filtrado/', {'select_filtro': palabra})
        self.assertEqual(response3.status_code, 200)

        lista_juegos_respuesta = response3.context['juegos']
        self.assertNotEqual(len(lista_juegos_respuesta), 0)

        contiene_la_palabra = True

        for juego in lista_juegos_respuesta:
            if not palabra in juego[1]:
                contiene_la_palabra = False

        self.assertEqual(contiene_la_palabra, True)

    def test_juegos_bd_not_empty(self):
        cantidad = Juego.objects.count()
        self.assertNotEqual(cantidad, 0)
