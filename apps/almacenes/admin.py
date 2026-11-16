from django.contrib import admin

from apps.ubicaciones.models import Ubicacion
from .models import Almacen


class UbicacionInline(admin.TabularInline):
    model = Ubicacion
    extra = 1


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion")
    search_fields = ("nombre", "direccion")
    list_filter = ("nombre",)
    inlines = [UbicacionInline]
