from django.urls import path
from SISCOSS import views

urlpatterns = [
    path('', views.index, name="Inicio"),
]