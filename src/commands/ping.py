import discord
from discord.ext import commands


# ping command

@commands.command()
async def ping(ctx):
    try:
        ping = round((ctx.bot.latency) * 1000)
        await ctx.send("Pong! - " + str(ping) + "ms")

    # exception handling
    except Exception as Error:
        await ctx.send(Error)

# connecting to main file

async def setup(bot):
    bot.add_command(ping)