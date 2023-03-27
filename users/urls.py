from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadaster/', views.cadaster, name='cadaster'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
