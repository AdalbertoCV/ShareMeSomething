from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from shares.models import Share
from shares.serializers import ShareSerializer, ShareCreateSerializer, ShareUpdateSerializer
from datetime import datetime

class ShareApiView(APIView):
    """
    Api view para la gestión de shares. 

    métodos: Get, post, update, delete
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        """ 
        Método get para obtener la lista de shares ya sea compartidos o recibidos

        filtros: fecha.
        """
        if id:
            share = get_object_or_404(Share, id = id)
            if share.remitente == request.user or share.destinatario == request.user:
                serializer = ShareSerializer(share, context={'request':request})
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({'detail':'No tienes permisos para realizar esta acción.'},status = status.HTTP_400_BAD_REQUEST)
        else:
            tipo = request.query_params.get('tipo', 'recibidos')
            fecha = request.query_params.get('fecha')  # YYYY-MM-DD 
            usuario_id = request.query_params.get('usuario_id')  

            if tipo.lower() == "recibidos":
                queryset = Share.objects.filter(destinatario=request.user)
                if usuario_id:
                    queryset = queryset.filter(remitente_id=usuario_id)

            elif tipo.lower() == "compartidos":
                queryset = Share.objects.filter(remitente=request.user)
                if usuario_id:
                    queryset = queryset.filter(destinatario_id=usuario_id)
            else:
                return Response({"detail": "El parámetro 'tipo' debe ser 'recibidos' o 'compartidos'."}, status=status.HTTP_400_BAD_REQUEST)

            if fecha:
                try:
                    fecha_parsed = datetime.strptime(fecha, "%Y-%m-%d").date()
                    queryset = queryset.filter(fecha_creacion__date=fecha_parsed)
                except ValueError:
                    return Response({"detail": "El formato de fecha debe ser YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShareSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
    
    def post(self, request):
        """
        Método post para crear un nuevo share.
        """
        serializer = ShareCreateSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            share = serializer.save()
            serializer_response = ShareSerializer(share, context={'request':request})
            return Response(serializer_response.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """
        Método put para modificar los datos de un share.
        """
        if id:
            share = get_object_or_404(Share, id = id)
            if share.remitente == request.user:
                serializer = ShareUpdateSerializer(share, data = request.data, partial = True)
                if serializer.is_valid():
                    share_actualizado = serializer.save()
                    serializer_response = ShareSerializer(share_actualizado, context={'request':request})
                    return Response(serializer_response.data, status = status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail':'No tienes permisos para realizar esta acción.'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':'El id del Share es requerido para su actualización'},status = status.HTTP_400_BAD_REQUEST)   