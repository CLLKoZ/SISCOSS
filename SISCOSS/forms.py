from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from SISCOSS.models import Institucion, Facultad, Carrera, Solicitud, TipoServicio, EstadoSolicitud, MiUsuario, MaestroPropio, InstitucionPropio

class InstitucionForm(forms.ModelForm):
	class Meta:
		model = InstitucionPropio
		#years = [(year, year) for year in ["Sykes", "Metro centro"]]
		fields = [
			'ubicacion',
		]

		labels = {
			'ubicacion': 'Ubicacion de la Institucion: ',
		}

		widgets = {
			'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la institucion'}),
			#'nombre_ins': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la institucion'}, choices=years),
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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MiUsuario
        fields = "__all__"

class UserCustomForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme su contraseña', widget=forms.PasswordInput)

    class Meta:
        model = MiUsuario
        fields = [
            'username',
            'type',
            'nombre',
            'email',
            'telefono',
        ]

        labels = {
            'username':'Carnet',
            'type':'',
            'nombre':'Nombre Completo',
            'email':'Correo Electronico',
            'telefono':'Numero de Telefono',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    #Veridicacion de coincidencia en contraseñas
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        #Guardando contraseñas en formato Hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class MaestroCreationForm(forms.ModelForm):
    #Contraseñas

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
            'facultad':'Facultad',
            'carrera':'Carrera',
            'escuela':'Escuela',
            'especialidad':'Especialidad',
            'esta_disponible':'¿Esta disponible?',
        }

        widgets = {
            'facultad': forms.Select(attrs={'class': 'form-control'}),
            'carrera': forms.Select(attrs={'class': 'form-control'}),
            'escuela': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'esta_disponible': forms.CheckboxInput(),
        }

class InstitucionCreationForm(forms.ModelForm):
    class Meta:
        model = InstitucionPropio
        fields = [
            'ubicacion',
        ]

        labels = {
            'ubicacion':'Ubicacion',
        }

        widgets = {
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
