from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import *

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud

		fields = [
			'facultad_soli',
			'carrera_soli',
			'tipo_servi_soli',
		]

		labels = {
			'facultad_soli': 'Seleccione la facultad: ',
			'carrera_soli': 'Seleccione la carrera: ',
			'tipo_servi_soli': '¿Qué tipo de servicio social desea?',
		}

		widgets = {
			'facultad_soli': forms.Select(attrs={'class': 'form-control'}),
			'carrera_soli': forms.Select(attrs={'class': 'form-control'}),
			'tipo_servi_soli': forms.Select(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['carrera_soli'].queryset = Carrera.objects.none()
		self.fields['tipo_servi_soli'].queryset = TipoServicio.objects.none()

		if 'facultad_soli' in self.data:
			try:
				facultad_id = int(self.data.get('facultad_soli'))
				self.fields['carrera_soli'].queryset = Carrera.objects.filter(facultad_carrera_id=facultad_id).order_by('nombre_carrera')
			except (ValueError, TypeError):
				pass #Invalida la entrada del usuario, ignora y regresa un query vacio en facultad
		elif self.instance.pk:
			self.fields['carrera_soli'].queryset = self.instance.facultad_soli.carrera_soli_set.order_by('nombre_carrera')

		if 'carrera_soli' in self.data:
			try:
				carrera_id = int(self.data.get('carrera_soli'))
				self.fields['tipo_servi_soli'].queryset = TipoServicio.objects.filter(carrera_tipo_id=carrera_id).order_by('nombre_servi')
			except (ValueError, TypeError):
				pass #Invalida la entrada del usuario, ignora y regresa un query vacio en carrera
		elif self.instance.pk:
			self.fields['tipo_servi_soli'].queryset = self.instance.carrera_soli.tipo_servi_soli_set.order_by('nombre_servi')

class AEvaluarForm(forms.ModelForm):
	class Meta:
		model = Solicitud

		fields = [
			'estado_soli',
			'comentario',
		]

		labels = {
			'estado_soli': 'Estado de solicitud: ',
			'comentario': 'Comentario a la solicitud: ',
		}

		widgets = {
			'estado_soli': forms.Select(attrs={'class':'form-control'}),
			'comentario': forms.Textarea(attrs={'class': 'form-control textArea'}),
		}

class EncargadoForm(forms.ModelForm):
	class Meta:
		model = EncargadoPropio

		fields = [
			'facultad',
		]

		labels = {
			'facultad': 'Facultad: ',
		}

		widgets = {
			'facultad': forms.Select(attrs={'class':'form-control'}),
		}

class MaestroForm(forms.ModelForm):
	class Meta:
		model = MaestroPropio

		fields = [
			'facultad',
			'carrera',
			'escuela',
			'especialidad',
			'esta_disponible',
		]

		labels = {
			'facultad': 'Facultad',
			'carrera': 'Carrera',
			'escuela': 'Escuela',
			'especialidad': 'Especialidad',
			'esta_disponible': '¿Se encuentra disponible?',
		}

		widgets = {
			'facultad' : forms.Select(attrs={'class': 'form-control'}),
			'carrera' : forms.Select(attrs={'class': 'form-control'}),
			'escuela' : forms.Select(attrs={'class': 'form-control'}),
			'especialidad' : forms.TextInput(attrs={'class': 'form-control'}),
			'esta_disponible' : forms.CheckboxInput(),
		}

class InstitucionForm(forms.ModelForm):
	class Meta:
		model = InstitucionPropio

		fields = [
			'ubicacion',
		]

		labels = {
			'ubicacion': 'Direccion de la institución',
		}

		widgets = {
			'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
		}