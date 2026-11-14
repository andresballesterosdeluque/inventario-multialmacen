from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from config.forms import BootstrapFormMixin
from lotes.models import Lote
from movimientos.models import Movimiento

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


class LoteChoiceField(forms.ModelChoiceField):
    """Muestra cada lote con su artículo, su almacén y el stock que tiene ahora."""

    def label_from_instance(self, lote):
        return (
            f"{lote.codigo} · {lote.articulo.nombre} · "
            f"{lote.ubicacion.almacen.nombre} · stock {lote.stock_actual()}"
        )


class DetalleForm(BootstrapFormMixin, forms.ModelForm):
    """Una fila del movimiento: un lote y la cantidad."""

    lote = LoteChoiceField(
        queryset=Lote.objects.select_related("articulo", "ubicacion__almacen").order_by("codigo"),
        empty_label="Elige un lote…",
    )

    class Meta:
        model = DetalleMovimiento
        fields = ("lote", "cantidad")
        widgets = {"cantidad": forms.NumberInput(attrs={"min": 1})}

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]
        if cantidad < 1:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad


# Conjunto de filas para el formulario del movimiento (se necesita al menos una).
DetalleFormSet = inlineformset_factory(
    Movimiento,
    DetalleMovimiento,
    form=DetalleForm,
    formset=DetalleMovimientoFormSet,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
