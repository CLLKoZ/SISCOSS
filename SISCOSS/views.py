from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from SISCOSS.forms import InstitucionForm, SolicitudForm, EvaluarSolicitudForm, AEvaluarForm, MaestroCreationForm, UserCustomForm, InstitucionCreationForm
from SISCOSS.models import Solicitud, Escuela, Carrera, Facultad, TipoServicio, EstadoSolicitud, Maestro, MaestroPropio, EstudiantePropio


# Create your views here.

def index(request):
	return render(request, "SISCOSS/index.html")

class ver_estado_solicitud(ListView):
	model = Solicitud
	template_name= 'SISCOSS/ver_estado_solicitud.html'
	
class asignar_encargado_escuela(ListView):
	model = Escuela
	template_name= 'SISCOSS/asignar_encargado_escuela.html'

class asignar_encargado_escuela_seleccionar(ListView):
	model = Maestro
	template_name= 'SISCOSS/asignar_encargado_escuela_seleccionar.html'

class SolicitudCrear(CreateView):
	model = Solicitud
	template_name = 'SISCOSS/solicitud.html'
	form_class = SolicitudForm
	second_form_class = InstitucionForm
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(SolicitudCrear, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			solicitud = form.save(commit=False)
			solicitud.institucion = form2.save()
			solicitud = form.save(commit=True)
			solicitud.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class ver_solicitudes_recibidas(ListView):
	model = Solicitud
	template_name= 'SISCOSS/ver_solicitudes_recibidas.html'

def cargar_carrera(request):
	facultad_id = request.GET.get('facultad_soli')
	carreras = Carrera.objects.filter(facultad_carrera_id=facultad_id).order_by('nombre_carrera')
	return render(request, 'SISCOSS/carreras_drop_list.html', {'carreras': carreras})

def cargar_tipo(request):
	carrera_id = request.GET.get('carrera_soli')
	tipos = TipoServicio.objects.filter(carrera_tipo_id=carrera_id).order_by('nombre_servi')
	return render(request, 'SISCOSS/tipo_drop_list.html', {'tipos': tipos})

def ver_estado(request):
	if request.method=='POST':
		buscar = request.POST['bscr']

		if buscar:
			match = Solicitud.objects.filter(Q(institucion__email_ins=buscar))
			if match:
				return render(request, 'SISCOSS/ver_estado.html', {'br': match})
			else:
				messages.error(request, 'No hay Solicitudes que coinsidan con el Email.')
		else:
			return HttpResponseRedirect('/ver_estado_soli/')

	return render(request, 'SISCOSS/ver_estado.html')

def formulario_evaluar_solicitud(request, id_solicitud):
	solicitud = Solicitud.objects.get(id=id_solicitud)
	if request.method == 'GET':
		form = AEvaluarForm(instance=solicitud)
	else:
		form = AEvaluarForm(request.POST, instance=solicitud)
		if form.is_valid():
			form.save()
		return redirect('SolicitudesRecibidas')
	return render(request, 'SISCOSS/evaluar_solicitud.html', {'form':form, 'solicitud':solicitud})

def ver_soli_facultad(request):
	facultad = Facultad.objects.all()
	if request.method=='POST':
		buscar = request.POST['bscr']

		if buscar:
			match = Solicitud.objects.filter(Q(facultad_soli_id=buscar))
			if match:
				return render(request, 'SISCOSS/ver_solicitud_facultad.html', {'br': match, 'facultad': facultad})
			else:
				messages.error(request, 'No hay solicitudes para esta la facultad seleccionada.')
		else:
			return HttpResponseRedirect('/ver_soli_facultad/')

	return render(request, 'SISCOSS/ver_solicitud_facultad.html', {'facultad':facultad})

class MaestroCrear(CreateView):
	model = MaestroPropio
	template_name = 'SISCOSS/crear_maestro.html'
	form_class = MaestroCreationForm
	second_form_class = UserCustomForm
	model.usuario.is_maestro = True
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(MaestroCrear, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			maestro = form.save(commit=False)
			maestro.usuario = form2.save()
			maestro = form.save(commit=True)
			maestro.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class InstitucionRegistrar(CreateView):
    model = MaestroPropio
    template_name = 'SISCOSS/crear_maestro.html'
    form_class = InstitucionCreationForm
    second_form_class = UserCustomForm
    model.usuario.is_maestro = True
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(InstitucionRegistrar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            maestro = form.save(commit=False)
            maestro.usuario = form2.save()
            maestro = form.save(commit=True)
            maestro.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

def Login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('inicio')
        else:
            error_message = 'UPS! Algo salio mal :(. Ingresa el usuario'
    return render(request, 'SISCOSS/login.html', {'form':form})


#@login_required()
def inicio(request):
    current_user = request.user
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if current_user.type == "MAESTRO":
            return render(request, "inicio.html")
        else:
            return redirect("MaestroCrear")

def logout_view(request):
    logout(request)
    return redirect('login')