from django.db import models

class Categoria(models.Model):
    cat_nombre = models.CharField(max_length=100)
    cat_descripcion = models.CharField(max_length=255,blank=True)

    def __str__(self): return self.cat_nombre
    