from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    '''
    Atributos heredados por AbstractUser

    username = models.CharField(max_length=150)
    password = models.CharField(_("password"), max_length=128)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    '''
    rut = models.CharField(max_length=12, unique=True)

    CARGOS = [
        ("GUARDIA", "Guardia"),
        ("ADMIN_DEBIL", "Administrativo Débil"),
        ("ADMIN_FUERTE", "Administrativo Fuerte"),
    ]
    cargo = models.CharField(max_length=20, choices=CARGOS)

    def registrar_entrada():
        #...
        return

    def registrar_salida():
        #...
        return
    
    def descargar_planilla():
        #...
        return
    
    def registrar_uso_ticket_entrada():
        #...
        return

    def es_guardia(self):
        return self.cargo == "GUARDIA"

    def es_admin_debil(self):
        return self.cargo == "ADMIN_DEBIL"

    def es_admin_fuerte(self):
        return self.cargo == "ADMIN_FUERTE"

class Guardia(Usuario):
    def __str__(self):
        return f"[Guardia] {self.username}"
    
    class Meta:
        verbose_name = "Guardia"
        verbose_name_plural = "Guardias"

class AdministrativoDebil(Usuario):
    def __str__(self):
        return f"[Administrativo débil] {self.username}"
    
    class Meta:
        verbose_name = "Administrativo débil"
        verbose_name_plural = "Administrativos débiles"

    def createGuardia(self, username, password, email, name, lastName, rut):
        try:
            guard = Guardia.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name,
                last_name=lastName,
                rut=rut,
                cargo="GUARDIA"
            )

            print(f"Se ha creado exitosamente un nuevo guardia (username: {guard.username})")
            return guard
        except Exception as e:
            print(f"Error al crear un nuevo guardia: {e}")
            return None

    def readGuardiaRut(self, rut):
        try:
            return Guardia.objects.get(rut=rut)
        except Guardia.DoesNotExist:
            print(f"No se encontro guardia con RUT {rut}")
            return None
    
    def readGuardiaEmail(self, email):
        try:
            return Guardia.objects.get(email=email)
        except Guardia.DoesNotExist:
            print(f"No se encontro guardia con email {email}")
            return None
    
    def readGuardiaUsername(self, username):
        try:
            return Guardia.objects.get(username=username)
        except Guardia.DoesNotExist:
            print(f"No se encontro guardia con nombre de usuario {username}")
            return None
    
    def readGuardiaName(self, name):
        guards = Guardia.objects.filter(first_name=name)
        if not guards.exists():
            print(f"No se encontraron guardias con nombre {name}")
            return None
        return guards
        
    def readGuardiaLastName(self, lastName):
        guards = Guardia.objects.filter(last_name=lastName)
        if not guards.exists():
            print(f"No se encontraron guardias con nombre {lastName}")
            return None
        return guards

    '''
    Al llamar a este metodo dejar "" en los parametros que no quieran modificarse
    '''
    def updateGuardia(self, rut, username, email, name, lastName):
        try:
            guard = Guardia.objects.get(rut=rut)
            if (username != ""):
                guard.username = username
            if (email != ""):
                guard.email = email
            if (name != ""):
                guard.first_name = name
            if (lastName != ""):
                guard.last_name = lastName
            guard.save()
            return guard
        except Guardia.DoesNotExist:
            print(f"No se encontro guardia con rut {rut}")
            return None
    
    def deleteGuardia(self, rut):
        try:
            guard = Guardia.objects.get(rut=rut)
            guard.delete();
            return "eliminado"
        except Exception as e:
            print(f"Error al eliminar guardia {rut}: {e}")
            return
    
    def gestionar_estacionamientos():
        #...
        return
    
    def crear_ticket_entrada():
        #...
        return

class AdministrativoFuerte(AdministrativoDebil):    
    class Meta:
        verbose_name = "Administrativo fuerte"
        verbose_name_plural = "Administrativos fuertes"

    def crear_administrativo_debil(self, username, password, email, name, lastName, rut):
        try:
            guard = AdministrativoDebil.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name,
                last_name=lastName,
                rut=rut,
                cargo="ADMIN_DEBIL"
            )

            print(f"Se ha creado exitosamente un nuevo administrativo débil (username: {guard.username})")
            return guard
        except Exception as e:
            print(f"Error al crear un nuevo guardia: {e}")
            return None