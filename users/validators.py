from django.core.exceptions import ValidationError
from string import digits, ascii_uppercase, ascii_lowercase, punctuation
from django.contrib.auth.models import User


def validate_characters(password):
    v = []
    for char in password:
        if char in digits:
            v.append('d')
        if char in ascii_lowercase:
            v.append('l')
        if char in ascii_uppercase:
            v.append('u')
        if char in punctuation:
            v.append('p')
    if 'd' in v and 'l' in v and 'u' in v and 'p' in v:
        return True
    return False


def validate_password(password, pw_confirm):
    if not isinstance(password, str):
        raise ValidationError('a senha precisa ser uma string')
    
    if len(password) < 8:
        raise ValidationError('A senha precisa ter no minimo 8 caracteres.')
    
    if not validate_characters(password):
        raise ValidationError(
            'A senha precisa ter pelomenos um caractere maiusculo, '
            'um minusculo, um número e um simbolo.'
        )
    
    if password != pw_confirm:
        raise ValidationError('As senhas não coincidem.')


def validate_username(username):
    username = username.strip()
    if not isinstance(username, str):
        raise ValidationError('O nome precisa ser uma string')

    if len(username) < 4:
        raise ValidationError(
            'O nome de usuario precisa ter no minimo 4 caracteres.'
        )
    
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        raise ValidationError('Usuário já existe.')
    
    if not username.isalnum():
        raise ValidationError(
            'O nome de usuário só pode conter letrar e números.'
        )


def validate_email(email):
    from django.core import validators

    is_valid = True
    try:
        validators.validate_email(email)
    except:
        is_valid, msg = False, 'E-mail inválido.'

    if User.objects.filter(email=email).exists():
        is_valid, msg = False, 'E-mail já existe.'

    if not is_valid:
        raise ValidationError(msg)
    