from django import forms

from config.forms import BootstrapFormMixin

from .models import Lote


class LoteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Lote
        fields = ('articulo', 'ubicacion', 'codigo', 'fecha_vencimiento',)
        widgets = {'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
