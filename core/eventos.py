from sistemas.sincronizacion import sincronizar_rangos
from utils.logger import Logger
from datetime import datetime

class Eventos:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_ready(self):
        print("\n" + "═" * 50)
        print(f"🚀 KR EMPIRE conectado: {self.bot.user}")
        print("═" * 50 + "\n")
        
        for guild in self.bot.guilds:
            Logger.info(f"🔍 Servidor: {guild.name}")
            await sincronizar_rangos(guild)
        
        Logger.exito("✅ Todo sincronizado\n")

def setup_eventos(bot):
    instancia = Eventos(bot)
    @bot.event
    async def on_ready():
        await instancia.on_ready()
