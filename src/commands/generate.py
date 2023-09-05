import discord
from discord.ext import commands
from misc.database import do_update, do_find_one, do_find_blacklist_user
from commands.say import Admins


# userData dictionary to put their data in cookieDict
userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


@commands.command(aliases = ["gen"])
async def generate(ctx, user_id = "<@!0>", amount = "0"):
    try:
        # make sure only users with manage_server can run the command or bot admins
        if ctx.author.id not in Admins:
            raise Exception("You don't have permission to run this command.")
        
        # fix up the user_id and amount

        user_id = user_id.strip("<@!>")
        user_id = int(user_id)
        amount = int(amount)

        # check the user
        if user_id == 0 or len(str(user_id)) < 17:
            raise Exception("You forgot to tag a user and amount to give.")
        
        guild = ctx.bot.get_guild(ctx.guild.id) # check if user is in the guild
        if guild.get_member(user_id) is None:
            raise Exception("Invalid user or not in the guild.")
        
        # check if user is blacklisted
        if await do_find_blacklist_user({"_id": str(user_id)}) != None:
            raise Exception("You can't generate cookies to a blacklisted user.")

        # check the amount
        if amount > 1000: # generate limit
            raise Exception("You can't generate more than 1,000 cookies at a time.")
        
        if amount == 0.0:
            raise Exception("You forgot to include an amount to give.")
        
        if amount < 0:
            operation = "Removed "
            tense = " from "
        else:
            operation = "Added "
            tense = " to "

        # if the receiver is not in the dictionary, add them    
        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}}) == None:
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) : {**userData}}})

        # generate the cookies if no errors have been raised
        data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

        if int(data["users"][str(user_id)]["Cookies"]) + amount < 0: # no letting the user go in negative cookies
            raise Exception("You can't put the user in negative cookies.")
        else:
            new_cookies = int(data["users"][str(user_id)]["Cookies"]) + amount
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies}})

        # get user information to tag them, try get_user and if that fails then fetch_user
        if ctx.bot.get_user(user_id) == None:
            user = await ctx.bot.fetch_user(user_id)
        else:
            user = ctx.bot.get_user(user_id)

        # send the confirmation embed
        gen_embed = discord.Embed(
            title = "🍪 Cookies Generated!",
            description = str(operation) + " ``" + str(amount) + "`` cookies" + str(tense) + user.mention + "'s balance.",
            color = 0x9b59b6,
            )
        
        await ctx.send(embed=gen_embed)

    # exception handling
    except discord.NotFound:
        await ctx.send("You have sent an invalid user.")
    except ValueError:
        await ctx.send("You're not sending actual cookies..")
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(generate)