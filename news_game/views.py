from django.shortcuts import render
from django.utils.decorators import method_decorator
from whoosh.index import open_dir

from news_game.scrap_news import descarga_noticias
from application.decorators import is_admin
index = './indices/IndexNewsGames'


@is_admin
def scrap_news(request):
    descarga_noticias(index)

    ix = open_dir(index)
    with ix.searcher() as searcher:
        cantidad = searcher.doc_count_all()

    return render(request, 'admin/scrap.html', {'cantidad': cantidad, 'elemento': 'noticias'})


def list_news(request):
    ix = open_dir(index)
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
