from dataclasses import dataclass, asdict


@dataclass
class Venta:
    id: int
    producto_id: int
    cantidad: int
    fecha: str
    precio_unitario: float

    @property
    def total(self) -> float:
        return self.cantidad * self.precio_unitario

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            producto_id=int(data["producto_id"]),
            cantidad=int(data["cantidad"]),
            fecha=data["fecha"],
            precio_unitario=float(data["precio_unitario"]),
        )
