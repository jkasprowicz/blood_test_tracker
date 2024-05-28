from django.urls import path
from .views import tracker_view, loader_view

urlpatterns = [
    path('enter_page/', tracker_view, name='tracker_view'),
    path('loader_page/', loader_view, name='loader_view'),
]