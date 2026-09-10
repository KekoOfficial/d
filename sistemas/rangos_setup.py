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
    
    jerarquia = cfg["rangos"]["jerarquia"]  # 🔝 El primero = más arriba
    colores = cfg["rangos"]["colores"]
    existentes = {rol.name: rol for rol in guild.roles}
    
    creados = 0
    actualizados = 0
    eliminados = 0

    # ── PASO 1: Crear y actualizar colores ──
    for nombre in jerarquia:
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

    # ── PASO 2: ORDENAR JERÁRQUICAMENTE ──
    Logger.info("🔄 Organizando jerarquía...")
    posiciones = {}
    for indice, nombre in enumerate(jerarquia):
        if nombre in existentes:
            # El primero de la lista = posición más alta
            # Usamos índice negativo para que el primero quede arriba
            posiciones[existentes[nombre]] = len(jerarquia) - indice
    
    try:
        await guild.edit_role_positions(positions=posiciones)
        Logger.exito(f"✅ Rangos ordenados correctamente")
    except Exception as e:
        Logger.error(f"⚠️ No se pudo ordenar: {e}")
        Logger.info("💡 Asegúrate de que el rol del bot esté arriba en Configuración → Roles")

    # ── PASO 3: Eliminar rangos que ya no están ──
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
    Logger.info(f"📊 Creados: {creados}, Actualizados: {actualizados}, Eliminados: {eliminados}")
    Logger.info(f"📋 Orden: 👑 Arriba = Fundador | Abajo = Miembro ✅")
    return creados, actualizados, eliminados
