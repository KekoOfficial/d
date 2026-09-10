from sistemas.rangos_setup import sincronizar_rangos
from sistemas.canales_setup import sincronizar_canales
from utils.logger import Logger
from datetime import datetime

class Eventos:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_ready(self):
        print("\n" + "═" * 60)
        print("🚀  KR EMPIRE — CONSTRUCTOR DE SERVIDOR INICIADO")
        print(f"🤖  Conectado como: {self.bot.user}")
        print(f"⏰  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("═" * 60 + "\n")
        
        for guild in self.bot.guilds:
            Logger.info(f"🌐 Servidor: {guild.name}")
            await sincronizar_rangos(guild)
            await sincronizar_canales(guild)
        
        Logger.exito("✅ ¡Servidor sincronizado al encender!\n")
        print("💡 Escribe kr!up en Discord para actualizar manualmente\n")

def setup_eventos(bot):
    instancia = Eventos(bot)
    @bot.event
    async def on_ready():
        await instancia.on_ready()
