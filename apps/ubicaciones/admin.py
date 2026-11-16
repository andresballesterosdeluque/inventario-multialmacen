from django.contrib import admin

from .models import Ubicacion


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("fk_alm", "ubi_estante", "ubi_nivel")
    search_fields = ("ubi_estante", "fk_alm__alm_nombre")
    list_filter = ("fk_alm",)
