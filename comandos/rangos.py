import discord
from core.permisos import solo_dueno
from utils.embeds import Embed
from config.config import cargar_config

cfg = cargar_config()
divisiones = cfg["divisiones"]

async def setup(bot):

    @bot.command(name="rango_lista")
    async def rango_lista(ctx):
        texto = "**🏰 KR EMPIRE — LISTA DE RANGOS POR DIVISIÓN**\n\n"
        for div_nombre, data in divisiones.items():
            auto = " ✅ [ELEGIBLE]" if data.get("autoasignable", False) else " 🔒 [SOLO EQUIPO]"
            texto += f"═══ {div_nombre} {auto} ═══\n"
            texto += f"   {data['descripcion']}\n"
            for nombre in data["rangos"]:
                texto += f"  ├ {nombre}\n"
            texto += "\n"
        await ctx.send(texto)

    @bot.command(name="crear_rangos")
    @solo_dueno()
    async def crear_rangos(ctx):
        mensaje = await ctx.send("⏳ Creando rangos por divisiones... esto puede tardar...")
        guild = ctx.guild
        total = 0

        for div_nombre, data in divisiones.items():
            for nombre, color in data["rangos"].items():
                if not discord.utils.get(guild.roles, name=nombre):
                    await guild.create_role(name=nombre, color=int(color.lstrip('#'), 16))
                    total += 1

        await mensaje.edit(embed=Embed.exito(
            "✅ Rangos Creados",
            f"Se crearon **{total} rangos** en **{len(divisiones)} divisiones**\n\n"
            "🔒 Autoridad: Fundadores, Admin, Staff, Distinciones, Niveles\n"
            "✅ Libres: Juegos, Estilo, Identidad, Idiomas, Intereses, Plataformas, Zona, Actividad, Notificaciones"
        ))

    @bot.command(name="borrar_rangos")
    @solo_dueno()
    async def borrar_rangos(ctx):
        await ctx.send("⚠️ **¿Eliminar TODOS los rangos del sistema?**\nEscribe `¡CONFIRMAR!` en 10 segundos para continuar.")
        
        def check(m):
            return m.author == ctx.author and m.content == "¡CONFIRMAR!"
        
        try:
            await bot.wait_for('message', check=check, timeout=10)
        except:
            await ctx.send("❌ Cancelado")
            return
        
        guild = ctx.guild
        eliminados = 0
        for data in divisiones.values():
            for nombre in data["rangos"]:
                rol = discord.utils.get(guild.roles, name=nombre)
                if rol and rol < guild.me.top_role:
                    await rol.delete()
                    eliminados += 1
        
        await ctx.send(embed=Embed.exito("✅ Rangos Eliminados", f"Se eliminaron **{eliminados} rangos**"))
