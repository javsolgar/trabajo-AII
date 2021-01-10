import os
import urllib.request
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID


def obten_lista_noticias(urls):
    soup_listas_noticias = []
    for url in urls:
        f = urllib.request.urlopen(url)
        tabla = BeautifulSoup(f, "lxml")
        filas = tabla.find_all('li', class_='li_lin16')

        for noticia in filas:
            soup_listas_noticias.append(noticia)

    return soup_listas_noticias


def obten_info_noticias(urls_noticias):
    soup_noticias = []
    for url_noticia in urls_noticias:
        f = urllib.request.urlopen(url_noticia)
        soup_noticia = BeautifulSoup(f, "lxml")
        soup_noticias.append(soup_noticia)
    return soup_noticias


def extrae_url_noticias(soup_noticias):
    urls_noticias = []
    for soup in soup_noticias:
        tipo = soup.find('span', class_=['upp', 'col_plat', 'b']).string.split(' ')
        if 'Noticia' in tipo:
            url_noticia = soup.find('a')['href']
            urls_noticias.append(url_noticia)
    return urls_noticias


def get_schema():
    return Schema(titulo=TEXT(stored=True),
                  escritor=TEXT(stored=True),
                  url_noticia=ID(stored=True),
                  juego=TEXT(stored=True),
                  url_juego=ID(stored=True),
                  url_imagen=ID(stored=True))


def crea_index(index):
    if not os.path.exists(index):
        os.mkdir(index)
    ix = create_in(index, schema=get_schema())


def almacena_noticias(soup_noticias, index):
    ix = open_dir(index)
    writer = ix.writer()
    for soup in soup_noticias:
        titulo = soup.find('h1').string.strip()

        try:
            escritor = soup.find('a', rel='author').string.strip()
        except AttributeError as e:
            escritor = '-'

        url_noticia = soup.find('span', id='data_compartir')['data-url']

        try:
            juego = soup.find('a', class_=['dtc', 'vam']).string.strip()
        except AttributeError as e:
            juego = '-'

        try:
            url_juego = soup.find('div', class_=['ico_ficha', 'mar_r5']).next_sibling['href']
        except AttributeError as e:
            url_juego = '-'

        url_imagen = soup.find('img', class_=['br3', 'wi100'])['src']
        if 'ficha' in url_imagen:
            url_imagen='-'

        writer.add_document(titulo=titulo,
                            escritor=escritor,
                            url_noticia=url_noticia,
                            juego=juego,
                            url_juego=url_juego,
                            url_imagen=url_imagen)
    writer.commit()


def descarga_noticias(index):
    urls = ['https://www.3djuegos.com/novedades/todo/juegos/0f0f0f0/fecha/',
            'https://www.3djuegos.com/novedades/todo/juegos/1pf0f0f0/fecha/']

    crea_index(index)
    soup_lista_noticias = obten_lista_noticias(urls)
    urls_noticias = extrae_url_noticias(soup_lista_noticias)
    soup_noticias = obten_info_noticias(urls_noticias)
    almacena_noticias(soup_noticias, index)

    ix = open_dir(index)
    with ix.searcher() as searcher:
        all_news = searcher.doc_count_all()
    print(all_news, 'noticias descargadas satisfactoriamente')


if __name__ == '__main__':
    index = '../indices/IndexNewsGames'
    descarga_noticias(index)
