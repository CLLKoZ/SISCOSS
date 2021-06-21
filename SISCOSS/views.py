from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
	return render(request, "SISCOSS/index.html")


def ver_estado_solicitud(request):
	return render(request, "SISCOSS/ver_estado_solicitud.html")