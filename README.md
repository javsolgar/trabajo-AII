[![Build Status](https://www.travis-ci.com/javsolgar/trabajo-AII.svg?branch=main)](https://www.travis-ci.com/javsolgar/trabajo-AII)

# trabajo-AII
Trabajo realizado por Javier Solís García para la asignatura de Acceso Inteligente a la Información.

**Índice:**

1. [Objetivos de la aplicación](https://github.com/javsolgar/trabajo-AII#objetivos-de-la-aplicaci%C3%B3n)
2. [Descripción de las partes del proyecto y el uso de las herramientas](https://github.com/javsolgar/trabajo-AII#descripci%C3%B3n-de-las-partes-del-proyecto-y-el-uso-de-las-herramientas)
3. [Manual de uso](https://github.com/javsolgar/trabajo-AII#manual-de-uso)

## Objetivos de la aplicación

Este proyecto tiene dos objetivos claros:

- Crear una página de videojuegos que ofreciera las últimas noticias, junto a información sobre los juegos mencionados en ellas.
- Implementar un sistema de recomendación en el que sus usuarios puedan valorar los juegos, y así poder obtener recomendaciones sobre otros juegos similares.

## Descripción de las partes del proyecto y el uso de las herramientas

Este proyecto puede dividirse en 4 partes o módulos principales:

1. La página en sí misma.
2. El módulo de noticias.
3. El módulo de videojuegos.
4. El módulo de las recomendaciones.

### La página

Como base para el resto de los módulos de la aplicación, se ha desarrollado una página web simple. Esta página tiene habilitada la posibilidad de iniciar sesión y registrarse.

Por otra parte, para el estilo se le ha dado un diseño sencillo, y se han recogido todas las opciones disponibles para el usuario en una barra de navegación superior.

Para el desarrollo de la página, se ha utilizado  Django 3.1.2 y Bootstrap 4

### Noticias

Este módulo alberga las noticias de las 2 primeras páginas de la web [3DJuegos](https://www.3djuegos.com/novedades/todo/juegos/0f0f0f0/fecha/). Estas noticias son almacenadas y permiten listarse para poder verlas todas.

Cada noticia contiene la información sobre su título, su escritor, la URL original de la noticia, la URL a la información del juego en el módulo de juegos, la URL a la página de información del juego en 3DJuegos, y en el caso de que sea posible, la URL de la imagen de la noticia.

Como se puede comprobar, en la página de 3DJuegos no solamente se publican noticias, si no también reportajes, videos u otro tipo de contenido. Por lo que, al obtener las noticias, solamente nos quedamos con las que contienen la palabra “Noticia” de alguna manera en su etiqueta. Adicionalmente, para obtener la información del juego sobre el que trata la noticia, se debe entrar a ver el contenido de la noticia. Este módulo también permite filtrar noticias por los juegos que se tratan en ellas.

Para la descarga de las noticias se ha usado Beautifulsoup 4, para obtener la información de la web, y Whoosh para registrar la información obtenida.

### Videojuegos

Este módulo contiene la información de los juegos mencionados en las noticias que hay registradas previamente en nuestra aplicación web. Para ello lo que se hace es obtener las URLs de los juegos mencionados en las noticias y obtener la información de la ficha del juego en 3DJuegos. Un ejemplo de una ficha podría ser este: [ficha "The Last of Us: Part II"](https://www.3djuegos.com/27868/the-last-of-us-parte-ii/)

De cada juego se registra: su título, la URL de la imagen del juego, las plataformas en las que se puede jugar, su desarrollador, sus géneros, su enlace original, y en el caso de que sea posible, el número de jugadores que tiene. Por otro lado, en la página del juego de nuestra web, se encuentra un botón que redirige al usuario a una lista de noticias sobre el juego en cuestión. Además, el módulo también permite filtrar los juegos por título, plataformas y por géneros.

Al igual que con la descarga de noticias, se ha usado Beautifulsoup 4, para obtener la información de la web, y Whoosh para registrar la información.

### Recomendaciones

Este módulo otorga al usuario la posibilidad de obtener recomendaciones en función de puntuaciones creadas por él y por otros usuarios. Para ello se han cargado los juegos almacenados en el módulo de [videojuegos](https://github.com/javsolgar/trabajo-AII/blob/finalizaci%C3%B3n/README.md#videojuegos) en una base de datos de SQLite 3.

El módulo de recomendaciones permite listar los juegos almacenados en la base de datos, pero con la adición de que estos son puntuables con estrellas. 
Las puntuaciones serán la herramienta que se utilizará para poder realizar las funcionalidades de este módulo, las cuales son: recomendar 4 juegos similares a uno dado, y recomendar juegos no puntuados por un usuario.

Para este módulo se han utilizado SQLite 3 y los sistemas de recomendación vistos en clase.

Para acelerar la carga de los datos iniciales del sistema de recomendación, y asegurar que no se pierden, se ha creado un fichero [initial_data.json](https://github.com/javsolgar/trabajo-AII/blob/main/initial_data.json). Este fichero contiene los datos de 5 usuarios (uno de ellos con permisos de administrador), 35 juegos, 15 tipos de etiquetas de cantidad de jugadores, 28 desarrolladores, 58 géneros, 17 plataformas y 81 puntuaciones a juegos generadas de forma aleatoria.

### Pruebas

Adicionalmente a lo anterior, para comprobar el correcto funcionamiento de la aplicación web, se han implementado pruebas de las vistas y pruebas de interfaz.

Estas pruebas se han automatizado en el repositorio de GitHub con la implementación del sistema de integración continua [Travis](https://github.com/javsolgar/trabajo-AII/blob/main/.travis.yml).
En total se han desarrollado un total de 26 pruebas, en las que se ha utilizado Selenium, DjangoRestFramework y el propio Travis.

Para hacer más fácil la instalación de todos los requisitos para hacer funcionar correctamente la aplicación, se ha creado un fichero [requirements.txt](https://github.com/javsolgar/trabajo-AII/blob/main/requirements.txt) que contiene todas las librerías a instalar. 

## Manual de uso

Nada más acceder a la aplicación, tras clonar el repositorio y ejecutar el comando `pip install -r requirements.txt` para instalar las librerías, y `python ./manage.py runserver` para ejecutar la aplicación, nos encontraremos en el menú de inicio, en el cuál podremos obtener información sobre las cuentas registradas previamente.

Adicionalmente tendremos las siguientes acciones disponibles:
- **Noticias:** se podrá ver la lista de noticias de la web y filtrar las noticias por juegos.
- **Juegos:** se podrá ver la lista de juegos de la web y filtrar los juegos por título, plataforma o género.
- **Acceder:** se podrá iniciar sesión o registrarse.

Si iniciamos sesión, se nos habilitará la sección de **recomendaciones**, desde la que podremos ver la lista de juegos puntuables y acceder a las opciones de; recomendar 4 juegos simulares a uno dado, y recomendar juegos no puntuados por el usuario. Para probar el módulo de recomendaciones, se debe iniciar con el **usuario “prueba”**, ya que el resto de los usuarios, o bien han puntuado ya todos los juegos, o bien no han puntuado los suficientes, lo que puede provocar que el sistema no tenga recomendaciones para ellos.

En el **menú de la cuenta de usuario** se podrá ver la lista de puntuaciones realizadas por el usuario y también aparecerá la opción de cerrar sesión.

Adicionalmente, en el caso de que se inicie sesión como **admin**, también se podrá refrescar el contenido del módulo de juegos y el módulo de noticias, además pasar juegos del módulo de juegos al módulo de recomendaciones, y recargar el propio sistema de recomendación.

### Usuarios registrados:

1. admin:
    - usuario: admin
    - contraseña: admin
    
2. prueba:
    - usuario: prueba
    - contraseña: 963852741A
  
Existen otros 3 usuarios a los que no se les debería de acceder, pero si se desea, comporten la contraseña con el usuario prueba y sus usuarios son: prueba2, prueba3, prueba4
