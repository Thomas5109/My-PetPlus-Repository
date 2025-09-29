from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
# isso aqui sao basicamente tabelas de Sql antes de virarem algo, tipo aqueles construtores em Java
# ou até mesmo os Structs do C, mas mais pro Java com toda certeza 

# Este modelo agora gerencia logins e senhas de forma segura

# Parte dos funcionarios
class Usuario(AbstractUser):
    # O AbstractUser já fornece os campos:
    # username, password (seguro, com hash), email, first_name, last_name, is_staff, etc.

    SEXO = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    ]
    
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    endereco = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username

# Parte dos clientes
class Cliente(models.Model):
    
    SEXO = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    ]
    
    ESTADO_CIVIL = [
        ('S', 'Solteiro (a)'),
        ('C', 'Casado (a)'),
        ('D', 'Divorciado (a)'),
        ('V', 'Viúvo (a)'),
    ]
    
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=11, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL)
    endereco = models.TextField()
    
    def __str__(self):
        return self.nome
    
# Tabelinha de animais
class Animal(models.Model):
    ESPECIES = [
        ('C', 'Cachorro'),
        ('G', 'Gato'),
        ('O', 'Outros'),
    ]

    SEXO = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    nome = models.CharField(max_length=100)
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='animais', null=True, blank=True)
    especie = models.CharField(max_length=1, choices=ESPECIES)
    raca = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)

    def __str__(self):
        return f"{self.nome} ({self.especie})"
    
# Agenda consulta
class Consulta(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name' : 'Veterinarios'} 
    )

    data = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField()
    observacoes = models.TextField(blank=True)

    def clean(self):
        # A lógica de verificação continua funcionando perfeitamente!
        if self.pk is None and Consulta.objects.filter(
            data=self.data, veterinario=self.veterinario).exists():
            raise ValidationError('Já existe uma consulta agendada para este horário com este veterinário.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        # Acessamos o nome do usuário com 'username' ou 'get_full_name()'
        vet_nome = self.veterinario.get_full_name() if self.veterinario else "A definir"
        return f"Consulta de {self.animal.nome} com Dr(a). {vet_nome} em {self.data.strftime('%d/%m/%Y às %H:%M')}"
