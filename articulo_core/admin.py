from django.contrib import admin
from .models import Articulo
from lote.models import Lote

class LoteInline(admin.TabularInline):
    model = Lote
    extra = 1

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_articulo', 'art_sku', 'precio_articulo', 'fk_cat')
    search_fields = ('nombre_articulo', 'art_sku')
    list_filter = ('fk_cat',)
    inlines = [LoteInline]