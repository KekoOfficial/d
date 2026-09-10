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

def es_canal_del_bot(nombre):
    datos = BaseDatos.leer("bot_canales.json", {"creados_por_bot": []})
    return nombre in datos["creados_por_bot"]

def obtener_permisos(guild, ver=True, hablar=True, requiere_rango=None):
    everyone = guild.default_role
    permisos = {everyone: discord.PermissionOverwrite(
        view_channel=ver,
        send_messages=hablar
    )}
    
    if requiere_rango:
        rol = discord.utils.get(guild.roles, name=requiere_rango)
        if rol:
            permisos[rol] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
    return permisos

async def sincronizar_canales(guild):
    Logger.info("🔍 Sincronizando canales...")
    
    creados = 0
    existentes = {c.name: c for c in guild.channels}

    for cat_data in estructura:
        cat_nombre = cat_data["categoria"]
        posicion = cat_data.get("posicion", 0)
        
        categoria = discord.utils.get(guild.categories, name=cat_nombre)
        if not categoria:
            permisos_cat = obtener_permisos(
                guild,
                ver=cat_data["permisos_base"].get("ver", True),
                hablar=cat_data["permisos_base"].get("hablar", True),
                requiere_rango=cat_data.get("requiere_rango")
            )
            categoria = await guild.create_category_channel(
                name=cat_nombre,
                overwrites=permisos_cat,
                position=posicion
            )
            registrar_canal_creado(cat_nombre)
            Logger.exito(f"📂 Categoría: {cat_nombre}")
            creados += 1
        else:
            Logger.info(f"⏭️ {cat_nombre} — existe")

        # Canales simples
        if "canales" in cat_data:
            for canal in cat_data["canales"]:
                nombre = canal["nombre"]
                tipo = canal["tipo"]
                if nombre not in existentes:
                    permisos_canal = obtener_permisos(
                        guild,
                        ver=cat_data["permisos_base"].get("ver", True),
                        hablar=cat_data["permisos_base"].get("hablar", True),
                        requiere_rango=cat_data.get("requiere_rango")
                    )
                    if tipo == "text":
                        await guild.create_text_channel(name, category=categoria, overwrites=permisos_canal)
                    else:
                        await guild.create_voice_channel(name, category=categoria, overwrites=permisos_canal)
                    registrar_canal_creado(nombre)
                    Logger.exito(f"  ✅ {nombre}")
                    creados += 1

        # Subcanales privados por juego
        if "subcanales" in cat_data:
            for juego, datos_juego in cat_data["subcanales"].items():
                req_rango = datos_juego.get("requiere_rango")
                permisos_juego = obtener_permisos(guild, ver=False, hablar=False, requiere_rango=req_rango)
                for canal in datos_juego["canales"]:
                    nombre = canal["nombre"]
                    tipo = canal["tipo"]
                    if nombre not in existentes:
                        if tipo == "text":
                            await guild.create_text_channel(nombre, category=categoria, overwrites=permisos_juego)
                        else:
                            await guild.create_voice_channel(nombre, category=categoria, overwrites=permisos_juego)
                        registrar_canal_creado(nombre)
                        Logger.exito(f"  ✅ {nombre}")
                        creados += 1

    Logger.info("════════════════════════════")
    Logger.info(f"📊 Canales creados: {creados}")
    return creados
