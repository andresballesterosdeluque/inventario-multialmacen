from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms.models import BaseInlineFormSet

from .models import DetalleMovimiento


class DetalleMovimientoFormSet(BaseInlineFormSet):
    """Evita salidas mayores al stock disponible al editar un movimiento."""

    def clean(self):
        super().clean()
        if self.instance.tipo != "SALIDA":
            return

        pedidos = {}
        for form in self.forms:
            datos = getattr(form, "cleaned_data", None)
            if not datos or datos.get("DELETE"):
                continue
            lote = datos.get("lote")
            cantidad = datos.get("cantidad")
            if lote and cantidad:
                pedidos[lote] = pedidos.get(lote, 0) + cantidad

        for lote, total in pedidos.items():
            disponible = lote.stock_actual()
            if self.instance.pk:
                # Si la salida ya existia, su propia cantidad ya esta descontada
                previo = DetalleMovimiento.objects.filter(
                    movimiento=self.instance, lote=lote
                ).aggregate(t=Sum("cantidad"))["t"] or 0
                disponible += previo
            if total > disponible:
                raise ValidationError(
                    f"Stock insuficiente en {lote}: disponible {disponible}, solicitado {total}."
                )


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
