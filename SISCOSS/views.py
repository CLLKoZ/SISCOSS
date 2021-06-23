from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from SISCOSS.forms import InstitucionForm, SolicitudForm
from SISCOSS.models import Solicitud, Escuela

# Create your views here.

def index(request):
	return render(request, "SISCOSS/index.html")

class ver_estado_solicitud(ListView):
	model = Solicitud
	template_name= 'SISCOSS/ver_estado_solicitud.html'
	
class asignar_encargado_escuela(ListView):
	model = Escuela
	template_name= 'SISCOSS/asignar_encargado_escuela.html'

class SolicitudCrear(CreateView):
	model = Solicitud
	template_name = 'SISCOSS/solicitud.html'
	form_class = SolicitudForm
	second_form_class = InstitucionForm
	success_url = ''

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