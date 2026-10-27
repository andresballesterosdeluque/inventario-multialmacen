from django.contrib import admin

from lotes.models import Lote
from .models import Articulo


class LoteInline(admin.TabularInline):
    model = Lote
    extra = 1
    readonly_fields = ("stock_actual",)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "unidad", "stock_total")
    search_fields = ("codigo", "nombre")
    list_filter = ("categoria", "unidad")
    inlines = [LoteInline]
