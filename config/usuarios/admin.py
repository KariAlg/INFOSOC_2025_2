from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
# Register your models here.
'''
admin.site.register(models.Usuario)
admin.site.register(models.AdministrativoDebil)
admin.site.register(models.AdministrativoFuerte)
admin.site.register(models.Guardia)
'''


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'rut', 'first_name', 'last_name', 'email', 'cargo', 'is_staff', 'is_active')
    list_filter = ('cargo', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'rut')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'rut', 'cargo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'rut', 'first_name', 'last_name', 'email', 'cargo', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )