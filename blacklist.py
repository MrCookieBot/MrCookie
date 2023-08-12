import discord
from discord.ext import commands
from daily import cookieDict
from say import Admins

blacklisted_users = []

openFile = open("BlacklistedUsers.txt", "r") # open the blacklisted file
lines = openFile.readlines() # read the lines
openFile.close() # close the blacklisted file

for user in lines:
    user = user.strip("\n")
    user_int = int(user)
    blacklisted_users.append(user_int)

@commands.command()
async def blacklist(ctx, user_id = "0"):
    try:
        # make sure only admins can run this command
        if ctx.author.id not in Admins:
            raise Exception("You don't have permission to run this command.")
        
        # make sure they sent a user_id
        if user_id == "0":
            raise Exception("Tell me which user, silly!")
        
        # make sure they didn't mention themself
        if user_id == ctx.author.id:
            raise Exception("You can't blacklist yourself dude..")
        
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


        # if user_id passes all checks, start the blacklist process -----------
        


    # exception handling
    except discord.NotFound:
        await ctx.send("You sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)
      
        

# connecting to main file

async def setup(bot):
    bot.add_command(blacklist)