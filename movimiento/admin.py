from django.contrib import admin
from .models import Movimiento
from detalle_movimiento.models import DetalleMovimiento

class DetalleMovimientoInline(admin.TabularInline):
    model = DetalleMovimiento
    extra = 1

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mov_tipo', 'fk_alm', 'mov_fecha', 'mov_responsable')
    search_fields = ('mov_responsable',)
    list_filter = ('mov_tipo', 'fk_alm')
    inlines = [DetalleMovimientoInline]