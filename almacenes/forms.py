from django import forms

from config.forms import BootstrapFormMixin

from .models import Almacen


class AlmacenForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ('nombre', 'direccion',)
