from core.permisos import solo_dueno
from utils.embeds import Embed
from sistemas.rangos_setup import sincronizar_rangos
from sistemas.canales_setup import sincronizar_canales

async def setup(bot):
    
    @bot.command(name="ayuda")
    async def ayuda(ctx):
        await ctx.send("""
**🏰 KR EMPIRE — CONSTRUCTOR DE SERVIDOR**

`kr!up` → Construir/actualizar TODO el servidor
`kr!estado` → Ver estado del bot
        """)
    
    @bot.command(name="estado")
    async def estado(ctx):
        await ctx.send(embed=Embed.info("Estado", "🟢 KR EMPIRE está funcionando correctamente"))
    
    @bot.command(name="up")
    @solo_dueno()
    async def up(ctx):
        mensaje = await ctx.send("🔍 **Paso 1/3** → Revisando rangos...")
        
        rangos_creados, rangos_act, rangos_borrados = await sincronizar_rangos(ctx.guild)
        
        await mensaje.edit(content="🔍 **Paso 2/3** → Revisando canales y permisos...")
        canales_creados = await sincronizar_canales(ctx.guild)
        
        resumen = f"""
✅ **SERVIDOR ACTUALIZADO COMPLETAMENTE**

👑 Rangos:
  ├ Creados: {rangos_creados}
  ├ Actualizados: {rangos_act}
  └ Eliminados: {rangos_borrados}

📂 Canales:
  └ Creados: {canales_creados}

Todo sincronizado desde `config.json` ✨
        """
        await mensaje.edit(content=resumen)
