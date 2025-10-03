from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)

    CARGOS = [
        ("GUARDIA", "Guardia"),
        ("ADMIN_DEBIL", "Administrativo Débil"),
        ("ADMIN_FUERTE", "Administrativo Fuerte"),
    ]
    cargo = models.CharField(max_length=20, choices=CARGOS)

    def es_guardia(self):
        return self.cargo == "GUARDIA"

    def es_admin_debil(self):
        return self.cargo == "ADMIN_DEBIL"

    def es_admin_fuerte(self):
        return self.cargo == "ADMIN_FUERTE"
