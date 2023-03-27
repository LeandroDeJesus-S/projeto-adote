from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from divulgation.models import Pet, Raça
from .models import AdoçõesPedido
from divulgation.views import states
from . import validators
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q


def list_pets(request):
    pets = Pet.objects.filter(status='P')
    breeds = Raça.objects.all()
    context = {'pets': pets, 'breeds': breeds}
    if request.method == 'GET':
        return render(request, 'adopts.html', context)

    context = {'pets': pets, 'breeds': breeds}
    return render(request, 'adopts.html', context)

def filter_pets(request):
    if request.method == 'POST':
        return redirect(request.META.get('http_referer', '/'))
    
    state = request.GET.get('estado')
    breed = request.GET.getlist('raca')[0]
    breed = Raça.objects.get(id=breed)
    all_breeds = Raça.objects.all()

    filtered_pets = Pet.objects.filter(Q(estado=state)|Q(raça__id=breed.pk), status='P')
    if breed.raça == 'Todas as raças':
        filtered_pets = Pet.objects.all()
        
    context = {
        'filtered_pets': filtered_pets, 
        'all_breeds': all_breeds,
        'raca': breed
    }
    return render(request, 'filtered_pets.html', context)


def see_pet(request, pet_id):
    if request.method == 'GET':
        pet = get_object_or_404(Pet, id=pet_id, status='P')
        return render(request, 'ver_pet.html', {'pet': pet})


@login_required(redirect_field_name='users:cadaster')
def solicitation(request, pet_id):
    pet = Pet.objects.filter(id=pet_id, status='P')
    if not pet.exists():
        messages.warning(request, 'Esse pet já foi adotado.')
        return redirect('list_pets')

    redirect_to = request.META.get('http_referer')
    adoption_request = AdoçõesPedido(
        pet=pet.first(), usuário=request.user,

    )
    adoption_request.save()
    messages.success(
        request, 'Solicitação de adoção realizada com sucesso.'
    )
    return redirect(reverse('see_pet', args=[pet_id]))

@login_required(redirect_field_name='users:login')
def adoption_process(request, solicitation_id):
    adopt_req = AdoçõesPedido.objects.get(id=solicitation_id)
    pet = Pet.objects.get(id=adopt_req.pet.id)
    status = request.GET.get('status')
    if status == 'A':
        adopt_req.status = 'AP'
        pet.status = 'A'
        email_message = f'Olá {adopt_req.usuário}, seu pedido de adoção foi aprovado.'
        
    if status == 'R':
        adopt_req.status = 'R'
        email_message = f'Olá {adopt_req.usuário}, seu pedido de adoção foi recusado.'
        
    pet.save()
    adopt_req.save()

    email = send_mail(
        f'Seu pedido de adoção para {adopt_req.pet.nome}',
        email_message,
        'teste@gmail.com',
        [adopt_req.usuário.email,]
    )
    messages.success(request, f'Pedido de adoção para {adopt_req.pet.nome} processado.')
    return redirect('see_solicitations')
