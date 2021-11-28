from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
#class CustomAdminUser(UserAdmin):
    #model = MiUsuario
    #add_form = CustomUserCreationForm

    #list_display = ('username', 'email', 'is_admin')
    #search_fields = ('username','email')
    #ordering = ('username','email')
    #readonly_fields = ('id',)

    #list_filter = ()
    #fieldsets = ()
    #filter_horizontal = ()

admin.site.register(MaestroPropio)
admin.site.register(EncargadoPropio)
admin.site.register(InstitucionPropio)
admin.site.register(TipoServicio)
admin.site.register(Facultad)
admin.site.register(ServicioSocial)
admin.site.register(Solicitud)
admin.site.register(Carrera)
admin.site.register(Escuela)