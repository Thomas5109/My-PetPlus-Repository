from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Animal, Consulta, Cliente
from .forms import ConsultaForm

# essa parte toda é da Recepcionista 
def lista_animais(request):
    animais = Animal.objects.all()
    return render(request, 'Recepcionista/lista_animais.html', {'animais': animais})

def lista_consultas(request):
    consultas = Consulta.objects.all().order_by('-data')
    return render(request, 'Recepcionista/lista_consultas.html', {'consultas': consultas})

#----------------------------------
#essa parte toda é do administrador 
# EDIT: ERREi fui mlk, esse trem ate agr n foi usado pra nada, literalmente se tu apagar nem diferenca faz (so de erro de sintaxe), 
# pelo que entendi isso era pra ser a parte onde a recepcionista cadastra, o ADM tem aquele admin.site.register(----)
# que basicamente deixa ele pronto, toda aquela interface do ADM é literalmente feita so do admin.site.register(----),
# so com aquela linha o adm tem poder de alterar/remover qualquer coisa do codigo XD, resumindo o agendar consulta ta totalmente inutilizado
# ja que a recepcionista nao tem essa permissao e o ADM literalmente so precisa de uma linha de codigo para ter uma interface completa
# XDD
  

def agendar_consulta(request):
    cliente = None
    animais = None
    form = ConsultaForm()

    if request.method == 'POST':
        # Botão buscar cliente
        if "buscar" in request.POST:
            cpf = request.POST.get("cpf")
            cliente = Cliente.objects.filter(cpf=cpf).first()  # evita erro de múltiplos
            if cliente:
                animais = cliente.animal_set.all()  # pegar os animais do cliente
            else:
                messages.error(request, "Cliente não encontrado.")

        # Botão salvar consulta
        elif "salvar" in request.POST:
            form = ConsultaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Consulta agendada com sucesso!')
                return redirect('lista_consultas')
            else:
                messages.error(request, 'Erro ao agendar a consulta. Verifique os dados.')

    return render(request, 'Administrador/agendar_consulta.html', {
        'form': form,
        'cliente': cliente,
        'animais': animais
    })



