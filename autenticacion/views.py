from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_full_name()}')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'autenticacion/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
