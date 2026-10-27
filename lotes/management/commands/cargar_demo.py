from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from almacenes.models import Almacen
from articulos.models import Articulo
from categorias.models import Categoria
from detalles_movimiento.models import DetalleMovimiento
from lotes.models import Lote
from movimientos.models import Movimiento
from ubicaciones.models import Ubicacion


class Command(BaseCommand):
    help = "Carga datos de demostración (3 registros por tabla). Se puede ejecutar varias veces."

    @transaction.atomic
    def handle(self, *args, **options):
        norte, _ = Almacen.objects.get_or_create(nombre="Norte", defaults={"direccion": "Calle 10 #5-20"})
        sur, _ = Almacen.objects.get_or_create(nombre="Sur", defaults={"direccion": "Carrera 15 #8-30"})
        central, _ = Almacen.objects.get_or_create(nombre="Central", defaults={"direccion": "Avenida 1 #12-45"})

        herr, _ = Categoria.objects.get_or_create(nombre="Herramientas")
        lub, _ = Categoria.objects.get_or_create(nombre="Lubricantes")
        pap, _ = Categoria.objects.get_or_create(nombre="Papelería")

        martillo, _ = Articulo.objects.get_or_create(
            codigo="ART-001", defaults={"nombre": "Martillo", "unidad": "unidad", "categoria": herr})
        aceite, _ = Articulo.objects.get_or_create(
            codigo="ART-002", defaults={"nombre": "Aceite 20W50", "unidad": "litro", "categoria": lub})
        resma, _ = Articulo.objects.get_or_create(
            codigo="ART-003", defaults={"nombre": "Resma de papel", "unidad": "paquete", "categoria": pap})

        u1, _ = Ubicacion.objects.get_or_create(almacen=norte, estante="E1", defaults={"nivel": "1"})
        u2, _ = Ubicacion.objects.get_or_create(almacen=sur, estante="E2", defaults={"nivel": "1"})
        u3, _ = Ubicacion.objects.get_or_create(almacen=central, estante="E3", defaults={"nivel": "1"})

        l1, _ = Lote.objects.get_or_create(codigo="L-001", articulo=martillo, defaults={"ubicacion": u1})
        l2, _ = Lote.objects.get_or_create(
            codigo="L-002", articulo=aceite, defaults={"ubicacion": u2, "fecha_vencimiento": date(2027, 6, 6)})
        l3, _ = Lote.objects.get_or_create(codigo="L-003", articulo=resma, defaults={"ubicacion": u3})

        m1, c1 = Movimiento.objects.get_or_create(
            fecha=date(2026, 10, 20), tipo="ENTRADA", observacion="Compra inicial de martillos")
        m2, c2 = Movimiento.objects.get_or_create(
            fecha=date(2026, 10, 20), tipo="ENTRADA", observacion="Compra de aceite")
        m3, c3 = Movimiento.objects.get_or_create(
            fecha=date(2026, 10, 21), tipo="SALIDA", observacion="Despacho de martillos")

        DetalleMovimiento.objects.get_or_create(movimiento=m1, lote=l1, defaults={"cantidad": 50})
        DetalleMovimiento.objects.get_or_create(movimiento=m2, lote=l2, defaults={"cantidad": 30})
        DetalleMovimiento.objects.get_or_create(movimiento=m3, lote=l1, defaults={"cantidad": 10})

        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
