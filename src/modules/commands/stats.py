from resources.mrcookie import instance as bot
import discord

from resources.checks import lookup_database, new_database

@bot.command(aliases = ["bal", "balance"])
async def stats(ctx):
    