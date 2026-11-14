from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from lotes.models import Lote
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.mixins import BusquedaMixin, EliminarProtegidoMixin

from .forms import AlmacenForm
from .models import Almacen


class AlmacenLista(PermissionRequiredMixin, BusquedaMixin, ListView):
    """Lista con búsqueda y paginación."""

    model = Almacen
    permission_required = "almacenes.view_almacen"
    campos_busqueda = ('nombre', 'direccion',)
    paginate_by = 10

    queryset = Almacen.objects.annotate(total_ubicaciones=Count('ubicaciones')).order_by('nombre')


class AlmacenCrear(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Almacen
    form_class = AlmacenForm
    permission_required = "almacenes.add_almacen"
    success_url = reverse_lazy("almacenes:lista")
    success_message = "Guardado correctamente."


class AlmacenEditar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Almacen
    form_class = AlmacenForm
    permission_required = "almacenes.change_almacen"
    success_url = reverse_lazy("almacenes:lista")
    success_message = "Cambios guardados."


class AlmacenEliminar(PermissionRequiredMixin, EliminarProtegidoMixin, DeleteView):
    model = Almacen
    permission_required = "almacenes.delete_almacen"
    success_url = reverse_lazy("almacenes:lista")
    mensaje_exito = "Eliminado correctamente."


@login_required
@permission_required("almacenes.view_almacen", raise_exception=True)
def stock(request):
    """Stock actual de cada lote, agrupado por almacén."""
    todos = Almacen.objects.order_by("nombre")
    elegido = request.GET.get("almacen", "")
    almacenes = todos.filter(pk=elegido) if elegido.isdigit() else todos

    grupos = []
    for almacen in almacenes:
        lotes = (
            Lote.objects.filter(ubicacion__almacen=almacen)
            .select_related("articulo", "ubicacion")
            .order_by("articulo__nombre", "codigo")
        )
        filas = [{"lote": lote, "stock": lote.stock_actual()} for lote in lotes]
        grupos.append({"almacen": almacen, "filas": filas, "total": sum(f["stock"] for f in filas)})

    contexto = {"grupos": grupos, "todos": todos, "elegido": elegido}
    return render(request, "almacenes/stock.html", contexto)
