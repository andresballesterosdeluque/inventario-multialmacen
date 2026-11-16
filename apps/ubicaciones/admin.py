from django.contrib import admin

from .models import Ubicacion


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("almacen", "estante", "nivel")
    search_fields = ("estante", "almacen__nombre")
    list_filter = ("almacen",)
