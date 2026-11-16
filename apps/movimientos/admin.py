from django.contrib import admin

from apps.detalles_movimiento.admin import DetalleMovimientoInline
from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("pk_mov_id", "mov_tipo", "mov_fecha", "mov_observacion")
    search_fields = ("mov_observacion",)
    list_filter = ("mov_tipo", "mov_fecha")
    inlines = [DetalleMovimientoInline]
