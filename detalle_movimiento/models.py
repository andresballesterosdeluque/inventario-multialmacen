from django.db import models

class DetalleMovimiento(models.Model):
    fk_mov = models.ForeignKey('movimiento.Movimiento', on_delete=models.CASCADE)
    fk_lot = models.ForeignKey('lote.Lote', on_delete=models.CASCADE)
    det_cantidad = models.IntegerField()

    def __str__(self): return f"Det{self.id}"