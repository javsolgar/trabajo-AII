from django.http import HttpResponseForbidden
from django.shortcuts import redirect


# Debe ser administrador para acceder a la función
def is_admin(funcion_decorada):
    def funcion_decoradora(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return funcion_decorada(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(request)

    return funcion_decoradora


# Redirige al inicio si el usuario esta authenticado
def redirect_if_authenticated(funcion_decorada):
    def funcion_decoradora(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return funcion_decorada(request, *args, **kwargs)
        else:
            return redirect('/')

    return funcion_decoradora
