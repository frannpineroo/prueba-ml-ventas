import csv
from datetime import datetime
from pathlib import Path

from modelos.producto import Producto
from modelos.venta import Venta


class GestionInventario:
    def __init__(self, directorio="data"):
        self.directorio = Path(directorio)
        self.directorio.mkdir(exist_ok=True)
        self.archivo_productos = self.directorio / "productos.csv"
        self.archivo_ventas = self.directorio / "ventas.csv"
        self.productos = {}
        self.ventas = []
        self._cargar()

    def _cargar(self):
        if self.archivo_productos.exists():
            with open(self.archivo_productos, newline="", encoding="utf-8") as f:
                for fila in csv.DictReader(f):
                    p = Producto.from_dict(fila)
                    self.productos[p.id] = p
        if self.archivo_ventas.exists():
            with open(self.archivo_ventas, newline="", encoding="utf-8") as f:
                for fila in csv.DictReader(f):
                    self.ventas.append(Venta.from_dict(fila))

    def _guardar_productos(self):
        campos = ["id", "nombre", "precio_compra", "precio_venta", "stock_actual", "categoria"]
        with open(self.archivo_productos, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for p in self.productos.values():
                writer.writerow(p.to_dict())

    def _guardar_ventas(self):
        campos = ["id", "producto_id", "cantidad", "fecha", "precio_unitario"]
        with open(self.archivo_ventas, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for v in self.ventas:
                writer.writerow(v.to_dict())

    def registrar_producto(self, nombre, precio_compra, precio_venta, stock, categoria="General"):
        nuevo_id = max(self.productos.keys(), default=0) + 1
        producto = Producto(nuevo_id, nombre, precio_compra, precio_venta, stock, categoria)
        self.productos[nuevo_id] = producto
        self._guardar_productos()
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
        self._guardar_productos()
        self._guardar_ventas()
        return venta

    def listar_ventas(self):
        return self.ventas
