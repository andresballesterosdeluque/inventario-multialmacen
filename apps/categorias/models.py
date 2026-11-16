from django.db import models


class Categoria(models.Model):
    pk_cat_id = models.BigAutoField(primary_key=True)
    cat_nombre = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = "tbl_categoria"
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.cat_nombre
