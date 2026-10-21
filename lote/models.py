from django.db import models
from articulo_core.models import Articulo
from almacen.models import Almacen

class Lote(models.Model):
    fk_art=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    fk_alm=models.ForeignKey(Almacen,on_delete=models.CASCADE)
    lot_codigo =models.CharField(max_length=50)
    lot_cantidad = models.IntegerField()
    lot_fecha_vencimiento = models.DateField()

    def __str__(self):return self.lot_codigo



