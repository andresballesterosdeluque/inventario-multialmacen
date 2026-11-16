from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from config.forms import BootstrapFormMixin
from apps.lotes.models import Lote
from apps.movimientos.models import Movimiento

from .models import DetalleMovimiento


class DetalleMovimientoFormSet(BaseInlineFormSet):
    """Evita salidas mayores al stock disponible al editar un movimiento."""

    def clean(self):
        super().clean()
        if self.instance.mov_tipo != "SALIDA":
            return

        pedidos = {}
        for form in self.forms:
            datos = getattr(form, "cleaned_data", None)
            if not datos or datos.get("DELETE"):
                continue
            lote = datos.get("fk_lot")
            cantidad = datos.get("det_cantidad")
            if lote and cantidad:
                pedidos[lote] = pedidos.get(lote, 0) + cantidad

        for lote, total in pedidos.items():
            disponible = lote.stock_actual()
            if self.instance.pk:
                # Si la salida ya existia, su propia cantidad ya esta descontada
                previo = DetalleMovimiento.objects.filter(
                    fk_mov=self.instance, fk_lot=lote
                ).aggregate(t=Sum("det_cantidad"))["t"] or 0
                disponible += previo
            if total > disponible:
                raise ValidationError(
                    f"Stock insuficiente en {lote}: disponible {disponible}, solicitado {total}."
                )


class LoteChoiceField(forms.ModelChoiceField):
    """Muestra cada lote con su artículo, su almacén y el stock que tiene ahora."""

    def label_from_instance(self, lote):
        return (
            f"{lote.lot_codigo} · {lote.fk_art.art_nombre} · "
            f"{lote.fk_ubi.fk_alm.alm_nombre} · stock {lote.stock_actual()}"
        )


class DetalleForm(BootstrapFormMixin, forms.ModelForm):
    """Una fila del movimiento: un lote y la cantidad."""

    fk_lot = LoteChoiceField(
        label="Lote",
        queryset=Lote.objects.select_related("fk_art", "fk_ubi__fk_alm").order_by("lot_codigo"),
        empty_label="Elige un lote…",
    )

    class Meta:
        model = DetalleMovimiento
        fields = ("fk_lot", "det_cantidad")
        widgets = {"det_cantidad": forms.NumberInput(attrs={"min": 1})}

    def clean_det_cantidad(self):
        cantidad = self.cleaned_data["det_cantidad"]
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
