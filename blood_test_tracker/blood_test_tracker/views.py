from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Login e/ou senha inválido(s). Tente Novamente.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def nao_autorizado(request):
    return render(request, 'not-authorized.html')