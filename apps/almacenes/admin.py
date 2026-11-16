from django.contrib import admin

from apps.ubicaciones.models import Ubicacion
from .models import Almacen


class UbicacionInline(admin.TabularInline):
    model = Ubicacion
    extra = 1


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ("alm_nombre", "alm_direccion")
    search_fields = ("alm_nombre", "alm_direccion")
    list_filter = ("alm_nombre",)
    inlines = [UbicacionInline]
