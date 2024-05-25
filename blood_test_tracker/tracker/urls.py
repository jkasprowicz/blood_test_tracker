from django.urls import path
from .views import tracker_view

urlpatterns = [
    path('enter_page/', tracker_view, name='tracker_view'),

]