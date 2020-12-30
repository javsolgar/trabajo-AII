from django.http import HttpResponseForbidden


# Debe ser administrador para acceder a la función
def is_admin(funcion_decorada):
    def funcion_decoradora(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return funcion_decorada(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(request)
    return funcion_decoradora
