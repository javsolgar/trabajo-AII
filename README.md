[![Build Status](https://www.travis-ci.com/javsolgar/trabajo-AII.svg?branch=main)](https://www.travis-ci.com/javsolgar/trabajo-AII)

# trabajo-AII
Trabajo realizado por Javier Solís García para la asignatura de Acceso Inteligente a la Información.

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

Este módulo otorga al usuario la posibilidad de obtener recomendaciones en función de puntuaciones creadas por él y por otros usuarios. Para ello se han cargado los juegos almacenados en el módulo de Videojuegos en una base de datos de SQLite 3.


### Usuarios registrados:

- admin:
    - usuario: admin
    - contraseña: admin
    
- prueba:
    - usuario: prueba
    - contraseña: 963852741A
  
- prueba2:
    - usuario: prueba2
    - contraseña: 963852741A
  
- prueba3:
    - usuario: prueba3
    - contraseña: 963852741A
  
- prueba3:
    - usuario: prueba3
    - contraseña: 963852741A
    
