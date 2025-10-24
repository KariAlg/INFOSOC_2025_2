from django.contrib.auth.backends import ModelBackend
from .models import Usuario
from utils.utils import normalizar_rut

class RutBackend(ModelBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        if not rut or not password:
            return None

        rut_normalizado = normalizar_rut(rut)

        try:
            user = Usuario.objects.get(rut=rut_normalizado)
        except Usuario.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
