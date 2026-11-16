from django.contrib import admin
from django.db import models
from django.db.models import Q, Sum


class Lote(models.Model):
    """Entidad débil: un lote solo existe para un artículo."""

    pk_lot_id = models.BigAutoField(primary_key=True)
    fk_art = models.ForeignKey(
        "articulos.Articulo", on_delete=models.CASCADE, related_name="lotes", verbose_name="artículo"
    )
    fk_ubi = models.ForeignKey(
        "ubicaciones.Ubicacion", on_delete=models.PROTECT, related_name="lotes", verbose_name="ubicación"
    )
    lot_codigo = models.CharField("código", max_length=30)
    lot_fecha_vencimiento = models.DateField("fecha de vencimiento", null=True, blank=True)

    class Meta:
        db_table = "tbl_lote"
        verbose_name = "lote"
        verbose_name_plural = "lotes"

    def __str__(self):
        return f"Lote {self.lot_codigo} ({self.fk_art.art_nombre})"

    @admin.display(description="Stock actual")
    def stock_actual(self):
        # entradas menos salidas
        r = self.detallemovimiento_set.aggregate(
            entradas=Sum("det_cantidad", filter=Q(fk_mov__mov_tipo="ENTRADA")),
            salidas=Sum("det_cantidad", filter=Q(fk_mov__mov_tipo="SALIDA")),
        )
        return (r["entradas"] or 0) - (r["salidas"] or 0)
