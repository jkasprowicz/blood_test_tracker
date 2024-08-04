# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from tracker.models import ExamResult
from fuzzywuzzy import process
import json
import re

def normalize_exam_name(exam_name, existing_names):
    # Find the best match for the exam name from the existing names
    best_match, score = process.extractOne(exam_name, existing_names)
    if score > 80:  # Threshold for similarity
        return best_match
    return exam_name.lower()

def extract_numeric_value(result):
    # Use regex to find numeric value in the result string
    match = re.search(r'[\d,.]+', result)
    if match:
        # Convert the matched string to a float
        return float(match.group(0).replace(',', '.'))
    return None

def dashboard(request):
    user_groups = request.user.groups.all()
    if user_groups.exists():
        return redirect('group_home', group_name=user_groups[0].name)
    else:
        messages.error(request, 'Grupo de usuário Invalido!')
        return redirect('logout')
    

@login_required
def group_home(request, group_name):
    user = request.user
    latest_exams = ExamResult.objects.filter(user=user).order_by('-uploaded_at')[:5]

    return render(request, 'group_home.html', {
        'user': user,
        'latest_exams': latest_exams,
    })



def graph_exams(request):
    return render(request, 'grafico_exames.html')

