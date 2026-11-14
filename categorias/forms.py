from django import forms

from config.forms import BootstrapFormMixin

from .models import Categoria


class CategoriaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)
