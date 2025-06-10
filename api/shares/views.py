from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from shares.models import Share, FotoShare
from shares.serializers import ShareSerializer, ShareSerializer, ShareUpdateSerializer
from users.models import Usuario
from datetime import datetime

class ShareApiView(APIView):
    """
    Api view para la gestión de shares. 

    métodos: Get, post, update, delete
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ 
        Método get para obtener la lista de shares ya sea compartidos o recibidos

        filtros: fecha.
        """
        tipo = request.query_params.get('tipo')  
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