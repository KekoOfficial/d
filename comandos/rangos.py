import discord
from utils.embeds import Embed
from config.config import cargar_config

cfg = cargar_config()
divisiones = cfg["divisiones"]

async def setup(bot):
    @bot.command(name="rango_lista")
    async def rango_lista(ctx):
        # Enviamos cada división por separado
        for div_nombre, data in divisiones.items():
            auto = " ✅ [ELEGIBLE]" if data.get("autoasignable", False) else " 🔒 [SOLO EQUIPO]"
            texto = f"**═══ {div_nombre} {auto} ═══**\n"
            for nombre in data["rangos"]:
                texto += f"├ {nombre}\n"
            await ctx.send(texto)
