from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from datetime import datetime

# Create your models here.

class Persona(models.Model):
	dui = models.CharField(validators=[RegexValidator(regex='^[0-9]{8}-?[0-9]{1}$', message='El campo debe tener 10 caracteres y con el formato indicado', code='nomatch')], max_length=10, primary_key=True)
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	telefono = models.CharField(max_length=8)
	direccion = models.CharField(max_length=150)
	email = models.EmailField()

class Facultad(models.Model):
	nombre_facu = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_facu

class Carrera(models.Model):
	facultad_carrera = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	nombre_carrera = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_carrera

class Escuela(models.Model):
	facultad_escuela = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	nombre_escuela = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_escuela

class Maestro(models.Model):
	persona = models.ForeignKey('Persona', on_delete=models.CASCADE,)
	facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	escuela = models.ForeignKey('Escuela', on_delete=models.CASCADE,)
	especialidad = models.CharField(max_length=100)
	disponibilidad = models.CharField(max_length=20)

class Institucion(models.Model):
	nombre_ins = models.CharField(max_length=100)
	email_ins = models.EmailField()

class TipoServicio(models.Model):
	carrera_tipo = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	nombre_servi = models.CharField(max_length=100)
	descripcion_servi = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre_servi

class EstadoSolicitud(models.Model):
	nombre_estado_soli = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre_estado_soli

class Solicitud(models.Model):
	institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE,)
	facultad_soli = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	carrera_soli = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	tipo_servi_soli = models.ForeignKey('TipoServicio', on_delete=models.CASCADE,)
	estado_soli = models.ForeignKey('EstadoSolicitud', on_delete=models.CASCADE,)
	fecha_realizacion = models.DateField(auto_now_add=True)
	comentario = models.CharField(max_length=500, blank=True)