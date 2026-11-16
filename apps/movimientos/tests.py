from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.almacenes.models import Almacen
from apps.articulos.models import Articulo
from apps.categorias.models import Categoria
from apps.detalles_movimiento.models import DetalleMovimiento
from apps.lotes.models import Lote
from apps.ubicaciones.models import Ubicacion

from .models import Movimiento


class MovimientosCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("crear_usuarios", verbosity=0)
        cls.bodeguero = get_user_model().objects.get(username="bodeguero")
        almacen = Almacen.objects.create(alm_nombre="Norte", alm_direccion="Calle 1")
        ubicacion = Ubicacion.objects.create(fk_alm=almacen, ubi_estante="E1", ubi_nivel="1")
        categoria = Categoria.objects.create(cat_nombre="Herramientas")
        articulo = Articulo.objects.create(art_codigo="A1", art_nombre="Martillo", art_unidad="unidad", fk_cat=categoria)
        cls.lote = Lote.objects.create(lot_codigo="L1", fk_art=articulo, fk_ubi=ubicacion)

    def entrar(self, usuario):
        self.client.login(username=usuario, password="Inventario2026")

    def datos(self, tipo, cantidad, lote=None, fecha="2026-10-01"):
        lote = lote or self.lote
        return {
            "mov_fecha": fecha, "mov_tipo": tipo, "mov_observacion": "prueba",
            "detalles-TOTAL_FORMS": "1", "detalles-INITIAL_FORMS": "0",
            "detalles-MIN_NUM_FORMS": "1", "detalles-MAX_NUM_FORMS": "1000",
            "detalles-0-fk_lot": str(lote.pk), "detalles-0-det_cantidad": str(cantidad),
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
        datos["detalles-0-fk_lot"] = ""
        datos["detalles-0-det_cantidad"] = ""
        r = self.client.post(reverse("movimientos:crear"), datos)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_fecha_futura_se_rechaza(self):
        self.entrar("bodeguero")
        r = self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 3, fecha="2999-01-01"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Movimiento.objects.count(), 0)

    def test_no_se_borra_una_entrada_que_ya_se_uso(self):
        entrada = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 1), mov_tipo="ENTRADA")
        DetalleMovimiento.objects.create(fk_mov=entrada, fk_lot=self.lote, det_cantidad=10)
        salida = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 2), mov_tipo="SALIDA")
        DetalleMovimiento.objects.create(fk_mov=salida, fk_lot=self.lote, det_cantidad=8)
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:eliminar", args=[entrada.pk]))
        self.assertTrue(Movimiento.objects.filter(pk=entrada.pk).exists())
        self.assertEqual(self.lote.stock_actual(), 2)

    def test_eliminar_movimiento_sin_problema(self):
        entrada = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 1), mov_tipo="ENTRADA")
        DetalleMovimiento.objects.create(fk_mov=entrada, fk_lot=self.lote, det_cantidad=10)
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:eliminar", args=[entrada.pk]))
        self.assertFalse(Movimiento.objects.filter(pk=entrada.pk).exists())

    def test_editar_una_entrada_no_puede_dejar_stock_negativo(self):
        entrada = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 1), mov_tipo="ENTRADA")
        d = DetalleMovimiento.objects.create(fk_mov=entrada, fk_lot=self.lote, det_cantidad=10)
        salida = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 2), mov_tipo="SALIDA")
        DetalleMovimiento.objects.create(fk_mov=salida, fk_lot=self.lote, det_cantidad=8)
        self.entrar("bodeguero")
        datos = self.datos("ENTRADA", 3)
        datos.update({"detalles-INITIAL_FORMS": "1", "detalles-0-pk_det_id": str(d.pk), "detalles-0-fk_mov": str(entrada.pk)})
        self.client.post(reverse("movimientos:editar", args=[entrada.pk]), datos)
        d.refresh_from_db()
        self.assertEqual(d.det_cantidad, 10)

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
        entrada = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 1), mov_tipo="ENTRADA", mov_observacion="compra")
        DetalleMovimiento.objects.create(fk_mov=entrada, fk_lot=self.lote, det_cantidad=10)
        salida = Movimiento.objects.create(fk_usu=self.bodeguero, mov_fecha=date(2026, 10, 5), mov_tipo="SALIDA", mov_observacion="venta")
        DetalleMovimiento.objects.create(fk_mov=salida, fk_lot=self.lote, det_cantidad=2)
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

    def test_el_movimiento_guarda_quien_lo_registro(self):
        self.entrar("bodeguero")
        self.client.post(reverse("movimientos:crear"), self.datos("ENTRADA", 5))
        self.assertEqual(Movimiento.objects.get().fk_usu.username, "bodeguero")

    def test_los_permisos_salen_del_rol(self):
        usuario = get_user_model().objects.create_user("nuevo", password="Inventario2026", usu_rol="JEFE")
        self.assertTrue(usuario.has_perm("articulos.add_articulo"))
        self.assertFalse(usuario.has_perm("movimientos.add_movimiento"))
        usuario = get_user_model().objects.get(pk=usuario.pk)
        usuario.usu_rol = "BODEGUERO"
        usuario.save()
        usuario = get_user_model().objects.get(pk=usuario.pk)
        self.assertTrue(usuario.has_perm("movimientos.add_movimiento"))
        self.assertFalse(usuario.has_perm("articulos.add_articulo"))
