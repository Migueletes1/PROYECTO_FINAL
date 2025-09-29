from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Proyecto 

class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES)

    class Meta:
        model = Usuario
        fields = ["username", "email", "rol", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput)
    from django import forms

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion", "area", "duracion_semanas", "estado", "aprendices"]

