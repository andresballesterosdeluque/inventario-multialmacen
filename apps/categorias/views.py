from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.mixins import BusquedaMixin, EliminarProtegidoMixin

from .forms import CategoriaForm
from .models import Categoria


class CategoriaLista(PermissionRequiredMixin, BusquedaMixin, ListView):
    """Lista con búsqueda y paginación."""

    model = Categoria
    permission_required = "categorias.view_categoria"
    campos_busqueda = ('nombre',)
    paginate_by = 10

    queryset = Categoria.objects.annotate(total_articulos=Count('articulos')).order_by('nombre')


class CategoriaCrear(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    permission_required = "categorias.add_categoria"
    success_url = reverse_lazy("categorias:lista")
    success_message = "Guardado correctamente."


class CategoriaEditar(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    permission_required = "categorias.change_categoria"
    success_url = reverse_lazy("categorias:lista")
    success_message = "Cambios guardados."


class CategoriaEliminar(PermissionRequiredMixin, EliminarProtegidoMixin, DeleteView):
    model = Categoria
    permission_required = "categorias.delete_categoria"
    success_url = reverse_lazy("categorias:lista")
    mensaje_exito = "Eliminado correctamente."
