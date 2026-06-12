from datetime import datetime

from servicios.gestion_inventario import GestionInventario


def generar_datos_demo():
    inventario = GestionInventario()
    if inventario.listar_productos():
        print("Ya hay datos cargados.")
        return

    productos = [
        ("Laptop", 800, 1200, 500, "Electronica"),
        ("Mouse", 15, 35, 2000, "Electronica"),
        ("Teclado", 45, 89, 800, "Electronica"),
    ]
    ventas = {
        "Laptop": [8, 10, 12, 9, 11, 14, 13, 15, 16, 18, 17, 20],
        "Mouse": [40, 45, 50, 48, 52, 55, 58, 60, 62, 65, 68, 70],
        "Teclado": [10, 12, 14, 13, 15, 16, 18, 19, 20, 22, 24, 25],
    }

    ids = {}
    for nombre, compra, venta, stock, cat in productos:
        p = inventario.registrar_producto(nombre, compra, venta, stock, cat)
        ids[nombre] = p.id

    for mes in range(1, 13):
        fecha = datetime(2024, mes, 15).strftime("%Y-%m-%d")
        for nombre, cantidades in ventas.items():
            inventario.registrar_venta(ids[nombre], cantidades[mes - 1], fecha)

    print("Datos de demo generados.")


if __name__ == "__main__":
    generar_datos_demo()
