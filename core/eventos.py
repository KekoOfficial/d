from .sistemas.sincronizacion import sincronizar_rangos
from utils.logger import Logger
from datetime import datetime

class Eventos:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_ready(self):
        print("\n" + "═" * 60)
        print("🚀  KR EMPIRE — SISTEMA INICIADO")
        print(f"🤖  Conectado como: {self.bot.user}")
        print(f"🌐  Servidores: {len(self.bot.guilds)}")
        print(f"⏰  Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("═" * 60 + "\n")
        
        # 🧠 SINCRONIZACIÓN AUTOMÁTICA AL ENCENDER
        for guild in self.bot.guilds:
            Logger.info(f"🔍 Sincronizando en: {guild.name}")
            await sincronizar_rangos(guild)
        
        Logger.exito("✅ ¡Todo actualizado automáticamente!")
        print("\n✅ Sistema listo\n")

def setup_eventos(bot):
    instancia = Eventos(bot)
    @bot.event
    async def on_ready():
        await instancia.on_ready()
