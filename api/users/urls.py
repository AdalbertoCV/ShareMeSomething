from django.urls import path
from .views import UsuarioApiView

urlpatterns = [
    path('usuarios/', UsuarioApiView.as_view()),         
    #path('usuarios/<int:id>/', UsuarioAPIView.as_view()), 
]
