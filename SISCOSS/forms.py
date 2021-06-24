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