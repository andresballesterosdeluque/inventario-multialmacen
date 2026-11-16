from django.db import models


class Ubicacion(models.Model):
    almacen = models.ForeignKey("almacenes.Almacen", on_delete=models.CASCADE, related_name="ubicaciones")
    estante = models.CharField(max_length=20)
    nivel = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Estante {self.estante} - {self.almacen}"
