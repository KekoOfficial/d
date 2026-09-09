from core.permisos import solo_dueno
from utils.embeds import Embed

async def setup(bot):
    @bot.command(name="estado")
    async def estado(ctx):
        await ctx.send(embed=Embed.info("Estado", "🟢 Sistema funcionando"))
    
    @bot.command(name="ayuda")
    async def ayuda(ctx):
        await ctx.send("**🏰 KR EMPIRE** ✅ En línea")
