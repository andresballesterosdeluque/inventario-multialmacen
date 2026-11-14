from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from almacenes.models import Almacen
from articulos.models import Articulo
from lotes.models import Lote
from movimientos.models import Movimiento


@login_required
def inicio(request):
    """Página de inicio con un resumen del inventario."""
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=30)

    ultimos = (
        Movimiento.objects.order_by("-fecha", "-id")[:5]
    )
    por_vencer = (
        Lote.objects.filter(fecha_vencimiento__isnull=False, fecha_vencimiento__lte=limite)
        .select_related("articulo", "ubicacion__almacen")
        .order_by("fecha_vencimiento")[:5]
    )
    contexto = {
        "total_articulos": Articulo.objects.count(),
        "total_lotes": Lote.objects.count(),
        "total_almacenes": Almacen.objects.count(),
        "total_movimientos": Movimiento.objects.count(),
        "ultimos": ultimos,
        "por_vencer": por_vencer,
        "hoy": hoy,
        "limite": limite,
    }
    return render(request, "inicio.html", contexto)
