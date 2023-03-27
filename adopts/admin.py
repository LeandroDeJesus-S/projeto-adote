from django.contrib import admin
from .models import AdoçõesPedido


class AdoçõesPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'pet', 'usuário', 'data', 'status'
    ]
    list_editable = ['status']

admin.site.register(AdoçõesPedido, AdoçõesPedidoAdmin)
