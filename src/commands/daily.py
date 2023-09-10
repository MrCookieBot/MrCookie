import discord
from discord.ext import commands
from datetime import datetime, timedelta

from misc.database import do_update, do_find_one


# user replica dictionary
userData = {"Streaks": 1, "ExpTime": datetime.now() + timedelta(hours = 23), "Cookies": 15, "Multiplier": 0, "RobExp": None}

# cookie calculations
base_cookies = 15

# daily
@commands.command()
async def daily(ctx):

    try:
        # check if user is in database
        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}) != None:
            data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # put the database for the user into this variable
            if data["users"][str(ctx.author.id)]["ExpTime"] == None or datetime.now() >= data["users"][str(ctx.author.id)]["ExpTime"]: # check if their exp date is over
            
                # check if their streak expired
                if data["users"][str(ctx.author.id)]["ExpTime"] == None:
                    new_streak = int(data["users"][str(ctx.author.id)]["Streaks"]) + 1 # add 1 to daily streak
                    await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Streaks": new_streak}})
                else:
                    if datetime.now() > data["users"][str(ctx.author.id)]["ExpTime"] + timedelta(hours = 23):
                        new_streak = 1 # reset their streak if it's been over 24 hours since exptime
                        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Streaks": new_streak}})
                    else:
                        new_streak = int(data["users"][str(ctx.author.id)]["Streaks"] + 1)
                        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Streaks": new_streak}}) # add 1 to daily streak

                # figure out weekly bonus
                data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data
                weekly_reward = 0 # the beginner weekly_reward if user does not reach 7 streaks
                
                if int(data["users"][str(ctx.author.id)]["Streaks"]) % 7 == 0: 
                    weekly_multiplier = int(data["users"][str(ctx.author.id)]["Streaks"]) // 7 # find out their 7 day bonus
                    if weekly_multiplier > 6:
                        weekly_reward = 60
                    else:
                        weekly_reward = weekly_multiplier * 10
                
                # figure out their daily bonus

                if int(data["users"][str(ctx.author.id)]["Streaks"]) % 14 == 0: # check if user hit 14 day streak

                    if int(data["users"][str(ctx.author.id)]["Multiplier"]) < 50: # if they did, check if they are under 50 multiplier
                        new_multiplier = int(data["users"][str(ctx.author.id)]["Multiplier"]) + 2 # if yes to both above, add 2 cookies to their multiplier
                        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Multiplier": new_multiplier}}) # if not, add 5

                if int(data["users"][str(ctx.author.id)]["Streaks"]) == 1: # if streak reset, reset multiplier as well
                    new_multiplier = 0
                    await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Multiplier": new_multiplier}})
                    

                # add their cookies up
                data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

                total = base_cookies + int(data["users"][str(ctx.author.id)]["Multiplier"])
                new_cookies = int(data["users"][str(ctx.author.id)]["Cookies"]) + total + weekly_reward # add up daily cookies
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies}})
                
                new_ExpTime = datetime.now() + timedelta(hours = 23) # set expiration date
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "ExpTime": new_ExpTime}})

                # send the embed
                data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

                embed = discord.Embed(
                    description = "You have collected your daily ``" + str(total) + "`` cookies!" + "\n" + 
                    "You are now on a streak of ``" + str(data["users"][str(ctx.author.id)]["Streaks"]) + "`` day.",
                    color = 0x2ecc71,
                    timestamp = data["users"][str(ctx.author.id)]["ExpTime"]
                    )

                embed.set_author(name = "Daily Cookies - " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
                embed.set_footer(text = "You can collect again in 23 hours.")

                if int(data["users"][str(ctx.author.id)]["Streaks"]) % 7 == 0: # bonus cookies every 10 day message
                    embed.add_field(name = "🍪 Bonus Cookies!", value = "For reaching a streak of **" + str(data["users"][str(ctx.author.id)]["Streaks"]) + "**, you receieved **" + str(weekly_reward) + "** extra cookies.", inline = True)
            
                await ctx.send(embed=embed)


            else: # send not time yet embed
                mathtime = int(data["users"][str(ctx.author.id)]["ExpTime"].timestamp()) # doing the math for embed timer
                embed = discord.Embed(
                    description = "You can collect your daily cookies " + "<t:" + str(mathtime) + ":R>",
                    color = 0x992d22,
                    timestamp = data["users"][str(ctx.author.id)]["ExpTime"]
                    )

                embed.set_author(name = "Keep waiting " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            
                await ctx.send(embed=embed)


        else: # If user has never run daily before, collect their data for cookieDict
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) : {**userData}}})
            data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}))


            # send the embed
            embed = discord.Embed(
                description = "You have collected your daily ``15`` cookies!" + "\n" + 
                "You are now on a streak of ``" + str(data["users"][str(ctx.author.id)]["Streaks"]) + "`` day.", 
                color = 0x2ecc71,
                timestamp = data["users"][str(ctx.author.id)]["ExpTime"]
                )

            embed.set_author(name = "Daily Cookies - " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            embed.set_footer(text = "You can collect again in 23 hours.")
            
            await ctx.send(embed=embed)
    
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(daily)