from django.db import models

from almacen.models import Almacen

class Movimiento (models.Model):
    Tipo=[('ENTRADA','Entrada'),('SALIDA','Salida')]

    fk_alm=models.ForeignKey(Almacen,on_delete=models.CASCADE)

    mov_tipo = models.CharField(max_length=10, choices=Tipo)

    mov_fecha=models.DateTimeField(auto_now_add=True)

    mov_responsable = models.CharField(max_length=100)
    def __str__(self):return f"{self.mov_tipo}-{self.id} "