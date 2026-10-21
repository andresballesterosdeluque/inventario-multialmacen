from django.db import models

class Almacen(models.Model):
    alm_nombre=models.CharField(max_length=100)
    alm_direccion=models.CharField(max_length=150)

    def __str__(self): return self.alm_nombre


