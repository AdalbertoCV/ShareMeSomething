from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, UsuarioUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView      
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer    

class UsuarioApiView(APIView):
    """
    Api View para la gestión de los usuarios de la aplicación.

    allowed methods: get, post, put, delete.
    """

    def get_permissions(self):
        """
        Asigna permisos dinámicamente según el método HTTP.
        """
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

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

        # Eliminar la imagen de perfil si existe
        if usuario.foto_perfil:
            usuario.foto_perfil.delete(save=False) 

        usuario.delete()
        return Response({"detail": "Tu cuenta ha sido eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Devuelve 400 en lugar de 401 si hay un error de autenticación
            return Response(
                {"detail": "Credenciales inválidas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    """
    Cierra la sesión del usuario invalidando el refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)