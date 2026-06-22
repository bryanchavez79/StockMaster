from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route("/")
def inicio():
    productos = base_datos.obtener_productos()
    return render_template("index.html", productos=obtener_productos_dict(productos))


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
    return render_template("reportes.html", productos=obtener_productos_dict(productos))


@app.route("/reportes/generar", methods=["POST"])
def generar_reporte():
    tipo = request.form.get("tipo")
    umbral = int(request.form.get("umbral") or 5)

    try:
        if tipo == "inventario":
            base_datos.generar_reporte_inventario()
            base_datos.exportar_productos_csv()
            flash("Reporte de inventario generado.", "success")
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


if __name__ == "__main__":
    base_datos.inicializar()
    app.run(debug=True)
