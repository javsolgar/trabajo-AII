from whoosh.index import open_dir
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from game.scrap_games import crea_index_games, get_url_juegos, obten_juegos, almacena_juegos

#from news_game.scrap_news import obten_lista_noticias, obten_info_noticias, crea_index, extrae_url_noticias, \
#    almacena_noticias

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client = None



    def test_scrap_news(self):
        crea_index_games(index_games)
        url_juegos = get_url_juegos(index_news)
        soup_juegos = obten_juegos(url_juegos[:2])
        almacena_juegos(soup_juegos, index_games)

        ix = open_dir(index_games)
        with ix.searcher() as searcher:
            all_games = searcher.doc_count_all()

        self.assertEqual(all_games, 2)
