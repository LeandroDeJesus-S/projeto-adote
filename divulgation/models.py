from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Raça(models.Model):
    raça = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.raça


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.tag


class Pet(models.Model):
    status_choices = (('P', 'Para adoção'), ('A', 'Adotado'))

    usuário = models.ForeignKey(User, models.DO_NOTHING)
    foto = models.ImageField(
        upload_to='pets', validators=[FileExtensionValidator(['png',
                                                             'jpeg',
                                                             'webp'])]
    )
    nome = models.CharField(max_length=300)
    descrição = models.TextField()
    estado = models.CharField(max_length=164)
    cidade = models.CharField(max_length=164)
    telefone = models.CharField(max_length=15)
    tags = models.ManyToManyField(Tag)
    raça = models.ForeignKey(Raça, models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices)

    def __str__(self) -> str:
        return self.nome
