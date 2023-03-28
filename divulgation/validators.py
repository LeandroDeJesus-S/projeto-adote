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


def cities(state_code):
    import requests as rq

    api = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_code}/municipios'
    req = rq.get(api).json()
    cities = [i['nome'] for i in req]
    return cities


def validate_city(city, state_code):
    state_cities = cities(state_code)
    for c in state_cities:
        if city.lower() == c.lower():
            return
    raise ValidationError(
        'Cidade inválida ou incorreta. Verifique se voce escreveu'
        'corretamente, leve em conta também as acentuações.'
    )

if __name__ == '__main__':
    validate_city('boa esperança', 'es')