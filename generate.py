import discord
from discord.ext import commands
from daily import cookieDict
from say import Admins


# userData dictionary to put their data in cookieDict
userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


@commands.command()
async def generate(ctx, user_id = "<@!0>", amount = "0"):
    try:
        # make sure only users with manage_server can run the command or bot admins
        if ctx.author.id not in Admins:
            if not ctx.author.guild_permissions.manage_guild:
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
        
        # check the amount
        if amount > 5000: # generate limit
            raise Exception("You can't generate more than 5,000 cookies at a time.")
        
        if amount == 0.0:
            raise Exception("You forgot to include an amount to give.")
        
        if amount < 0:
            operation = "Removed "
            tense = " from "
        else:
            operation = "Added "
            tense = " to "

        # if the receiver is not in the dictionary, add them    
        if ctx.guild.id not in cookieDict:            
            cookieDict[ctx.guild.id] = {}
        if user_id not in cookieDict[ctx.guild.id]:
            cookieDict[ctx.guild.id][user_id] = {**userData}

        # generate the cookies if no errors have been raised
        if cookieDict[ctx.guild.id][user_id]["Cookies"] + amount < 0: # no letting the user go in negative cookies
            raise Exception("You can't put the user in negative cookies.")
        else:
            cookieDict[ctx.guild.id][user_id]["Cookies"] = cookieDict[ctx.guild.id][user_id]["Cookies"] + amount

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