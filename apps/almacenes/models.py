from django.db import models


class Almacen(models.Model):
    pk_alm_id = models.BigAutoField(primary_key=True)
    alm_nombre = models.CharField("nombre", max_length=100)
    alm_direccion = models.CharField("dirección", max_length=150)

    class Meta:
        db_table = "tbl_almacen"
        verbose_name = "almacén"
        verbose_name_plural = "almacenes"

    def __str__(self):
        return self.alm_nombre
