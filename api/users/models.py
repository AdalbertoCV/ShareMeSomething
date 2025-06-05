from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.utils import generar_nombre_imagen

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to=generar_nombre_imagen, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    pasatiempos = models.TextField(blank=True)


    def __str__(self):
        return self.username