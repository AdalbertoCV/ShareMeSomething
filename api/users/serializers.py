from rest_framework import serializers
from users.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de usuarios
    """
    foto_perfil = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "foto_perfil", "descripcion", "pasatiempos"]

    def get_foto_perfil(self, obj):
        """
        Devuelve la URL completa de la foto de perfil
        """
        request = self.context.get('request')
        if obj.foto_perfil:
            return request.build_absolute_uri(obj.foto_perfil.url)
        return None