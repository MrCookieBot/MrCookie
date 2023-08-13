import discord
from discord.ext import commands


# ping command

@commands.command()
async def ping(ctx):
    try:
        # check if user is blacklisted
        from blacklist import blacklisted_users
        if ctx.author.id in blacklisted_users:
            raise Exception("You are blacklisted from MrCookie.")

        ping = round((ctx.bot.latency) * 1000)
        await ctx.send("Pong! - " + str(ping) + "ms")

    # exception handling
    except Exception as Error:
        await ctx.send(Error)

# connecting to main file

async def setup(bot):
    bot.add_command(ping)