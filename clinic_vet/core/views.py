from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Animal, Consulta, Cliente
from .forms import ConsultaForm


# =================================================================
# VIEWS PARA RECEPCIONISTA
# =================================================================

def lista_animais(request):
    """
    Exibe uma lista de todos os animais cadastrados no sistema.
    """
    animais = Animal.objects.all()
    return render(request, 'Recepcionista/lista_animais.html', {'animais': animais})


def lista_consultas(request):
    """
    Exibe uma lista de todas as consultas, ordenadas da mais recente para a mais antiga.
    """
    consultas = Consulta.objects.all().order_by('-data')
    return render(request, 'Recepcionista/lista_consultas.html', {'consultas': consultas})


def agendar_consulta(request):
    """
    View para agendamento de novas consultas.
    Permite buscar um cliente por CPF (com ou sem pontuação) e salvar a consulta.
    """

    cliente = None
    animais = None
    form = ConsultaForm()

    if request.method == 'POST':

        # ------------------------------------------------------------
        # BOTÃO "BUSCAR CLIENTE"
        # ------------------------------------------------------------
        if 'buscar' in request.POST:
            cpf_digitado = request.POST.get('cpf', '').strip()
            cpf_limpo = ''.join(filter(str.isdigit, cpf_digitado))  # remove pontos e traços
            print("DEBUG: CPF digitado:", cpf_digitado)
            print("DEBUG: CPF limpo:", cpf_limpo)

            if len(cpf_limpo) != 11:
                messages.error(request, "CPF inválido. Digite os 11 dígitos numéricos.")
            else:
                # Busca o cliente, mesmo que CPF esteja com pontuação
                cliente = Cliente.objects.filter(
                    Q(cpf=cpf_limpo) | Q(cpf__icontains=cpf_limpo)
                ).first()

                if cliente:
                    # Tenta buscar os pets associados
                    try:
                        animais = cliente.animal_set.all()  # use cliente.animais.all() se tiver related_name
                    except Exception:
                        animais = None
                    messages.success(request, f"Cliente {cliente.nome} encontrado com sucesso!")
                else:
                    messages.error(request, f"Nenhum cliente encontrado com o CPF {cpf_limpo}.")

        # ------------------------------------------------------------
        # BOTÃO "SALVAR CONSULTA"
        # ------------------------------------------------------------
        elif 'salvar' in request.POST:
            form = ConsultaForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Consulta agendada com sucesso!')
                return redirect('lista_consultas')
            else:
                messages.error(request, 'Erro ao agendar a consulta. Verifique os dados.')

                # Recupera o cliente atual (CPF vindo de campo oculto)
                cpf_cliente = request.POST.get('cpf_cliente_atual')
                if cpf_cliente:
                    cliente = Cliente.objects.filter(
                        Q(cpf=cpf_cliente) | Q(cpf__icontains=cpf_cliente)
                    ).first()
                    if cliente:
                        try:
                            animais = cliente.animal_set.all()
                        except Exception:
                            animais = None

    return render(request, 'Recepcionista/agendar_consulta.html', {
        'form': form,
        'cliente': cliente,
        'animais': animais,
    })
