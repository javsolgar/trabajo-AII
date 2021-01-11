from django.shortcuts import render

from application.decorators import authenticated
from recommendation.models import Juego
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


@authenticated
def list_games(request):
    juegos = Juego.objects.all()
    cantidad = Juego.objects.count()
    return render(request, 'recommendation/list_game.html', {'juegos': juegos, 'cantidad': cantidad})


@authenticated
def show_game(request):
    id = request.GET.get('id')
    juego = Juego.objects.get(id=id)
    plataformas = ''
    for plataforma in juego.plataformas.all():
        plataformas += plataforma.nombre + ', '

    generos = ''
    for genero in juego.generos.all():
        generos += genero.nombre + ', '

    noticias = False

    ix = open_dir(index_news)
    with ix.searcher() as searcher:
        query = QueryParser('juego', ix.schema).parse(juego.titulo)
        results = searcher.search(query)
        for resultado in results:
            if resultado['titulo'] != '':
                noticias = True
                break
    ix.close()

    return render(request, 'recommendation/show_game.html',
                  {'juego': juego, 'plataformas': plataformas[:-2], 'generos': generos[:-2], 'noticias':noticias})
