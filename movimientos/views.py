from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from detalles_movimiento.forms import DetalleFormSet
from detalles_movimiento.models import DetalleMovimiento

from .forms import FiltroMovimientoForm, MovimientoForm
from .models import Movimiento
from .servicios import StockNegativo, eliminar_movimiento, guardar_movimiento

# Los formularios de las filas usan este prefijo (lo necesita el JavaScript de la página).
PREFIJO = "detalles"


@login_required
@permission_required("movimientos.view_movimiento", raise_exception=True)
def lista(request):
    """Lista de movimientos con filtros. También sirve como reporte."""
    filtro = FiltroMovimientoForm(request.GET or None)
    movimientos = Movimiento.objects.all()

    if filtro.is_valid():
        datos = filtro.cleaned_data
        if datos["tipo"]:
            movimientos = movimientos.filter(tipo=datos["tipo"])
        if datos["desde"]:
            movimientos = movimientos.filter(fecha__gte=datos["desde"])
        if datos["hasta"]:
            movimientos = movimientos.filter(fecha__lte=datos["hasta"])
        if datos["almacen"]:
            en_almacen = DetalleMovimiento.objects.filter(lote__ubicacion__almacen=datos["almacen"])
            movimientos = movimientos.filter(pk__in=en_almacen.values("movimiento"))
        if datos["q"]:
            texto = datos["q"].strip()
            coincide = DetalleMovimiento.objects.filter(
                Q(lote__codigo__icontains=texto) | Q(lote__articulo__nombre__icontains=texto)
            )
            movimientos = movimientos.filter(
                Q(observacion__icontains=texto) | Q(pk__in=coincide.values("movimiento"))
            )

    # primero se filtra y después se suman los artículos y las unidades de cada movimiento
    movimientos = movimientos.annotate(
        total_articulos=Count("detallemovimiento"),
        total_unidades=Sum("detallemovimiento__cantidad"),
    ).order_by("-fecha", "-id")

    parametros = request.GET.copy()
    parametros.pop("page", None)
    pagina = Paginator(movimientos, 10).get_page(request.GET.get("page"))
    contexto = {"filtro": filtro, "page_obj": pagina, "query": parametros.urlencode()}
    return render(request, "movimientos/movimiento_list.html", contexto)


@login_required
@permission_required("movimientos.view_movimiento", raise_exception=True)
def detalle(request, pk):
    """Un movimiento con todos sus artículos."""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    filas = movimiento.detallemovimiento_set.select_related(
        "lote__articulo", "lote__ubicacion__almacen"
    ).order_by("id")
    total = filas.aggregate(t=Sum("cantidad"))["t"] or 0
    contexto = {"movimiento": movimiento, "filas": filas, "total": total}
    return render(request, "movimientos/movimiento_detail.html", contexto)


def _formulario(request, movimiento, titulo):
    """Parte común de crear y editar: el formulario del movimiento y sus filas de artículos."""
    if request.method == "POST":
        form = MovimientoForm(request.POST, instance=movimiento)
        # las filas se revisan después de los datos generales, porque la validación del
        # stock necesita saber si el movimiento es una entrada o una salida
        form_ok = form.is_valid()
        formset = DetalleFormSet(request.POST, instance=form.instance, prefix=PREFIJO)
        formset_ok = formset.is_valid()
        if form_ok and formset_ok:
            try:
                guardado = guardar_movimiento(form, formset)
            except StockNegativo as error:
                messages.error(request, str(error))
            else:
                messages.success(request, f"Movimiento #{guardado.pk} guardado.")
                return redirect("movimientos:detalle", pk=guardado.pk)
    else:
        inicial = {"fecha": timezone.localdate()} if movimiento.pk is None else None
        form = MovimientoForm(instance=movimiento, initial=inicial)
        formset = DetalleFormSet(instance=movimiento, prefix=PREFIJO)
    contexto = {"form": form, "formset": formset, "titulo": titulo, "movimiento": movimiento}
    return render(request, "movimientos/movimiento_form.html", contexto)


@login_required
@permission_required("movimientos.add_movimiento", raise_exception=True)
def crear(request):
    return _formulario(request, Movimiento(), "Registrar movimiento")


@login_required
@permission_required("movimientos.change_movimiento", raise_exception=True)
def editar(request, pk):
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return _formulario(request, movimiento, f"Editar movimiento #{movimiento.pk}")


@login_required
@permission_required("movimientos.delete_movimiento", raise_exception=True)
def eliminar(request, pk):
    """Pide confirmación y luego borra el movimiento con sus detalles."""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    if request.method == "POST":
        try:
            eliminar_movimiento(movimiento)
        except StockNegativo as error:
            messages.error(request, str(error))
            return redirect("movimientos:detalle", pk=pk)
        messages.success(request, "Movimiento eliminado.")
        return redirect("movimientos:lista")
    filas = movimiento.detallemovimiento_set.select_related("lote__articulo")
    return render(request, "movimientos/movimiento_confirm_delete.html", {"movimiento": movimiento, "filas": filas})
