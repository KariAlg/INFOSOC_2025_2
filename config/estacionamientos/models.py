from django.db import models


class ZonaEstacionamiento(models.Model):
    nombre_zona = models.CharField(max_length=100, unique=True)
    n_estacionamientos_totales = models.PositiveIntegerField()
    disponibles = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre_zona} ({self.disponibles}/{self.n_estacionamientos_totales})"


class RegistroVehiculo(models.Model):
    patente = models.CharField(max_length=20)
    nombre_conductor = models.CharField(max_length=100)
    apellido_conductor = models.CharField(max_length=100, blank=True, null=True)
    rut_conductor = models.CharField(max_length=12, blank=True, null=True)

    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(blank=True, null=True)

    zona_estacionamiento = models.ForeignKey(
        ZonaEstacionamiento, on_delete=models.CASCADE, related_name="registros"
    )

    def __str__(self):
        return f"{self.patente} ({self.zona_estacionamiento.nombre_zona})"
