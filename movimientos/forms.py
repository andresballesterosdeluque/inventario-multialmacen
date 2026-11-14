from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from almacenes.models import Almacen
from config.forms import BootstrapFormMixin

from .models import Movimiento


class MovimientoForm(BootstrapFormMixin, forms.ModelForm):
    """Datos generales del movimiento. Los artículos se agregan aparte, con el formset."""

    class Meta:
        model = Movimiento
        fields = ("fecha", "tipo", "observacion")
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "observacion": forms.TextInput(
                attrs={"placeholder": "Opcional: motivo, proveedor, número de guía…"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo"].choices = [("", "Elige el tipo…")] + Movimiento.TIPOS
        self.fields["observacion"].label = "Observación"

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > timezone.localdate():
            raise ValidationError("La fecha no puede ser futura.")
        return fecha


class FiltroMovimientoForm(BootstrapFormMixin, forms.Form):
    """Filtros de la lista de movimientos (el reporte)."""

    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Observación, lote o artículo"}),
    )
    tipo = forms.ChoiceField(
        label="Tipo", required=False, choices=[("", "Todos")] + Movimiento.TIPOS
    )
    almacen = forms.ModelChoiceField(
        label="Almacén",
        required=False,
        queryset=Almacen.objects.order_by("nombre"),
        empty_label="Todos",
    )
    desde = forms.DateField(
        label="Desde", required=False, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
    )
    hasta = forms.DateField(
        label="Hasta", required=False, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
    )

    def clean(self):
        datos = super().clean()
        desde, hasta = datos.get("desde"), datos.get("hasta")
        if desde and hasta and desde > hasta:
            raise ValidationError("La fecha «desde» no puede ser mayor que «hasta».")
        return datos
