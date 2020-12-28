from django.shortcuts import render
from game.scrap_games import descarga_juegos

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


def scrap_games(request):
    descarga_juegos(index_games, index_news)
    return render(request, 'game/scrap_game.html')
