import discord
from discord.ext import commands


# ping command

@commands.command()
async def ping(ctx):
    ping = round((ctx.bot.latency) * 1000)
    await ctx.send("Pong! - " + str(ping) + "ms")


# connecting to main file

async def setup(bot):
    bot.add_command(ping)