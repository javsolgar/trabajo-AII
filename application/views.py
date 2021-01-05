from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from whoosh.index import open_dir

from application.decorators import redirect_if_authenticated
from application.decorators import is_admin
from news_game.scrap_news import descarga_noticias
from game.scrap_games import descarga_juegos

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


def inicio(request):
    return render(request, 'application/inicio.html')


@redirect_if_authenticated
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(username=username, password=password)
            login(request, usuario)

            return render(request, 'application/inicio.html')
        else:
            return render(request, 'registration/sing_up.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'registration/sing_up.html', {'form': form})


@is_admin
def scrap_all(request):
    # Descarga y cuenta noticias
    descarga_noticias(index_news)
    ix = open_dir(index_news)
    with ix.searcher() as searcher:
        noticias = searcher.doc_count_all()

    # Descarga y cuenta juegos
    descarga_juegos(index_games, index_news)
    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        juegos = searcher.doc_count_all()

    return render(request, 'admin/scrap_all.html', {'noticias': noticias, 'juegos': juegos})
