from django.shortcuts import render

from application.decorators import authenticated
from recomendation.models import Juego

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'

@authenticated
def list_games(request):
    juegos = Juego.objects.all()
    cantidad = Juego.objects.count()
    return render(request, 'recomendation/list_game.html', {'juegos': juegos, 'cantidad': cantidad})



