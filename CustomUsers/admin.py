from django.contrib import admin
from .models import MiUsuario
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomAdminUser(UserAdmin):
    model = MiUsuario
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'is_admin')
    search_fields = ('username','email')
    ordering = ('username','email')
    readonly_fields = ('id',)

    list_filter = ()
    fieldsets = ()
    filter_horizontal = ()

admin.site.register(MiUsuario, CustomAdminUser)