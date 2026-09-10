from config.config import cargar_config

cfg = cargar_config()

async def setup(bot):
    @bot.command(name="rango_lista")
    async def rango_lista(ctx):
        jerarquia = cfg["rangos"]["jerarquia"]
        colores = cfg["rangos"]["colores"]
        
        # Dividimos en mensajes más cortos para no exceder el límite de Discord
        mensaje = "**👑 LISTA DE RANGOS — KR EMPIRE**\n\n"
        
        for nombre in jerarquia:
            linea = f"{nombre} — `{colores.get(nombre, '#808080')}`\n"
            # Si se hace muy largo, enviamos y empezamos uno nuevo
            if len(mensaje) + len(linea) > 1800:
                await ctx.send(mensaje)
                mensaje = ""
            mensaje += linea
        
        if mensaje:
            await ctx.send(mensaje)
