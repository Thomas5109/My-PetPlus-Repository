from django.core.exceptions import ValidationError
from validate_docbr import CPF
import re # Importe a biblioteca de expressões regulares

def validate_cpf(value):
    """
    Validador para o campo CPF. Garante que o CPF é válido.
    """
    cpf_validator = CPF()
    cpf_digits = ''.join(filter(str.isdigit, str(value)))
    if not cpf_validator.validate(cpf_digits):
        raise ValidationError('CPF inválido.', code='invalid_cpf')

# V----------- ADICIONE ESTA NOVA FUNÇÃO ABAIXO -----------V
def validate_telefone(value):
    """
    Valida se o número de telefone está no formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX.
    """
    # Regex para validar os dois formatos de telefone
    pattern = re.compile(r'^\(\d{2}\) \d{4,5}-\d{4}$')
    if not pattern.match(value):
        raise ValidationError(
            'Número de telefone inválido. Use o formato (XX) XXXXX-XXXX.',
            code='invalid_telefone'
        )