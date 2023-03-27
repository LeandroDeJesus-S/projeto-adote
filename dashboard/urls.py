from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api-adoptions-breed/', views.api_adoptions_breed, name="api_adoptions_breed"),
]
