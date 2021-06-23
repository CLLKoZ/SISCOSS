from django.urls import path
from SISCOSS import views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('ver_estado_solicitud/', views.ver_estado_solicitud.as_view(), name="EstadoSolicitud"),
    path('asignar_encargado_escuela/', views.asignar_encargado_escuela.as_view(), name="AsignarEncargadoEscuela"),
    path('solicitud/', views.SolicitudCrear.as_view(), name = "Solicitud"),
    path('ver_solicitudes_recibidas/', views.ver_solicitudes_recibidas.as_view(), name="SolicitudesRecibidas"),
    #path('evaluar_solicitud/', name="Evaluar"),
]