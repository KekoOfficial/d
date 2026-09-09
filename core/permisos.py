from config.config import Config

def es_dueno(ctx):
    return ctx.author.id == Config.DUENO_ID

def solo_dueno():
    from discord.ext import commands
    return commands.check(lambda ctx: es_dueno(ctx))
