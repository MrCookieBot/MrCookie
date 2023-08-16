import discord
from discord.ext import commands
from daily import cookieDict

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
        from blacklist import blacklisted_users
        if user_id in blacklisted_users:
            raise Exception("You can't give cookies to a blacklisted user.")

        # check if user is in the guild
        guild = ctx.bot.get_guild(ctx.guild.id)
        if guild.get_member(user_id) is None:
            raise Exception("Invalid user or not in the guild.")
        
        if amount == 0.0:
            raise Exception("You forgot to include an amount to give.")
        if amount < 0.0:
            raise Exception("Don't be cheap, send more than 0 cookies!")

        # if the sender/receiver is not in the dictionary, add them, also add the guild_id
        if ctx.guild.id not in cookieDict:            
            cookieDict[ctx.guild.id] = {}

        if ctx.author.id not in cookieDict[ctx.guild.id]:
            cookieDict[ctx.guild.id][ctx.author.id] = {**userData}
            
        if user_id not in cookieDict:
            cookieDict[ctx.guild.id][user_id] = {**userData}

        # if sender doesn't have enough cookies, raise an error

        if cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] < amount:
            raise Exception("You don't have that many cookies!")
           
        
        # transfer the cookies if no errors have been raised
        cookieDict[ctx.guild.id][user_id]["Cookies"] = cookieDict[ctx.guild.id][user_id]["Cookies"] + amount
        cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] = cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] - amount

        # send the transfer embed
        embed = discord.Embed(
            title = "🍪 Cookies Transferred!",
            description = "<@!" + str(ctx.author.id) + "> just gave <@!" + str(user_id) + "> ``" + str(amount) + "`` cookies!",
            color = 0x2ecc71,
            )

        #for footer, try get_user and if that fails then fetch_user
        if ctx.bot.get_user(user_id) == None:
            embed.set_footer(text = str(await ctx.bot.fetch_user(user_id)) + " now has " + str(cookieDict[ctx.guild.id][user_id]["Cookies"]) + " cookies.")
        else:
            embed.set_footer(text = str(ctx.bot.get_user(user_id)) + " now has " + str(cookieDict[ctx.guild.id][user_id]["Cookies"]) + " cookies.")
            
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