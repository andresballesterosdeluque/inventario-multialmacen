from django.db import models


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey("movimientos.Movimiento", on_delete=models.CASCADE)
    lote = models.ForeignKey("lotes.Lote", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movimiento} - {self.lote} x{self.cantidad}"
