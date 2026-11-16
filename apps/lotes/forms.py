from django import forms

from config.forms import BootstrapFormMixin

from .models import Lote


class LoteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Lote
        fields = ('fk_art', 'fk_ubi', 'lot_codigo', 'lot_fecha_vencimiento',)
        widgets = {'lot_fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
