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
    
    # Para saber qué rangos creó el bot
    @staticmethod
    def registrar_rango_creado(nombre):
        datos = BaseDatos.leer("bot_rangos.json", {"creados_por_bot": []})
        if nombre not in datos["creados_por_bot"]:
            datos["creados_por_bot"].append(nombre)
            BaseDatos.guardar("bot_rangos.json", datos)
    
    @staticmethod
    def es_rango_del_bot(nombre):
        datos = BaseDatos.leer("bot_rangos.json", {"creados_por_bot": []})
        return nombre in datos["creados_por_bot"]
