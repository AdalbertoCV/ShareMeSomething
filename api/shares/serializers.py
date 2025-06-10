from rest_framework import serializers
from shares.models import Share, FotoShare
from users.serializers import UsuarioSerializer
from django.utils import timezone

class FotoShareSerializer(serializers.ModelSerializer):
    """
    Serializador para las fotos del share.
    """

    imagen = serializers.ImageField()

    class Meta:
        model = FotoShare
        fields = ['id', 'imagen']

class ShareSerializer(serializers.ModelSerializer):
    """
    Serializador para listar Shares con fotos y usuarios relacionados.
    """

    remitente = UsuarioSerializer(read_only=True)
    destinatario = UsuarioSerializer(read_only=True)
    fotos = FotoShareSerializer(many=True, read_only=True)

    class Meta:
        model = Share
        fields = [ 'id','titulo','descripcion','categoria','fecha_creacion','remitente','destinatario','fotos']

class ShareUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar título, descripción y categoría de un Share.
    """
    class Meta:
        model = Share
        fields = ['titulo', 'descripcion', 'categoria']

    def validate_categoria(self, value):
        categorias_validas = [opcion[0] for opcion in Share.CATEGORIA_CHOICES]
        if value not in categorias_validas:
            raise serializers.ValidationError("Categoría no válida.")
        return value