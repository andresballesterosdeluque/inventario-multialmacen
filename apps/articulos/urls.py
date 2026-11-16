from django.urls import path

from . import views

app_name = "articulos"

urlpatterns = [
    path("", views.ArticuloLista.as_view(), name="lista"),
    path("nuevo/", views.ArticuloCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.ArticuloEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.ArticuloEliminar.as_view(), name="eliminar"),
]
