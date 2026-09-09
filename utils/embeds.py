import discord
from datetime import datetime

class Embed:
    @staticmethod
    def exito(titulo, descripcion=""):
        return discord.Embed(
            title=f"✅ {titulo}", description=descripcion,
            color=0x00FF00, timestamp=datetime.now()
        )
    
    @staticmethod
    def error(titulo, descripcion=""):
        return discord.Embed(
            title=f"❌ {titulo}", description=descripcion,
            color=0xFF0000, timestamp=datetime.now()
        )
    
    @staticmethod
    def info(titulo, descripcion=""):
        return discord.Embed(
            title=f"ℹ️ {titulo}", description=descripcion,
            color=0x9932CC, timestamp=datetime.now()
        )
