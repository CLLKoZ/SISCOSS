from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import MiUsuario

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = MiUsuario
        fields = '__all__'

class UserCustomForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirme su contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MiUsuario
        fields = [
            'username',
            'nombre',
            'email',
            'telefono',
        ]

        labels = {
            'username':'Carnet',
            'nombre':'Nombre Completo',
            'email':'Correo Electronico',
            'telefono':'Numero de Telefono',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    #Veridicacion de coincidencia en contraseñas
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinsiden!")
        return password2

    def save(self, commit=True):
        #Guardando contraseñas en formato Hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserCustomInsForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirme su contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MiUsuario
        fields = [
            'username',
            'nombre',
            'email',
            'telefono',
        ]

        labels = {
            'username':'Nombre de Usuario',
            'nombre':'Nombre del encargado',
            'email':'Correo Electronico',
            'telefono':'Numero de Telefono',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    #Veridicacion de coincidencia en contraseñas
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinsiden!")
        return password2

    def save(self, commit=True):
        #Guardando contraseñas en formato Hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user