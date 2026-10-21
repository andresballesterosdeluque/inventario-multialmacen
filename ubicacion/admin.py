from django.contrib import admin

from .models import Ubicacion

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_alma', 'ubi_codigo', 'ubi_pasillo')
    search_fields = ('ubi_codigo', 'ubi_pasillo')
    list_filter = ('fk_alma',)