from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Animal, Consulta, Turno, HorarioTrabalho

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# --- Ações customizadas para Ativar/Desativar ---
@admin.action(description="Ativar usuários selecionados")
def ativar_usuarios(modeladmin, request, queryset):
    """Ação para ativar múltiplos usuários de uma vez."""
    updated_count = queryset.update(is_active=True)
    # Adiciona a mensagem de sucesso para o admin
    modeladmin.message_user(request, f"{updated_count} usuários foram ativados com sucesso.")

@admin.action(description="Desativar usuários selecionados")
def desativar_usuarios(modeladmin, request, queryset):
    """Ação para desativar múltiplos usuários de uma vez."""

    if 'post' in request.POST:
        # O usuário confirmou, então execute a ação
        updated_count = queryset.update(is_active=False)
        modeladmin.message_user(request, f"{updated_count} usuários foram desativados com sucesso.")
        # Retorne None para que o Django redirecione de volta para a lista
        return None

    # Se ainda não foi confirmado, mostre a página de confirmação
    context = {
        'queryset': queryset,
        'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        'title': 'Confirmar Desativação',
    }
    return render(request, 'admin/core/acao_confirmar_desativacao.html', context)


# Inline para gerenciar os horários de trabalho (mantido da US-04)
class HorarioTrabalhoInline(admin.TabularInline):
    model = HorarioTrabalho
    extra = 1
    fields = ('dia_semana', 'turno')
    autocomplete_fields = ['turno']

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'idade')
    list_filter = ('is_staff', 'is_active', 'groups')

    # Campos que serão exibidos na lista de usuários
    list_display = (
        'username', 
        'email', 
        'get_full_name',  # Exibe o nome completo
        'get_perfil',     # NOVO: Exibe o perfil (grupo)
        'is_active'       # Exibe o status Ativo/Inativo
    )

    # Filtros que aparecem na barra lateral direita
    list_filter = ('is_active', 'groups')

    # Adiciona a barra de busca (já estava funcionando, mas é bom deixar explícito)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Adiciona as ações customizadas ao dropdown "Ação"
    actions = [ativar_usuarios, desativar_usuarios]

    # Mostra a idade como um campo não editável na página de edição
    readonly_fields = ('idade',)

    # CORREÇÃO: Remova 'idade' daqui, pois não é um campo editável
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('cpf', 'telefone', 'data_nascimento', 'sexo', 'endereco')}),
    )
    
    # E daqui também
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('first_name', 'last_name', 'email', 'cpf', 'telefone', 'data_nascimento', 'sexo', 'endereco')}),
    )

    # Adiciona o inline à página de edição do usuário
    inlines = [HorarioTrabalhoInline]

    # --- Métodos customizados para a list_display ---
 
    @admin.display(description="Perfil")
    def get_perfil(self, obj):
        """Retorna os nomes dos grupos do usuário, separados por vírgula."""
        # Pega todos os grupos do usuário e extrai apenas o nome de cada um
        nomes_dos_grupos = [g.name for g in obj.groups.all()]
        return ", ".join(nomes_dos_grupos) if nomes_dos_grupos else "- Sem Perfil -"

    @admin.display(description="Nome Completo")
    def get_full_name(self, obj):
        """Retorna o nome completo do usuário."""
        return obj.get_full_name()


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'hora_inicio', 'hora_fim')
    search_fields = ('nome',)

# --- Registro dos Modelos ---
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente)
admin.site.register(Animal)
admin.site.register(Consulta)
