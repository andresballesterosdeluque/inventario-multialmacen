from django import forms

from config.forms import BootstrapFormMixin

from .models import Articulo


class ArticuloForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ('categoria', 'codigo', 'nombre', 'unidad',)
