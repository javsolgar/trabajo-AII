from django.shortcuts import render
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

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
                   juego['plataformas'].replace(',', ', '),
                   juego['desarrollador'],
                   juego['generos'].replace(',', ', '),
                   juego['url_juego'],
                   juego['jugadores'],
                   juego['url_imagen']]

    ix.close()
    return render(request, 'game/show.html', {'juego': res})


def buscar_juegos_titulo(request):
    return render(request, 'game/filtro.html', {'filtro': 'titulo'})


def list_plataformas(request):
    res = []
    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        juegos = searcher.documents()

        for juego in juegos:
            plataformas = juego['plataformas'].split(',')

            for plataforma in plataformas:

                if plataforma not in res:
                    res.append(plataforma)

    ix.close()
    return render(request, 'game/filtro.html', {'opciones': sorted(res), 'filtro': 'plataformas'})


def list_generos(request):
    res = []
    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        juegos = searcher.documents()

        for juego in juegos:
            generos = juego['generos'].split(',')

            for genero in generos:

                if genero not in res:
                    res.append(genero)

    ix.close()
    return render(request, 'game/filtro.html', {'opciones': sorted(res), 'filtro': 'generos'})


def list_games_filtrados(request):
    res = []
    ix = open_dir(index_games)
    respuesta_formulario = request.GET.get('select_filtro')

    if '_' in respuesta_formulario:
        filtro, valor = respuesta_formulario.split('_')
    else:
        filtro = 'titulo'
        valor = respuesta_formulario

    with ix.searcher() as searcher:
        query = QueryParser(filtro, ix.schema).parse(valor)
        juegos = searcher.search(query)
        for juego in juegos:
            url_imagen = juego['url_imagen']
            titulo = juego['titulo']

            res.append([url_imagen, titulo])

    ix.close()
    return render(request, 'game/list.html', {'juegos': res})
