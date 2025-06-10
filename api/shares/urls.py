from django.urls import path
from .views import ShareApiView

urlpatterns = [
    path('shares/', ShareApiView.as_view()),         
]
