import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from servicios.analizador_datos import AnalizadorDatos
from servicios.gestion_inventario import GestionInventario


class MachineLearning:
    def __init__(self, inventario: GestionInventario, analizador: AnalizadorDatos, directorio="models"):
        self.inventario = inventario
        self.analizador = analizador
        self.directorio = Path(directorio)
        self.directorio.mkdir(exist_ok=True)
        self.modelos = {}
        self.metricas = {}
        self._cargar()

    def _cargar(self):
        archivo = self.directorio / "metricas.json"
        if archivo.exists():
            with open(archivo, encoding="utf-8") as f:
                self.metricas = json.load(f)
        for archivo in self.directorio.glob("modelo*.joblib"):
            producto_id = int(archivo.stem.split("_")[-1])
            self.modelos[producto_id] = joblib.load(archivo)

    def _guardar_metricas(self):
        with open(self.directorio / "metricas.json", "w", encoding="utf-8") as f:
            json.dump(self.metricas, f, indent=2, ensure_ascii=False)

    def _datos_producto(self, producto_id):
        serie = self.analizador.serie_mensual()
        datos = serie[serie["producto_id"] == producto_id]
        if len(datos) < 3:
            return None
        return datos[["indice_mes"]].values, datos["cantidad"].values

    def entrenar(self, producto_id=None):
        productos = [self.inventario.obtener_producto(producto_id)] if producto_id else self.inventario.listar_productos()
        entrenados = 0

        for producto in productos:
            if not producto:
                continue
            datos = self._datos_producto(producto.id)
            if datos is None:
                print(f"{producto.nombre}: se necesitan al menos 3 meses de ventas.")
                continue

            X, y = datos
            modelo = LinearRegression()
            modelo.fit(X, y)
            pred = modelo.predict(X)

            self.modelos[producto.id] = modelo
            joblib.dump(modelo, self.directorio / f"modelo_{producto.id}.joblib")
            self.metricas[str(producto.id)] = {
                "producto": producto.nombre,
                "mae": round(float(mean_absolute_error(y, pred)), 2),
                "rmse": round(float(np.sqrt(mean_squared_error(y, pred))), 2),
                "r2": round(float(r2_score(y, pred)), 2),
                "ultimo_mes": int(X.max()),
            }
            entrenados += 1
            print(f"Modelo entrenado: {producto.nombre}")

        self._guardar_metricas()
        if entrenados == 0:
            print("No se entrenó ningún modelo.")

    def predecir(self, producto_id, meses=1):
        if producto_id not in self.modelos:
            print("Entrene el modelo primero (opción 4).")
            return

        producto = self.inventario.obtener_producto(producto_id)
        ultimo = self.metricas[str(producto_id)]["ultimo_mes"]
        modelo = self.modelos[producto_id]

        print(f"\nPredicciones para {producto.nombre}:")
        for i in range(1, meses + 1):
            cantidad = max(0, float(modelo.predict([[ultimo + i]])[0]))
            ingreso = cantidad * producto.precio_venta
            ganancia = cantidad * producto.margen
            print(f"  Mes {i}: {cantidad:.0f} uds | Ingresos ${ingreso:.2f} | Ganancia ${ganancia:.2f}")

    def stock_y_ganancias(self, producto_id, meses=1):
        if producto_id not in self.modelos:
            print("Entrene el modelo primero (opción 4).")
            return

        producto = self.inventario.obtener_producto(producto_id)
        ultimo = self.metricas[str(producto_id)]["ultimo_mes"]
        modelo = self.modelos[producto_id]

        demanda = sum(max(0, float(modelo.predict([[ultimo + i]])[0])) for i in range(1, meses + 1))
        stock_recomendado = int(np.ceil(demanda * 1.2))
        reponer = max(0, stock_recomendado - producto.stock_actual)
        ganancia = demanda * producto.margen

        print(f"\n{producto.nombre}")
        print(f"  Stock actual: {producto.stock_actual}")
        print(f"  Demanda prevista: {demanda:.0f}")
        print(f"  Stock recomendado: {stock_recomendado}")
        print(f"  Unidades a reponer: {reponer}")
        print(f"  Ganancia estimada: ${ganancia:.2f}")

    def mostrar_metricas(self):
        if not self.metricas:
            print("No hay modelos entrenados.")
            return
        print("\n--- Metricas de modelos ---")
        for datos in self.metricas.values():
            print(f"{datos['producto']}: MAE={datos['mae']} RMSE={datos['rmse']} R2={datos['r2']}")
