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

# 🛡️ Convertir permisos del JSON a formato de Discord
def obtener_objeto_permisos(permiso_config):
    permisos = discord.Permissions()
    
    permisos_dict = {
        "administrar_servidor": "manage_guild",
        "administrar_canales": "manage_channels",
        "administrar_roles": "manage_roles",
        "moderar_miembros": "kick_members",
        "gestionar_mensajes": "manage_messages",
        "ver_canales": "view_channel",
        "enviar_mensajes": "send_messages",
        "ver_registro_auditoria": "view_audit_log",
        "ban_miembros": "ban_members",
        "expulsar_miembros": "kick_members",
        "mencionar_todos": "mention_everyone",
        "gestionar_emojis": "manage_emojis"
    }
    
    for clave, valor in permiso_config.items():
        if clave in permisos_dict and valor:
            setattr(permisos, permisos_dict[clave], True)
    
    # ✅ Por defecto TODOS tienen permiso de ver canales si no se especifica lo contrario
    if "ver_canales" not in permiso_config:
        permisos.view_channel = True
    
    return permisos

async def sincronizar_rangos(guild):
    Logger.info("🔍 Sincronizando rangos...")
    
    jerarquia = cfg["rangos"]["jerarquia"]
    colores = cfg["rangos"]["colores"]
    permisos_rangos = cfg["rangos"].get("permisos_por_rango", {})
    existentes = {rol.name: rol for rol in guild.roles}
    
    creados = 0
    actualizados = 0
    eliminados = 0

    # ── Crear o actualizar cada rango con sus permisos ──
    for nombre in jerarquia:
        color_hex = colores.get(nombre, "#808080")
        permisos_obj = obtener_objeto_permisos(permisos_rangos.get(nombre, {}))
        
        if nombre not in existentes:
            try:
                await guild.create_role(
                    name=nombre,
                    color=int(color_hex.lstrip('#'), 16),
                    permissions=permisos_obj
                )
                registrar_rango_creado(nombre)
                Logger.exito(f"✅ CREADO: {nombre} + permisos asignados")
                creados += 1
            except Exception as e:
                Logger.error(f"❌ No se pudo crear {nombre}: {e}")
        else:
            # Ya existe → actualizar color Y permisos
            rol = existentes[nombre]
            cambios = {}
            
            if str(rol.color) != color_hex:
                cambios["color"] = int(color_hex.lstrip('#'), 16)
            
            if rol.permissions != permisos_obj:
                cambios["permissions"] = permisos_obj
            
            if cambios:
                try:
                    await rol.edit(**cambios)
                    Logger.info(f"🔄 Actualizado: {nombre}")
                    actualizados += 1
                except Exception as e:
                    Logger.error(f"⚠️ No se pudo actualizar {nombre}: {e}")
    
    # ── Ordenar jerarquía ──
    Logger.info("🔄 Organizando jerarquía...")
    posiciones = {}
    for indice, nombre in enumerate(jerarquia):
        if nombre in existentes:
            posiciones[existentes[nombre]] = len(jerarquia) - indice
    
    try:
        await guild.edit_role_positions(positions=posiciones)
        Logger.exito(f"✅ Rangos ordenados")
    except Exception as e:
        Logger.warning(f"⚠️ No se pudo ordenar: {e}")

    # ── Eliminar solo lo que ya NO está en config ──
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
    Logger.info(f"📊 Creados: {creados} | Actualizados: {actualizados} | Eliminados: {eliminados}")
    return creados, actualizados, eliminados
