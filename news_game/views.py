from django.shortcuts import render
from django.utils.decorators import method_decorator
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from news_game.scrap_news import descarga_noticias
from application.decorators import is_admin

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


@is_admin
def scrap_news(request):
    descarga_noticias(index_news)

    ix = open_dir(index_news)
    with ix.searcher() as searcher:
        cantidad = searcher.doc_count_all()

    return render(request, 'admin/scrap.html', {'cantidad': cantidad, 'elemento': 'noticias'})


def list_news(request):
    ix = open_dir(index_news)
    res = []
    with ix.searcher() as searcher:
        cantidad = searcher.doc_count()
        noticias = searcher.documents()
        for noticia in noticias:
            titulo = noticia['titulo']
            escritor = noticia['escritor']
            url_noticia = noticia['url_noticia']
            juego = noticia['juego']
            res.append([titulo, escritor, url_noticia, juego])

    ix.close()
    return render(request, 'news_game/list.html', {'noticias': res, 'cantidad': cantidad})


def list_filtrar_juego(request):
    titulo_juego = request.GET.get('juego')
    ix = open_dir(index_news)
    res = []
    with ix.searcher() as searcher:
        query = QueryParser('juego', ix.schema).parse(titulo_juego)
        result = searcher.search(query)

        for noticia in result:
            titulo = noticia['titulo']
            escritor = noticia['escritor']
            url_noticia = noticia['url_noticia']
            juego = noticia['juego']

            res.append([titulo, escritor, url_noticia, juego])

    ix.close()
    return render(request, 'news_game/list.html', {'noticias': res, 'cantidad': len(res)})


def list_games_names(request):
    res = []
    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        juegos = searcher.documents()
        for juego in juegos:
            res.append(juego['titulo'])
    ix.close()
    return render(request, 'news_game/filtro.html', {'juegos': res})
