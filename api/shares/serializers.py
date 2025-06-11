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
    
class ShareUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar los datos de un share
    """

    fotos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    fotos_eliminar = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Share
        fields = ['titulo','descripcion','categoria','fotos', 'fotos_eliminar']
        extra_kwargs = {
            'titulo': {'required': False},
            'descripcion': {'required': False},
            'categoria': {'required': False},
        }

    def update(self, instance, validated_data):
        """
        Método para manejar la actualización de los campos del modelo, incluyendo la agregación o eliminación de fotos.
        """

        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.save()

        # si se enviaron nuevas fotos, las creamos.
        fotos_nuevas = validated_data.get('fotos', [])
        for foto in fotos_nuevas:
            FotoShare.objects.create(share=instance, imagen=foto)

        # si se envian fotos a eliminar, manejamos la elimianción.
        fotos_eliminar_ids = validated_data.get('fotos_eliminar', [])
        if fotos_eliminar_ids:
            fotos_a_eliminar = FotoShare.objects.filter(id__in=fotos_eliminar_ids, share=instance)
            for foto in fotos_a_eliminar:
                foto.imagen.delete(save=False)  # Borramos el archivo físico
                foto.delete()  # Borramos la instancia en la base de datos

        return instance