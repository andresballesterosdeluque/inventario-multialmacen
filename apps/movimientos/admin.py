from django.contrib import admin

from apps.detalles_movimiento.admin import DetalleMovimientoInline
from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("pk_mov_id", "mov_tipo", "mov_fecha", "mov_observacion", "fk_usu")
    search_fields = ("mov_observacion",)
    list_filter = ("mov_tipo", "mov_fecha")
    readonly_fields = ("fk_usu",)
    inlines = [DetalleMovimientoInline]

    def save_model(self, request, obj, form, change):
        # un movimiento nuevo queda a nombre de quien lo registra
        if not change:
            obj.fk_usu = request.user
        super().save_model(request, obj, form, change)
