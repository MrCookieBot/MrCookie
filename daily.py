import discord
from discord.ext import commands
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta

# dictionaries
cookieDict = {}

userData = {"Streaks": 1, "ExpTime": datetime.now() + timedelta(hours = 24), "Cookies": 15, "Multiplier": 0, "RobExp": None}

# cookie calculations
base_cookies = 15

# daily
@commands.command()
async def daily(ctx):

    if ctx.guild.id not in cookieDict:
        cookieDict[ctx.guild.id] = {}
    if ctx.author.id in cookieDict[ctx.guild.id]: # if user has run daily before, pull up their data
        if cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"] == None or datetime.now() >= cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"]: # check if their exp date is over
            
            # check if their streak expired
            if cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"]== None:
                cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] = cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] + 1 # add 1 to daily streak
            else:
                if datetime.now() > cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"] + timedelta(hours = 24):
                    cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] = 1 # reset their streak if it's been over 24 hours since exptime
                else:
                    cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] = cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] + 1 # add 1 to daily streak

            # figure out weekly bonus
            weekly_reward = 0 # the beginner weekly_reward if user does not reach 10 streaks
            if cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] % 10 == 0:  ## meaning they just hit a streak 10,20,30,40, etc
                weekly_multiplier = cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] // 1 # find out their 10 day bonus
                if weekly_multiplier > 60:
                    weekly_reward = 60
                else:
                    weekly_reward = weekly_multiplier
                
            # figure out their daily bonus
            if cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] // 14 == 0: # check if user hit another 14th multiple streak
                if cookieDict[ctx.guild.id][ctx.author.id]["Multiplier"] < 50: # check if user hit 50 multiplier yet
                    cookieDict[ctx.guild.id][ctx.author.id]["Multiplier"] = cookieDict[ctx.guild.id][ctx.author.id]["Multiplier"] + 5 # if not, add 5
            if cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] == 1: # if streak reset, reset multiplier as well
                cookieDict[ctx.guild.id][ctx.author.id]["Multiplier"] = 0
            

            # add their streaks and cookies up
            total = base_cookies + cookieDict[ctx.guild.id][ctx.author.id]["Multiplier"]
            cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] = cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] + total + weekly_reward # add up daily cookies
            cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"] = datetime.now() + timedelta(hours = 24) # set expiration date

            # send the embed
            embed = discord.Embed(
                description = "You have collected your daily ``" + str(total) + "`` cookies!" + "\n" + 
                "You are now on a streak of ``" + str(cookieDict[ctx.guild.id][ctx.author.id]["Streaks"]) + "`` day.",
                color = 0x2ecc71,
                timestamp = cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"]
                )

            embed.set_author(name = "Daily Cookies - " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            embed.set_footer(text = "You can collect again in 24 hours.")

            if cookieDict[ctx.guild.id][ctx.author.id]["Streaks"] % 10 == 0: # bonus cookies every 10 day message
                embed.add_field(name = "🍪 Bonus Cookies!", value = "For reaching a streak of **" + str(cookieDict[ctx.guild.id][ctx.author.id]["Streaks"]) + "**, you receieved **" + str(weekly_multiplier) + "** extra cookies.", inline = True)
            
            await ctx.send(embed=embed)


        else: # send not time yet embed
            mathtime = int(cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"].timestamp()) # doing the math for embed timer
            embed = discord.Embed(
                description = "You can collect your daily cookies " + "<t:" + str(mathtime) + ":R>",
                color = 0x992d22,
                timestamp = cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"]
                )

            embed.set_author(name = "Keep waiting " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            
            await ctx.send(embed=embed)


    else: # If user has never run daily before, collect their data for cookieDict
        cookieDict[ctx.guild.id][ctx.author.id] = {**userData}

        # send the embed
        embed = discord.Embed(
            description = "You have collected your daily ``15`` cookies!" + "\n" + 
            "You are now on a streak of ``" + str(cookieDict[ctx.guild.id][ctx.author.id]["Streaks"]) + "`` day.", 
            color = 0x2ecc71,
            timestamp = cookieDict[ctx.guild.id][ctx.author.id]["ExpTime"]
            )

        embed.set_author(name = "Daily Cookies - " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
        embed.set_footer(text = "You can collect again in 24 hours.")
            
        await ctx.send(embed=embed)


# connecting to main file

async def setup(bot):
    bot.add_command(daily)