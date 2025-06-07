from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, UsuarioUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

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
            usuarios = Usuario.objects.filter(is_staff=False)
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
    
    def put(self, request, id=None):
        """
        Método put para actualizar la información de un usuario
        """

        if not id:
            return Response({"detail":"El ID es requerido para actualizar."}, status = status.HTTP_400_BAD_REQUEST)
        
        usuario = get_object_or_404(Usuario, id = id, is_staff = False)

        if request.user != usuario:
        
            return Response({"detail": "No tienes permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            usuario = serializer.save()
            response_serializer = UsuarioSerializer(usuario, context={'request': request})
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None):
        """
        Método DELETE para eliminar la cuenta del usuario.
        """
        if not id:
            return Response({"detail": "El ID es requerido para eliminar."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = get_object_or_404(Usuario, id=id, is_staff=False)

        if request.user != usuario:
            return Response({"detail": "No tienes permiso para eliminar esta cuenta."}, status=status.HTTP_403_FORBIDDEN)

        usuario.delete()
        return Response({"detail": "Tu cuenta ha sido eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    """
    Cierra la sesión del usuario invalidando el refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)