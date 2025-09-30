# core/tests.py

from django.test import TestCase
from .models import Cliente, Animal
from datetime import date, timedelta

class ModelTests(TestCase):

    def setUp(self):
        """Prepara o ambiente para cada teste."""
        self.hoje = date.today()

    def test_criar_cliente_e_calcular_idade_corretamente(self):
        """
        Testa se um novo Cliente pode ser criado e se sua idade é calculada corretamente.
        """
        data_nascimento_cliente = self.hoje.replace(year=self.hoje.year - 25)
        
        cliente = Cliente.objects.create(
            nome="João da Silva",
            email="joao.silva@example.com",
            telefone="11987654321",
            data_nascimento=data_nascimento_cliente,
            endereco="Rua Teste, 123"
        )

        self.assertEqual(cliente.nome, "João da Silva")
        self.assertEqual(str(cliente), "João da Silva")
        self.assertEqual(cliente.idade, 25)

    def test_criar_animal_e_associar_dono(self):
        """
        Testa a criação de um Animal, sua idade e a associação com um Cliente (dono).
        """
        data_nascimento_dono = self.hoje.replace(year=self.hoje.year - 30)
        dono = Cliente.objects.create(
            nome="Maria Souza",
            email="maria.souza@example.com",
            telefone="21912345678",
            data_nascimento=data_nascimento_dono
        )

        data_nascimento_animal = self.hoje.replace(year=self.hoje.year - 5)
        animal = Animal.objects.create(
            nome="Rex",
            dono=dono,
            especie="C",
            raca="Labrador",
            data_nascimento=data_nascimento_animal,
            sexo="M"
        )

        self.assertEqual(animal.nome, "Rex")
        self.assertEqual(animal.idade, 5) 
        self.assertEqual(animal.dono.nome, "Maria Souza")
        self.assertEqual(str(animal), "Rex (C)")
        
        self.assertEqual(dono.animais.count(), 1)
        self.assertEqual(dono.animais.first().nome, "Rex")

    def test_idade_na_vespera_do_aniversario(self):
        """
        Testa o caso extremo: a idade um dia ANTES do aniversário.
        """
        # CORREÇÃO: Usamos timedelta para calcular o dia de amanhã de forma segura.
        amanha = self.hoje + timedelta(days=1)
        
        # Agora criamos a data de nascimento baseada no dia de amanhã, 18 anos atrás.
        aniversario_amanha = amanha.replace(year=amanha.year - 18)

        cliente = Cliente.objects.create(
            nome="Ana Véspera",
            data_nascimento=aniversario_amanha
        )
        
        # A pessoa ainda deve ter 17 anos, não 18, pois o aniversário é amanhã.
        self.assertEqual(cliente.idade, 17)