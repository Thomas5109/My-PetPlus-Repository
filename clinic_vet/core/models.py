from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from datetime import date #Para poder fazer o calculo da idade dos usuarios, clientes e animais

from django.db.models.signals import post_delete
from django.dispatch import receiver


# Este modelo agora gerencia logins e senhas de forma segura
# Parte dos funcionarios
class Usuario(AbstractUser):
    # O AbstractUser já fornece os campos:
    # username, password (seguro, com hash), email, first_name, last_name, is_staff, etc.
    email = models.EmailField(unique=True)
    
    SEXO = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    ]
    
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    endereco = models.TextField(blank=False, null=False)
    
    @property
    def idade(self):
        #Se não tiver data de nascimento, retorna 0
        if not self.data_nascimento:
            return 0
        
        #Calculo mirabolante para calcular a idade
        hoje = date.today()
        idade_calculada = hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return idade_calculada
    
    #Função para comparar o Cpf cadastrado com o dos outros
    def clean(self):
        super().clean()

        #Verifica o Cpf em algum Cliente
        if Cliente.objects.filter(cpf = self.cpf).exists():
            raise ValidationError({'cpf': 'Este CPF já está cadastrado para um cliente.'})
        
        #Verifica o Email (ignorando maiúsculas/minúsculas)
        if self.email and Cliente.objects.filter(email__iexact=self.email).exists():
            raise ValidationError({'email': 'Cliente com este Email já existe.'})

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
        ('S', 'Solteiro(a)'),
        ('C', 'Casado(a)'),
        ('D', 'Divorciado(a)'),
        ('V', 'Viúvo(a)'),
    ]

    ATENDIMENTO = [
        ('W', 'Whatsapp'),
        ('E', 'Email'),
        ('A', 'Ambos'),
    ]
    
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=False, blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO)
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL)
    preferencia_de_atendimento = models.CharField(max_length=1, choices=ATENDIMENTO)
    endereco = models.TextField(blank=False, null=False)

    @property
    def idade(self):
        if not self.data_nascimento:
            return 0
                
        hoje = date.today()
        idade_calculada = hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return idade_calculada

    def clean(self):
        super().clean()

        # 1. Validação do CPF
        if Usuario.objects.filter(cpf = self.cpf).exists():
            raise ValidationError({'cpf': 'Este CPF já está cadastrado para outro usuário.'})
        if Cliente.objects.filter(cpf = self.cpf).exclude(pk = self.pk).exists():
            raise ValidationError({'cpf': 'Este CPF já está cadastrado para um cliente.'})
        
        # 2. Validação do Email (ignorando maiúsculas/minúsculas)
        if self.email:
            if Usuario.objects.filter(email__iexact=self.email).exists():
                raise ValidationError({'email': 'Este e-mail já está cadastrado para um usuário do sistema.'})
            if Cliente.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
                raise ValidationError({'email': 'Cliente com este Email já existe.'})

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
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='animais', blank=False, null=False)
    especie = models.CharField(max_length=1, choices=ESPECIES)
    raca = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    observacoes = models.TextField(blank=True)

    @property
    def idade(self):
        if not self.data_nascimento:
            return 0
                
        hoje = date.today()
        idade_calculada = hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return idade_calculada

    def __str__(self):
        return f"{self.nome} ({self.especie})"
    
class DocumentoAnimal(models.Model):
    """
    Armazena documentos e arquivos relacionados a um animal específico,
    atendendo aos critérios da nova história de usuário.
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='documentos', verbose_name="Animal")
    titulo = models.CharField(max_length=100, help_text="Ex: Hemograma completo - Clínica X", verbose_name="Título/Descrição")
    data_documento = models.DateField(verbose_name="Data do Documento")

     # O upload_to cria uma pasta 'documentos_animais' dentro do seu diretório de media
    arquivo = models.FileField(upload_to='documentos_animais/', verbose_name="Arquivo")

    def __str__(self):
        return f"{self.titulo} ({self.animal.nome})"
    
    class Meta:
        verbose_name = "Documento do Animal"
        verbose_name_plural = "Documentos dos Animais"
        # Ordena os documentos mais recentes primeiro
        ordering = ['-data_documento']

# VINCULE A FUNÇÃO AO SINAL post_delete DO MODELO DocumentoAnimal
@receiver(post_delete, sender=DocumentoAnimal)
def deletar_arquivo_documento(sender, instance, **kwargs):
    """
    Esta função "ouve" o sinal de exclusão do DocumentoAnimal
    e apaga o arquivo associado.
    """
    # A variável 'instance' é o objeto que acabou de ser deletado.
    # O 'if instance.arquivo' garante que não haverá erro se não houver arquivo.
    if instance.arquivo:
        # O método .delete() do campo de arquivo cuida da exclusão do arquivo físico.
        # save=False impede que o modelo tente se salvar novamente, o que não é necessário.
        instance.arquivo.delete(save=False)

# Agenda consulta
class Consulta(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name' : 'Veterinarios'} 
    )

    data = models.DateTimeField(blank=False, null=False)
    motivo = models.TextField(blank=False, null=False)
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
    
# NOVO MODELO PARA OS TURNOS (Critério de Aceite 3 e 6)
class Turno(models.Model):
    """
    Representa um turno de trabalho padrão, com nome, hora de início e fim.
    Ex: Manhã (08:00 - 12:00)
    """
    nome = models.CharField(max_length=50, unique=True, help_text="Ex: Manhã, Tarde, Plantão Noturno")
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        # Formata a hora para exibir sem os segundos
        return f"{self.nome} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fim.strftime('%H:%M')})"

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ['hora_inicio']


# NOVO MODELO PARA A AGENDA DE TRABALHO (Critério de Aceite 1, 2 e 4)
class HorarioTrabalho(models.Model):
    """
    Associa um veterinário a um turno em um dia específico da semana.
    """
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    # ForeignKey para o funcionário. Limitamos a escolha para usuários que pertencem ao grupo 'Veterinarios'
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='horarios_trabalho',
        limit_choices_to={'groups__name': 'Veterinarios'}
    )
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        # O get_dia_semana_display() pega o nome do dia (ex: 'Segunda-feira') em vez do número (0)
        return f"{self.veterinario.get_full_name()} - {self.get_dia_semana_display()} - {self.turno.nome}"

    class Meta:
        verbose_name = "Horário de Trabalho"
        verbose_name_plural = "Horários de Trabalho"
        # Garante que não é possível cadastrar o mesmo turno, no mesmo dia, para o mesmo veterinário duas vezes
        unique_together = ('veterinario', 'dia_semana', 'turno')
        ordering = ['veterinario', 'dia_semana', 'turno__hora_inicio']