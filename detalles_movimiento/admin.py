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
        movimiento = datos.get("movimiento")
        lote = datos.get("lote")
        cantidad = datos.get("cantidad")
        if movimiento and lote and cantidad and movimiento.tipo == "SALIDA":
            disponible = lote.stock_actual()
            if self.instance.pk:
                previo = DetalleMovimiento.objects.select_related("movimiento").get(pk=self.instance.pk)
                if previo.movimiento.tipo == "SALIDA" and previo.lote_id == lote.pk:
                    disponible += previo.cantidad
            if cantidad > disponible:
                raise ValidationError(
                    f"Stock insuficiente en {lote}: disponible {disponible}, solicitado {cantidad}."
                )
        return datos


@admin.register(DetalleMovimiento)
class DetalleMovimientoAdmin(admin.ModelAdmin):
    form = DetalleMovimientoForm
    list_display = ("movimiento", "lote", "cantidad")
    search_fields = ("lote__codigo",)
    list_filter = ("movimiento__tipo",)
