# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib import messages

def dashboard(request):
    user_groups = request.user.groups.all()
    if user_groups.exists():
        return redirect('group_home', group_name=user_groups[0].name)
    else:
        messages.error(request, 'Grupo de usuário Invalido!')
        return redirect('logout')