from django.contrib import admin

from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_nombre', 'cat_descripcion')
    list_filter = ('cat_nombre',)
    search_fields = ('cat_nombre', 'cat_descripcion')