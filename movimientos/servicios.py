"""Lo que hace falta para guardar y borrar movimientos sin dejar el stock en negativo."""
from django.db import transaction

from detalles_movimiento.models import DetalleMovimiento
from lotes.models import Lote


class StockNegativo(Exception):
    """Pasa cuando un cambio dejaría un lote con menos de cero unidades."""


def _revisar_stock(lotes_ids):
    for lote in Lote.objects.filter(pk__in=lotes_ids):
        stock = lote.stock_actual()
        if stock < 0:
            raise StockNegativo(
                f"El cambio dejaría el lote {lote.codigo} con stock negativo ({stock}). "
                "No se guardó nada."
            )


def guardar_movimiento(form, formset):
    """Guarda el movimiento y sus detalles en un solo paso.

    Si algún lote queda con stock negativo (por ejemplo, al bajar una entrada que ya
    se había sacado), se deshace todo y se lanza StockNegativo.
    """
    lotes_antes = set()
    if form.instance.pk:
        lotes_antes = set(
            DetalleMovimiento.objects.filter(movimiento=form.instance).values_list("lote_id", flat=True)
        )
    with transaction.atomic():
        movimiento = form.save()
        formset.instance = movimiento
        formset.save()
        lotes_despues = set(movimiento.detallemovimiento_set.values_list("lote_id", flat=True))
        _revisar_stock(lotes_antes | lotes_despues)
    return movimiento


def eliminar_movimiento(movimiento):
    """Borra el movimiento y sus detalles. Si el stock queda en negativo, lo deshace."""
    lotes = set(movimiento.detallemovimiento_set.values_list("lote_id", flat=True))
    with transaction.atomic():
        movimiento.delete()
        _revisar_stock(lotes)
