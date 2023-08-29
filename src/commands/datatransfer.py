import discord
from discord.ext import commands

@commands.command()
async def datatransfer(ctx):
    await ctx.send("Hello")




# connecting to main file

async def setup(bot):
    bot.add_command(datatransfer)