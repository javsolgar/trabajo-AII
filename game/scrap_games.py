import os
import urllib.request
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD


def get_schema():
    return Schema(titulo=TEXT(stored=True),
                  plataformas=TEXT(stored=True),
                  desarrollador=ID(stored=True),
                  generos=KEYWORD(stored=True),
                  url_juego=ID(stored=True),
                  jugadores=KEYWORD(stored=True),
                  url_imagen=ID(stored=True))


def crea_index_games(index):
    if not os.path.exists(index):
        os.mkdir(index)
    ix = create_in(index, schema=get_schema())


def get_url_juegos(index_news):
    url_juegos = []
    ix = open_dir(index_news)
    with ix.searcher() as searcher:
        noticias = searcher.documents()
        for noticia in noticias:
            if noticia['url_juego'] != '-':
                url_juegos.append(noticia['url_juego'])
    return url_juegos


def obten_juegos(urls):
    soup_juegos = []
    for url in urls:
        f = urllib.request.urlopen(url)
        soup = BeautifulSoup(f, "lxml")

        soup_juegos.append(soup)

    return soup_juegos


def almacena_juegos(soup_juegos, index_games):
    ix = open_dir(index_games)
    writer = ix.writer()
    juegos_almacenados = []
    for soup in soup_juegos:

        ficha = soup.find('div', id='gs_resumen')

        # Título
        titulo = ficha.find('h1', class_='s22').string.strip()

        if not (titulo in juegos_almacenados):

            # Url_juego
            enlace_titulo = soup.find('strong').find_parent()
            url_juego = enlace_titulo['href']

            # Url_imagen
            url_imagen = soup.find('img', class_=['dib', 'mar_b10'])['src']

            # Plataformas
            enlaces_plataformas = enlace_titulo.find_next_sibling() \
                .find('div', class_=['flecha3x5', 'pr', 't5', 'mar_l5', 'mar_r3']) \
                .find_next_siblings()
            plataformas = enlaces_plataformas[0].string.strip()
            for enlace in enlaces_plataformas:
                if enlace.string.strip() != plataformas:
                    plataformas += ',' + enlace.string.strip()

            # Desarolladora
            tabla1 = ficha.find('dl')
            fila_desarrollador = False
            desarrollador = '_'
            for elemento in tabla1:

                if elemento.string == 'Desarrollador:':
                    fila_desarrollador = True
                elif fila_desarrollador:
                    desarrollador = elemento.string.strip()
                    break

            # Jugadores
            tabla2 = ficha.find_all('dl')[1]
            fila_jugadores = False
            jugadores = '-'
            for elemento in tabla2:
                if elemento.string == 'Jugadores:':
                    fila_jugadores = True
                elif fila_jugadores:
                    jugadores = elemento.string.split(' ')[0]
                    break

            # Generos
            try:
                generos = ficha.find('dt', class_='edit_tematicas').find_parent().find('span').string.strip()
                nombre_generos2 = ficha.find('dt', class_='edit_tematicas').find_next_sibling().find_all('a')
                for nombre in nombre_generos2:
                    generos += ',' + nombre.string.strip()
            except AttributeError as e:
                generos = '-'

            # print(titulo)
            writer.add_document(titulo=titulo,
                                plataformas=plataformas,
                                desarrollador=desarrollador,
                                generos=generos,
                                url_juego=url_juego,
                                jugadores=jugadores,
                                url_imagen=url_imagen)
            juegos_almacenados.append(titulo)

    writer.commit()


def descarga_juegos(index_games, index_news):
    crea_index_games(index_games)
    url_juegos = get_url_juegos(index_news)
    soup_juegos = obten_juegos(url_juegos)
    almacena_juegos(soup_juegos, index_games)

    ix = open_dir(index_games)
    with ix.searcher() as searcher:
        all_games = searcher.doc_count_all()
    print(all_games, 'juegos descargados satisfactoriamente')


if __name__ == '__main__':
    index_news = '../indices/IndexNewsGames'
    index_games = '../indices/IndexGames'
    descarga_juegos(index_games, index_news)
