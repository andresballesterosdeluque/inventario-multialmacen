from django.urls import path

from . import views

app_name = "lotes"

urlpatterns = [
    path("", views.LoteLista.as_view(), name="lista"),
    path("nuevo/", views.LoteCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.LoteEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.LoteEliminar.as_view(), name="eliminar"),
]
