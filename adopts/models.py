from django.db import models
from divulgation.models import Pet
from django.contrib.auth.models import User
from datetime import datetime


class AdoçõesPedido(models.Model):
    choices = (
        ('AG', 'Aguardando aprovação'),
        ('AP', 'Aprovado'),
        ('R', 'Recusado'),
    )
    pet = models.ForeignKey(Pet, models.DO_NOTHING)
    usuário = models.ForeignKey(User, models.DO_NOTHING)
    data = models.DateField(default=datetime.now)
    status = models.CharField(max_length=2, choices=choices, default='AG')

    def __str__(self) -> str:
        return self.usuário.username
