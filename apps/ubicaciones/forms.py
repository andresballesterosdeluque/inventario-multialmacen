from django import forms

from config.forms import BootstrapFormMixin

from .models import Ubicacion


class UbicacionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ('almacen', 'estante', 'nivel',)
