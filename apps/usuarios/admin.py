from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """El mismo admin de usuarios de Django, con la columna del rol."""

    list_display = ("username", "first_name", "last_name", "usu_rol", "is_staff", "is_active")
    list_filter = ("usu_rol", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Rol en el sistema", {"fields": ("usu_rol",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Rol en el sistema", {"fields": ("usu_rol",)}),)


# Los roles están en la columna usu_rol de tbl_usuario, así que los grupos de Django no se usan.
admin.site.unregister(Group)
