from django.urls import path
from SISCOSS import views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('ver_estado_solicitud/', views.ver_estado_solicitud.as_view(), name="EstadoSolicitud"),
    path('asignar_encargado_escuela/', views.asignar_encargado_escuela.as_view(), name="AsignarEncargadoEscuela"),
    #path('asignar_encargado_escuela_seleccionar/', views.asignar_encargado_escuela_seleccionar.as_view(), name="AsignarEncargadoEscuelaSeleccionar"),
    path('crear_solicitud/', views.SolicitudCrear.as_view(), name = "CrearSolicitud"),
    #path('maestro/solicitudes/', views.ver_solicitud, name="SolicitudesMaestro"),
    path('crear_servicio/<int:solicitud_id>', views.crear_servicio, name="CrearServicio"),
    path('rechazo_solicitud/<int:solicitud_id>', views.rechazar, name="RechazarSolicitud"),
    path('ajax/cargar-carreras/', views.cargar_carrera, name='ajax_cargar_carrera'),
    path('ajax/cargar-tipos/', views.cargar_tipo, name='ajax_cargar_tipo'),
    #path('ver_estado_soli/', views.ver_estado, name='ver_estado_soli'),
    path('solo_ver/', views.solo_ver, name='SoloVer'),
    #path('crear_maestro/', views.MaestroCrear.as_view(), name="MaestroCrear"),
    path('ver_solicitud/', views.ver_solicitud, name='VerSolicitud'),
]