from rest_framework import serializers
from users.models import Usuario
from utils.utils import validar_contraseña_segura

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
    
class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para la creación de un nuevo usuario.
    """
    password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "password", "confirm_password","foto_perfil", "descripcion", "pasatiempos"]

    def validate(self, data):
        """
        Método para las validaciones adicionales (passwords)

        params: 
        - data: datos recibidos en la request
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        validar_contraseña_segura(data["password"])
        return data
    
    def create(self, validated_data):
        """
        método para el registro del usuario en la base de datos.

        params: 
        - validated_data: datos validados de la request para realizar el registro
        """

        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
    

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para editar los campos de un usuario
    """
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "foto_perfil", "descripcion", "pasatiempos"]
