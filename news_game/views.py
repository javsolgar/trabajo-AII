from django.shortcuts import render
from news_game.scrap_news import descarga_noticias

index = './indices/IndexNewsGames'


def scrap_news(request):
    descarga_noticias(index)
    return render(request, 'news_game/scrap_news.html')
