import discord
from utils.logger import Logger
from config.config import cargar_config
from database.database import BaseDatos

cfg = cargar_config()
estructura = cfg["canales"]["estructura"]

def registrar_canal_creado(nombre):
    datos = BaseDatos.leer("bot_canales.json", {"creados_por_bot": []})
    if nombre not in datos["creados_por_bot"]:
        datos["creados_por_bot"].append(nombre)
        BaseDatos.guardar("bot_canales.json", datos)

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
    existentes = {c.name: c for c in guild.channels}
    everyone = guild.default_role

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
            registrar_canal_creado(cat_nombre)
            Logger.exito(f"📂 CREADA CATEGORÍA: {cat_nombre}")
            Logger.info(f"   ↳ Permisos aplicados ✅")
            creados += 1
        else:
            try:
                await categoria.edit(overwrites=permisos_categoria)
                Logger.info(f"📂 {cat_nombre} — permisos actualizados ✅")
            except Exception as e:
                Logger.info(f"⚠️ No se pudieron actualizar permisos de {cat_nombre}: {e}")

        if "canales" in cat_data:
            for canal_info in cat_data["canales"]:
                nombre_canal = canal_info["nombre"]
                tipo = canal_info["tipo"]
                
                if nombre_canal not in existentes:
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
                    registrar_canal_creado(nombre_canal)
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
                    
                    if nombre_canal not in existentes:
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
                        registrar_canal_creado(nombre_canal)
                        Logger.exito(f"  ✅ {nombre_canal} [Solo: {nombre_rango}]")
                        creados += 1

    Logger.info("════════════════════════════")
    Logger.info(f"📊 Total canales/categorías creados: {creados}")
    Logger.info("✅ Permisos aplicados a todo ✅\n")
    return creados
