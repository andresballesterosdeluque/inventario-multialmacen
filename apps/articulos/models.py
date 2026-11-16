from django.contrib import admin
from django.db import models


class Articulo(models.Model):
    pk_art_id = models.BigAutoField(primary_key=True)
    fk_cat = models.ForeignKey(
        "categorias.Categoria", on_delete=models.PROTECT, related_name="articulos", verbose_name="categoría"
    )
    art_codigo = models.CharField("código", max_length=30, unique=True)
    art_nombre = models.CharField("nombre", max_length=100)
    art_unidad = models.CharField("unidad", max_length=20)

    class Meta:
        db_table = "tbl_articulo"
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return f"{self.art_codigo} - {self.art_nombre}"

    @admin.display(description="Stock total")
    def stock_total(self):
        # suma el stock de todos sus lotes
        return sum(lote.stock_actual() for lote in self.lotes.all())
