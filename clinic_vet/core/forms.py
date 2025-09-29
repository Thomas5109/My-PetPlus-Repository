from django import forms
from .models import Consulta
# isso aqui ta sem utilidade para falar a real (vai na parte de Views.py, resumindo isso seria usado la)
# Apesar de ter uma modificacao na onde tem a seta, porque o gemini me disse que isso poderia virar bug no futuro 
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