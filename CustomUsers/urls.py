from django.urls import path
from CustomUsers import views

urlpatterns = [
    path('login/', views.Login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('despacho/', views.despachador, name="Despacho"),
    path('registro_proyeccion/', views.ProyeccionUserCreate.as_view(), name="ProyeccionReg"),
]