import discord
from discord.ext import commands

import math # for tracking memory usage
from psutil import Process # for tracking memory usage
from os import getpid # for tracking memory usage

import datetime # for tracking uptime
import time # for tracking uptime

from misc.database import do_find

start_time = time.time()


class Uptime:
    def __init__(self, bot):
        self.bot = bot


@commands.command(aliases = ["status"])
async def info(ctx):
    try:
        process = Process(getpid())
        process_mem = math.floor(process.memory_info()[0] / float(2 ** 20))

        # uptime tracking
        current_time = time.time()
        difference = int(round(current_time - start_time))

        # send the info embed
        info_embed = discord.Embed(
            color = 0x546e7a,
            )
    
        # bot avatar + bot name at the top
        info_embed.set_author(name = ctx.bot.user.name, icon_url = ctx.bot.user.avatar)

        # info lines
        info_embed.add_field(name = "Uptime", value = str(datetime.timedelta(seconds=difference)), inline = True)
        info_embed.add_field(name = "Memory", value = str(process_mem) + " MB", inline = True)
        info_embed.add_field(name = "Prefix", value = ".", inline = True)
        info_embed.add_field(name = "Version", value = "Beta", inline = True)
    
        total_users = 0 # count how many total users are in the database
        data = await do_find() # get the data from database

        for guild_dict in data: # add up all the users
            total_users += len(guild_dict["users"])
        info_embed.add_field(name = "Users", value = total_users, inline = True)
    
        info_embed.add_field(name = "Guilds", value = len(ctx.bot.guilds), inline = True)

        info_embed.add_field(name = "━━━━━━━━━━━━━" + "\n" "Creator", value = "dr.john", inline = True)
        info_embed.add_field(name = "━━━━━━━━━━━━━" + "\n" "Twitter", value = "[@DrJohn_](https://twitter.com/DrJohn_)", inline = True)
        info_embed.add_field(name = "━━━━━━━━━━━━━" + "\n" "Support", value = "[MrCookie HQ](https://discord.gg/QQTC3ABV9U)", inline = True)

        await ctx.send(embed=info_embed)

    # exception handling
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(info)