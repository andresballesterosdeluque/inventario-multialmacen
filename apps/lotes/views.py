from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.mixins import BusquedaMixin, EliminarProtegidoMixin

from .forms import LoteForm
from .models import Lote


class LoteLista(PermissionRequiredMixin, BusquedaMixin, ListView):
    """Lista con búsqueda y paginación."""

    model = Lote
    permission_required = "lotes.view_lote"
    campos_busqueda = ('codigo', 'articulo__nombre', 'ubicacion__estante', 'ubicacion__almacen__nombre',)
    paginate_by = 10

    queryset = Lote.objects.select_related('articulo', 'ubicacion__almacen').order_by('codigo')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        contexto["hoy"] = hoy
        contexto["limite"] = hoy + timedelta(days=30)  # "por vencer" = vence en menos de 30 días
        return contexto


class LoteCrear(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lote
    form_class = LoteForm
    permission_required = "lotes.add_lote"
    success_url = reverse_lazy("lotes:lista")
    success_message = "Guardado correctamente."


class LoteEditar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lote
    form_class = LoteForm
    permission_required = "lotes.change_lote"
    success_url = reverse_lazy("lotes:lista")
    success_message = "Cambios guardados."


class LoteEliminar(PermissionRequiredMixin, EliminarProtegidoMixin, DeleteView):
    model = Lote
    permission_required = "lotes.delete_lote"
    success_url = reverse_lazy("lotes:lista")
    mensaje_exito = "Eliminado correctamente."
