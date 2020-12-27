import os
import urllib.request
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID

index = './indices/IndexNewsVideogames'


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
        url_noticia = soup.find('a')['href']
        urls_noticias.append(url_noticia)
    return urls_noticias


def save_noticias():
    pass


def get_schema():
    return Schema(titulo=TEXT(stored=True),
                  subtitulo=TEXT(stored=True),
                  texto=TEXT(stored=True),
                  escritor=TEXT(stored=True),
                  url_noticia=ID(stored=True),
                  juego=ID(stored=True),
                  url_juego=ID(stored=True))


def crea_index():
    if not os.path.exists(index):
        os.mkdir(index)
    ix = create_in(index, schema=get_schema())


def almacena_noticias(soup_noticias):
    ix = open_dir(index)
    writer = ix.writer()
    for soup in soup_noticias:
        titulo = soup.find('h1').string.strip()
        subtitulo = soup.find('p').string.strip()
        parrafos = soup.find_all('p', class_=['s16', 'fftext', 'c2', 'lh27', 'img100'])[:-1]

        try:
            texto = parrafos[0].text
            if len(parrafos) > 1:
                for parrafo in parrafos[1:]:
                    texto += '\n' + parrafo.text
        except IndexError as e:
            texto = '_'
        except AttributeError as e:
            texto = '_'

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

        writer.add_document(titulo=titulo,
                            subtitulo=subtitulo,
                            texto=texto,
                            escritor=escritor,
                            url_noticia=url_noticia,
                            juego=juego,
                            url_juego=url_juego)
    writer.commit()


def descarga_noticias():

    urls = ['https://www.3djuegos.com/novedades/todo/juegos/0f0f0f0/fecha/',
            'https://www.3djuegos.com/novedades/todo/juegos/1pf0f0f0/fecha/']

    crea_index()
    soup_lista_noticias = obten_lista_noticias(urls)
    urls_noticias = extrae_url_noticias(soup_lista_noticias)
    soup_noticias = obten_info_noticias(urls_noticias)
    almacena_noticias(soup_noticias)
    print('noticias descargadas satisfactoriamente')


if __name__ == '__main__':
    descarga_noticias()
