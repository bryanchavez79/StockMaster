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

## Instalación

1. Asegúrate de tener Python 3.11 o superior instalado.
2. Abre una terminal en la carpeta del proyecto `e:\StockMaster`.
3. (Opcional) Crea un entorno virtual:

```bash
python -m venv .venv
```

4. Activa el entorno virtual:

- PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- CMD:
  ```cmd
  .venv\Scripts\activate.bat
  ```

5. Ejecuta la aplicación:

```bash
python main.py
```

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

## Pruebas rápidas

1. Ejecuta `python main.py`.
2. Elige `1` para agregar un producto y completa el formulario.
3. Elige `2` para ver la lista de productos y confirmar que el producto quedó guardado.
4. Elige `9` para ir al submenú de reportes.
   - Selecciona `1` para generar inventario completo.
   - Selecciona `2` para generar stock bajo.
   - Selecciona `3` para generar stock crítico.
   - Luego elige el formato de salida: `1` TXT, `2` CSV o `3` Ambos.
5. Verifica los archivos generados en las carpetas `reportes/` y `datos/`.

## Formato de CSV para importación

El archivo CSV debe tener estas columnas en la primera fila:

```csv
codigo,nombre,categoria,precio,stock
P001,Manzana,Fruta,0.50,100
P002,Arroz,Alimentos,1.20,50
```

- `codigo`: identificador único del producto
- `nombre`: nombre del producto
- `categoria`: categoría del producto
- `precio`: precio unitario (número decimal)
- `stock`: cantidad en inventario (entero)

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
