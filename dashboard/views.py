from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from divulgation.models import Raça
from adopts.models import AdoçõesPedido
from django.http import JsonResponse
def dashboard(request):
    return render(request, 'dashboard.html')


@csrf_exempt
def api_adoptions_breed(request):
    breeds = Raça.objects.all()

    total_adoptions = []
    for breed in breeds:
        num_adoptions_per_breed = AdoçõesPedido.objects.filter(
            pet__raça=breed, usuário=request.user, status='AP'
        ).count()
        total_adoptions.append(num_adoptions_per_breed)

    breeds_name = [breed.raça for breed in breeds]        
    data = {
        'número de adoções': total_adoptions,
        'labels': breeds_name
    }
    return JsonResponse(data)
