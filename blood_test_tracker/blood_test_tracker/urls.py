"""
URL configuration for blood_test_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_view
from django.conf.urls.static import static
from django.conf import settings
from .views import login_view, logout_view, nao_autorizado
from profiles.views import dashboard, group_home, graph_exams


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('not-authorized/', nao_autorizado, name='nao_autorizado'),
    path('dashboard/', dashboard, name='dashboard'),
    path('group/<str:group_name>/', group_home, name='group_home'),
    path('grafico_exames/', graph_exams, name='graph_exams'),
    path('', home_view, name='home'),
    path('', include('tracker.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)