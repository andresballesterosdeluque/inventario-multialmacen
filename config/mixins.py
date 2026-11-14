from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect


class BusquedaMixin:
    """Agrega una búsqueda (?q=texto) a una lista.

    Cada vista dice en qué campos buscar con `campos_busqueda`.
    """

    campos_busqueda = ()

    def get_queryset(self):
        consulta = super().get_queryset()
        texto = self.request.GET.get("q", "").strip()
        if texto and self.campos_busqueda:
            condicion = Q()
            for campo in self.campos_busqueda:
                condicion |= Q(**{f"{campo}__icontains": texto})
            consulta = consulta.filter(condicion)
        return consulta

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["q"] = self.request.GET.get("q", "").strip()
        # para que la paginación conserve la búsqueda
        parametros = self.request.GET.copy()
        parametros.pop("page", None)
        contexto["query"] = parametros.urlencode()
        return contexto


class EliminarProtegidoMixin:
    """Al eliminar, si el registro tiene datos relacionados avisa y no da error."""

    mensaje_exito = "Registro eliminado."

    def form_valid(self, form):
        destino = self.get_success_url()
        try:
            respuesta = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar porque tiene registros relacionados. "
                "Primero hay que quitar o cambiar esos registros.",
            )
            return redirect(destino)
        messages.success(self.request, self.mensaje_exito)
        return respuesta
