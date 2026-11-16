from django.urls import path

from . import views

app_name = "almacenes"

urlpatterns = [
    path("", views.AlmacenLista.as_view(), name="lista"),
    path("nuevo/", views.AlmacenCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.AlmacenEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.AlmacenEliminar.as_view(), name="eliminar"),
    path("stock/", views.stock, name="stock"),
]
