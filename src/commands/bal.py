import discord
from discord.ext import commands

from misc.database import do_update, do_find_one



# get the rank 

def position(author_id, data):
    def sorting(values):
        return data["users"][str(values)]["Cookies"]

    rank = 0
    cookielist = list(data["users"])
    cookielist.sort(reverse = True, key = sorting)
  

    for key in cookielist:
        if int(key) == author_id:
            rank = cookielist.index(key) + 1
            break
    
    return rank



# userData dictionary

userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


# bal command

@commands.command(aliases = ["balance", "stats"])
async def bal(ctx, user_id = "0"):

    try:
        # check if user is legit
        user_id = user_id.strip("<@!>")
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            raise Exception("Invalid user or not in the guild.")

        # figure out if user pinged someone or not
        if user_id == 0:
            user_id = ctx.author.id
            user = ctx.author
            # check if the user is in the database, if not add them
            if await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}}) == None:
                print("I was not supposed to run")
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) : {**userData}}})
        else:
            # checking if the user is legit
            if len(str(user_id)) < 17:
                raise Exception("You sent an invalid user.")
            # check if user is blacklisted
            #from commands.blacklist import blacklisted_users
            #if user_id in blacklisted_users:
                #raise Exception("You can't check the balance of a blacklisted user.")
            
            guild = ctx.bot.get_guild(ctx.guild.id) # find ID by right clicking on server icon and choosing "copy id" at the bottom
            if guild.get_member(user_id) is None:
                raise Exception("Invalid user or not in the guild.")
            
            # get_user's data, if they never used bot then fetch it
            if ctx.bot.get_user(user_id) == None:
                user = await ctx.bot.fetch_user(user_id)
            else:
                user = ctx.bot.get_user(user_id)
            
            # check if the user is in the database, if not add them
            if await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}}) == None:
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) : {**userData}}})


        # get the user's rank
        data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}})) # refresh the data dict with new database data

        user_rank = position(user_id, data)


        # send the embed
        embed = discord.Embed(
            title = str(user.display_name) + "'s Cookie Balance",
            color = 0x7289da,
            )
    
    
        embed.add_field(name = "Cookies", value = str(data["users"][str(user_id)]["Cookies"]), inline = True)
        embed.add_field(name = "Rank", value = "#" + str(user_rank), inline = True)
        embed.set_thumbnail(url = user.display_avatar)

        await ctx.send(embed=embed)
    
    except discord.NotFound:
        await ctx.send("You sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)



# connecting to main file

async def setup(bot):
    bot.add_command(bal)