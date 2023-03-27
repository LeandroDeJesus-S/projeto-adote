from django.shortcuts import render, redirect
from .models import Tag, Raça, Pet
import requests as rq
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import validators
from django.shortcuts import get_object_or_404
from adopts.models import AdoçõesPedido
from django.core.paginator import Paginator
from django.http import JsonResponse

def states(request) -> list:
    try:
        site = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/'
        req = rq.get(site).json()
        states = sorted([{'estado': i['nome'], 'id': i['sigla']} for i in req], key=lambda i: i['estado'])
        return states
    except rq.exceptions.ConnectionError:
        messages.error(
            request, 'Estamos com um problema interno no momento, sentimos muito.'
        )
        return []

def cities(state_code):
    import requests as rq

    api = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_code}/municipios'
    req = rq.get(api).json()
    cities = [i['nome'] for i in req]
    return cities


@login_required(login_url='users:login')
def new_pet(request):
    TAGS = Tag.objects.all()
    RACAS = Raça.objects.order_by('raça')
    STATES = states(request)
    context = {'tags': TAGS, 'racas': RACAS, 'estados': STATES}
    has_state = request.POST.get('has_state')
    if has_state:
        context.update({'cidades': city(STATES)})
    if not STATES:
        return render(request, 'newpet.html', context)

    if request.method == 'GET':
        return render(request, 'newpet.html', context)
    
    photo = request.FILES.get('foto')
    name = request.POST.get('nome')
    description = request.POST.get('descricao')
    state = request.POST.get('estado')
    city = request.POST.get('cidade')
    phone = request.POST.get('telefone')
    tags = request.POST.getlist('tags')
    raca = request.POST.get('raca')
    raca = Raça.objects.get(id=raca)
    
    try:
        validators.validate_empty_fields(
            photo, name, description, state,
            city, phone, raca, tags
        )
        # validators.validate_city(city, state)
        validators.validate_phone_number(phone)
    except Exception as msg:
        msg = list(msg)
        messages.error(request, *msg)
        return render(request, 'newpet.html', context)
    
    pet = Pet(
        usuário=request.user, foto=photo, nome=name, descrição=description,
        estado=state, cidade=city, telefone=phone, raça=raca
    )
    # pet.save()

    for tag in tags:
        tag_name = Tag.objects.get(id=tag)
        pet.tags.add(tag_name)
    # pet.save()
    
    messages.success(request, f'Pet "{name}" adicionado com sucesso.')
    return redirect('see_pet', pet_id=pet.id)


@login_required(login_url='users:login')
def my_pets(request):
    pets = Pet.objects.filter(usuário=request.user)
    CONTEXT = {'pets': pets}
    if request.method == 'GET':
        return render(request, 'mypets.html', CONTEXT)


@login_required(login_url='users:login') 
def remove_pet(request, pet_id):
    pet_to_del = get_object_or_404(Pet, id=pet_id)
    if pet_to_del.usuário != request.user:
        msg = 'Você não tem permissão para deletar este pet.'
        messages.error(request, msg)
        return redirect('my_pets')

    PET_NAME = pet_to_del.nome
    pet_to_del.delete()
    messages.success(request, f'O pet {PET_NAME} foi deletado.')
    return redirect('my_pets')


@login_required(login_url='users:login')
def see_solicitations(request):
    if request.method == 'GET':
        solicitations = AdoçõesPedido.objects.filter(status='AG', usuário=request.user)
        paginator = Paginator(solicitations, 8)
        actual_page_num = request.GET.get('page')
        page_obj = paginator.get_page(actual_page_num)
        return render(request, 'see_solicitations.html', {
            'page_obj': page_obj
        })
