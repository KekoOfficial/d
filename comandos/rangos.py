from core.permisos import solo_dueno
from utils.embeds import Embed
from config.config import cargar_config
from database.database import BaseDatos

cfg = cargar_config()

async def setup(bot):
    
    @bot.command(name="rango_lista")
    async def rango_lista(ctx):
        texto = "**👑 RANGOS BASE:**\n"
        for nombre, color in cfg["rangos_base"].items():
            texto += f"├ {nombre} → `{color}`\n"
        texto += "\n**🎮 RANGOS DE JUEGO:**\n"
        for nombre, color in cfg["rangos_juegos"].items():
            texto += f"├ {nombre}\n"
        texto += "\n**🌐 IDIOMAS:**\n"
        for nombre, color in cfg["idiomas"].items():
            texto += f"├ {nombre}\n"
        await ctx.send(texto)

    @bot.command(name="crear_rangos")
    @solo_dueno()
    async def crear_rangos(ctx):
        await ctx.send("⏳ Creando rangos...")
        guild = ctx.guild
        
        # Crear rangos base
        creados = 0
        for nombre, color in cfg["rangos_base"].items():
            if not discord.utils.get(guild.roles, name=nombre):
                await guild.create_role(name=nombre, color=int(color.lstrip('#'), 16))
                creados += 1
        
        # Crear rangos de juegos
        for nombre, color in cfg["rangos_juegos"].items():
            if not discord.utils.get(guild.roles, name=nombre):
                await guild.create_role(name=nombre, color=int(color.lstrip('#'), 16))
                creados += 1
        
        # Crear rangos de idiomas
        for nombre, color in cfg["idiomas"].items():
            if not discord.utils.get(guild.roles, name=nombre):
                await guild.create_role(name=nombre, color=int(color.lstrip('#'), 16))
                creados += 1
        
        await ctx.send(embed=Embed.exito("Rangos Creados", f"✅ Se crearon **{creados}** rangos correctamente"))

    @bot.command(name="borrar_rangos")
    @solo_dueno()
    async def borrar_rangos(ctx):
        await ctx.send("⚠️ **¿Eliminar todos los rangos del sistema?**\nEscribe `¡CONFIRMAR!` en 10 segundos para continuar.")
        
        def check(m):
            return m.author == ctx.author and m.content == "¡CONFIRMAR!"
        
        try:
            await bot.wait_for('message', check=check, timeout=10)
        except:
            await ctx.send("❌ Cancelado")
            return
        
        guild = ctx.guild
        eliminados = 0
        
        todos_los_rangos = list(cfg["rangos_base"].keys()) + list(cfg["rangos_juegos"].keys()) + list(cfg["idiomas"].keys())
        
        for nombre in todos_los_rangos:
            rol = discord.utils.get(guild.roles, name=nombre)
            if rol and rol < guild.me.top_role:
                await rol.delete()
                eliminados += 1
        
        await ctx.send(embed=Embed.exito("Rangos Eliminados", f"✅ Se eliminaron **{eliminados}** rangos"))
