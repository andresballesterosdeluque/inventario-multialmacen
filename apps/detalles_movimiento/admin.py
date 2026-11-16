from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .forms import DetalleMovimientoFormSet
from .models import DetalleMovimiento


class DetalleMovimientoInline(admin.TabularInline):
    model = DetalleMovimiento
    formset = DetalleMovimientoFormSet
    extra = 1


class DetalleMovimientoForm(forms.ModelForm):
    """Misma validacion cuando se crea o edita un detalle por separado."""

    class Meta:
        model = DetalleMovimiento
        fields = "__all__"

    def clean(self):
        datos = super().clean()
        movimiento = datos.get("fk_mov")
        lote = datos.get("fk_lot")
        cantidad = datos.get("det_cantidad")
        if movimiento and lote and cantidad and movimiento.mov_tipo == "SALIDA":
            disponible = lote.stock_actual()
            if self.instance.pk:
                previo = DetalleMovimiento.objects.select_related("fk_mov").get(pk=self.instance.pk)
                if previo.fk_mov.mov_tipo == "SALIDA" and previo.fk_lot_id == lote.pk:
                    disponible += previo.det_cantidad
            if cantidad > disponible:
                raise ValidationError(
                    f"Stock insuficiente en {lote}: disponible {disponible}, solicitado {cantidad}."
                )
        return datos


@admin.register(DetalleMovimiento)
class DetalleMovimientoAdmin(admin.ModelAdmin):
    form = DetalleMovimientoForm
    list_display = ("fk_mov", "fk_lot", "det_cantidad")
    search_fields = ("fk_lot__lot_codigo",)
    list_filter = ("fk_mov__mov_tipo",)
