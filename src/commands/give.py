import discord
from discord.ext import commands
from misc.database import do_update, do_find_one, do_find_blacklist_user


# userData dictionary to put their data in cookieDict
userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}

@commands.command(aliases = ["gift", "transfer"])
async def give(ctx, user_id = "<@!0>", amount = "0"):
    try:
        user_id = user_id.strip("<@!>")
        user_id = int(user_id)
        amount = int(amount)

        # do all the checks before giving a cookie
        if user_id == ctx.author.id:
            raise Exception("You can't give cookies to yourself, silly!")
        if user_id == 0 or len(str(user_id)) < 17:
            raise Exception("You forgot to tag a user and amount to give.")
        
        # check if user is blacklisted
        if await do_find_blacklist_user({"_id": str(user_id)}) != None:
            raise Exception("You can't give cookies to a blacklisted user.")

        # check if user is in the guild
        guild = ctx.bot.get_guild(ctx.guild.id)
        if guild.get_member(user_id) is None:
            raise Exception("Invalid user or not in the guild.")
        
        if amount == 0.0:
            raise Exception("You forgot to include an amount to give.")
        if amount < 0.0:
            raise Exception("Don't be cheap, send more than 0 cookies!")

        # if the sender is not in the dictionary, add them    
        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}) == None:
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) : {**userData}}})
            
        # if the receiver is not in the dictionary, add them    
        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}}) == None:
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) : {**userData}}})

        # if sender doesn't have enough cookies, raise an error
        data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

        if int(data["users"][str(ctx.author.id)]["Cookies"]) < amount:
            raise Exception("You don't have that many cookies!")
           
        
        # transfer the cookies if no errors have been raised
        new_cookies = int(data["users"][str(user_id)]["Cookies"]) + amount
        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) + "." + "Cookies": new_cookies}})

        new_cookies2 = int(data["users"][str(ctx.author.id)]["Cookies"]) - amount
        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies2}})

        # fetch/get_user information from receiver
        if ctx.bot.get_user(user_id) == None:
            receieve_user = await ctx.bot.fetch_user(user_id)
        else:
            receieve_user = ctx.bot.get_user(user_id)
        
        # get_user information from sender
        sender_user = ctx.bot.get_user(ctx.author.id)

        # send the transfer embed
        data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

        embed = discord.Embed(
            title = "🍪 Cookies Transferred!",
            description = sender_user.mention + " just gave " + receieve_user.mention + " ``" + str(amount) + "`` cookies!",
            color = 0x2ecc71,
            )

        #for footer, try get_user and if that fails then fetch_user
        embed.set_footer(text = receieve_user.display_name + " now has " + str(data["users"][str(user_id)]["Cookies"]) + " cookies.")
            
        await ctx.send(embed=embed)

# exception handling

    except discord.NotFound:
        await ctx.send("You have sent an invalid user.")
    except ValueError:
        await ctx.send("You're not sending actual cookies..")
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(give)