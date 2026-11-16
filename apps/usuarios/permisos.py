"""Qué puede hacer cada rol.

Los permisos son los que Django crea para cada modelo: add, change, delete y view.
Las vistas los piden con PermissionRequiredMixin o con @permission_required, y las
plantillas con {{ perms }}. El rol está en la columna usu_rol de tbl_usuario.
"""
from django.contrib.auth.backends import ModelBackend

from .models import Usuario

CRUD = ("add", "change", "delete", "view")
SOLO_VER = ("view",)

# rol -> (app, modelo) -> acciones
PERMISOS_POR_ROL = {
    Usuario.Rol.ADMIN: {
        ("almacenes", "almacen"): CRUD,
        ("ubicaciones", "ubicacion"): CRUD,
        ("categorias", "categoria"): SOLO_VER,
        ("articulos", "articulo"): SOLO_VER,
        ("lotes", "lote"): SOLO_VER,
        ("movimientos", "movimiento"): SOLO_VER,
        ("detalles_movimiento", "detallemovimiento"): SOLO_VER,
    },
    Usuario.Rol.JEFE: {
        ("categorias", "categoria"): CRUD,
        ("articulos", "articulo"): CRUD,
        ("lotes", "lote"): CRUD,
        ("almacenes", "almacen"): SOLO_VER,
        ("ubicaciones", "ubicacion"): SOLO_VER,
        ("movimientos", "movimiento"): SOLO_VER,
        ("detalles_movimiento", "detallemovimiento"): SOLO_VER,
    },
    Usuario.Rol.BODEGUERO: {
        ("movimientos", "movimiento"): CRUD,
        ("detalles_movimiento", "detallemovimiento"): CRUD,
        ("lotes", "lote"): SOLO_VER,
        ("articulos", "articulo"): SOLO_VER,
        ("ubicaciones", "ubicacion"): SOLO_VER,
        ("almacenes", "almacen"): SOLO_VER,
        ("categorias", "categoria"): SOLO_VER,
    },
}


def permisos_del_rol(rol):
    """Devuelve los permisos del rol con el formato de Django: 'app.accion_modelo'."""
    permisos = set()
    for (app, modelo), acciones in PERMISOS_POR_ROL.get(rol, {}).items():
        for accion in acciones:
            permisos.add(f"{app}.{accion}_{modelo}")
    return permisos


class RolBackend(ModelBackend):
    """Inicia sesión igual que Django, pero los permisos salen del rol del usuario."""

    def get_all_permissions(self, user_obj, obj=None):
        permisos = set(super().get_all_permissions(user_obj, obj))
        if user_obj.is_active and not user_obj.is_anonymous:
            permisos |= permisos_del_rol(user_obj.usu_rol)
        return permisos
