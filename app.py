from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pathlib import Path
import base_datos
from productos import Producto

app = Flask(__name__)
app.secret_key = "stockmaster-secret-key"


def obtener_productos_dict(productos):
    return [
        {
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio": producto.precio,
            "stock": producto.stock,
        }
        for producto in productos
    ]


def obtener_archivos_disponibles():
    """Obtiene lista de archivos de reportes disponibles"""
    reportes_dir = Path(__file__).parent / "reportes"
    datos_dir = Path(__file__).parent / "datos"
    
    archivos = []
    
    if reportes_dir.exists():
        for archivo in reportes_dir.glob("*.txt"):
            archivos.append({
                "nombre": archivo.name,
                "tipo": "txt",
                "ruta": f"reportes/{archivo.name}",
                "tamaño": f"{archivo.stat().st_size} bytes"
            })
    
    if datos_dir.exists():
        for archivo in datos_dir.glob("*.csv"):
            archivos.append({
                "nombre": archivo.name,
                "tipo": "csv",
                "ruta": f"datos/{archivo.name}",
                "tamaño": f"{archivo.stat().st_size} bytes"
            })
    
    return sorted(archivos, key=lambda x: x["nombre"], reverse=True)


@app.route("/")
def inicio():
    search = request.args.get("search", "").strip() or None
    categoria = request.args.get("categoria", "").strip() or None
    stock_bajo = request.args.get("stock_bajo") == "1"
    sort_by = request.args.get("sort_by", "nombre")
    sort_dir = request.args.get("sort_dir", "asc")

    stock_umbral = 5 if stock_bajo else None
    productos = base_datos.obtener_productos_filtrados(
        search=search,
        categoria=categoria,
        stock_bajo=stock_umbral,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    categorias = base_datos.obtener_categorias()

    return render_template(
        "index.html",
        productos=obtener_productos_dict(productos),
        categorias=categorias,
        search=search,
        categoria=categoria,
        stock_bajo=stock_bajo,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


@app.route("/producto/nuevo", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()

        try:
            producto = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock),
            )
            base_datos.agregar_producto(producto)
            flash("Producto agregado correctamente.", "success")
            return redirect(url_for("inicio"))
        except Exception as error:
            flash(f"Error al agregar producto: {error}", "danger")

    return render_template("producto_form.html", accion="Crear", producto=None)


@app.route("/producto/<codigo>/editar", methods=["GET", "POST"])
def editar_producto(codigo):
    producto = base_datos.obtener_producto(codigo)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()

        try:
            producto_actualizado = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock),
            )
            base_datos.actualizar_producto(producto_actualizado)
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("inicio"))
        except Exception as error:
            flash(f"Error al actualizar producto: {error}", "danger")

    return render_template("producto_form.html", accion="Editar", producto=producto)


@app.route("/producto/<codigo>/eliminar", methods=["POST"])
def eliminar_producto(codigo):
    if base_datos.eliminar_producto(codigo):
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("No se pudo eliminar el producto.", "danger")
    return redirect(url_for("inicio"))


@app.route("/reportes")
def reportes():
    productos = base_datos.obtener_productos()
    archivos = obtener_archivos_disponibles()
    return render_template("reportes.html", productos=obtener_productos_dict(productos), archivos=archivos)


@app.route("/reportes/generar", methods=["POST"])
def generar_reporte():
    tipo = request.form.get("tipo")
    umbral = int(request.form.get("umbral") or 5)

    try:
        if tipo == "inventario":
            base_datos.generar_reporte_inventario()
            base_datos.exportar_inventario_csv()
            flash("Reporte de inventario generado. Descarga el archivo CSV inventario.csv para una planilla completa.", "success")
        elif tipo == "stock_bajo":
            base_datos.generar_reporte_stock_bajo(umbral)
            base_datos.exportar_stock_bajo_csv(umbral)
            flash("Reporte de stock bajo generado.", "success")
        elif tipo == "stock_critico":
            base_datos.generar_reporte_stock_critico(umbral)
            base_datos.exportar_stock_critico_csv(umbral)
            flash("Reporte de stock crítico generado.", "success")
        else:
            flash("Tipo de reporte inválido.", "danger")
    except Exception as error:
        flash(f"Error al generar reporte: {error}", "danger")

    return redirect(url_for("reportes"))


@app.route("/descargar/<path:ruta>")
def descargar_archivo(ruta):
    """Descarga un archivo de reportes o datos"""
    base_dir = Path(__file__).parent
    archivo_path = base_dir / ruta
    
    # Validar que el archivo existe y está dentro del directorio permitido
    if not archivo_path.exists() or not archivo_path.is_file():
        flash("Archivo no encontrado.", "danger")
        return redirect(url_for("reportes"))
    
    # Verificar que el archivo está en los directorios permitidos
    if not (ruta.startswith("reportes/") or ruta.startswith("datos/")):
        flash("Acceso denegado.", "danger")
        return redirect(url_for("reportes"))
    
    return send_file(
        archivo_path,
        as_attachment=True,
        download_name=archivo_path.name
    )


if __name__ == "__main__":
    base_datos.inicializar()
    app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=None)
