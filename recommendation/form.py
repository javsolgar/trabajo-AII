from django import forms


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
