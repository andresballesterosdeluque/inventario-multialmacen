from datetime import date

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from almacenes.models import Almacen
from articulos.models import Articulo
from categorias.models import Categoria
from detalles_movimiento.models import DetalleMovimiento
from lotes.models import Lote
from ubicaciones.models import Ubicacion

from .models import Movimiento


class MovimientosCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("crear_roles", verbosity=0)
        almacen = Almacen.objects.create(nombre="Norte", direccion="Calle 1")
        ubicacion = Ubicacion.objects.create(almacen=almacen, estante="E1", nivel="1")
        categoria = Categoria.objects.create(nombre="Herramientas")
        articulo = Articulo.objects.create(codigo="A1", nombre="Martillo", unidad="unidad", categoria=categoria)
        cls.lote = Lote.objects.create(codigo="L1", articulo=articulo, ubicacion=ubicacion)

    def entrar(self, usuario):
        self.client.login(username=usuario, password="Inventario2026")

    def datos(self, tipo, cantidad, lote=None, fecha="2026-10-01"):
        lote = lote or self.lote
        return {
            "fecha": fecha, "tipo": tipo, "observacion": "prueba",
            "detalles-TOTAL_FORMS": "1", "detalles-INITIAL_FORMS": "0",
            "detalles-MIN_NUM_FORMS": "1", "detalles-MAX_NUM_FORMS": "1000",
            "detalles-0-lote": str(lote.pk), "detalles-0-cantidad": str(cantidad),
        }

    def test_anonimo_va_al_login(self):
        r = self.client.get(reverse("movimientos:lista"))
        self.assertRedirects(r, "/login/?next=/movimientos/")

    def test_bodeguero_registra_entrada(self):
        self.entrar("bodeguero")
        r = self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 20))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.lote.stock_actual(), 20)

    def test_salida_mayor_que_el_stock_se_rechaza(self):
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 5))
        r = self.client.post(reverse("movimientos:crear"), self.datos("SALIDA", 9))
        self.assertEqual(r.status_code, 200)  # vuelve al formulario con el error
        self.assertEqual(Movimiento.objects.count(), 1)
        self.assertEqual(self.lote.stock_actual(), 5)

    def test_salida_valida(self):
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 10))
        self.client.post(reverse("movimientos:crear"), self.datos("SALIDA", 4))
        self.assertEqual(self.lote.stock_actual(), 6)

    def test_sin_articulos_se_rechaza(self):
        self.entrar("bodeguero")
        datos = self.datos("ENTRADA", 3)
        datos["detalles-0-lote"] = ""
        datos["detalles-0-cantidad"] = ""
        r = self.client.post(reverse("movimientos:crear"), datos)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_fecha_futura_se_rechaza(self):
        self.entrar("bodeguero")
        r = self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 3, fecha="2999-01-01"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_no_se_borra_una_entrada_que_ya_se_uso(self):
        entrada = Movimiento.objects.create(fecha=date(2026, 10, 1), tipo="ENTRADA")
        DetalleMovimiento.objects.create(movimiento=entrada, lote=self.lote, cantidad=10)
        salida = Movimiento.objects.create(fecha=date(2026, 10, 2), tipo="SALIDA")
        DetalleMovimiento.objects.create(movimiento=salida, lote=self.lote, cantidad=8)
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:eliminar", args=[entrada.pk]))
        self.assertTrue(Movimiento.objects.filter(pk=entrada.pk).exists())
        self.assertEqual(self.lote.stock_actual(), 2)

    def test_eliminar_movimiento_sin_problema(self):
        entrada = Movimiento.objects.create(fecha=date(2026, 10, 1), tipo="ENTRADA")
        DetalleMovimiento.objects.create(movimiento=entrada, lote=self.lote, cantidad=10)
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:eliminar", args=[entrada.pk]))
        self.assertFalse(Movimiento.objects.filter(pk=entrada.pk).exists())

    def test_editar_una_entrada_no_puede_dejar_stock_negativo(self):
        entrada = Movimiento.objects.create(fecha=date(2026, 10, 1), tipo="ENTRADA")
        d = DetalleMovimiento.objects.create(movimiento=entrada, lote=self.lote, cantidad=10)
        salida = Movimiento.objects.create(fecha=date(2026, 10, 2), tipo="SALIDA")
        DetalleMovimiento.objects.create(movimiento=salida, lote=self.lote, cantidad=8)
        self.entrar("bodeguero")
        datos = self.datos("ENTRADA", 3)
        datos.update({"detalles-INITIAL_FORMS": "1", "detalles-0-id": str(d.pk), "detalles-0-movimiento": str(entrada.pk)})
        self.client.post(reverse("movimientos:editar", args=[entrada.pk]), datos)
        d.refresh_from_db()
        self.assertEqual(d.cantidad, 10)

    def test_jefe_solo_puede_ver_movimientos(self):
        self.entrar("jefe")
        self.assertEqual(self.client.get(reverse("movimientos:lista")).status_code, 200)
        self.assertEqual(self.client.get(reverse("movimientos:crear")).status_code, 403)

    def test_bodeguero_no_puede_crear_almacenes(self):
        self.entrar("bodeguero")
        self.assertEqual(self.client.get(reverse("almacenes:crear")).status_code, 403)
        self.assertEqual(self.client.get(reverse("almacenes:lista")).status_code, 200)

    def test_jefe_crea_articulo_y_administrador_no(self):
        self.entrar("jefe")
        self.assertEqual(self.client.get(reverse("articulos:crear")).status_code, 200)
        self.client.logout()
        self.entrar("admin")
        self.assertEqual(self.client.get(reverse("almacenes:crear")).status_code, 200)

    def test_filtros_de_la_lista(self):
        entrada = Movimiento.objects.create(fecha=date(2026, 10, 1), tipo="ENTRADA", observacion="compra")
        DetalleMovimiento.objects.create(movimiento=entrada, lote=self.lote, cantidad=10)
        salida = Movimiento.objects.create(fecha=date(2026, 10, 5), tipo="SALIDA", observacion="venta")
        DetalleMovimiento.objects.create(movimiento=salida, lote=self.lote, cantidad=2)
        self.entrar("bodeguero")
        url = reverse("movimientos:lista")
        self.assertEqual(len(self.client.get(url, {"tipo": "SALIDA"}).context["page_obj"]), 1)
        self.assertEqual(len(self.client.get(url, {"q": "Martillo"}).context["page_obj"]), 2)
        self.assertEqual(len(self.client.get(url, {"desde": "2026-10-03"}).context["page_obj"]), 1)
        self.assertEqual(len(self.client.get(url, {"q": "nada que ver"}).context["page_obj"]), 0)

    def test_todas_las_pantallas_cargan_para_el_administrador(self):
        self.entrar("admin")
        for nombre in ["inicio", "almacenes:lista", "almacenes:stock", "ubicaciones:lista",
                       "categorias:lista", "articulos:lista", "lotes:lista", "movimientos:lista"]:
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200, nombre)

    def test_logout_cierra_la_sesion(self):
        self.entrar("jefe")
        self.client.post(reverse("logout"))
        self.assertEqual(self.client.get(reverse("inicio")).status_code, 302)
