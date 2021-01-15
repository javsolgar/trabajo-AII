from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from application.models import Perfil


# Create your models here.

class Plataforma(models.Model):
    nombre = models.TextField()


class Genero(models.Model):
    nombre = models.TextField()


class Desarrollador(models.Model):
    nombre = models.TextField()

class Jugadores(models.Model):
    jugadores = models.TextField()

class Juego(models.Model):
    titulo = models.TextField()
    url_juego = models.URLField()
    url_imagen = models.URLField()
    jugadores = models.ForeignKey(Jugadores, on_delete=models.CASCADE)
    desarrollador = models.ForeignKey(Desarrollador, on_delete=models.CASCADE)
    plataformas = models.ManyToManyField(Plataforma)
    generos = models.ManyToManyField(Genero)


class Puntuacion(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    valor = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(2)])
