from discord.ext import commands
from resources.mrcookie import instance as bot
from resources.checks import is_admin, validate_userid, is_blacklisted

@bot.command()
async def blacklist(ctx, temp_ID):
    try:
        if await is_admin(ctx.author.id) == False: raise Exception("You don't have permission to run this command.")
        
        userID = await validate_userid(temp_ID) 
        if userID == None: raise Exception("Invalid user.")
            
        if ctx.author.id == userID: raise Exception("You can't blacklist yourself.")
            
        if await is_blacklisted(userID) == True: raise Exception("User is already blacklisted.")
        
        await bot.db.add_blacklist({"_id": str(userID)})
        await ctx.send("Blacklisted " + str(userID))


    except Exception as Error:
        await ctx.send(Error)
    
@blacklist.error
async def blacklist_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("You didn't specify a user.")