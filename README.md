# StockMaster

StockMaster es un sistema de gestión de inventario modular y fácil de extender.

Repositorio GitHub: [StockMaster](https://github.com/bryanchavez79/StockMaster)

[![StockMaster](https://img.shields.io/badge/Repo-StockMaster-blue)](https://github.com/bryanchavez79/StockMaster)

> **¡Pruébalo localmente!** Ejecuta `python app.py` y abre `http://stockmaster:5000` en el navegador.

## Estructura del proyecto

- `main.py` - punto de entrada de la aplicación.
- `productos.py` - definición de la entidad `Producto` y validaciones de datos.
- `base_datos.py` - acceso a datos con SQLite y funciones CRUD.
- `interfaz.py` - menú de consola y flujo de usuario.
- `inventario.db` - base de datos SQLite creada automáticamente.
- `datos/` - exportaciones de datos como CSV.
- `imagenes/` - recursos gráficos o documentación visual.
- `reportes/` - reportes de inventario en texto.

## Estado actual del proyecto

- Repositorio: https://github.com/bryanchavez79/StockMaster
- Rama principal: `main`
- Archivos clave:
  - [`main.py`](main.py) - punto de entrada de la aplicación.
  - [`interfaz.py`](interfaz.py) - menú principal y submenú de reportes.
  - [`base_datos.py`](base_datos.py) - lógica de SQLite y operaciones CRUD.
  - [`productos.py`](productos.py) - modelo `Producto` y validaciones.

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

5. Ejecuta la aplicación de consola:

```bash
python main.py
```

### Interfaz web

1. Instala Flask si aún no lo has hecho:

```bash
pip install Flask
```

2. Ejecuta la aplicación web:

```bash
python app.py
```

3. Configura el nombre de host `stockmaster` en tu sistema (opcional):

   - **Windows**: Abre `C:\Windows\System32\drivers\etc\hosts` como administrador y agrega:
     ```
     127.0.0.1 stockmaster
     ```
   - **macOS/Linux**: Edita `/etc/hosts` y agrega:
     ```
     127.0.0.1 stockmaster
     ```

4. Abre en el navegador:

```text
http://stockmaster:5000
```

   Si no configuraste el archivo `hosts`, usa:
   ```text
   http://127.0.0.1:5000
   ```

5. Desde la web podrás:
   - ver y administrar productos
   - crear, editar y eliminar productos
   - generar reportes de inventario, stock bajo y stock crítico

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

## Importación desde CSV

1. Prepara un archivo CSV con las columnas:
   `codigo,nombre,categoria,precio,stock`
2. Elige la opción `10. Importar desde CSV` en el menú principal.
3. Ingresa la ruta del archivo CSV a importar.
4. El sistema agregará o actualizará los productos existentes según el `codigo`.

## Generación de reportes

1. Elige la opción `9. Reportes` en el menú principal.
2. Selecciona el reporte que deseas generar:
   - `1` Inventario completo
   - `2` Stock bajo
   - `3` Stock crítico
3. Elige el tipo de salida:
   - `1` TXT
   - `2` CSV
   - `3` Ambos
4. Revisa los archivos generados en `reportes/` y `datos/`.

### Descarga de reportes desde la web

1. Abre la interfaz web en `http://stockmaster:5000`
2. Haz clic en el menú **Reportes**
3. Completa el formulario:
   - Selecciona el tipo de reporte
   - Ingresa el umbral (si aplica)
   - Haz clic en **Generar**
4. Los reportes se generan automáticamente
5. En la sección **Reportes disponibles para descargar** encontrarás todos los archivos
6. Haz clic en **Descargar** para obtener el archivo

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
