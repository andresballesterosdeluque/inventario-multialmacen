from django.contrib import admin

from .models import Lote

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'lot_codigo', 'fk_art', 'fk_alm', 'lot_cantidad', 'lot_fecha_vencimiento')
    search_fields = ('lot_codigo',)
    list_filter = ('fk_art', 'fk_alm')