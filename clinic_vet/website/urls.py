# website/urls.py

from django.urls import path
from django.views.generic import TemplateView
from . import views # Importa as views do app 'website'
from django.contrib.auth import views as auth_views


urlpatterns = [
    # URL da página inicial, agora gerenciada pelo app 'website'
    # Páginas do Website
    path('', views.home, name='home'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    # Usamos a LogoutView pronta do Django, que redireciona para a home
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 

    # Rota "secreta" que decide para onde redirecionar após o login
    path('redirect/', views.redirect_apos_login, name='redirect_apos_login'),

    # Painéis (Dashboards) de cada tipo de usuário
    path('painel/recepcionista/', views.dashboard_recepcionista, name='dashboard_recepcionista'),
    path('painel/veterinario/', views.dashboard_veterinario, name='dashboard_veterinario'),
    path('painel/tutor/', views.dashboard_tutor, name='dashboard_tutor'),
]