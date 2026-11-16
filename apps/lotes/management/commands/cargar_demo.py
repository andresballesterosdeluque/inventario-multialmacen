from datetime import date

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.almacenes.models import Almacen
from apps.articulos.models import Articulo
from apps.categorias.models import Categoria
from apps.detalles_movimiento.models import DetalleMovimiento
from apps.lotes.models import Lote
from apps.movimientos.models import Movimiento
from apps.ubicaciones.models import Ubicacion


class Command(BaseCommand):
    help = "Carga datos de demostración (3 registros por tabla). Se puede ejecutar varias veces."

    @transaction.atomic
    def handle(self, *args, **options):
        norte, _ = Almacen.objects.get_or_create(alm_nombre="Norte", defaults={"alm_direccion": "Calle 10 #5-20"})
        sur, _ = Almacen.objects.get_or_create(alm_nombre="Sur", defaults={"alm_direccion": "Carrera 15 #8-30"})
        central, _ = Almacen.objects.get_or_create(alm_nombre="Central", defaults={"alm_direccion": "Avenida 1 #12-45"})

        herr, _ = Categoria.objects.get_or_create(cat_nombre="Herramientas")
        lub, _ = Categoria.objects.get_or_create(cat_nombre="Lubricantes")
        pap, _ = Categoria.objects.get_or_create(cat_nombre="Papelería")

        martillo, _ = Articulo.objects.get_or_create(
            art_codigo="ART-001", defaults={"art_nombre": "Martillo", "art_unidad": "unidad", "fk_cat": herr})
        aceite, _ = Articulo.objects.get_or_create(
            art_codigo="ART-002", defaults={"art_nombre": "Aceite 20W50", "art_unidad": "litro", "fk_cat": lub})
        resma, _ = Articulo.objects.get_or_create(
            art_codigo="ART-003", defaults={"art_nombre": "Resma de papel", "art_unidad": "paquete", "fk_cat": pap})

        u1, _ = Ubicacion.objects.get_or_create(fk_alm=norte, ubi_estante="E1", defaults={"ubi_nivel": "1"})
        u2, _ = Ubicacion.objects.get_or_create(fk_alm=sur, ubi_estante="E2", defaults={"ubi_nivel": "1"})
        u3, _ = Ubicacion.objects.get_or_create(fk_alm=central, ubi_estante="E3", defaults={"ubi_nivel": "1"})

        l1, _ = Lote.objects.get_or_create(lot_codigo="L-001", fk_art=martillo, defaults={"fk_ubi": u1})
        l2, _ = Lote.objects.get_or_create(
            lot_codigo="L-002", fk_art=aceite, defaults={"fk_ubi": u2, "lot_fecha_vencimiento": date(2027, 6, 6)})
        l3, _ = Lote.objects.get_or_create(lot_codigo="L-003", fk_art=resma, defaults={"fk_ubi": u3})

        m1, c1 = Movimiento.objects.get_or_create(
            mov_fecha=date(2026, 10, 20), mov_tipo="ENTRADA", mov_observacion="Compra inicial de martillos")
        m2, c2 = Movimiento.objects.get_or_create(
            mov_fecha=date(2026, 10, 20), mov_tipo="ENTRADA", mov_observacion="Compra de aceite")
        m3, c3 = Movimiento.objects.get_or_create(
            mov_fecha=date(2026, 10, 21), mov_tipo="SALIDA", mov_observacion="Despacho de martillos")

        DetalleMovimiento.objects.get_or_create(fk_mov=m1, fk_lot=l1, defaults={"det_cantidad": 50})
        DetalleMovimiento.objects.get_or_create(fk_mov=m2, fk_lot=l2, defaults={"det_cantidad": 30})
        DetalleMovimiento.objects.get_or_create(fk_mov=m3, fk_lot=l1, defaults={"det_cantidad": 10})

        call_command("crear_roles", stdout=self.stdout)
        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
