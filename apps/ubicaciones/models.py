from django.db import models


class Ubicacion(models.Model):
    """Entidad débil: una ubicación solo existe dentro de un almacén."""

    pk_ubi_id = models.BigAutoField(primary_key=True)
    fk_alm = models.ForeignKey(
        "almacenes.Almacen", on_delete=models.CASCADE, related_name="ubicaciones", verbose_name="almacén"
    )
    ubi_estante = models.CharField("estante", max_length=20)
    ubi_nivel = models.CharField("nivel", max_length=20, blank=True)

    class Meta:
        db_table = "tbl_ubicacion"
        verbose_name = "ubicación"
        verbose_name_plural = "ubicaciones"

    def __str__(self):
        return f"Estante {self.ubi_estante} - {self.fk_alm}"
