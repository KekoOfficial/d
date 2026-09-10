from core.permisos import solo_dueno
from utils.embeds import Embed
from sistemas.sincronizacion import sincronizar_rangos

async def setup(bot):
    
    @bot.command(name="estado")
    async def estado(ctx):
        await ctx.send(embed=Embed.info("Estado", "🟢 Sistema funcionando"))
    
    @bot.command(name="ayuda")
    async def ayuda(ctx):
        await ctx.send("**🏰 KR EMPIRE** ✅ En línea\n`kr!up` → Revisar y actualizar rangos")
    
    @bot.command(name="up")
    @solo_dueno()
    async def up(ctx):
        mensaje = await ctx.send("🔍 Revisando y actualizando todo...")
        await sincronizar_rangos(ctx.guild)
        await mensaje.edit(embed=Embed.exito("✅ Actualizado", "Todo revisado, creado y limpiado correctamente"))
