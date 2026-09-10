import discord
from utils.logger import Logger
from config.config import cargar_config
from database.database import BaseDatos

cfg = cargar_config()
divisiones = cfg["divisiones"]

# Obtiene TODOS los rangos que DEBERÍAN existir según config
def obtener_rangos_esperados():
    esperados = {}
    for div_nombre, data in divisiones.items():
        for nombre, color in data["rangos"].items():
            esperados[nombre] = color
    return esperados

# Ejecuta la sincronización completa
async def sincronizar_rangos(guild):
    Logger.info("🔄 Iniciando sincronización automática de rangos...")
    
    esperados = obtener_rangos_esperados()
    existentes = {rol.name: rol for rol in guild.roles}
    
    creados = 0
    actualizados = 0
    eliminados = 0

    # ── PASO 1: Crear o actualizar rangos que deben existir ──
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
            # Si ya existe, verifica que el color sea correcto
            rol = existentes[nombre]
            if str(rol.color) != color:
                try:
                    await rol.edit(color=int(color.lstrip('#'), 16))
                    Logger.info(f"🔄 Color actualizado: {nombre}")
                    actualizados += 1
                except:
                    pass

    # ── PASO 2: Eliminar rangos del bot que ya no están en config ──
    for nombre, rol in existentes.items():
        if BaseDatos.es_rango_del_bot(nombre) and nombre not in esperados:
            try:
                if rol < guild.me.top_role:
                    await rol.delete()
                    Logger.exito(f"🗑️ Eliminado: {nombre} (ya no está en config)")
                    eliminados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo eliminar {nombre}: {e}")

    # ── Resumen ──
    Logger.info("══════════════════════════════════")
    Logger.info(f"📊 SINCRONIZACIÓN COMPLETA")
    Logger.info(f"   ✅ Creados: {creados}")
    Logger.info(f"   🔄 Actualizados: {actualizados}")
    Logger.info(f"   🗑️ Eliminados: {eliminados}")
    Logger.info("══════════════════════════════════")
