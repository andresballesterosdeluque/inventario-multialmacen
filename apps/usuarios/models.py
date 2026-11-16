from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Tabla única de usuarios del sistema. Los tres actores se distinguen por el rol.

    Hereda de AbstractUser: username, password, first_name, last_name, email,
    is_active, is_staff, is_superuser, last_login y date_joined.
    Aquí solo se agrega el rol.
    """

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        JEFE = "JEFE", "Jefe de bodega"
        BODEGUERO = "BODEGUERO", "Bodeguero"

    pk_usu_id = models.BigAutoField(primary_key=True)
    usu_rol = models.CharField("rol", max_length=10, choices=Rol.choices, default=Rol.BODEGUERO)

    class Meta:
        db_table = "tbl_usuario"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def save(self, *args, **kwargs):
        # el superusuario (createsuperuser) siempre queda como administrador
        if self.is_superuser:
            self.usu_rol = self.Rol.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username
