from django.db import models
from datetime import datetime
from django.db.models.fields import proxy
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
#class EstudianteManager(models.Manager):
    #def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type=MiUsuario.Tipos.ESTUDIANTE)

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



#<----- USUARIOS ----->
#class Etudiante(MiUsuario):
    #objects = EstudianteManager()

    #@property
    #def more(self):
        #return self.maestropropio

    #class Meta:
        #proxy = True

    #def save(self, *args, **kwargs):
        #if not self.pk:
            #self.type = MiUsuario.Tipos.ESTUDIANTE
        #return super().save(*args, **kwargs)

class Institucion(MiUsuario):
    objects = InstitucionManager()

    @property
    def more(self):
        return self.institucionpropio


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
        return self.encargadopropio

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
        return self.proyeccionpropio

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MiUsuario.Tipos.PROYECCION_SOC
        return super().save(*args, **kwargs)