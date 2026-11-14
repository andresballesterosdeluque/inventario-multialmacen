from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.mixins import BusquedaMixin, EliminarProtegidoMixin

from .forms import UbicacionForm
from .models import Ubicacion


class UbicacionLista(PermissionRequiredMixin, BusquedaMixin, ListView):
    """Lista con búsqueda y paginación."""

    model = Ubicacion
    permission_required = "ubicaciones.view_ubicacion"
    campos_busqueda = ('estante', 'nivel', 'almacen__nombre',)
    paginate_by = 10

    queryset = Ubicacion.objects.select_related('almacen').order_by('almacen__nombre', 'estante')


class UbicacionCrear(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    permission_required = "ubicaciones.add_ubicacion"
    success_url = reverse_lazy("ubicaciones:lista")
    success_message = "Guardado correctamente."


class UbicacionEditar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    permission_required = "ubicaciones.change_ubicacion"
    success_url = reverse_lazy("ubicaciones:lista")
    success_message = "Cambios guardados."


class UbicacionEliminar(PermissionRequiredMixin, EliminarProtegidoMixin, DeleteView):
    model = Ubicacion
    permission_required = "ubicaciones.delete_ubicacion"
    success_url = reverse_lazy("ubicaciones:lista")
    mensaje_exito = "Eliminado correctamente."
