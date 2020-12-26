from django.shortcuts import render
from news_videogame.scrap_news import descarga_noticias


def scrap_news(request):
    descarga_noticias()
    return render(request, 'news_videogame/scrap_news.html')
