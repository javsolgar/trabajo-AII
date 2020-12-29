from django.http import HttpResponseForbidden


# Debe ser administrador para acceder a la función
def is_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(request)
    return wrapper_func
