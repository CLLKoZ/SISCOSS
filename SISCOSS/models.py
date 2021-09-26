from django.db import models
from django.db.models.fields import proxy
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

# Create your models here.

#Custom USER MANAGER
class MiManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Los usuarios deben tener un email")
        if not username:
            raise ValueError("Los usuarios deben tener un nombre de usuario")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

#CUSTOM USER MODEL
class MiUsuario(AbstractBaseUser, PermissionsMixin):
    class Tipos(models.TextChoices):
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"
        INSTITUCION = "INSTITUCION", "Institucion"
        MAESTRO = "MAESTRO", "Maestro"
        ENCARGADO_FACU = "ENCARGADO_FACU", "Encargado de la Facultad"
        PROYECCION_SOC = "PROYECCION_SOC", "Proyeccion Social"

    username = models.CharField(_("Nombre del usuario"), blank=True, max_length=255, unique=True)
    type = models.CharField(_('Tipo'), max_length=50, choices=Tipos.choices, default=Tipos.ESTUDIANTE)
    nombre = models.CharField(_("Nombre del usuario"), blank=True, max_length=255)
    email = models.EmailField(verbose_name="direccion de correo", max_length=60, unique=True)
    telefono = models.CharField(max_length=9, verbose_name="numero de telefono")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creacion")
    last_login = models.DateTimeField(verbose_name="utima sesion", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MiManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('user:detail', kwargs={'username': self.username})

#<----- MANAGERS DE USUARIOS ----->
class EstudianteManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.ESTUDIANTE)

class InstitucionManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.INSTITUCION)

class MaestroManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.MAESTRO)

class EncargadoManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.ENCARGADO_FACU)

class ProyeccionManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.PROYECCION_SOC)

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
	carrera_escuela = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	nombre_escuela = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_escuela

#<----- INFORMACION PROPIA DE USUARIOS ----->
class MaestroPropio(models.Model):
	dui = models.CharField(validators=[RegexValidator(regex='^[0-9]{8}-?[0-9]{1}$', message='El campo debe tener 10 caracteres y con el formato indicado', code='nomatch')], max_length=10, primary_key=True)
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
    n_materias_aprobadas = models.PositiveSmallIntegerField()
    porcentaje_carrera = models.DecimalField(max_digits=2, decimal_places=0)

    def save(self, *args, **kwargs):
        totales = self.carrera.n_materias_necesarias
        aprobadas = self.n_materias_cursadas
        self.porcentaje_carrera = (aprobadas/totales) * 100
        super().save(*args, **kwargs)

class InstitucionPropio(models.Model):
    usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
    ubicacion = models.TextField(max_length=255, default="None")

class EncargadoPropio(models.Model):
    usuario = models.OneToOneField(MiUsuario, on_delete=CASCADE)
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE,)

class TipoServicio(models.Model):
	carrera_tipo = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	nombre_servi = models.CharField(max_length=100)
	descripcion_servi = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre_servi

class EstadoSolicitud(models.Model):
	nombre_estado_soli = models.CharField(max_length=50, default='Pendiente')

	def __str__(self):
		return self.nombre_estado_soli

class Solicitud(models.Model):
	institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE,)
	facultad_soli = models.ForeignKey('Facultad', on_delete=models.CASCADE,)
	carrera_soli = models.ForeignKey('Carrera', on_delete=models.CASCADE,)
	tipo_servi_soli = models.ForeignKey('TipoServicio', on_delete=models.CASCADE,)
	estado_soli = models.ForeignKey('EstadoSolicitud', default = 1, on_delete=models.CASCADE,)
	fecha_realizacion = models.DateField(auto_now_add=True)
	comentario = models.CharField(max_length=500, blank=True)

	#<----- USUARIOS ----->
class Etudiante(MiUsuario):
    objects = EstudianteManager()

    @property
    def more(self):
        return self.maestropropio

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.ESTUDIANTE
        return super().save(*args, **kwargs)

class Institucion(MiUsuario):
    objects = InstitucionManager()

    @property
    def more(self):
        return self.maestropropio


    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.INSTITUCION
        return super().save(*args, **kwargs)

class Maestro(MiUsuario):
    objects = MaestroManager()

    @property
    def more(self):
        return self.maestropropio

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.MAESTRO
        return super().save(*args, **kwargs)

class Encargado_facu(MiUsuario):
    objects = EncargadoManager()

    @property
    def more(self):
        return self.maestropropio

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.ENCARGADO_FACU
        return super().save(*args, **kwargs)

class Proyeccion_soc(MiUsuario):
    objects = ProyeccionManager()

    @property
    def more(self):
        return self.maestropropio

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.PROYECCION_SOC
        return super().save(*args, **kwargs)