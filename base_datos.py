import csv
import sqlite3
from pathlib import Path
from productos import Producto

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "inventario.db"
DATOS_DIR = BASE_DIR / "datos"
REPORTES_DIR = BASE_DIR / "reportes"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS productos (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
"""


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar() -> None:
    with conectar() as conexion:
        conexion.execute(CREATE_TABLE_SQL)
        conexion.commit()


def agregar_producto(producto: Producto) -> None:
    with conectar() as conexion:
        conexion.execute(
            "INSERT INTO productos (codigo, nombre, categoria, precio, stock) VALUES (?, ?, ?, ?, ?)",
            (producto.codigo, producto.nombre, producto.categoria, producto.precio, producto.stock),
        )
        conexion.commit()


def obtener_productos() -> list[Producto]:
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT codigo, nombre, categoria, precio, stock FROM productos ORDER BY nombre"
        )
        return [Producto.from_row(row) for row in cursor.fetchall()]


def obtener_producto(codigo: str) -> Producto | None:
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT codigo, nombre, categoria, precio, stock FROM productos WHERE codigo = ?",
            (codigo,),
        )
        row = cursor.fetchone()
        return Producto.from_row(row) if row else None


def buscar_productos_por_categoria(categoria: str) -> list[Producto]:
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT codigo, nombre, categoria, precio, stock FROM productos WHERE LOWER(categoria) = LOWER(?) ORDER BY nombre",
            (categoria,),
        )
        return [Producto.from_row(row) for row in cursor.fetchall()]


def buscar_productos_por_nombre(nombre: str) -> list[Producto]:
    with conectar() as conexion:
        termino = f"%{nombre}%"
        cursor = conexion.execute(
            "SELECT codigo, nombre, categoria, precio, stock FROM productos WHERE LOWER(nombre) LIKE LOWER(?) ORDER BY nombre",
            (termino,),
        )
        return [Producto.from_row(row) for row in cursor.fetchall()]


def obtener_productos_bajo_stock(umbral: int = 5) -> list[Producto]:
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT codigo, nombre, categoria, precio, stock FROM productos WHERE stock <= ? ORDER BY stock, nombre",
            (umbral,),
        )
        return [Producto.from_row(row) for row in cursor.fetchall()]


def actualizar_producto(producto: Producto) -> None:
    with conectar() as conexion:
        conexion.execute(
            "UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE codigo = ?",
            (producto.nombre, producto.categoria, producto.precio, producto.stock, producto.codigo),
        )
        conexion.commit()


def eliminar_producto(codigo: str) -> bool:
    with conectar() as conexion:
        cursor = conexion.execute(
            "DELETE FROM productos WHERE codigo = ?",
            (codigo,),
        )
        conexion.commit()
        return cursor.rowcount > 0


def exportar_productos_csv(destino: Path | str = DATOS_DIR / "productos.csv") -> Path:
    DATOS_DIR.mkdir(exist_ok=True)
    productos = obtener_productos()

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["codigo", "nombre", "categoria", "precio", "stock"])
        for producto in productos:
            escritor.writerow([
                producto.codigo,
                producto.nombre,
                producto.categoria,
                f"{producto.precio:.2f}",
                producto.stock,
            ])

    return destino_path


def importar_productos_csv(origen: Path | str) -> tuple[int, int, int]:
    origen_path = Path(origen)
    if not origen_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {origen_path}")

    insertados = 0
    actualizados = 0
    errores = 0

    with origen_path.open("r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                producto = Producto(
                    codigo=fila.get("codigo", "").strip(),
                    nombre=fila.get("nombre", "").strip(),
                    categoria=fila.get("categoria", "").strip(),
                    precio=float(fila.get("precio", "0")),
                    stock=int(fila.get("stock", "0")),
                )
            except Exception:
                errores += 1
                continue

            existente = obtener_producto(producto.codigo)
            if existente:
                actualizar_producto(producto)
                actualizados += 1
            else:
                agregar_producto(producto)
                insertados += 1

    return insertados, actualizados, errores


def generar_reporte_inventario(destino: Path | str = REPORTES_DIR / "inventario.txt") -> Path:
    REPORTES_DIR.mkdir(exist_ok=True)
    productos = obtener_productos()

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", encoding="utf-8") as archivo:
        archivo.write("INVENTARIO DE PRODUCTOS\n")
        archivo.write("========================\n")
        archivo.write(f"Total de productos: {len(productos)}\n\n")

        for producto in productos:
            archivo.write(f"{producto.codigo} | {producto.nombre} | {producto.categoria} | ${producto.precio:.2f} | stock: {producto.stock}\n")

    return destino_path


def exportar_stock_bajo_csv(umbral: int = 5, destino: Path | str = DATOS_DIR / "stock_bajo.csv") -> Path:
    DATOS_DIR.mkdir(exist_ok=True)
    productos = obtener_productos_bajo_stock(umbral)

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["codigo", "nombre", "categoria", "precio", "stock"])
        for producto in productos:
            escritor.writerow([
                producto.codigo,
                producto.nombre,
                producto.categoria,
                f"{producto.precio:.2f}",
                producto.stock,
            ])

    return destino_path


def exportar_stock_critico_csv(umbral: int = 2, destino: Path | str = DATOS_DIR / "stock_critico.csv") -> Path:
    DATOS_DIR.mkdir(exist_ok=True)
    productos = obtener_productos_bajo_stock(umbral)

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["codigo", "nombre", "categoria", "precio", "stock"])
        for producto in productos:
            escritor.writerow([
                producto.codigo,
                producto.nombre,
                producto.categoria,
                f"{producto.precio:.2f}",
                producto.stock,
            ])

    return destino_path


def generar_reporte_stock_bajo(umbral: int = 5, destino: Path | str = REPORTES_DIR / "stock_bajo.txt") -> Path:
    REPORTES_DIR.mkdir(exist_ok=True)
    productos = obtener_productos_bajo_stock(umbral)

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE STOCK BAJO\n")
        archivo.write("====================\n")
        archivo.write(f"Umbral de alerta: {umbral}\n")
        archivo.write(f"Productos en riesgo: {len(productos)}\n\n")

        if productos:
            for producto in productos:
                archivo.write(f"{producto.codigo} | {producto.nombre} | {producto.categoria} | ${producto.precio:.2f} | stock: {producto.stock}\n")
        else:
            archivo.write("No hay productos con stock bajo en este momento.\n")

    return destino_path


def generar_reporte_stock_critico(umbral: int = 2, destino: Path | str = REPORTES_DIR / "stock_critico.txt") -> Path:
    REPORTES_DIR.mkdir(exist_ok=True)
    productos = obtener_productos_bajo_stock(umbral)

    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    with destino_path.open("w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE STOCK CRÍTICO\n")
        archivo.write("========================\n")
        archivo.write(f"Umbral crítico: {umbral}\n")
        archivo.write(f"Productos en riesgo crítico: {len(productos)}\n\n")

        if productos:
            for producto in productos:
                archivo.write(f"{producto.codigo} | {producto.nombre} | {producto.categoria} | ${producto.precio:.2f} | stock: {producto.stock}\n")
        else:
            archivo.write("No hay productos en stock crítico en este momento.\n")

    return destino_path
