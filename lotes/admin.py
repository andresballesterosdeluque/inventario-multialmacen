from django.contrib import admin

from .models import Lote


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "articulo", "ubicacion", "fecha_vencimiento", "stock_actual")
    search_fields = ("codigo", "articulo__nombre")
    list_filter = ("articulo", "fecha_vencimiento")
