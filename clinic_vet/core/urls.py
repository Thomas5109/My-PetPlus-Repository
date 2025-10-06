from django.urls import path
from . import views

urlpatterns = [
    path('animais/', views.lista_animais, name='lista_animais'),#acesso da Recepcionista
    path('agendar_consulta/', views.agendar_consulta, name='agendar_consulta'),
    path('consultas/', views.lista_consultas, name='lista_consultas'),#acesso da Recepcionista
]