from django.contrib import admin
from .models import Cliente, Animal, MedicoVeterinario, Consulta

# Incrivel como 4 comandos me fazem repensar a vontade de fazer essa porra KKAKAKAKKAKAK
# Na moral vei, esses 4 comandos fazem aquela parte toda de administrador rodar 
# (digo no sentido de ser uma interface muito completa), mas é claro que se não fosse 
# pelo models.py que ta bem formado nao daria nem de ligar esse trem, enfim basicamente
# essa parte aqui roda tudo la do ADM, interface, deletar, editar, a porra toda XD
      
admin.site.register(Cliente)
admin.site.register(Animal)
admin.site.register(MedicoVeterinario)
admin.site.register(Consulta)
# Register your models here.

# Aé o Gemini me disse também que isso ai tem como fazer melhor XD, esse 
# de baixo da uma melhorada brava **de acordo com ele

# ░░░░░░░░░░░░▄▄░░░░░░░░░
# ░░░░░░░░░░░█░░█░░░░░░░░
# ░░░░░░░░░░░█░░█░░░░░░░░
# ░░░░░░░░░░█░░░█░░░░░░░░
# ░░░░░░░░░█░░░░█░░░░░░░░
# ███████▄▄█░░░░░██████▄░░
# ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░
# ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░
# ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░
# ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░
# ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░
# ▓▓▓▓▓▓█████░░░░░░░░░█░░
# ██████▀░░░░▀▀██████▀░░░░

# # 1. Crie uma classe de configuração para o seu modelo 
# class ConsultaAdmin(admin.ModelAdmin):
#     """ Define a customização do Admin para o modelo Consulta. """
    
#     # Adiciona colunas na lista de consultas para visualização rápida
#     list_display = ('data', 'animal', 'veterinario', 'motivo')
    
#     # Adiciona um filtro na lateral direita da página
#     list_filter = ('veterinario', 'data')
    
#     # Adiciona uma barra de busca no topo da página
#     search_fields = ('animal__nome', 'motivo')

# # -- Mantenha os outros registros como estão --
# admin.site.register(Cliente)
# admin.site.register(Animal)
# admin.site.register(MedicoVeterinario)

# # 2. Registre o modelo Consulta JUNTO com a sua classe de configuração
# admin.site.register(Consulta, ConsultaAdmin)
