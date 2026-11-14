// Filas de artículos del formulario de movimiento: agregar y quitar sin recargar la página.
(function () {
  var contenedor = document.getElementById('filas-detalle');
  if (!contenedor) return;
  var total = document.getElementById('id_detalles-TOTAL_FORMS');
  var plantilla = document.getElementById('plantilla-fila').innerHTML;
  var boton = document.getElementById('agregar-fila');

  function visibles() {
    return Array.prototype.filter.call(contenedor.querySelectorAll('.fila-detalle'), function (f) { return !f.hidden; });
  }
  function revisarBotones() {
    var solo = visibles().length <= 1;
    visibles().forEach(function (f) { var b = f.querySelector('.btn-quitar'); if (b) b.disabled = solo; });
  }

  boton.addEventListener('click', function () {
    var n = parseInt(total.value, 10);
    var div = document.createElement('div');
    div.innerHTML = plantilla.replace(/__prefix__/g, n).trim();
    contenedor.appendChild(div.firstElementChild);
    total.value = n + 1;
    revisarBotones();
  });

  contenedor.addEventListener('click', function (e) {
    var b = e.target.closest('.btn-quitar');
    if (!b || b.disabled) return;
    var fila = b.closest('.fila-detalle');
    // la fila se oculta y se marca para borrar; Django la ignora al guardar
    var marca = fila.querySelector('input[type=checkbox][name$="-DELETE"]');
    if (marca) marca.checked = true;
    fila.hidden = true;
    revisarBotones();
  });
  revisarBotones();
})();
