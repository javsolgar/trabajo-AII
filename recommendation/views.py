import shelve

from django.shortcuts import render, get_object_or_404

from application.models import Perfil
from recommendation.form import FormularioPuntuaciones, FormularioJuegos
from application.decorators import authenticated
from recommendation.models import Juego, Puntuacion
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from recommendation.recommendations import topMatches, getRecommendations

index_news = './indices/IndexNewsGames'
index_games = './indices/IndexGames'


@authenticated
def list_games(request):
    juegos = Juego.objects.all()
    cantidad = Juego.objects.count()
    return render(request, 'recommendation/list_game.html', {'juegos': juegos, 'cantidad': cantidad})


@authenticated
def create_rating(request):
    form = FormularioPuntuaciones(request.POST)

    if form.is_valid():
        puntuacion = form.cleaned_data.get('puntuacion')

        juego_id = request.GET.get('id')
        juego = Juego.objects.get(id=juego_id)
        usuario = request.user
        perfil, creado = Perfil.objects.get_or_create(usuario=usuario)
        no_existe_puntuacion = Puntuacion.objects.filter(perfil=perfil, juego=juego).count() == 0

        # Guardar si no existe y no es 0 el valor
        if no_existe_puntuacion and puntuacion != '0':

            rating, creado = Puntuacion.objects.get_or_create(
                perfil=perfil,
                juego=juego,
                valor=puntuacion
            )
        else:
            rating = Puntuacion.objects.get(perfil=perfil, juego=juego)

            # Actualizar si el valor no es 0
            if puntuacion != '0':
                rating.valor = puntuacion
                rating.save()

            # Eliminar si el valor es 0
            else:
                rating.delete()


@authenticated
def show_game(request):
    if request.method == 'POST':
        create_rating(request)

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

    usuario = request.user
    perfil, creado = Perfil.objects.get_or_create(usuario=usuario)

    try:

        puntuacion = Puntuacion.objects.get(juego=juego, perfil=perfil)
        form = FormularioPuntuaciones(initial={'puntuacion': puntuacion.valor})

    except Exception as e:
        form = FormularioPuntuaciones()

    return render(request, 'recommendation/show_game.html',
                  {
                      'juego': juego,
                      'plataformas': plataformas[:-2],
                      'generos': generos[:-2],
                      'noticias': noticias,
                      'form': form
                  }
                  )


@authenticated
def get_ratings(request):
    usuario = request.user
    perfil = Perfil.objects.get(usuario=usuario)

    cantidad = Puntuacion.objects.filter(perfil=perfil).count()
    puntuaciones = []
    if cantidad > 0:
        puntuaciones = Puntuacion.objects.filter(perfil=perfil).all()

    return render(request, 'recommendation/list_ratings.html',
                  {'puntuaciones': puntuaciones, 'cantidad': cantidad})


@authenticated
def recomend_4_similars_games(request):
    form = FormularioJuegos()
    return render(request, 'recommendation/search_game_name.html', {'form': form})


@authenticated
def get_4_similars_games(request):
    form = FormularioJuegos(request.GET, request.FILES)
    if form.is_valid():
        id_juego = form.cleaned_data.get('juego_id')
        juego = get_object_or_404(Juego, pk=id_juego)
        shelf = shelve.open("./recommendation/data/dataRS.dat")
        ItemsPrefs = shelf['ItemsPrefs']
        shelf.close()
        recomendaciones = topMatches(ItemsPrefs, int(id_juego), n=4)
        juegos = []
        for recomendacion in recomendaciones:
            juegos.append(Juego.objects.get(pk=recomendacion[1]))
        return render(request, 'recommendation/juegos_similares.html', {'original': juego, 'juegos': juegos})
    else:
        return render(request, 'recommendation/juegos_similares.html')


@authenticated
def recomend_no_rated_games(request):
    usuario = request.user
    perfil = Perfil.objects.get(usuario=usuario)
    shelf = shelve.open('./recommendation/data/dataRS.dat')
    prefs = shelf['Prefs']
    shelf.close()
    rankings = getRecommendations(prefs, int(perfil.id))
    recomendaciones = rankings[:4]
    juegos = []

    for recomendacion in recomendaciones:
        juegos.append(Juego.objects.get(id=recomendacion[1]))

    if len(juegos) > 0:

        return render(request, 'recommendation/juegos_recomendados.html', {'juegos': juegos})
    else:
        return render(request, 'recommendation/juegos_recomendados.html')
