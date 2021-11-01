from django.urls import path
from CustomUsers import views

urlpatterns = [
    path('login/', views.Login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('despacho/', views.despachador, name="Despacho"),
    path('registro_proyeccion/', views.ProyeccionUserCreate.as_view(), name="ProyeccionReg"),
    path('registro_encargado/', views.EncargadoUserCrear.as_view(), name="EncargadoReg"),
    path('registro_maestro/', views.MaestroUserCrear.as_view(), name="MaestroReg"),
    path('registro_institucion/', views.InstitucionUserCrear.as_view(), name="InstitucionReg"),
]