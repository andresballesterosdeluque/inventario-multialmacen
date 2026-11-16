from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

PASSWORD = "Inventario2026"

USUARIOS = [
    # usuario, rol, nombre, apellido, es superusuario (entra al panel de administración)
    ("admin", "ADMIN", "Administrador", "", True),
    ("jefe", "JEFE", "Jefe", "de bodega", False),
    ("bodeguero", "BODEGUERO", "Bodeguero", "", False),
]


class Command(BaseCommand):
    help = "Crea los usuarios de prueba, uno por rol. Se puede ejecutar varias veces."

    @transaction.atomic
    def handle(self, *args, **options):
        Usuario = get_user_model()
        for usuario, rol, nombre, apellido, es_super in USUARIOS:
            u, creado = Usuario.objects.get_or_create(username=usuario)
            if creado:
                u.set_password(PASSWORD)
            u.first_name, u.last_name = nombre, apellido
            u.usu_rol = rol
            u.is_superuser = es_super
            u.is_staff = es_super
            u.save()
        self.stdout.write(self.style.SUCCESS("Usuarios de prueba listos."))
