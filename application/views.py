import shelve

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from whoosh.index import open_dir

from application.decorators import not_authenticated
from application.decorators import is_admin
from recommendation.models import Juego, Genero, Plataforma, Desarrollador, Jugadores, Puntuacion
from news_game.scrap_news import descarga_noticias
from game.scrap_games import descarga_juegos
from recommendation.recommendations import transformPrefs

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


def inicio(request):
    return render(request, 'application/inicio.html')


@not_authenticated
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

@is_admin
def carga_juegos_bd(request):

    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        juegos = searcher.documents()
        for juego in juegos:

            # Crea generos
            try:
                generos = juego['generos'].split(',')
                generos_objetos = []
                for genero in generos:
                    genero_objeto, creado = Genero.objects.get_or_create(nombre=genero)
                    generos_objetos.append(genero_objeto)
            except Exception as e:
                print(e)

            # Crea plataformas
            try:
                plataformas = juego['plataformas'].split(',')
                plataformas_objetos = []
                for plataforma in plataformas:
                    plataforma_objeto, creado = Plataforma.objects.get_or_create(nombre=plataforma)
                    plataformas_objetos.append(plataforma_objeto)
            except Exception as e:
                print(e)

            # Crea desarrollador
            try:
                desarrollador, creado = Desarrollador.objects.get_or_create(nombre=juego['desarrollador'])
            except Exception as e:
                print(e)

            # Crea jugadores
            try:
                jugadores_objeto, creado = Jugadores.objects.get_or_create(jugadores=juego['jugadores'])
            except Exception as e:
                print(e)

            # Crea juego
            try:
                juego_objeto, creado = Juego.objects.get_or_create(titulo=juego['titulo'],
                                                                   url_juego=juego['url_juego'],
                                                                   url_imagen=juego['url_imagen'],
                                                                   desarrollador=desarrollador,
                                                                   jugadores=jugadores_objeto)
                for genero_obj in generos_objetos:
                    juego_objeto.generos.add(genero_obj)

                for plataforma_obj in plataformas_objetos:
                    juego_objeto.plataformas.add(plataforma_obj)

                juego_objeto.save()
            except Exception as e:
                print(e)

    return render(request, 'admin/guarda_db.html', {'cantidad': Juego.objects.count()})


@is_admin
def carga_rs(request):
    Prefs = {}  # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open('../trabajo-AII/recommendation/data/dataRS.dat')
    puntuaciones = Puntuacion.objects.all()
    for puntuacion in puntuaciones:
        perfil = int(puntuacion.perfil.id)
        juego_id = int(puntuacion.juego.id)
        valor = float(puntuacion.valor)
        Prefs.setdefault(perfil, {})
        Prefs[perfil][juego_id] = valor
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf.close()
    return render(request, 'admin/carga_RS.html')
