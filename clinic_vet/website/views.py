# website/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Consulta # Importe seu modelo de Consulta
from datetime import date, timedelta    # Importe o 'date' para pegar a data de hoje

def home(request):
    return render(request, 'website/home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('redirect_apos_login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('redirect_apos_login') # Redireciona para o nosso hub
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
            
    return render(request, 'website/login.html')

# RESTAURANDO a view "inteligente" que faz o redirecionamento
@login_required
def redirect_apos_login(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    elif user.groups.filter(name='Veterinarios').exists():
        return redirect('dashboard_veterinario')
    elif user.groups.filter(name='Recepcionistas').exists():
        return redirect('dashboard_recepcionista')
    else:
        return redirect('dashboard_tutor')

# --- As views dos painéis continuam as mesmas ---
@login_required
def dashboard_recepcionista(request):
    # --- Lógica do Filtro ---
    # Pega o valor do filtro da URL (ex: ?filtro=semana), se não houver, pega da sessão, se não houver, usa 'hoje' como padrão.
    filtro_selecionado = request.GET.get('filtro', request.session.get('filtro_agenda', 'hoje'))

    # Salva a última escolha do usuário na sessão dele
    request.session['filtro_agenda'] = filtro_selecionado

    hoje = date.today()
    consultas = Consulta.objects.all() # Começa com todas as consultas
    filtro_label = "Todas as Consultas" # Título padrão

    # Aplica o filtro de acordo com a escolha
    if filtro_selecionado == 'hoje':
        consultas = consultas.filter(data__date=hoje)
        filtro_label = "Consultas de Hoje"
    elif filtro_selecionado == 'semana':
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        consultas = consultas.filter(data__date__range=[inicio_semana, fim_semana])
        filtro_label = "Consultas desta Semana"
    elif filtro_selecionado == 'mes':
        consultas = consultas.filter(data__year=hoje.year, data__month=hoje.month)
        filtro_label = "Consultas deste Mês"
    elif filtro_selecionado == 'ano':
        consultas = consultas.filter(data__year=hoje.year)
        filtro_label = "Consultas deste Ano"
    
    # Ordena o resultado final pela data
    consultas_filtradas = consultas.order_by('data')

    context = {
        'consultas': consultas_filtradas,
        'filtro_selecionado': filtro_selecionado,
        'filtro_label': filtro_label,
    }
    return render(request, 'website/dashboard_recepcionista.html', context)

@login_required
def dashboard_veterinario(request):
    return render(request, 'website/dashboard_veterinario.html')

@login_required
def dashboard_tutor(request):
    return render(request, 'website/dashboard_tutor.html')