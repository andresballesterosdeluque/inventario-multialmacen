# Sistema de Inventario - Multialmacen

Proyecto de inventario con manejo de Almacenes, Artículos, Lotes, Ubicaciones y Movimientos.

Estudiantes: Andres Felipe Ballesteros - Temistocle Atencio - Alain Suarez

Materia: Programacion Avanzada

### Modelo de Datos
El sistema implementa el modelo relacional con relaciones:
- Almacén (1) -> (N) Ubicación (Débil)
- Artículo (1) -> (N) Lote (Débil)
- Movimiento (1) -> (N) DetalleMovimiento (Débil)
- DetalleMovimiento (N) -> (1) Lote

Cumple con inlines en el admin de Django para tablas débiles

lo cual son Almacen , Articulo , Movimiento - hago una aclaracion en el django aparece como articulo core 
pero el nombre de la clase es Articulo .

### Tecnologías
- Python 3.14.8
- Django 6.1.2
- SQLite3

### Instalación y Ejecución

 Clonar el repositorio:
```bash
git clone https://github.com/andresballesterosdeluque/inventario-multialmacen.git
cd inventario-multialmacen

usuario = admin
clave= admin123

"http://127.0.0.1:8000/admin/ para entrar se debe añadir el admin/ , ya que al hacer runserver , se manda http://127.0.0.1:8000 "