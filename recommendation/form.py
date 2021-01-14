from django import forms

from recommendation.models import Juego


class FormularioPuntuaciones(forms.Form):
    choices = (
        (0, '-'),
        (1, '★'),
        (2, 2 * '★'),
        (3, 3 * '★'),
        (4, 4 * '★'),
        (5, 5 * '★')
    )
    puntuacion = forms.ChoiceField(label='', choices=choices)


def get_choices_game_names():
    choices = []
    juegos = Juego.objects.all()
    for juego in juegos:
        choices.append((juego.id, juego.titulo))
    return tuple(choices)


class FormularioJuegos(forms.Form):
    juego_id = forms.ChoiceField(label='', choices=get_choices_game_names())
