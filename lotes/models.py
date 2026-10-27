from django.contrib import admin
from django.db import models
from django.db.models import Q, Sum


class Lote(models.Model):
    articulo = models.ForeignKey("articulos.Articulo", on_delete=models.CASCADE, related_name="lotes")
    ubicacion = models.ForeignKey("ubicaciones.Ubicacion", on_delete=models.PROTECT, related_name="lotes")
    codigo = models.CharField(max_length=30)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Lote {self.codigo} ({self.articulo.nombre})"

    @admin.display(description="Stock actual")
    def stock_actual(self):
        # entradas menos salidas
        r = self.detallemovimiento_set.aggregate(
            entradas=Sum("cantidad", filter=Q(movimiento__tipo="ENTRADA")),
            salidas=Sum("cantidad", filter=Q(movimiento__tipo="SALIDA")),
        )
        return (r["entradas"] or 0) - (r["salidas"] or 0)
