from django.urls import path
from SISCOSS import views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('ver_estado_solicitud/', views.ver_estado_solicitud.as_view(), name="EstadoSolicitud"),
    path('asignar_encargado_escuela/', views.asignar_encargado_escuela.as_view(), name="AsignarEncargadoEscuela"),
    path('asignar_encargado_escuela_seleccionar/', views.asignar_encargado_escuela_seleccionar.as_view(), name="AsignarEncargadoEscuelaSeleccionar"),
    path('solicitud/', views.SolicitudCrear.as_view(), name = "Solicitud"),
    path('ver_solicitudes_recibidas/', views.ver_solicitudes_recibidas.as_view(), name="SolicitudesRecibidas"),
    path('evaluar_solicitud/<int:id_solicitud>/', views.formulario_evaluar_solicitud, name="Evaluar"),
    path('ajax/cargar-carreras/', views.cargar_carrera, name='ajax_cargar_carrera'),
    path('ajax/cargar-tipos/', views.cargar_tipo, name='ajax_cargar_tipo'),
    path('ver_estado_soli/', views.ver_estado, name='ver_estado_soli'),
    path('ver_soli_facultad/', views.ver_soli_facultad, name='VerSoliFacultad')
]