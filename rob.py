import discord
from discord.ext import commands
from daily import cookieDict
from datetime import datetime, timedelta


@commands.command()
async def rob(ctx, user_id = "0"):

    try:
        # check if guild/user is in database, if not add it
        if ctx.guild.id not in cookieDict:
            cookieDict[ctx.guild.id] = {}
        if ctx.author.id not in cookieDict[ctx.guild.id]:
            raise Exception("You need at least 15 cookies to rob someone.")
        
        # make sure their rob cooldown is over
        if cookieDict[ctx.guild.id][ctx.author.id]["RobExp"] == None or datetime.now() > cookieDict[ctx.guild.id][ctx.author.id]["RobExp"]:

            # check if the sender has enough cookies to rob
            if cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] < 15:
                raise Exception("You need at least 15 cookies to rob someone.")
    
            # check if user_id is valid
            user_id = user_id.strip("<@!>")
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                raise Exception("You sent an invalid user.")

            # if user didn't mention someone, find someone random to rob
            if user_id == 0:
                await ctx.send("i didnt code finding a random user yet lol")

            # if user did mention someone, verify that user is real
            else:
                if len(str(user_id)) < 17:
                    raise Exception("You sent an invalid user.")
            
                # check if user is in the guild
                guild = ctx.bot.get_guild(ctx.guild.id)
                if guild.get_member(user_id) is None:
                    raise Exception("User is not in the guild.")
                
                # if user is not in the database, they cannot be robbed
                if user_id not in cookieDict[ctx.guild.id]:
                    raise Exception("User does not have enough cookies to be robbed.")
                
                # if user has less than 15 cookies, they cannot be robbed
                if cookieDict[ctx.guild.id][user_id]["Cookies"] < 15:
                    raise Exception("User does not have enough cookies to be robbed.")

                # get_user's data - OPTIONAL !!!
                user = ctx.bot.get_user(user_id)
    
        
            # add 24 hours to their rob cooldown again
            cookieDict[ctx.guild.id][ctx.author.id]["RobExp"] = datetime.now() + timedelta(hours = 3)

            # go through the robbing process of the user
            await ctx.send("I didn't code the random rob chance yet lol")
        
        else:
            mathtime = int(cookieDict[ctx.guild.id][ctx.author.id]["RobExp"].timestamp()) # doing the math for embed timer
            timeout_embed = discord.Embed(
                description = "You can rob someone again " + "<t:" + str(mathtime) + ":R>",
                color = 0x992d22,
                timestamp = cookieDict[ctx.guild.id][ctx.author.id]["RobExp"]
                )

            timeout_embed.set_author(name = "Not so fast " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            
            await ctx.send(embed=timeout_embed)           

    except discord.NotFound:
        await ctx.send("You have sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(rob)