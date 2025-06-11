from rest_framework import serializers
from shares.models import Share, FotoShare
from users.serializers import UsuarioSerializer
from users.models import Usuario

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


class ShareCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para la creación de un nuevo share.
    """

    fotos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    destinatario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Share
        fields = ['titulo','descripcion','categoria','destinatario','fotos']

    def create(self,validated_data):
        """
        Método para manejar la creación del share.
        """
        request = self.context.get('request')
        remitente = request.user  

        fotos_data = validated_data.pop('fotos', [])
        destinatario = validated_data.pop('destinatario')

        share = Share.objects.create(remitente=remitente, destinatario=destinatario, **validated_data)

        for foto in fotos_data:
            FotoShare.objects.create(share=share, imagen=foto)

        return share