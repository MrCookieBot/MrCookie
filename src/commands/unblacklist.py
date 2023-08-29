import discord
from discord.ext import commands
from commands.say import Admins

from misc.database import do_find_blacklist_user, do_delete_blacklist_user

@commands.command()
async def unblacklist(ctx, user_id = "0"):
    try:
       # make sure only admins can run this command
        if ctx.author.id not in Admins:
            raise Exception("You don't have permission to run this command.")
        
        # make sure they sent a user_id
        if user_id == "0":
            raise Exception("Tell me which user, silly!")
        
        # make sure user_id is valid
        user_id = user_id.strip("<@!>")
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            raise Exception("You sent an invalid user.")
        
        # checking if the user_id meets minimum length
        if len(str(user_id)) < 17:
            raise Exception("You sent an invalid user.")
        
        # get_user's data, if they never used the bot then fetch it
        if ctx.bot.get_user(user_id) == None:
            user = await ctx.bot.fetch_user(user_id)
        else:
            user = ctx.bot.get_user(user_id)
        
        # check if user is blacklisted
        if await do_find_blacklist_user({"_id": str(user_id)}) == None:
            raise Exception("User is not blacklisted.")

        # if user_id passes all checks, start the unblacklist process -----------

        #await do_update_blacklist_user({"_id": str(user_id)}, {'$unset'})
        await do_delete_blacklist_user({"_id": str(user_id)})


        await ctx.send("Unblacklisted " + str(user.mention) + " (" + str(user_id) + ") .")


    # exception handling
    except discord.NotFound:
        await ctx.send("You sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)
      
        

# connecting to main file

async def setup(bot):
    bot.add_command(unblacklist)