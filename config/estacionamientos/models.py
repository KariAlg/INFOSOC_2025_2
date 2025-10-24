from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone 
from utils.utils import normalizar_patente, normalizar_rut


class ZonaEstacionamiento(models.Model):
    nombre_zona = models.CharField(max_length=100, unique=True)
    n_estacionamientos_totales = models.PositiveIntegerField()
    disponibles = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre_zona} ({self.disponibles}/{self.n_estacionamientos_totales})"
    
    @classmethod
    def crear_estacionamiento(cls,nombre_zona,n_estacionamientos_totales,disponibles=None): 
        if disponibles is None:
            disponibles=n_estacionamientos_totales

        try:
            zona= cls.objects.create(
                nombre_zona=nombre_zona,
                n_estacionamientos_totales=n_estacionamientos_totales,
                disponibles=disponibles
            )

            print(f"Se ha creado exitosamente una nueva zona (Zona: {zona.nombre_zona})")
            return zona
        
        except Exception as e:
            print(f"Error al crear una nueva zona: {e}")
            return None
        

    def modificar_estacionamiento(self,nombre_zona,n_estacionamientos_totales,disponibles):
        try:
            zona=ZonaEstacionamiento.objects.get(nombre_zona=nombre_zona)
            zona.nombre_zona=nombre_zona
            zona.n_estacionamientos_totales=n_estacionamientos_totales
            zona.disponibles=disponibles

            zona.save()
            return zona

        except ZonaEstacionamiento.DoesNotExist:
            print(f"No se encontro una zona con ese nombre {nombre_zona}")
            return None

    def delete_estacionamiento(self):
        if self.registros.filter(hora_salida__isnull=True).exists():
            raise ValidationError("No se puede borrar la zona: hay vehículos estacionados.")
        self.delete()

    def ocupados(self):
        return self.n_estacionamientos_totales - self.disponibles
    
    def ingresa_vehiculo(self):
        if self.disponibles <= 0:
            raise ValidationError("No hay puestos de estacionamiento disponibles en la zona.")
        self.disponibles -= 1
        self.save(update_fields=["disponibles"])
        return self.disponibles
    
    def salida_vehiculo(self):
        self.disponibles += 1
        self.save(update_fields=["disponibles"])
        return self.disponibles
    


class RegistroVehiculo(models.Model):
    patente = models.CharField(max_length=20)
    nombre_conductor = models.CharField(max_length=100)
    apellido_conductor = models.CharField(max_length=100, blank=True, null=True)
    rut_conductor = models.CharField(max_length=12, blank=True, null=True)

    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(blank=True, null=True)

    zona_estacionamiento = models.ForeignKey(
        "ZonaEstacionamiento",
        on_delete=models.CASCADE,
        related_name="registros"
    )

    # -------------------------------------------------------
    # MÉTODOS DE INSTANCIA
    # -------------------------------------------------------

    def save(self, *args, **kwargs):
        """Normaliza la patente y el RUT antes de guardar."""
        if self.patente:
            self.patente = normalizar_patente(self.patente)
        if self.rut_conductor:
            self.rut_conductor = normalizar_rut(self.rut_conductor)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patente} ({self.zona_estacionamiento.nombre_zona})"

    # -------------------------------------------------------
    # MÉTODOS DE CLASE
    # -------------------------------------------------------

    @classmethod
    def ingresar(cls, patente, nombre, apellido, rut, zona, hora_entrada=None, hora_salida=None):
        """
        Registra la entrada de un vehículo:
        - Normaliza patente y RUT.
        - Verifica que no tenga una entrada activa.
        - Descuenta un cupo de la zona.
        """
        patente = normalizar_patente(patente)
        rut = normalizar_rut(rut)

        if cls.objects.filter(patente=patente, hora_salida__isnull=True).exists():
            raise ValidationError(
                f"El vehículo con patente {patente} ya está estacionado y no ha salido aún."
            )

        if hora_entrada is None:
            hora_entrada = timezone.now()

        if zona.disponibles <= 0:
            raise ValidationError("Zona sin cupos disponibles.")

        registro = cls.objects.create(
            patente=patente,
            nombre_conductor=nombre,
            apellido_conductor=apellido,
            rut_conductor=rut,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            zona_estacionamiento=zona
        )

        # Descontar uno disponible
        registro.zona_estacionamiento.ingresa_vehiculo()
        return registro

    @classmethod
    def salida(cls, patente, hora_salida=None):
        """
        Registra la salida de un vehículo:
        - Busca la entrada activa.
        - Marca hora de salida.
        - Suma un cupo disponible.
        """
        patente = normalizar_patente(patente)
        try:
            vehiculo = cls.objects.get(patente=patente, hora_salida__isnull=True)
            if hora_salida is None:
                vehiculo.hora_salida = timezone.now()
            vehiculo.save()
            vehiculo.zona_estacionamiento.salida_vehiculo()
            return vehiculo
        except cls.DoesNotExist:
            raise ValidationError(f"No se encontró un vehículo con patente {patente} estacionado actualmente.")