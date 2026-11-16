from django.urls import path

from . import views

app_name = "categorias"

urlpatterns = [
    path("", views.CategoriaLista.as_view(), name="lista"),
    path("nuevo/", views.CategoriaCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.CategoriaEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.CategoriaEliminar.as_view(), name="eliminar"),
]
