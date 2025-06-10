from django.db import models
from users.models import Usuario
from utils.utils import generar_nombre_imagen_share


CATEGORIA_CHOICES = [
    ('viajes', 'Viajes'),
    ('comida', 'Comida'),
    ('arte', 'Arte'),
    ('musica', 'Música'),
    ('peliculas', 'Películas'),
    ('videojuegos', 'Videojuegos'),
    ('amor', 'Amor'),
    ('amistad', 'Amistad'),
    ('comedia', 'Comedia'),
    ('libros', 'Libros'),
    ('terror', 'Terror'),
    ('redes_sociales', 'Redes Sociales'),
    ('vida_social', 'Vida Social'),
    ('deportes', 'Deportes'),
    ('tecnologia', 'Tecnología'),
    ('tendencias', 'Tendencias'),
    ('salud', 'Salud'),
    ('educacion', 'Educación'),
    ('negocios', 'Negocios'),
]

class Share(models.Model):
    """
    Modelo para el "Share", almacena fotografias y la información más relevante de tus recuerdos favoritos
    con tu amigo.
    """
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices= CATEGORIA_CHOICES)
    remitente = models.ForeignKey(Usuario,related_name='shares_enviados',on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Usuario,related_name='shares_recibidos',on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} de {self.remitente} para {self.destinatario} - {self.fecha_creacion}"
    

class FotoShare(models.Model):
    """
    Relación de las fotografías con el post en cuestión
    """
    share = models.ForeignKey(Share, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=generar_nombre_imagen_share)

    def __str__(self):
        return f"Foto de {self.share.titulo}"