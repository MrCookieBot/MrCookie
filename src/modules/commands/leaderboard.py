from resources.mrcookie import instance as bot
import discord

from resources.checks import lookup_database, new_database

@bot.command()
async def leaderboard(ctx):
    try:
        await ctx.send("test")

    except Exception as Error:
        await ctx.send(Error)