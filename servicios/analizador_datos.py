import pandas as pd

from servicios.gestion_inventario import GestionInventario


class AnalizadorDatos:
    def __init__(self, inventario: GestionInventario):
        self.inventario = inventario

    def _dataframe(self):
        filas = []
        for venta in self.inventario.listar_ventas():
            producto = self.inventario.obtener_producto(venta.producto_id)
            if not producto:
                continue
            filas.append({
                "producto_id": venta.producto_id,
                "producto": producto.nombre,
                "categoria": producto.categoria,
                "fecha": pd.to_datetime(venta.fecha),
                "cantidad": venta.cantidad,
                "total": venta.total,
                "ganancia": venta.cantidad * producto.margen,
            })
        if not filas:
            return pd.DataFrame()
        df = pd.DataFrame(filas)
        df["mes"] = df["fecha"].dt.to_period("M").astype(str)
        return df

    def serie_mensual(self):
        df = self._dataframe()
        if df.empty:
            return df
        serie = df.groupby(["producto_id", "producto", "mes"], as_index=False)["cantidad"].sum()
        serie["indice_mes"] = serie.groupby("producto_id").cumcount() + 1
        return serie

    def mostrar_analisis(self):
        df = self._dataframe()
        if df.empty:
            print("No hay ventas para analizar.")
            return

        print("\n--- Resumen ---")
        print(f"Unidades vendidas: {df['cantidad'].sum()}")
        print(f"Ingresos: ${df['total'].sum():.2f}")
        print(f"Ganancias: ${df['ganancia'].sum():.2f}")

        print("\n--- Por producto ---")
        por_producto = df.groupby("producto").agg(
            unidades=("cantidad", "sum"),
            ingresos=("total", "sum"),
            ganancias=("ganancia", "sum"),
        )
        print(por_producto)

        print("\n--- Por mes ---")
        por_mes = df.groupby("mes").agg(
            unidades=("cantidad", "sum"),
            ingresos=("total", "sum"),
        )
        print(por_mes)
