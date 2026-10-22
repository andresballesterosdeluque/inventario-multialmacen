from django.db import models
from almacen.models import Almacen


class Ubicacion(models.Model):
    fk_alma = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    ubi_codigo = models.CharField(max_length=20)
    ubi_pasillo = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.ubi_codigo}-{self.fk_alma}"