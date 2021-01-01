from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from application.decorators import redirect_if_authenticated


def inicio(request):
    return render(request, 'application/inicio.html')


@redirect_if_authenticated
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(username=username, password=password)
            login(request, usuario)

            return render(request, 'application/inicio.html')
        else:
            return render(request, 'registration/sing_up.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'registration/sing_up.html', {'form': form})
