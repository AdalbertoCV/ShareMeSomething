from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer
from django.shortcuts import get_object_or_404

class UsuarioApiView(APIView):
    """
    Api View para la gestión de los usuarios de la aplicación.

    allowed methods: get, post, put, delete.
    """

    def get(self, request, id=None):
        """
        Método get para el listado y visualización de usuarios.
        """
        if id:
            usuario = get_object_or_404(Usuario, id=id)
            serializer = UsuarioSerializer(usuario, context={'request': request})
            return Response(serializer.data)
        else:
            usuarios = Usuario.objects.all()
            serializer = UsuarioSerializer(usuarios, many = True, context={'request': request})
            return Response(serializer.data)
        
    def post(self, request):
        """
        Método post para el registro de un nuevo usuario.
        """
        serializer = UsuarioCreateSerializer(data = request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            response_serializer = UsuarioSerializer(usuario, context = {'request':request})
            return Response(response_serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)