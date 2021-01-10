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

    def test_juegos_bd_not_empty(self):
        cantidad = Juego.objects.count()
        self.assertNotEqual(cantidad, 0)
