from django import forms

from SISCOSS.models import Institucion, Facultad, Carrera, Solicitud, TipoServicio

class InstitucionForm(forms.ModelForm):
	class Meta:
		model = Institucion

		fields = [
			'nombre_ins',
			'email_ins',
		]

		labels = {
			'nombre_ins': 'Nombre de la Institucion: ',
			'email_ins': 'Email de la Institucion: ',
		}

		widgets = {
			'nombre_ins': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la institucion'}),
			'email_ins': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email de la institucion'}),
		}

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud

		fields = [
			'facultad_soli',
			'carrera_soli',
			'tipo_servi_soli',
			'estado_soli',
			'comentario',
		]

		labels = {
			
		}

		widgets = {
			
		}