from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        # 🔹 No incluimos username, se asignará automáticamente
        fields = ["first_name", "last_name", "email", "rut", "cargo", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

        # Filtra las opciones del cargo según el usuario
        if usuario:
            if usuario.es_admin_debil():
                self.fields["cargo"].choices = [("GUARDIA", "Guardia")]
            elif usuario.es_guardia():
                self.fields["cargo"].choices = []

    def save(self, commit=True):
        user = super().save(commit=False)
        # 🔹 Si username está vacío, lo rellenamos con el RUT
        if not user.username:
            user.username = user.rut
        if commit:
            user.save()
        return user
    
    
class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email", "cargo"]
        widgets = {
            "cargo": forms.Select(choices=Usuario.CARGOS)
        }

    def __init__(self, *args, **kwargs):
        creador = kwargs.pop("creador", None)
        super().__init__(*args, **kwargs)

        # Si el usuario autenticado es admin débil, solo puede ver/editar guardias
        if creador and creador.es_admin_debil():
            self.fields["cargo"].choices = [("GUARDIA", "Guardia")]