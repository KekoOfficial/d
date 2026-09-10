import discord
from utils.logger import Logger
from config.config import cargar_config
from database.database import BaseDatos

cfg = cargar_config()

def registrar_rango_creado(nombre):
    datos = BaseDatos.leer("bot_rangos.json", {"creados_por_bot": []})
    if nombre not in datos["creados_por_bot"]:
        datos["creados_por_bot"].append(nombre)
        BaseDatos.guardar("bot_rangos.json", datos)

def es_rango_del_bot(nombre):
    datos = BaseDatos.leer("bot_rangos.json", {"creados_por_bot": []})
    return nombre in datos["creados_por_bot"]

async def sincronizar_rangos(guild):
    Logger.info("🔍 Sincronizando rangos...")
    
    jerarquia = cfg["rangos"]["jerarquia"]
    colores = cfg["rangos"]["colores"]
    existentes = {rol.name: rol for rol in guild.roles}
    
    creados = 0
    actualizados = 0
    eliminados = 0

    # Crear o actualizar rangos según jerarquía
    for nombre in reversed(jerarquia):  # Invertido para orden correcto
        color_hex = colores.get(nombre, "#808080")
        
        if nombre not in existentes:
            try:
                await guild.create_role(name=nombre, color=int(color_hex.lstrip('#'), 16))
                registrar_rango_creado(nombre)
                Logger.exito(f"✅ Creado: {nombre}")
                creados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo crear {nombre}: {e}")
        else:
            rol = existentes[nombre]
            if str(rol.color) != color_hex:
                try:
                    await rol.edit(color=int(color_hex.lstrip('#'), 16))
                    Logger.info(f"🔄 Color actualizado: {nombre}")
                    actualizados += 1
                except:
                    pass

    # Eliminar rangos del bot que ya no están en config
    for nombre, rol in existentes.items():
        if es_rango_del_bot(nombre) and nombre not in jerarquia:
            try:
                if rol < guild.me.top_role:
                    await rol.delete()
                    Logger.exito(f"🗑️ Eliminado: {nombre}")
                    eliminados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo eliminar {nombre}: {e}")

    Logger.info("════════════════════════════")
    Logger.info(f"📊 Rangos → Creados: {creados}, Actualizados: {actualizados}, Eliminados: {eliminados}")
    return creados, actualizados, eliminados
