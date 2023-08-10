import discord
from discord.ext import commands


@commands.command()
async def help(ctx):
    # send the transfer embed
    help_embed = discord.Embed(
        description = "Here's a list of all our commands and how to use them.",
        color = 0x546e7a,
        )
    
    # title and profile icon
    help_embed.set_author(name = "MrCookie Help Page", icon_url = ctx.bot.user.avatar)

    help_embed.add_field(name = "Information", value = "``.help`` ➙ View this help page to learn about MrCookie." + "\n" +
    "``.ping`` ➙ Find the latency from the bot to Discord." + "\n" +
    "``.info`` ➙ Information about the bot's status and more." + "\n" +
    "``.invite`` ➙ Invite MrCookie to your server. ", inline = False)
    
    help_embed.add_field(name = "Your Cookies", value = "``.daily`` ➙ Collect free cookies once everyday, amount increases based on streak." + "\n" + 
    "``.rob (userID)`` ➙ Try to steal another user's cookies, but you may not succeed." + "\n" +
    "``.eat`` ➙ Eat one cookie cause you're hungry." + "\n" +
    "``.give (userID) (amount)`` ➙ [Aliases: transfer, gift] Give another user some of your cookies.", inline = False)
    
    help_embed.add_field(name = "Cookie Stats", value = "``.leaderboard`` ➙ [Aliases: lb] View who has the highest cookies in this server." + "\n" +
    "``.bal (optional: userID)`` ➙ [Aliases: balance, stats] View your or another user's cookie balance.", inline = False)

    help_embed.add_field(name = "Admin Commands", value = "``.say (optional: channelID) (message)`` ➙ Have the bot post your message." + "\n" +
    "``.generate (userID) (amount)`` ➙ Add or remove cookies from a user in this server.", inline = False)

    help_embed.set_footer(text = "Need help? Join our support server at discord.gg/QQTC3ABV9U")
            
    await ctx.send(embed=help_embed)




# connecting to main file

async def setup(bot):
    bot.add_command(help)