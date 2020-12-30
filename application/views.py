from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def inicio(request):
    return render(request, 'application/inicio.html')


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
