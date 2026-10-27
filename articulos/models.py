from django.contrib import admin
from django.db import models


class Articulo(models.Model):
    categoria = models.ForeignKey("categorias.Categoria", on_delete=models.PROTECT, related_name="articulos")
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @admin.display(description="Stock total")
    def stock_total(self):
        # suma el stock de todos sus lotes
        return sum(lote.stock_actual() for lote in self.lotes.all())
