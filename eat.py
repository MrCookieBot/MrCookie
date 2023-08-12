import discord
from discord.ext import commands
from daily import cookieDict

@commands.command()
async def eat(ctx):
    try:
        if ctx.guild.id not in cookieDict:
            cookieDict[ctx.guild.id] = {}
        if ctx.author.id not in cookieDict[ctx.guild.id]:
            raise Exception("You have no cookies to eat.")
        if cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] - 1 < 0:
            raise Exception("You have no cookies to eat.")

        # if no errors, continue with command
        cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] = cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] - 1 # removes 1 cookie from their total
        await ctx.send("Yummy! You ate 1 cookie 🍪")

    # exception handling
    except Exception as Error:
        await ctx.send(Error)
        



# connecting to main file

async def setup(bot):
    bot.add_command(eat)