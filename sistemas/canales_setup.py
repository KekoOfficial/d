import discord
from utils.logger import Logger
from config.config import cargar_config

cfg = cargar_config()
estructura = cfg["canales"]["estructura"]

def obtener_todos_nombres_esperados():
    """Obtiene todos los nombres de categorías y canales que DEBEN existir"""
    esperados = set()
    
    for cat_data in estructura:
        cat_nombre = cat_data["categoria"]
        esperados.add(cat_nombre)
        
        if "canales" in cat_data:
            for canal in cat_data["canales"]:
                esperados.add(canal["nombre"])
        
        if "canales_por_juego" in cat_data:
            for juego in cat_data["canales_por_juego"]:
                for canal in juego["canales"]:
                    esperados.add(canal["nombre"])
    
    return esperados

def obtener_permisos_desde_acceso(guild, acceso):
    everyone = guild.default_role
    permisos = {}

    ver_todos = acceso.get("todos_pueden_ver", True)
    escribir_todos = acceso.get("todos_pueden_escribir", True)
    solo_rango = acceso.get("solo_rango_especifico")

    permisos[everyone] = discord.PermissionOverwrite(
        view_channel=ver_todos,
        send_messages=escribir_todos,
        read_message_history=ver_todos
    )

    if solo_rango:
        rol = discord.utils.get(guild.roles, name=solo_rango)
        if rol:
            permisos[rol] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

    return permisos

async def sincronizar_canales(guild):
    Logger.info("🔍 Sincronizando categorías y canales...")
    
    creados = 0
    eliminados = 0
    esperados = obtener_todos_nombres_esperados()
    
    # Obtener canales y categorías existentes
    todos_canales = list(guild.channels)
    everyone = guild.default_role

    # ── PASO 1: Eliminar TODO lo que NO está en config ──
    Logger.info("🔍 Eliminando canales y categorías que no están en la configuración...")
    for canal in todos_canales:
        if canal.name not in esperados:
            # No eliminar si está arriba del rol del bot
            if isinstance(canal, discord.CategoryChannel):
                # Verificar si hay canales dentro que no se puedan eliminar
                puede_eliminar = True
                for _ in canal.channels:
                    if _.position >= guild.me.top_role.position:
                        puede_eliminar = False
                        break
                if puede_eliminar and canal.position < guild.me.top_role.position:
                    try:
                        await canal.delete()
                        Logger.exito(f"🗑️ Eliminada categoría: {canal.name}")
                        eliminados += 1
                    except Exception as e:
                        Logger.info(f"⚠️ No se pudo eliminar {canal.name}: {e}")
            else:
                if canal.position < guild.me.top_role.position:
                    try:
                        await canal.delete()
                        Logger.exito(f"🗑️ Eliminado canal: {canal.name}")
                        eliminados += 1
                    except Exception as e:
                        Logger.info(f"⚠️ No se pudo eliminar {canal.name}: {e}")

    # Esperar un momento para que Discord actualice
    import asyncio
    await asyncio.sleep(0.5)

    # ── PASO 2: Crear categorías y canales desde cero según config ──
    Logger.info("🔍 Creando estructura desde configuración...")
    for cat_data in estructura:
        cat_nombre = cat_data["categoria"]
        posicion = cat_data.get("posicion", 0)
        acceso = cat_data.get("acceso", {})

        categoria = discord.utils.get(guild.categories, name=cat_nombre)
        permisos_categoria = obtener_permisos_desde_acceso(guild, acceso)
        
        if not categoria:
            categoria = await guild.create_category_channel(
                name=cat_nombre,
                overwrites=permisos_categoria,
                position=posicion
            )
            Logger.exito(f"📂 CREADA CATEGORÍA: {cat_nombre}")
            creados += 1
        else:
            try:
                await categoria.edit(overwrites=permisos_categoria)
                Logger.info(f"📂 {cat_nombre} — configurada ✅")
            except Exception as e:
                Logger.info(f"⚠️ No se pudo configurar {cat_nombre}: {e}")

        if "canales" in cat_data:
            for canal_info in cat_data["canales"]:
                nombre_canal = canal_info["nombre"]
                tipo = canal_info["tipo"]
                
                existe = discord.utils.get(guild.channels, name=nombre_canal)
                if not existe:
                    if tipo == "text":
                        await guild.create_text_channel(
                            nombre_canal,
                            category=categoria,
                            overwrites=permisos_categoria
                        )
                    else:
                        await guild.create_voice_channel(
                            nombre_canal,
                            category=categoria,
                            overwrites=permisos_categoria
                        )
                    Logger.exito(f"  ✅ {nombre_canal}")
                    creados += 1

        if "canales_por_juego" in cat_data:
            for juego in cat_data["canales_por_juego"]:
                nombre_rango = juego["nombre_rango"]
                rol = discord.utils.get(guild.roles, name=nombre_rango)
                
                permisos_juego = {everyone: discord.PermissionOverwrite(view_channel=False)}
                if rol:
                    permisos_juego[rol] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True
                    )
                    Logger.info(f"   ↳ Canal privado para: {nombre_rango}")
                else:
                    Logger.info(f"   ⚠️ Rango '{nombre_rango}' no encontrado. Crea el rango primero con kr!up")

                for canal_info in juego["canales"]:
                    nombre_canal = canal_info["nombre"]
                    tipo = canal_info["tipo"]
                    
                    existe = discord.utils.get(guild.channels, name=nombre_canal)
                    if not existe:
                        if tipo == "text":
                            await guild.create_text_channel(
                                nombre_canal,
                                category=categoria,
                                overwrites=permisos_juego
                            )
                        else:
                            await guild.create_voice_channel(
                                nombre_canal,
                                category=categoria,
                                overwrites=permisos_juego
                            )
                        Logger.exito(f"  ✅ {nombre_canal} [Solo: {nombre_rango}]")
                        creados += 1

    Logger.info("════════════════════════════")
    Logger.info(f"📊 Eliminados: {eliminados} | Creados: {creados}")
    Logger.info("✅ Servidor configurado completamente por el bot\n")
    return creados
