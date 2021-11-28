from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from .forms import UserCustomForm, UserCustomInsForm
from .models import MiUsuario
from django.contrib.auth.decorators import login_required
from SISCOSS.models import EncargadoPropio, MaestroPropio, InstitucionPropio
from SISCOSS.forms import EncargadoForm, MaestroForm, InstitucionForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import *

# Create your views here.
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
                return redirect('Despacho')
        else:
            error_message = 'UPS! Algo salio mal :(. Ingresa el usuario'
    return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def despachador(request):
    current_user = request.user
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if current_user.type == "MAESTRO":
            return redirect('VerSolicitud')
        elif current_user.type == "INSTITUCION":
            return redirect('VerSolicitud')
        elif current_user.type == "ESTUDIANTE":
            return render(request, "SISCOSS/estudiante/solicitudes.html")
        elif current_user.type == "ENCARGADO_FACU":
            return redirect('VerSolicitud')
        elif current_user.type == "PROYECCION_SOC":
            return redirect('VerSolicitud')
        else:
            return redirect('Inicio')

class ProyeccionUserCreate(CreateView):
    model = MiUsuario
    template_name = "proyeccion_registro.html"
    form_class = UserCustomForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ProyeccionUserCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.type = "PROYECCION_SOC"
            usuario = form.save(commit=True)
            usuario.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EncargadoUserCrear(CreateView):
    model = EncargadoPropio
    template_name = 'encargado_registro.html'
    form_class = EncargadoForm
    second_form_class = UserCustomForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(EncargadoUserCrear, self).get_context_data(**kwargs)
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
            encargado = form.save(commit=False)
            usuario = form2.save(commit=False)
            usuario.type = "ENCARGADO_FACU"
            usuario = form2.save(commit=True)
            encargado.usuario = form2.save()
            encargado = form.save(commit=True)
            encargado.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class MaestroUserCrear(CreateView):
    model = MaestroPropio
    template_name = 'maestro_registro.html'
    form_class = MaestroForm
    second_form_class = UserCustomForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MaestroUserCrear, self).get_context_data(**kwargs)
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
            usuario = form2.save(commit=False)
            usuario.type = "MAESTRO"
            usuario = form2.save(commit=True)
            maestro.usuario = form2.save()
            maestro = form.save(commit=True)
            maestro.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class InstitucionUserCrear(CreateView):
    model = InstitucionPropio
    template_name = 'institucion_registro.html'
    form_class = InstitucionForm
    second_form_class = UserCustomInsForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(InstitucionUserCrear, self).get_context_data(**kwargs)
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
            institucion = form.save(commit=False)
            usuario = form2.save(commit=False)
            usuario.type = "INSTITUCION"
            usuario = form2.save(commit=True)
            institucion.usuario = form2.save()
            institucion = form.save(commit=True)
            institucion.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))