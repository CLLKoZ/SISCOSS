from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from SISCOSS.forms import *
from SISCOSS.models import *


# Create your views here.
def index(request):
	return render(request, "SISCOSS/index.html")

class ver_estado_solicitud(ListView):
	model = Solicitud
	template_name= 'SISCOSS/ver_estado_solicitud.html'
	
class asignar_encargado_escuela(ListView):
	model = Escuela
	template_name= 'SISCOSS/asignar_encargado_escuela.html'

#class asignar_encargado_escuela_seleccionar(ListView):
	#model = Maestro
	#template_name= 'SISCOSS/asignar_encargado_escuela_seleccionar.html'

# Creacion de solicitudes por Institucion
@login_required
def solicitud_crear(request):
	current_user = request.user
	ins = InstitucionPropio.objects.filter(id=current_user.id)
	if current_user.type == "INSTITUCION":
		if request.method == 'POST':
			form = SolicitudForm(request.POST)
			if form.is_valid():
				solicitud = form.save(commit=False)
				solicitud.institucion = ins
				solicitud = form.save(commit=True)
				solicitud.save()
			return redirect('VerSolicitud')
		else:
			form = SolicitudForm
		return render(request, 'SISCOSS/institucion/crear_solicitud.html', {'form': form})
	else:
		return redirect('Despacho')

class SolicitudCrear(CreateView, LoginRequiredMixin):
	model = Solicitud
	template_name = "SISCOSS/institucion/crear_solicitud.html"
	form_class = SolicitudForm
	success_url = '/ver_solicitud/'

	def get_context_data(self, **kwargs):
		context = super(SolicitudCrear, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			solicitud = form.save(commit=False)
			usuario = self.request.user
			ins = InstitucionPropio.objects.get(usuario=usuario.id)
			solicitud.institucion = ins
			solicitud = form.save(commit=True)
			solicitud.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

#Ver solicitudes Maestro | Encargado | Proyeccion social | Institucion
@login_required
def ver_solicitud(request):
	current_user = request.user
	if current_user.type == "MAESTRO":
		m = MaestroPropio.objects.get(usuario=current_user.id)
		f = Facultad.objects.get(id=m.facultad.id)
		c = Carrera.objects.get(id=m.carrera.id)
		solicitud = Solicitud.objects.filter(estado_soli="PENDIENTE", facultad_soli_id=f.id, carrera_soli_id=c.id)
		return render(request, 'SISCOSS/maestro/solictud_recibida.html', {'solicitud': solicitud})

	elif current_user.type == "ENCARGADO_FACU":
		e = EncargadoPropio.objects.get(usuario=current_user.id)
		f = Facultad.objects.get(id=e.facultad.id)
		facu_nombre = f.nombre_facu
		carrera = Carrera.objects.filter(facultad_carrera=f.id)
		solicitud = Solicitud.objects.filter(facultad_soli_id=f.id)

		if request.method == 'POST':
			buscar = request.POST['buscar']

			if buscar:
				c = Carrera.objects.get(id=buscar)
				carrera_nombre = c.nombre_carrera
				match = Solicitud.objects.filter(Q(carrera_soli=buscar, facultad_soli=f.id))
				if match:
					return render(request, 'SISCOSS/encargado/solicitudes.html', {'match': match, 'carrera': carrera, 'carrera_nombre': carrera_nombre})
				else:
					messages.error(request, 'No hay solicitudes para la carrera ' + carrera_nombre)
			else:
				return HttpResponseRedirect('/ver_solicitud/')
		return render(request, 'SISCOSS/encargado/solicitudes.html', {'solicitud': solicitud, 'carrera': carrera, 'facu_nombre': facu_nombre})

	elif current_user.type == "PROYECCION_SOC":
		solicitud = Solicitud.objects.all()
		facultad = Facultad.objects.all()

		if request.method == 'POST':
			buscar = request.POST['buscar']

			if buscar:
				f = Facultad.objects.get(id=buscar)
				facu_nombre = f.nombre_facu
				match = Solicitud.objects.filter(Q(facultad_soli=buscar))
				if match:
					return render(request, 'SISCOSS/proyeccion/solicitudes.html', {'match': match, 'facultad': facultad, 'facu_nombre': facu_nombre})
				else:
					messages.error(request, 'No hay solicitudes para la facultad ' + facu_nombre)
			else:
				return HttpResponseRedirect('/ver_solicitud/')
		return render(request, 'SISCOSS/proyeccion/solicitudes.html', {'solicitud': solicitud, 'facultad': facultad})

	elif current_user.type == "INSTITUCION":
		ins = InstitucionPropio.objects.get(usuario=current_user.id)
		solicitud = Solicitud.objects.filter(institucion=ins.id)
		return render(request, 'SISCOSS/institucion/solicitudes.html', {'solicitud': solicitud})

	else:
		redirect('Despacho')

def solo_ver(request):
	current_user = request.user
	if current_user.type == "MAESTRO":
		m = MaestroPropio.objects.get(usuario=current_user.id)
		f = Facultad.objects.get(id=m.facultad.id)
		c = Carrera.objects.get(id=m.carrera.id)
		solicitud = Solicitud.objects.filter(facultad_soli_id=f.id, carrera_soli_id=c.id)
		return render(request, 'SISCOSS/maestro/solo_ver.html', {'solicitud': solicitud})
	else:
		redirect('Despacho')

def cargar_carrera(request):
	facultad_id = request.GET.get('facultad_soli')
	carreras = Carrera.objects.filter(facultad_carrera_id=facultad_id).order_by('nombre_carrera')
	return render(request, 'SISCOSS/carreras_drop_list.html', {'carreras': carreras})

def cargar_tipo(request):
	carrera_id = request.GET.get('carrera_soli')
	tipos = TipoServicio.objects.filter(carrera_tipo_id=carrera_id).order_by('nombre_servi')
	return render(request, 'SISCOSS/tipo_drop_list.html', {'tipos': tipos})

@login_required
def crear_servicio(request, solicitud_id):
	current_user = request.user
	solicitud = Solicitud.objects.get(id=solicitud_id)
	if current_user.type == "MAESTRO":
		if request.method == 'POST':
			form = ServicioSocialForm(request.POST)
			if form.is_valid():
				servicio = form.save(commit=False)
				servicio.solicitud = solicitud
				solicitud.estado_soli = "APROBADA"
				solicitud.save()
				servicio = form.save(commit=True)
				servicio.save()
			return redirect('VerSolicitud')
		else:
			form = ServicioSocialForm()
		return render(request, 'SISCOSS/maestro/crear_servicio.html', {'form': form})
	else:
		return redirect('Despacho')

@login_required
def rechazar(request, solicitud_id):
	current_user = request.user
	solicitud = Solicitud.objects.get(id=solicitud_id)
	if current_user.type == "MAESTRO":
		if request.method == 'GET':
			form = RechazoForm(instance=solicitud)
		else:
			form = RechazoForm(request.POST, instance=solicitud)
			if form.is_valid():
				solicitud = form.save(commit=False)
				solicitud.solicitud = solicitud
				solicitud.estado_soli = "RECHAZADA"
				solicitud = form.save(commit=True)
				solicitud.save()
			return redirect('VerSolicitud')
		return render(request, 'SISCOSS/maestro/rechazo_solicitud.html', {'form': form})
	else:
		return redirect('Despacho')

@login_required
def ver_servicio_social(request):
	current_user = request.user
	if current_user.type == "MAESTRO":
		m = MaestroPropio.objects.get(usuario=current_user.id)
		f = Facultad.objects.get(id=m.facultad.id)
		c = Carrera.objects.get(id=m.carrera.id)
		servicio = ServicioSocial.objects.filter(solicitud__facultad_soli_id=f.id, solicitud__carrera_soli_id=c.id)
		return render(request, 'SISCOSS/maestro/solictud_recibida.html', {'solicitud': solicitud})

	elif current_user.type == "ENCARGADO_FACU":
		e = EncargadoPropio.objects.get(usuario=current_user.id)
		f = Facultad.objects.get(id=e.facultad.id)
		facu_nombre = f.nombre_facu
		carrera = Carrera.objects.filter(facultad_carrera=f.id)
		solicitud = Solicitud.objects.filter(facultad_soli_id=f.id)

		if request.method == 'POST':
			buscar = request.POST['buscar']

			if buscar:
				c = Carrera.objects.get(id=buscar)
				carrera_nombre = c.nombre_carrera
				match = Solicitud.objects.filter(Q(carrera_soli=buscar, facultad_soli=f.id))
				if match:
					return render(request, 'SISCOSS/encargado/solicitudes.html', {'match': match, 'carrera': carrera, 'carrera_nombre': carrera_nombre})
				else:
					messages.error(request, 'No hay solicitudes para la carrera ' + carrera_nombre)
			else:
				return HttpResponseRedirect('/ver_solicitud/')
		return render(request, 'SISCOSS/encargado/solicitudes.html', {'solicitud': solicitud, 'carrera': carrera, 'facu_nombre': facu_nombre})

	elif current_user.type == "PROYECCION_SOC":
		solicitud = Solicitud.objects.all()
		facultad = Facultad.objects.all()

		if request.method == 'POST':
			buscar = request.POST['buscar']

			if buscar:
				f = Facultad.objects.get(id=buscar)
				facu_nombre = f.nombre_facu
				match = Solicitud.objects.filter(Q(facultad_soli=buscar))
				if match:
					return render(request, 'SISCOSS/proyeccion/solicitudes.html', {'match': match, 'facultad': facultad, 'facu_nombre': facu_nombre})
				else:
					messages.error(request, 'No hay solicitudes para la facultad ' + facu_nombre)
			else:
				return HttpResponseRedirect('/ver_solicitud/')
		return render(request, 'SISCOSS/proyeccion/solicitudes.html', {'solicitud': solicitud, 'facultad': facultad})

	elif current_user.type == "INSTITUCION":
		ins = InstitucionPropio.objects.get(usurio=current_user.id)
		solicitud = Solicitud.objects.filter(institucion=ins.id)
		return render(request, 'SISCOSS/institucion/solicitudes.html', {'solicitud': solicitud})

	else:
		redirect('Despacho')