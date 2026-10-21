from django.db import models
from categoria.models import Categoria

class Articulo(models.Model):
    fk_cat = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    nombre_articulo = models.CharField(max_length=100)
    art_sku = models.CharField(max_length=50, unique=True)
    precio_articulo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self): 
        return self.nombre_articulo