from datetime import datetime

from modelos.producto import Producto
from modelos.venta import Venta


class GestionInventario:
    def __init__(self):
        self.productos = {}
        self.ventas = []

    def registrar_producto(self, nombre, precio_compra, precio_venta, stock, categoria="General"):
        nuevo_id = max(self.productos.keys(), default=0) + 1
        producto = Producto(nuevo_id, nombre, precio_compra, precio_venta, stock, categoria)
        self.productos[nuevo_id] = producto
        return producto

    def obtener_producto(self, producto_id):
        return self.productos.get(producto_id)

    def listar_productos(self):
        return sorted(self.productos.values(), key=lambda p: p.id)

    def registrar_venta(self, producto_id, cantidad, fecha=None):
        producto = self.obtener_producto(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        if cantidad <= 0 or cantidad > producto.stock_actual:
            raise ValueError("Cantidad invalida o stock insuficiente")

        fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        venta = Venta(
            max([v.id for v in self.ventas], default=0) + 1,
            producto_id,
            cantidad,
            fecha,
            producto.precio_venta,
        )
        producto.stock_actual -= cantidad
        self.ventas.append(venta)
        return venta

    def listar_ventas(self):
        return self.ventas
