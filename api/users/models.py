from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    pasatiempos = models.TextField(blank=True)


    def __str__(self):
        return self.username