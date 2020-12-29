from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from django.contrib.auth.decorators import user_passes_test

from application.decorators import is_admin
from game.scrap_games import descarga_juegos

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


@is_admin
def scrap_games(request):
    descarga_juegos(index_games, index_news)

    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        cantidad = searcher.doc_count_all()
    return render(request, 'admin/scrap.html', {'cantidad': cantidad, 'elemento': 'juegos'})


def list_games(request):
    ix = open_dir(index_games)
    res = []
    with ix.searcher() as searcher:
        juegos = searcher.documents()
        for juego in juegos:
            url_imagen = juego['url_imagen']
            titulo = juego['titulo']

            res.append([url_imagen, titulo])

    ix.close()
    return render(request, 'game/list.html', {'juegos': res})


def show_game(request, game_title):
    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        query = QueryParser('titulo', ix.schema).parse(game_title)
        result = searcher.search(query)
        for juego in result:
            res = [juego['titulo'],
                   juego['plataformas'],
                   juego['desarrollador'],
                   juego['generos'].replace(',', ', '),
                   juego['url_juego'],
                   juego['jugadores'],
                   juego['url_imagen']]

    ix.close()
    return render(request, 'game/show.html', {'juego': res})
