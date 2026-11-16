from django.db import models


class Movimiento(models.Model):
    TIPOS = [("ENTRADA", "Entrada"), ("SALIDA", "Salida")]

    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    observacion = models.CharField(max_length=200, blank=True)
    lotes = models.ManyToManyField("lotes.Lote", through="detalles_movimiento.DetalleMovimiento")

    def __str__(self):
        return f"{self.tipo} #{self.pk} ({self.fecha})"
