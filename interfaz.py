from productos import Producto
import base_datos


def leer_producto() -> Producto:
    print("\n=== Agregar Producto ===")
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()

    while True:
        try:
            precio = float(input("Precio: ").strip())
            break
        except ValueError:
            print("❌ Precio inválido. Ingresa un número válido.")

    while True:
        try:
            stock = int(input("Stock: ").strip())
            break
        except ValueError:
            print("❌ Stock inválido. Ingresa un número entero.")

    return Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock)


def mostrar_producto(producto: Producto) -> None:
    print("\n----- PRODUCTO -----")
    print(f"Código: {producto.codigo}")
    print(f"Nombre: {producto.nombre}")
    print(f"Categoría: {producto.categoria}")
    print(f"Precio: ${producto.precio:.2f}")
    print(f"Stock: {producto.stock}")
    print("---------------------")


def mostrar_productos(productos: list[Producto]) -> None:
    if not productos:
        print("\n📦 No hay productos registrados.")
        return

    print("\n===== LISTA DE PRODUCTOS =====")
    for producto in productos:
        mostrar_producto(producto)


def leer_actualizacion(producto: Producto) -> Producto:
    print("\n=== Actualizar producto ===")
    print(f"Código: {producto.codigo} (no se puede cambiar)")

    nombre = input(f"Nombre [{producto.nombre}]: ").strip() or producto.nombre
    categoria = input(f"Categoría [{producto.categoria}]: ").strip() or producto.categoria

    precio = producto.precio
    while True:
        valor = input(f"Precio [{producto.precio}]: ").strip()
        if not valor:
            break
        try:
            precio = float(valor)
            break
        except ValueError:
            print("❌ Precio inválido. Ingresa un número válido.")

    stock = producto.stock
    while True:
        valor = input(f"Stock [{producto.stock}]: ").strip()
        if not valor:
            break
        try:
            stock = int(valor)
            break
        except ValueError:
            print("❌ Stock inválido. Ingresa un número entero.")

    return Producto(
        codigo=producto.codigo,
        nombre=nombre,
        categoria=categoria,
        precio=precio,
        stock=stock,
    )


def solicitar_codigo() -> str:
    return input("Código del producto: ").strip()


def solicitar_categoria() -> str:
    return input("Categoría a buscar: ").strip()


def solicitar_nombre_busqueda() -> str:
    return input("Nombre o parte del nombre a buscar: ").strip()


def solicitar_umbral_stock(mensaje: str = "Umbral de stock (número entero, por defecto 5): ", default: int = 5) -> int:
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return default
        try:
            return int(valor)
        except ValueError:
            print("❌ Ingresa un número entero válido.")


def solicitar_tipo_salida() -> str:
    while True:
        opcion = input("Selecciona formato de salida (1=TXT, 2=CSV, 3=Ambos): ").strip()
        if opcion in {"1", "2", "3"}:
            return opcion
        print("❌ Opción inválida. Elige 1, 2 o 3.")


def leer_ruta_csv() -> str:
    return input("Ruta del archivo CSV a importar: ").strip()


def confirmar_accion(mensaje: str) -> bool:
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == "s"


def ejecutar_menu_reportes() -> None:
    while True:
        print("""
------------------------------
       MENÚ DE REPORTES
------------------------------
1. Reporte de inventario completo
2. Reporte de stock bajo
3. Reporte de stock crítico
4. Volver al menú principal
""")

        opcion = input("Seleccione una opción de reporte: ").strip()

        if opcion == "1":
            tipo = solicitar_tipo_salida()
            try:
                if tipo in {"1", "3"}:
                    ruta_txt = base_datos.generar_reporte_inventario()
                    print(f"\n✅ Reporte de inventario generado: {ruta_txt}")
                if tipo in {"2", "3"}:
                    ruta_csv = base_datos.exportar_productos_csv()
                    print(f"\n✅ Inventario completo exportado a CSV: {ruta_csv}")
            except Exception as error:
                print(f"\n❌ Error al generar reporte de inventario completo: {error}")

        elif opcion == "2":
            umbral = solicitar_umbral_stock("Umbral de stock bajo (por defecto 5): ", 5)
            tipo = solicitar_tipo_salida()
            try:
                if tipo in {"1", "3"}:
                    ruta_txt = base_datos.generar_reporte_stock_bajo(umbral)
                    print(f"\n✅ Reporte de stock bajo generado: {ruta_txt}")
                if tipo in {"2", "3"}:
                    ruta_csv = base_datos.exportar_stock_bajo_csv(umbral)
                    print(f"\n✅ CSV de stock bajo generado: {ruta_csv}")

                productos_bajos = base_datos.obtener_productos_bajo_stock(umbral)
                if productos_bajos:
                    print("\n=== Productos con stock bajo ===")
                    mostrar_productos(productos_bajos)
                else:
                    print("\n✅ No hay productos con stock bajo en este momento.")
            except Exception as error:
                print(f"\n❌ Error al generar reporte de stock bajo: {error}")

        elif opcion == "3":
            umbral = solicitar_umbral_stock("Umbral de stock crítico (por defecto 2): ", 2)
            tipo = solicitar_tipo_salida()
            try:
                if tipo in {"1", "3"}:
                    ruta_txt = base_datos.generar_reporte_stock_critico(umbral)
                    print(f"\n✅ Reporte de stock crítico generado: {ruta_txt}")
                if tipo in {"2", "3"}:
                    ruta_csv = base_datos.exportar_stock_critico_csv(umbral)
                    print(f"\n✅ CSV de stock crítico generado: {ruta_csv}")

                productos_criticos = base_datos.obtener_productos_bajo_stock(umbral)
                if productos_criticos:
                    print("\n=== Productos con stock crítico ===")
                    mostrar_productos(productos_criticos)
                else:
                    print("\n✅ No hay productos con stock crítico en este momento.")
            except Exception as error:
                print(f"\n❌ Error al generar reporte de stock crítico: {error}")

        elif opcion == "4":
            break

        else:
            print("❌ Opción inválida.")


def ejecutar_menu() -> None:
    base_datos.inicializar()

    while True:
        print("""
==============================
 SISTEMA DE GESTIÓN DE STOCK
==============================
1. Agregar producto
2. Ver productos
3. Buscar por nombre
4. Buscar por categoría
5. Ver stock bajo
6. Actualizar producto
7. Eliminar producto
8. Exportar inventario
9. Reportes
10. Importar desde CSV
11. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                producto = leer_producto()
                base_datos.agregar_producto(producto)
                print("\n✅ Producto agregado correctamente.")
            except Exception as error:
                print(f"\n❌ No se pudo agregar el producto: {error}")

        elif opcion == "2":
            productos = base_datos.obtener_productos()
            mostrar_productos(productos)

        elif opcion == "3":
            nombre = solicitar_nombre_busqueda()
            if not nombre:
                print("❌ Debes ingresar un texto para buscar.")
                continue

            productos = base_datos.buscar_productos_por_nombre(nombre)
            if not productos:
                print(f"\n🔎 No se encontraron productos con '{nombre}'.")
            else:
                mostrar_productos(productos)

        elif opcion == "4":
            categoria = solicitar_categoria()
            if not categoria:
                print("❌ Debes ingresar una categoría.")
                continue

            productos = base_datos.buscar_productos_por_categoria(categoria)
            if not productos:
                print(f"\n🔎 No se encontraron productos en la categoría '{categoria}'.")
            else:
                mostrar_productos(productos)

        elif opcion == "5":
            umbral = solicitar_umbral_stock()
            productos = base_datos.obtener_productos_bajo_stock(umbral)
            if not productos:
                print(f"\n✅ No hay productos con stock menor o igual a {umbral}.")
            else:
                print(f"\n🔻 Productos con stock menor o igual a {umbral}:")
                mostrar_productos(productos)

        elif opcion == "6":
            codigo = solicitar_codigo()
            if not codigo:
                print("❌ Debes ingresar un código.")
                continue

            producto = base_datos.obtener_producto(codigo)
            if not producto:
                print(f"\n❌ No existe un producto con código '{codigo}'.")
                continue

            try:
                producto_actualizado = leer_actualizacion(producto)
                base_datos.actualizar_producto(producto_actualizado)
                print("\n✅ Producto actualizado correctamente.")
            except Exception as error:
                print(f"\n❌ No se pudo actualizar el producto: {error}")

        elif opcion == "7":
            codigo = solicitar_codigo()
            if not codigo:
                print("❌ Debes ingresar un código.")
                continue

            producto = base_datos.obtener_producto(codigo)
            if not producto:
                print(f"\n❌ No existe un producto con código '{codigo}'.")
                continue

            mostrar_producto(producto)
            if confirmar_accion("¿Deseas eliminar este producto?"):
                eliminado = base_datos.eliminar_producto(codigo)
                if eliminado:
                    print("\n✅ Producto eliminado correctamente.")
                else:
                    print("\n❌ No se pudo eliminar el producto.")

        elif opcion == "8":
            try:
                ruta_csv = base_datos.exportar_productos_csv()
                ruta_txt = base_datos.generar_reporte_inventario()
                print(f"\n✅ Inventario exportado a CSV: {ruta_csv}")
                print(f"✅ Reporte generado: {ruta_txt}")
            except Exception as error:
                print(f"\n❌ Error al exportar inventario: {error}")

        elif opcion == "9":
            ejecutar_menu_reportes()

        elif opcion == "10":
            origen = leer_ruta_csv()
            if not origen:
                print("❌ Debes ingresar una ruta de archivo CSV.")
                continue
            try:
                insertados, actualizados, errores = base_datos.importar_productos_csv(origen)
                print(f"\n✅ Importación finalizada: insertados={insertados}, actualizados={actualizados}, errores={errores}.")
            except Exception as error:
                print(f"\n❌ No se pudo importar el CSV: {error}")

        elif opcion == "11":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida.")
