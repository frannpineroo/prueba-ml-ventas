from servicios.analizador_datos import AnalizadorDatos
from servicios.gestion_inventario import GestionInventario
from servicios.machine_learning import MachineLearning


def mostrar_productos(inventario):
    productos = inventario.listar_productos()
    if not productos:
        print("No hay productos.")
        return
    for p in productos:
        print(f"  {p}")


def main():
    inventario = GestionInventario()
    analizador = AnalizadorDatos(inventario)
    ml = MachineLearning(inventario, analizador)

    while True:
        print("\n--- Gestion de Inventario ---")
        print("1. Registrar producto")
        print("2. Registrar venta")
        print("3. Analizar datos (Pandas)")
        print("4. Entrenar modelos ML")
        print("5. Predecir ventas")
        print("6. Stock recomendado y ganancias")
        print("7. Ver metricas de modelos")
        print("8. Salir")

        opcion = input("Opcion: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ")
            compra = float(input("Precio compra: "))
            venta = float(input("Precio venta: "))
            stock = int(input("Stock: "))
            categoria = input("Categoria: ") or "General"
            p = inventario.registrar_producto(nombre, compra, venta, stock, categoria)
            print(f"Producto registrado con ID {p.id}")

        elif opcion == "2":
            mostrar_productos(inventario)
            try:
                pid = int(input("ID producto: "))
                cantidad = int(input("Cantidad: "))
                venta = inventario.registrar_venta(pid, cantidad)
                print(f"Venta registrada. Total: ${venta.total:.2f}")
            except ValueError as e:
                print(e)

        elif opcion == "3":
            analizador.mostrar_analisis()

        elif opcion == "4":
            mostrar_productos(inventario)
            pid = input("ID producto (Enter = todos): ").strip()
            ml.entrenar(int(pid) if pid else None)

        elif opcion == "5":
            mostrar_productos(inventario)
            try:
                pid = int(input("ID producto: "))
                meses = int(input("Meses a predecir: "))
                ml.predecir(pid, meses)
            except ValueError:
                print("Datos invalidos.")

        elif opcion == "6":
            mostrar_productos(inventario)
            try:
                pid = int(input("ID producto: "))
                meses = int(input("Meses: "))
                ml.stock_y_ganancias(pid, meses)
            except ValueError:
                print("Datos invalidos.")

        elif opcion == "7":
            ml.mostrar_metricas()

        elif opcion == "8":
            break

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
