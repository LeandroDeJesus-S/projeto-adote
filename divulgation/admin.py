from django.contrib import admin
from .models import Tag, Pet, Raça

# Register your models here.
class RacaAdmin(admin.ModelAdmin):
    ordering = ['raça']
    list_per_page = 20
    search_fields = ['raça']
    list_display = ['id', 'raça']

class PetAdmin(admin.ModelAdmin):
    list_display = [
        'usuário', 'nome', 'raça', 'estado', 'cidade', 'status'
    ]
    list_editable = ['status']

admin.site.register(Raça, RacaAdmin)
admin.site.register(Tag)
admin.site.register(Pet, PetAdmin)
