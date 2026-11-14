from django.urls import path

from . import views

app_name = "ubicaciones"

urlpatterns = [
    path("", views.UbicacionLista.as_view(), name="lista"),
    path("nuevo/", views.UbicacionCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.UbicacionEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.UbicacionEliminar.as_view(), name="eliminar"),
]
