from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from SISCOSS.models import Solicitud

# Create your views here.

def index(request):
	return render(request, "SISCOSS/index.html")


class ver_estado_solicitud(ListView):
	model = Solicitud
	template_name= 'SISCOSS/ver_estado_solicitud.html'
	

def asignar_encargado_escuela(request):
	return render(request, "SISCOSS/asignar_encargado_escuela.html")