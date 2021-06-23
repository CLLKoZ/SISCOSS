from django import forms

from SISCOSS.models import Institucion, Facultad, Carrera, Solicitud, TipoServicio, EstadoSolicitud

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

class EvaluarSolicitudForm(forms.ModelForm):
	class Meta:
		model = EstadoSolicitud

		fields = [
			'nombre_estado_soli',
		]

		labels = {
			'nombre_estado_soli': 'Estado de solicitud',
		}

		widgets = {
			'nombre_estado_soli': forms.TextInput(attrs={'class':'form-control'}),
		}