import discord
from discord.ext import commands
from misc.database import do_update, do_find_one



@commands.command()
async def eat(ctx):
    try:
        data = await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}) # refresh the data dict with new database data

        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}) == None:
            raise Exception("You have no cookies to eat.")
        
        if int(data["users"][str(ctx.author.id)]["Cookies"]) - 1 < 0:
            raise Exception("You have no cookies to eat.")

        # if no errors, continue with command
        new_cookies = int(data["users"][str(ctx.author.id)]["Cookies"]) - 1 # removes 1 cookie from their total
        await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies}})
        await ctx.send("Yummy! You ate 1 cookie 🍪")


    # exception handling
    except Exception as Error:
        await ctx.send(Error)
        



# connecting to main file

async def setup(bot):
    bot.add_command(eat)