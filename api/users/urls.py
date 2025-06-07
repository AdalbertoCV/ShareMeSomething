from django.urls import path
from .views import UsuarioApiView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,     
    TokenRefreshView,         
)

urlpatterns = [
    path('usuarios/', UsuarioApiView.as_view()),         
    path('usuarios/<int:id>/', UsuarioApiView.as_view()), 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
]
