# appTiindux/urls.py
from django.urls import path
from .views import setup_connection, select_query, usuarios_por_curso

urlpatterns = [
    path('login/', setup_connection, name='login'),
    path('Consulta/', select_query, name='Consulta'),
    path('usuarios_por_curso/', usuarios_por_curso, name='usuarios_por_curso'),

]
