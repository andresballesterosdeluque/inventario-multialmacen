  Sistema de Inventario - Multialmacén

Sistema de información desarrollado con Django para gestionar el inventario de varios almacenes: almacenes, ubicaciones, categorías, artículos, lotes y movimientos de entrada y salida.

Toda la información se registra desde el panel de administración de Django.

| | |
|---|---|
| Estudiantes | Andrés Felipe Ballesteros, Temistocle Atencio, Alain Suárez |
| Materia | Programación Avanzada |
| Docente | Brayan Otero |

---

## 1. Qué hace el sistema

- Registra almacenes y sus ubicaciones (código y pasillo).

- Clasifica los artículos por categoría.

- Controla los lotes de cada artículo: cantidad, almacén y fecha de vencimiento.

- Registra movimientos de entrada y salida por almacén, con el detalle de los lotes afectados.

---

## 2. Modelo de datos

Cada tabla del diagrama es un modelo de Django y vive en su propia app.

| App | Modelo | Descripción |
|---|---|---|
| `almacen` | Almacen | Almacenes físicos |
| `ubicacion` | Ubicacion | Entidad débil de Almacen |
| `categoria` | Categoria | Clasificación de los artículos |
| `articulo_core` | Articulo | Productos del inventario |
| `lote` | Lote | Entidad débil de Articulo (también asociada a un Almacen) |
| `movimiento` | Movimiento | Entradas y salidas por almacén |
| `detalle_movimiento` | DetalleMovimiento | Tabla intermedia de la relación N:M entre Movimiento y Lote |

Nota:la app del artículo se llama `articulo_core`, pero la clase del modelo es `Articulo`.

### Relaciones

- Categoría (1) → (N) Artículo

- Almacén (1) → (N) Ubicación (entidad débil)

- Artículo (1) → (N) Lote (entidad débil)

- Almacén (1) → (N) Movimiento

- Movimiento (N) ↔ (N) Lote, resuelta con la tabla intermedia DetalleMovimiento

### Inlines en el admin

Las entidades débiles y la tabla intermedia se registran con inline dentro del formulario de su dueño:

- Ubicaciones dentro de Almacén

- Lotes dentro de Artículo

- Detalles de movimiento dentro de Movimiento

---

## 3. Versiones tecnológicas que se usan

- Python 3.14.8

- Django 6.1.2

- SQLite3

---

## 4. Instalación y ejecución

Paso 1. Clonar el repositorio:

```bash
git clone https://github.com/andresballesterosdeluque/inventario-multialmacen.git
cd inventario-multialmacen
```

Paso 2. Crear y activar el entorno virtual:

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash (Windows)
```

**Paso 3.** Instalar las dependencias:

```bash
pip install -r requirements.txt
```

**Paso 4.** Ejecutar el servidor (la base `db.sqlite3` ya incluye los datos de prueba):

```bash
python manage.py runserver
```

Paso 5. Entrar al panel de administración:

http://127.0.0.1:8000/admin/

> Importante: hay que añadir `/admin/` al final de la dirección. Si se entra solo con http://127.0.0.1:8000 no aparece nada, porque la página principal no tiene contenido.

---

## 5. Credenciales del administrador

| | |
|---|---|
| **Usuario** | `admin` |
| **Clave** | `admin123` |

---

## 6. Estructura del proyecto

```
inventario-multialmacen/
├── configuracion/        # settings.py, urls.py
├── almacen/              # modelo Almacen
├── ubicacion/            # modelo Ubicacion (entidad débil de Almacen)
├── categoria/            # modelo Categoria
├── articulo_core/        # modelo Articulo
├── lote/                 # modelo Lote (entidad débil de Articulo)
├── movimiento/           # modelo Movimiento
├── detalle_movimiento/   # modelo DetalleMovimiento (tabla intermedia del N:M)
├── docs/                 # diagramas: diagrama_actores.png, diagrama_er.png
├── db.sqlite3            # base de datos con los datos de prueba
├── manage.py
├── requirements.txt
└── README.md
```

---

## 7. Diagramas

- Diagrama de casos de uso: `docs/diagrama_actores.png`

- Diagrama entidad-relación: `docs/diagrama_er.png`

