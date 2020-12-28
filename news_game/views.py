from django.shortcuts import render
from whoosh.index import open_dir

from news_game.scrap_news import descarga_noticias

index = './indices/IndexNewsGames'


def scrap_news(request):
    descarga_noticias(index)
    return render(request, 'news_game/scrap_news.html')


def list_news(request):
    ix = open_dir(index)
    res = []
    with ix.searcher() as searcher:
        noticias = searcher.documents()
        for noticia in noticias:
            titulo = noticia['titulo']
            escritor = noticia['escritor']
            url_noticia = noticia['url_noticia']
            juego = noticia['juego']

            res.append([titulo, escritor, url_noticia, juego])

    ix.close()
    return render(request, 'news_game/list.html', {'noticias': res})
