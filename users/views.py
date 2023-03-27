from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import constants
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from .validators import validate_password, validate_username
from django.contrib.auth.decorators import login_required


def cadaster(request):
    if request.method == 'GET':
        return render(request, 'cadaster.html')

    name = request.POST.get('nome')
    email = request.POST.get('email')
    password = request.POST.get('senha')
    pw_confirmation = request.POST.get('confirmar_senha')

    HAS_EMPTY_FIELD = not name.strip() or not email.strip() \
                      or not password.strip() or not pw_confirmation.strip()
    if HAS_EMPTY_FIELD:
        messages.error(request, 'Não podem haver campos  vazios.')
        return render(request, 'cadaster.html')

    try:
        validate_username(name)
    except Exception as msg:
        msg = list(msg)
        messages.error(request, msg[0])
        return render(request, 'cadaster.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return render(request, 'cadaster.html')
    
    EMAIL_EXISTS = User.objects.filter(email=email).exists()
    if EMAIL_EXISTS:
        messages.error(request, 'O email informado já existe.')
        return render(request, 'cadaster.html')
    
    try:
        validate_password(password, pw_confirmation)
    except Exception as msg:
        msg = list(msg)
        messages.error(request, msg[0])
        return render(request, 'cadaster.html')

    try:
        user = User.objects.create_user(name, email, password)
        user.save()
        messages.success(
            request, f'Cadastrado realizado com sucesso, você já pode fazer login.'
        )
        return redirect('users:login')
    except Exception as error:
        messages.error(request, 'Desculpe, sofremos um erro interno.')
        print(error)
        return render(request, 'cadaster.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    name = request.POST.get('nome')
    password = request.POST.get('senha')

    user = auth.authenticate(request, username=name, password=password)
    if user is None:
        messages.error(request, 'Usuário ou senha incorretos.')
        return render(request, 'login.html')
    
    auth.login(request, user)
    messages.success(request, f'Você entrou como {user}.')
    return redirect('/')


def logout(request):
    messages.info(request, f'{request.user} desconectado')
    auth.logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def home(request):
    return render(request, 'home.html')
