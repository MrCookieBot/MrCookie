import discord
from discord.ext import commands
from daily import cookieDict 


# get the rank 

def position(guild_id, author_id):
    def sorting(values):
        return cookieDict[guild_id][values]['Cookies']

    rank = 0
    cookielist = list(cookieDict[guild_id])
    cookielist.sort(reverse = True, key = sorting)
  

    for key in cookielist:
        if key == author_id:
            rank = cookielist.index(key) + 1
            break
    
    return rank



# userData dictionary

userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


# bal command

@commands.command(aliases = ["balance", "stats"])
async def bal(ctx, user_id = "0"):

    try:
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
            if ctx.guild.id not in cookieDict:
                cookieDict[ctx.guild.id] = {}
            if ctx.author.id not in cookieDict[ctx.guild.id]:
                cookieDict[ctx.guild.id][user_id] = {**userData}
        else:
            # checking if the user is legit
            if len(str(user_id)) < 17:
                raise Exception("You sent an invalid user.")
            
            guild = ctx.bot.get_guild(ctx.guild.id) # find ID by right clicking on server icon and choosing "copy id" at the bottom
            if guild.get_member(user_id) is None:
                raise Exception("Invalid user or not in the guild.")
            
            # get_user's data, if they never used bot then fetch it
            if ctx.bot.get_user(user_id) == None:
                user = await ctx.bot.fetch_user(user_id)
            else:
                user = ctx.bot.get_user(user_id)
            
            # check if the user is in the database, if not add them
            if user_id not in cookieDict[ctx.guild.id]:
                cookieDict[ctx.guild.id][user_id] = {**userData}

        # send the embed
        embed = discord.Embed(
            title = str(user.display_name) + "'s Cookie Balance",
            color = 0x7289da,
            )
    
    
        embed.add_field(name = "Cookies", value = str(cookieDict[ctx.guild.id][user.id]["Cookies"]), inline = True)
        embed.add_field(name = "Rank", value = "#" + str(position(ctx.guild.id, user_id)), inline = True)
        embed.set_thumbnail(url = user.display_avatar)

        await ctx.send(embed=embed)
    
    except discord.NotFound:
        await ctx.send("You have sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)



# connecting to main file

async def setup(bot):
    bot.add_command(bal)