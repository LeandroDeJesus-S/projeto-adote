from django.core.exceptions import ValidationError


def validate_empty_fields(*fields):
    for field in fields:
        if not field:
            raise ValidationError('Não pode haver campos vazios.')


def validate_phone_number(number):
    if not number.isnumeric():
        raise ValidationError(
            'Por favor, digite um número válido.'
        )

    if len(number) > 15:
        raise ValidationError(
            'O numéro deve ter no máximo 15 digitos.'
        )

    if len(number) < 8:
        raise ValidationError(
            'O número não contem o número minimo de caracteres'
        )





def validate_city(city, state_code):
    state_citys = citys(state_code)
    for c in state_citys:
        if city.lower() == c.lower():
            return
    raise ValidationError(
        'Cidade inválida ou incorreta. Verifique se voce escreveu'
        'corretamente, leve em conta também as acentuações.'
    )

if __name__ == '__main__':
    validate_city('boa esperança', 'es')