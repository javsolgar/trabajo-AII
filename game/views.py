from django.shortcuts import render
from whoosh.index import open_dir

from game.scrap_games import descarga_juegos

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


def scrap_games(request):
    descarga_juegos(index_games, index_news)
    return render(request, 'game/scrap_game.html')


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
    return render(request, 'game/games_list.html', {'juegos': res})
