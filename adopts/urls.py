from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_pets, name='list_pets'),
    path('pet/<int:pet_id>/', views.see_pet, name='see_pet'),
    path('solicitation/<int:pet_id>', views.solicitation, name='adoption_request'),
    path('filter/', views.filter_pets, name='filter_pets'),
    path('adoption-process/<int:solicitation_id>/', views.adoption_process, name='adoption_process')
]
