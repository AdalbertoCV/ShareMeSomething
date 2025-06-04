from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
from django.shortcuts import get_object_or_404

class UsuarioApiView(APIView):

    def get(self, request, id=None):
        if id:
            usuario = get_object_or_404(Usuario, id=id)
            serializer = UsuarioSerializer(usuario, context={'request': request})
            return Response(serializer.data)
        else:
            usuarios = Usuario.objects.all()
            serializer = UsuarioSerializer(usuarios, many = True, context={'request': request})
            return Response(serializer.data)