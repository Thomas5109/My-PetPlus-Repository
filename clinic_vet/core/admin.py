from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Animal, DocumentoAnimal, Consulta, Turno, HorarioTrabalho

from django.shortcuts import render
from django.urls import reverse

from django.utils.html import format_html
import os 

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

# --- INÍCIO DA NOVA SEÇÃO: ADMINISTRAÇÃO DE ANIMAIS E SEUS DOCUMENTOS ---

# Responsável por mostrar os documentos DENTRO da página de um Animal.
class DocumentoAnimalInline(admin.TabularInline):
    model = DocumentoAnimal
    extra = 1 # Mostra 1 formulário extra para adicionar um novo documento.
    fields = ('titulo', 'data_documento', 'arquivo')

# Responsável por criar uma PÁGINA SEPARADA para gerenciar TODOS os documentos.
@admin.register(DocumentoAnimal)
class DocumentoAnimalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'animal', 'data_documento', 'visualizar_arquivo')
    search_fields = ('titulo', 'animal__nome')
    list_filter = ('animal__especie', 'data_documento')
    autocomplete_fields = ['animal']

 # Método que gera o link para o arquivo
    @admin.display(description="Arquivo")
    def visualizar_arquivo(self, obj):
        # Verifica se o objeto DocumentoAnimal tem um arquivo associado
        if obj.arquivo:
            # Pega o caminho do arquivo e a URL
            file_url = obj.arquivo.url
            # Pega a extensão do arquivo para ver se é uma imagem
            file_extension = os.path.splitext(file_url)[1].lower()
            
            # Se for uma imagem comum, mostra uma miniatura
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-height: 60px; max-width: 100px;" />'
                    '</a>',
                    file_url,
                    file_url
                )
            # Se for outro tipo de arquivo (PDF, etc.), mostra um link de texto
            else:
                return format_html(
                    '<a href="{}" target="_blank">Ver/Baixar Arquivo</a>',
                    file_url
                )
        # Se não houver arquivo, informa o usuário
        return "Sem arquivo"

# A CLASSE ADMIN DE ANIMAL, QUE USA AS OUTRAS DUAS
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dono', 'especie', 'raca', 'documentos')
    search_fields = ('nome', 'dono__nome') # Permite buscar pelo nome do pet ou do dono.
    list_filter = ('especie',)
    inlines = [DocumentoAnimalInline] # Aqui acontece a mágica!

    #Link do documento
    @admin.display(description="Documentos")
    def documentos(self, obj):
        
        #Conta o numero de docs (obj) que o animal tem
        count = obj.documentos.count()

        if count == 0:
            return "Nenhum"        
        # Constrói a URL para a lista de DocumentoAnimal, filtrando pelo ID do animal atual
        url = (
            reverse("admin:core_documentoanimal_changelist")
            + f"?animal__id__exact={obj.id}"
        )
        # Cria o link HTML
        return format_html('<a href="{}">Ver ({})</a>', url, count)

# --- Registro dos Modelos ---
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente)
admin.site.register(Consulta)
