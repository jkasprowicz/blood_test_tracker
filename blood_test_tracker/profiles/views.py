# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from tracker.models import ExamResult

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

    # Prepare data for graphs
    graph_data = {}
    for exam in latest_exams:
        if exam.exam_type not in graph_data:
            graph_data[exam.exam_type] = {
                'labels': [],
                'data': []
            }

        # Append data for the current exam_type
        graph_data[exam.exam_type]['labels'].append(exam.data_entrada.strftime('%Y-%m-%d'))
        graph_data[exam.exam_type]['data'].append(exam.results)

    return render(request, 'group_home.html', {
        'user': user,
        'latest_exams': latest_exams,
        'graph_data': graph_data
    })