from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.AdministrativoDebil)
admin.site.register(models.AdministrativoFuerte)
admin.site.register(models.Guardia)