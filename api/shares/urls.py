from django.urls import path
from .views import ShareApiView, TipoShareApiView

urlpatterns = [
    path('shares/', ShareApiView.as_view()), 
    path('shares/<int:id>/', ShareApiView.as_view()),
    path('shares/tipos/', TipoShareApiView.as_view())
]
