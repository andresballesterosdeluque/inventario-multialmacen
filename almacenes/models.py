from django.db import models


class Almacen(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
