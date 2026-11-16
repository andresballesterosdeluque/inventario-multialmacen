from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.db import transaction

PASSWORD = "Inventario2026"

CRUD = ("add", "change", "delete", "view")
SOLO_VER = ("view",)

# Qué puede hacer cada rol, modelo por modelo.
ROLES = {
    "Administrador": {
        "almacen": CRUD, "ubicacion": CRUD,
        "categoria": SOLO_VER, "articulo": SOLO_VER, "lote": SOLO_VER,
        "movimiento": SOLO_VER, "detallemovimiento": SOLO_VER,
    },
    "Jefe de bodega": {
        "categoria": CRUD, "articulo": CRUD, "lote": CRUD,
        "almacen": SOLO_VER, "ubicacion": SOLO_VER,
        "movimiento": SOLO_VER, "detallemovimiento": SOLO_VER,
    },
    "Bodeguero": {
        "movimiento": CRUD, "detallemovimiento": CRUD,
        "lote": SOLO_VER, "articulo": SOLO_VER, "ubicacion": SOLO_VER,
        "almacen": SOLO_VER, "categoria": SOLO_VER,
    },
}

USUARIOS = [
    # usuario, grupo, nombre, apellido, es_staff (entra al panel de administración)
    ("admin", "Administrador", "Administrador", "", True),
    ("jefe", "Jefe de bodega", "Jefe", "de bodega", False),
    ("bodeguero", "Bodeguero", "Bodeguero", "", False),
]


class Command(BaseCommand):
    help = "Crea los roles (grupos con permisos) y los usuarios de prueba. Se puede ejecutar varias veces."

    @transaction.atomic
    def handle(self, *args, **options):
        for nombre, modelos in ROLES.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            permisos = []
            for modelo, acciones in modelos.items():
                codigos = [f"{accion}_{modelo}" for accion in acciones]
                permisos += list(Permission.objects.filter(codename__in=codigos))
            grupo.permissions.set(permisos)

        for usuario, grupo, nombre, apellido, staff in USUARIOS:
            u, creado = User.objects.get_or_create(username=usuario)
            if creado:
                u.set_password(PASSWORD)
            u.first_name, u.last_name = nombre, apellido
            if usuario == "admin":
                u.is_superuser = True
            u.is_staff = staff
            u.save()
            u.groups.add(Group.objects.get(name=grupo))
        self.stdout.write(self.style.SUCCESS("Roles y usuarios de prueba listos."))
