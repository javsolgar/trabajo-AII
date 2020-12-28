from whoosh.index import open_dir
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from game.scrap_games import crea_index_games, get_url_juegos, obten_juegos, almacena_juegos

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test_list(self):
        response = self.client.get('/games/')
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        ix = open_dir(index_news)
        with ix.searcher() as searcher:
            noticias = searcher.documents()
            for noticia in noticias:
                juego = noticia['juego']
                break
        ix.close()
        self.client.get('/games/'+juego+'/')

    def test_scrap_games(self):
        crea_index_games(index_games)
        url_juegos = get_url_juegos(index_news)
        soup_juegos = obten_juegos(url_juegos[:2])
        almacena_juegos(soup_juegos, index_games)

        ix = open_dir(index_games)
        with ix.searcher() as searcher:
            all_games = searcher.doc_count_all()

        self.assertNotEqual(all_games, 0)
