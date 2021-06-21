from django.contrib import admin

from SISCOSS.models import Maestro, Facultad, Escuela, Carrera
# Register your models here.

admin.site.register(Maestro)
admin.site.register(Facultad)
admin.site.register(Escuela)
admin.site.register(Carrera)