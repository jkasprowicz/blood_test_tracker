from django.shortcuts import render

# Create your views here.


def tracker_view(request):
    return render(request, 'enter_page.html')

def loader_view(request):
    return render(request, 'loader_page.html')