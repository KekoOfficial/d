import discord
from discord.ext import commands
from config.config import Config

def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    return commands.Bot(
        command_prefix=Config.cargar()["prefijo"],
        intents=intents,
        help_command=None
    )
