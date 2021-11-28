from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from CustomUsers.models import MiUsuario
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.

class Estados(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        APROBADA = "APROBADA", "Aprobada"
        RECHAZADA = "RECHAZADA", "Rechazada"

class EstadosServicios(models.TextChoices):
        NO_INICIADO = "NO INICIADO", "No Iniciado"
        INICIADO = "INICIADO", "Iniciado"
        FINALIZADO = "FINALIZADO", "Finalizado"

#<----- INFORMACION NECESARIA OTRAS TABLAS ----->
class Facultad(models.Model):
	nombre_facu = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_facu

class Carrera(models.Model):
    facultad_carrera = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
    nombre_carrera = models.CharField(max_length=100)
    n_materias_necesarias = models.PositiveSmallIntegerField(default=48)

    def __str__(self):
        return self.nombre_carrera

class Escuela(models.Model):
	carrera_escuela = models.OneToOneField(Carrera, on_delete=models.CASCADE,)
	nombre_escuela = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_escuela

class TipoServicio(models.Model):
	carrera_tipo = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	nombre_servi = models.CharField(max_length=100)
	descripcion_servi = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre_servi

class Solicitud(models.Model):
	institucion = models.ForeignKey('InstitucionPropio', on_delete=models.CASCADE,)
	facultad_soli = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	carrera_soli = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	tipo_servi_soli = models.ForeignKey('TipoServicio', on_delete=models.CASCADE,)
	estado_soli = models.CharField(_('Estado'), max_length=50, choices=Estados.choices, default=Estados.PENDIENTE)
	fecha_realizacion = models.DateField(auto_now_add=True)
	comentario = models.CharField(max_length=500, blank=True)

#<----- INFORMACION PROPIA DE USUARIOS ----->
class MaestroPropio(models.Model):
	usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
	facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	escuela = models.ForeignKey('Escuela', on_delete=models.CASCADE,)
	especialidad = models.CharField(max_length=100)
	esta_disponible = models.BooleanField(default=True)

class EstudiantePropio(models.Model):
    usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE,)

class InstitucionPropio(models.Model):
	usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
	nombre_ins = models.CharField(max_length=50, blank=False, default="")
	ubicacion = models.TextField(max_length=255, default="None")

class EncargadoPropio(models.Model):
    usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE,)

class MiniExpediente(models.Model):
	estudiante = models.OneToOneField('EstudiantePropio', on_delete=CASCADE)
	materias_aprobadas = models.IntegerField()
	porcentaje_aprobado = models.DecimalField(max_digits=4, decimal_places=2)
	horas_sociales = models.IntegerField()

	def save(self, *args, **kwargs):
		todas = self.estudiante.carrera.n_materias_necesarias
		aprobadas = self.materias_aprobadas
		self.porcentaje_aprobado = (aprobadas/todas)*100
		super().save(*args, **kwargs)

class ServicioSocial(models.Model):
	solicitud = models.OneToOneField('Solicitud', on_delete=CASCADE)
	horas_alumno = models.IntegerField()
	cantidad_alumnos = models.IntegerField()
	duracion_horas = models.IntegerField()
	fecha_inicio = models.DateField(auto_now=True)
	fecha_fin = models.DateField(null=True)
	estado_servicio = models.CharField(_('EstadoServicio'), max_length=50, choices=EstadosServicios.choices, default=EstadosServicios.NO_INICIADO)

	def save(self, *args, **kwargs):
		cant_a = self.cantidad_alumnos
		horas_a = self.horas_alumno
		self.duracion_horas = cant_a * horas_a
		super().save(*args, **kwargs)

class ServicioAlumno(models.Model):
	servicio_social = models.ForeignKey('ServicioSocial', on_delete=CASCADE)
	alumno = models.ForeignKey('EstudiantePropio', on_delete=CASCADE)
	observacion = models.CharField(max_length=255 ,blank=True)

class RegistroServicioDiario(models.Model):
	servicio_alumno = models.ForeignKey('ServicioAlumno', on_delete=CASCADE)
	horas_invertidas = models.IntegerField()
	fecha_dia = models.DateField(auto_now=True)
	descripcion_actividad = models.CharField(max_length=255)
	nombre_encargado = models.CharField(max_length=50)