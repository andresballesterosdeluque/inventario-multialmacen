from django.conf import settings
from django.db import models


class Movimiento(models.Model):
    TIPOS = [("ENTRADA", "Entrada"), ("SALIDA", "Salida")]

    pk_mov_id = models.BigAutoField(primary_key=True)
    mov_fecha = models.DateField("fecha")
    mov_tipo = models.CharField("tipo", max_length=10, choices=TIPOS)
    mov_observacion = models.CharField("observación", max_length=200, blank=True)
    # quién registró el movimiento (se llena solo con el usuario que inició sesión)
    fk_usu = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="movimientos",
        verbose_name="registrado por",
        editable=False,
    )
    # relación N:M con Lote, resuelta con la tabla intermedia tbl_detalle_movimiento
    lotes = models.ManyToManyField("lotes.Lote", through="detalles_movimiento.DetalleMovimiento")

    class Meta:
        db_table = "tbl_movimiento"
        verbose_name = "movimiento"
        verbose_name_plural = "movimientos"

    def __str__(self):
        return f"{self.mov_tipo} #{self.pk} ({self.mov_fecha})"
