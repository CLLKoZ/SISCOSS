from django.urls import path
from SISCOSS import views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('ver_estado_solicitud/', views.ver_estado_solicitud, name="EstadoSolicitud"),
]