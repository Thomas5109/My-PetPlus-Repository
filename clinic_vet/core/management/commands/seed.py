# core/management/commands/seed.py

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import Group
from core.models import Usuario, Cliente, Animal, Consulta, Turno

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando o seeding do banco de dados...')

        # Limpa os dados existentes para evitar duplicatas
        self.stdout.write('Limpando dados antigos...')
        Consulta.objects.all().delete()
        Animal.objects.all().delete()
        Cliente.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()
        Turno.objects.all().delete()

        faker = Faker('pt_BR')

        # --- Cria Grupos ---
        grupo_veterinarios, _ = Group.objects.get_or_create(name='Veterinarios')
        grupo_recepcionistas, _ = Group.objects.get_or_create(name='Recepcionistas')

        # --- Cria Usuários ---
        self.stdout.write('Criando usuários (veterinários e recepcionistas)...')
        veterinarios = []
        for _ in range(3):
            first_name = faker.first_name()
            last_name = faker.last_name()
            user = Usuario.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='123',
                first_name=first_name,
                last_name=last_name,
                cpf=faker.cpf(), # <--- ADICIONE ESTA LINHA
                is_staff=True
            )
            user.groups.add(grupo_veterinarios)
            veterinarios.append(user)

        for _ in range(2):
            first_name = faker.first_name()
            last_name = faker.last_name()
            user = Usuario.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='123',
                first_name=first_name,
                last_name=last_name,
                cpf=faker.cpf(), # <--- ADICIONE ESTA LINHA
                is_staff=True
            )
            user.groups.add(grupo_recepcionistas)

        # --- Cria Clientes (Tutores) ---
        self.stdout.write('Criando clientes (tutores)...')
        clientes = []
        for _ in range(20):
            cliente = Cliente.objects.create(
                nome=faker.name(),
                email=faker.email(),
                cpf=faker.cpf(),
                telefone=faker.phone_number(),
                data_nascimento=faker.date_of_birth(minimum_age=18, maximum_age=80),
                endereco=faker.address()
            )
            clientes.append(cliente)

        # --- Cria Animais ---
        self.stdout.write('Criando pets...')
        animais = []
        racas_cachorro = ['Labrador', 'Golden Retriever', 'Bulldog', 'Poodle', 'Vira-lata']
        racas_gato = ['Siamês', 'Persa', 'Maine Coon', 'Bengal', 'Vira-lata']
        for cliente in clientes:
            for _ in range(random.randint(1, 2)):
                especie = random.choice(['C', 'G'])
                animal = Animal.objects.create(
                    nome=faker.first_name(),
                    dono=cliente,
                    especie=especie,
                    raca=random.choice(racas_cachorro if especie == 'C' else racas_gato),
                    data_nascimento=faker.date_of_birth(minimum_age=0, maximum_age=15),
                    peso=random.uniform(1.0, 40.0)
                )
                animais.append(animal)
        
        # --- Cria Turnos ---
        Turno.objects.create(nome='Manhã', hora_inicio='08:00', hora_fim='12:00')
        Turno.objects.create(nome='Tarde', hora_inicio='14:00', hora_fim='18:00')

        # --- Cria Consultas ---
        self.stdout.write('Agendando consultas...')
        motivos = ['Check-up de rotina', 'Vacinação', 'Dor na pata', 'Problemas de pele', 'Não está comendo']
        for _ in range(40):
            data_consulta = faker.date_time_between(start_date='-30d', end_date='+30d', tzinfo=timezone.get_current_timezone())
            Consulta.objects.create(
                animal=random.choice(animais),
                veterinario=random.choice(veterinarios),
                data=data_consulta,
                motivo=random.choice(motivos)
            )

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
