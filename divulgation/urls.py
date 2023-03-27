from django.urls import path
from . import views

urlpatterns = [
    path('new-pet/', views.new_pet, name='new_pet'),
    path('my-pets/', views.my_pets, name='my_pets'),
    path('remove-pet/<int:pet_id>/', views.remove_pet, name='remove_pet'),
    path('see-solicitations/', views.see_solicitations, name='see_solicitations')
]
