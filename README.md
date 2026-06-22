# StockMaster

StockMaster es un sistema de gestión de inventario modular y fácil de extender.

Repositorio: https://github.com/bryanchavez79/StockMaster

## Estructura del proyecto

- `main.py` - punto de entrada de la aplicación.
- `productos.py` - definición de la entidad `Producto` y validaciones de datos.
- `base_datos.py` - acceso a datos con SQLite y funciones CRUD.
- `interfaz.py` - menú de consola y flujo de usuario.
- `inventario.db` - base de datos SQLite creada automáticamente.
- `datos/` - exportaciones de datos como CSV.
- `imagenes/` - recursos gráficos o documentación visual.
- `reportes/` - reportes de inventario en texto.

## Funcionalidades actuales

- Agregar producto
- Ver todos los productos
- Buscar productos por nombre
- Buscar productos por categoría
- Ver stock bajo
- Generar reporte de stock bajo y CSV de stock bajo
- Actualizar producto
- Eliminar producto
- Exportar inventario a CSV
- Importar productos desde CSV
- Generar reporte de inventario en texto

## Uso

1. Ejecuta la aplicación con:

```bash
python main.py
```

2. Selecciona una opción del menú.

4. Para exportar el inventario o generar reportes, elige la opción "Reportes".
   - Dentro del submenú de reportes puedes elegir:
     - Inventario completo
     - Stock bajo
     - Stock crítico
   - Para cada reporte se puede generar:
     - TXT
     - CSV
     - Ambos
5. Para importar productos desde un archivo CSV, elige la opción "Importar desde CSV".

## Archivos generados

- `inventario.db` se crea en la raíz del proyecto.
- `datos/productos.csv` se genera al exportar el inventario.
- `reportes/inventario.txt` se genera como reporte de inventario.

## Requisitos

- Python 3.11 o superior.

## Siguientes mejoras posibles

- Agregar importación desde CSV.
- Añadir categorías predefinidas.
- Implementar un front-end web con Flask o FastAPI.
- Crear reportes en PDF o Excel.
