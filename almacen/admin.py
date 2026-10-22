from django.contrib import admin
from .models import Almacen
from ubicacion.models import Ubicacion

class UbicacionInline(admin.TabularInline):
    model = Ubicacion
    extra = 1

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('id', 'alm_nombre', 'alm_direccion')
    search_fields = ('alm_nombre',)
    list_filter = ('alm_nombre',)
    inlines = [UbicacionInline]