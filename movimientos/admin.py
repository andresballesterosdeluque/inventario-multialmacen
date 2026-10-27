from django.contrib import admin

from detalles_movimiento.admin import DetalleMovimientoInline
from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "fecha", "observacion")
    search_fields = ("observacion",)
    list_filter = ("tipo", "fecha")
    inlines = [DetalleMovimientoInline]
