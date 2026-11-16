from django.contrib import admin

from apps.lotes.models import Lote
from .models import Articulo


class LoteInline(admin.TabularInline):
    model = Lote
    extra = 1
    readonly_fields = ("stock_actual",)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("art_codigo", "art_nombre", "fk_cat", "art_unidad", "stock_total")
    search_fields = ("art_codigo", "art_nombre")
    list_filter = ("fk_cat", "art_unidad")
    inlines = [LoteInline]
