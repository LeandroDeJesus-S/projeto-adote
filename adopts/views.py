from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from divulgation.models import Pet, Raça
from .models import AdoçõesPedido
from divulgation.views import states
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator


def list_pets(request):
    pets = Pet.objects.filter(status='P')
    breeds = Raça.objects.all()
    
    paginator = Paginator(pets, per_page=10)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(num_page)
    
    context = {'page_obj': page_obj, 'breeds': breeds, 'states': states(request)}
    if request.method == 'GET':
        return render(request, 'adopts.html', context)

    context = {'page_obj': page_obj, 'breeds': breeds}
    return render(request, 'adopts.html', context)

def filter_pets(request):
    if request.method == 'POST':
        return redirect(request.META.get('http_referer', '/'))
    
    all_breeds = Raça.objects.all()
    all_states = states(request)
    state = request.GET.getlist('estado', [all_states[0]['id']])[0]
    breed = request.GET.getlist('raca')[0]
    breed = Raça.objects.get(id=breed)
    
    filtered_pets = Pet.objects.filter(estado=state, raça__id=breed.pk, status='P')
    if breed.raça == 'Todas as raças':
        filtered_pets = Pet.objects.filter(estado=state, status='P')
    
    paginator = Paginator(filtered_pets, per_page=10)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(num_page)
    
    context = {
        'page_obj': page_obj, 
        'all_breeds': all_breeds,
        'raca': breed,
        'all_states': all_states,
        'filtered_state': state
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
