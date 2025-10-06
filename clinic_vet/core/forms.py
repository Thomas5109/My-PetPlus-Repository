from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Cliente, Consulta


# isso aqui ta sem utilidade para falar a real (vai na parte de Views.py, resumindo isso seria usado la)
# Apesar de ter uma modificacao na onde tem a seta, porque o gemini me disse que isso poderia virar bug no futuro 

# --- Formulário para a página de CRIAÇÃO de usuário ---
class UsuarioAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # CORREÇÃO: Definimos explicitamente TODOS os campos que queremos na tela de criação.
        # Isso inclui os de senha, que estavam faltando
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'cpf', 'telefone',
            'data_nascimento', 'sexo', 'endereco'  # <-- CAMPOS ADICIONADOS AQUI
        )        
        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 0000[0]-0000'}),
        }
# O resto do seu arquivo forms.py (UsuarioAdminChangeForm, ClienteAdminForm, etc.)
# está correto e não precisa de nenhuma alteração.

# --- Formulário para a página de EDIÇÃO de usuário ---
class UsuarioAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__'
        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 0000[0]-0000'}),
        }

# --- Formulário para o modelo Cliente ---
class ClienteAdminForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 0000[0]-0000'}),
        }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['animal', 'veterinario', 'data', 'motivo', 'observacoes']
        widgets = {
        'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        veterinario = cleaned_data.get('veterinario')
        
        if data and veterinario:
            # A linha "if qs.exists():" estava faltando! <<<<<<<---------------
            qs = Consulta.objects.filter(data=data, veterinario=veterinario)
            if qs.exists(): # Verifica se a consulta encontrou algo
                raise forms.ValidationError(
                    'Já existe uma consulta agendada neste horário para este veterinário'
                )
        # Não se esqueça de retornar os dados limpos se tudo estiver OK
        return cleaned_data