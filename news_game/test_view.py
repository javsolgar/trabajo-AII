from whoosh.index import open_dir
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from news_game.scrap_news import obten_lista_noticias, obten_info_noticias, crea_index, extrae_url_noticias, \
    almacena_noticias

index = './indices/IndexNewsGames'


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test_scrap_news(self):
        url = ['https://www.3djuegos.com/novedades/todo/juegos/0f0f0f0/fecha/']
        crea_index(index)
        soup_lista_noticias = obten_lista_noticias(url)
        self.assertNotEqual(len(soup_lista_noticias), 0)

        urls_noticias = extrae_url_noticias(soup_lista_noticias)
        self.assertNotEqual(len(urls_noticias), 0)

        soup_noticias = obten_info_noticias(urls_noticias[:2])
        almacena_noticias(soup_noticias, index)

        ix = open_dir(index)
        with ix.searcher() as searcher:
            all_news = searcher.doc_count_all()

        self.assertEqual(all_news, 2)
