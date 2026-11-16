from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.mixins import BusquedaMixin, EliminarProtegidoMixin

from .forms import ArticuloForm
from .models import Articulo


class ArticuloLista(PermissionRequiredMixin, BusquedaMixin, ListView):
    """Lista con búsqueda y paginación."""

    model = Articulo
    permission_required = "articulos.view_articulo"
    campos_busqueda = ('codigo', 'nombre', 'categoria__nombre',)
    paginate_by = 10

    queryset = Articulo.objects.select_related('categoria').order_by('codigo')


class ArticuloCrear(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    permission_required = "articulos.add_articulo"
    success_url = reverse_lazy("articulos:lista")
    success_message = "Guardado correctamente."


class ArticuloEditar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Articulo
    form_class = ArticuloForm
    permission_required = "articulos.change_articulo"
    success_url = reverse_lazy("articulos:lista")
    success_message = "Cambios guardados."


class ArticuloEliminar(PermissionRequiredMixin, EliminarProtegidoMixin, DeleteView):
    model = Articulo
    permission_required = "articulos.delete_articulo"
    success_url = reverse_lazy("articulos:lista")
    mensaje_exito = "Eliminado correctamente."
