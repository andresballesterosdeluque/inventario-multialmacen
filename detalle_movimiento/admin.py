from django.contrib import admin

from .models import DetalleMovimiento

@admin.register(DetalleMovimiento)
class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_mov', 'fk_lot', 'det_cantidad')
    list_filter = ('fk_mov', 'fk_lot')
    search_fields = ('id',)