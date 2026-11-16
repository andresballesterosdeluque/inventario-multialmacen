from django.db import models


class DetalleMovimiento(models.Model):
    """Tabla intermedia del N:M entre Movimiento y Lote. Guarda la cantidad."""

    pk_det_id = models.BigAutoField(primary_key=True)
    fk_mov = models.ForeignKey("movimientos.Movimiento", on_delete=models.CASCADE, verbose_name="movimiento")
    fk_lot = models.ForeignKey("lotes.Lote", on_delete=models.PROTECT, verbose_name="lote")
    det_cantidad = models.PositiveIntegerField("cantidad")

    class Meta:
        db_table = "tbl_detalle_movimiento"
        verbose_name = "detalle de movimiento"
        verbose_name_plural = "detalles de movimiento"

    def __str__(self):
        return f"{self.fk_mov} - {self.fk_lot} x{self.det_cantidad}"
