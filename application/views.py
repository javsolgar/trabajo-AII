from django.shortcuts import render


def inicio(request):
    return render(request, 'application/inicio.html')


def registro(request):
    return render(request, 'registration/sing_up.html')
