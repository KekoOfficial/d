import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from core.bot import setup_bot
from utils.logger import Logger

bot = setup_bot()

async def cargar_modulos():
    from comandos import admin, rangos
    await admin.setup(bot)
    await rangos.setup(bot)
    Logger.exito("Módulos cargados")

@bot.event
async def on_ready():
    print("\n" + "═" * 50)
    print(f"🚀 KR EMPIRE conectado: {bot.user}")
    print("═" * 50 + "\n")
    await cargar_modulos()
    print("✅ Sistema listo. Escribe kr!ayuda en Discord\n")

Logger.info("Iniciando bot...")
try:
    bot.run(Config.TOKEN)
except Exception as e:
    Logger.error(f"Error: {e}")
