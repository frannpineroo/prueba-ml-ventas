from dataclasses import dataclass, asdict


@dataclass
class Producto:
    id: int
    nombre: str
    precio_compra: float
    precio_venta: float
    stock_actual: int
    categoria: str = "General"

    @property
    def margen(self) -> float:
        return self.precio_venta - self.precio_compra

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            nombre=data["nombre"],
            precio_compra=float(data["precio_compra"]),
            precio_venta=float(data["precio_venta"]),
            stock_actual=int(data["stock_actual"]),
            categoria=data.get("categoria", "General"),
        )
