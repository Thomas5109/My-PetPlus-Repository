# flake8: noqa
import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    Usuario,
    HorarioTrabalho,
    Cliente,
    Animal,
    DocumentoAnimal,
    Consulta,
    Turno,
)


# =============================================================================
# ADMIN DE USUÁRIO
# =============================================================================

# --- Ações customizadas para Ativar/Desativar ---
@admin.action(description="Ativar usuários selecionados")
def ativar_usuarios(modeladmin, request, queryset):
    """Ação para ativar múltiplos usuários de uma vez."""
    updated_count = queryset.update(is_active=True)
    modeladmin.message_user(
        request, f"{updated_count} usuários foram ativados com sucesso."
    )


@admin.action(description="Desativar usuários selecionados")
def desativar_usuarios(modeladmin, request, queryset):
    """Ação para desativar múltiplos usuários de uma vez."""
    if "post" in request.POST:
        updated_count = queryset.update(is_active=False)
        modeladmin.message_user(
            request, f"{updated_count} usuários foram desativados com sucesso."
        )
        return None

    context = {
        "queryset": queryset,
        "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        "title": "Confirmar Desativação",
    }
    return render(request, "admin/core/acao_confirmar_desativacao.html", context)


# Inline para gerenciar os horários de trabalho
class HorarioTrabalhoInline(admin.TabularInline):
    model = HorarioTrabalho
    extra = 1
    fields = ("dia_semana", "turno")
    autocomplete_fields = ["turno"]


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "get_full_name",
        "get_perfil",
        "idade",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    actions = [ativar_usuarios, desativar_usuarios]
    readonly_fields = ("idade",)
    inlines = [HorarioTrabalhoInline]
    fieldsets = UserAdmin.fieldsets + (
        ("Informações Adicionais", {"fields": ("cpf", "telefone", "data_nascimento", "sexo", "endereco")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações Adicionais",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "cpf",
                    "telefone",
                    "data_nascimento",
                    "sexo",
                    "endereco",
                )
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["cpf"].widget = forms.TextInput(
            attrs={"data-mask": "000.000.000-00"}
        )
        form.base_fields["telefone"].widget = forms.TextInput(
            attrs={"data-mask": "(00) 0000[0]-0000"}
        )
        return form

    @admin.display(description="Perfil")
    def get_perfil(self, obj):
        """Retorna os nomes dos grupos do usuário, separados por vírgula."""
        nomes_dos_grupos = [g.name for g in obj.groups.all()]
        return ", ".join(nomes_dos_grupos) if nomes_dos_grupos else "- Sem Perfil -"

    @admin.display(description="Nome Completo")
    def get_full_name(self, obj):
        """Retorna o nome completo do usuário."""
        return obj.get_full_name()


# =============================================================================
# ADMIN DE CLIENTE
# =============================================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "telefone", "email", "idade")
    search_fields = ("nome", "cpf", "email")


# =============================================================================
# ADMIN DE ANIMAL E DOCUMENTOS
# =============================================================================
class DocumentoAnimalInline(admin.TabularInline):
    model = DocumentoAnimal
    extra = 1
    fields = ("titulo", "data_documento", "arquivo")


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("nome", "dono", "especie", "raca", "documentos")
    search_fields = ("nome", "dono__nome")
    list_filter = ("especie",)
    inlines = [DocumentoAnimalInline]
    autocomplete_fields = ["dono"]

    @admin.display(description="Documentos")
    def documentos(self, obj):
        count = obj.documentos.count()
        if count == 0:
            return "Nenhum"
        url = reverse(
            "admin:core_documentoanimal_changelist"
        ) + f"?animal__id__exact={obj.id}"
        return format_html('<a href="{}">Ver ({})</a>', url, count)


@admin.register(DocumentoAnimal)
class DocumentoAnimalAdmin(admin.ModelAdmin):
    list_display = ("titulo", "animal", "data_documento", "visualizar_arquivo")
    search_fields = ("titulo", "animal__nome")
    list_filter = ("animal__especie", "data_documento")
    autocomplete_fields = ["animal"]

    @admin.display(description="Arquivo")
    def visualizar_arquivo(self, obj):
        if obj.arquivo:
            file_url = obj.arquivo.url
            file_extension = os.path.splitext(file_url)[1].lower()
            if file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-height: 60px; max-width: 100px;" />'
                    "</a>",
                    file_url,
                    file_url,
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank">Ver/Baixar Arquivo</a>', file_url
                )
        return "Sem arquivo"


# =============================================================================
# ADMIN DE AGENDA (CONSULTAS E TURNOS)
# =============================================================================
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("animal", "veterinario", "data", "motivo")
    search_fields = ("animal__nome", "veterinario__username", "motivo")
    list_filter = ("data", "veterinario")
    autocomplete_fields = ["animal", "veterinario"]


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("nome", "hora_inicio", "hora_fim")
    search_fields = ("nome",)