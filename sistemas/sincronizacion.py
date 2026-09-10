import discord
from utils.logger import Logger
from config.config import cargar_config
from database.database import BaseDatos

cfg = cargar_config()
divisiones = cfg["divisiones"]

def obtener_rangos_esperados():
    esperados = {}
    for div_nombre, data in divisiones.items():
        for nombre, color in data["rangos"].items():
            esperados[nombre] = color
    return esperados

async def sincronizar_rangos(guild):
    Logger.info("🔄 Revisando rangos...")
    
    esperados = obtener_rangos_esperados()
    existentes = {rol.name: rol for rol in guild.roles}
    
    creados = 0
    eliminados = 0

    # Crear solo lo que FALTA
    for nombre, color in esperados.items():
        if nombre not in existentes:
            try:
                await guild.create_role(name=nombre, color=int(color.lstrip('#'), 16))
                BaseDatos.registrar_rango_creado(nombre)
                Logger.exito(f"✅ Creado: {nombre}")
                creados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo crear {nombre}: {e}")
        else:
            Logger.info(f"⏭️ Ya existe: {nombre} — no se toca")

    # Eliminar solo lo que EL BOT CREÓ y ya no está en config
    for nombre, rol in existentes.items():
        if BaseDatos.es_rango_del_bot(nombre) and nombre not in esperados:
            try:
                if rol < guild.me.top_role:
                    await rol.delete()
                    Logger.exito(f"🗑️ Eliminado: {nombre}")
                    eliminados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo eliminar {nombre}: {e}")

    Logger.info("════════════════════════════")
    Logger.info(f"📊 Resumen: Creados={creados}, Eliminados={eliminados}")
    Logger.info("✅ Revisión terminada\n")
