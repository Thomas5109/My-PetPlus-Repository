from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Animal, Consulta, Turno, HorarioTrabalho

# Inline para gerenciar os horários de trabalho diretamente na página do usuário
class HorarioTrabalhoInline(admin.TabularInline):
    model = HorarioTrabalho
    # 'extra' define quantos campos em branco para novos horários aparecem por padrão
    extra = 1
    # Define os campos que aparecerão no inline
    fields = ('dia_semana', 'turno')
    # Melhora a performance carregando o turno relacionado de forma mais eficiente
    autocomplete_fields = ['turno']

class UsuarioAdmin(UserAdmin):
    # Mostra campos extras para que apareçam na tela de edição do admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'idade')
    list_filter = ('is_staff', 'is_active', 'groups')

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

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'hora_inicio', 'hora_fim')
    # Adiciona uma barra de busca para facilitar encontrar os turnos
    search_fields = ('nome',)

# Registre seus modelos para que apareçam na área de admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente)
admin.site.register(Animal)
admin.site.register(Consulta)
