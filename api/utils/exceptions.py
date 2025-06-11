from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                'detail': 'No autenticado. Por favor inicia sesión.'
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'detail': 'No tienes permisos para acceder a este recurso.'
            }
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'detail': 'Recurso no encontrado.'
            }
    else:
        return Response({
            'detail': 'Ha ocurrido un error interno en el servidor.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response