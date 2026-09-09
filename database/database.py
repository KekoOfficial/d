import json
import os

class BaseDatos:
    @staticmethod
    def leer(archivo, por_defecto=None):
        ruta = f"data/{archivo}"
        if not os.path.exists(ruta):
            return por_defecto or {}
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def guardar(archivo, datos):
        ruta = f"data/{archivo}"
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
