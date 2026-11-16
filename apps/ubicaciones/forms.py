from django import forms

from config.forms import BootstrapFormMixin

from .models import Ubicacion


class UbicacionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ('fk_alm', 'ubi_estante', 'ubi_nivel',)
