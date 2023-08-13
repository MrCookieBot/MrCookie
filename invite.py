import discord
from discord.ext import commands


@commands.command()
async def invite(ctx):
    try:
        # check if user is blacklisted
        from blacklist import blacklisted_users
        if ctx.author.id in blacklisted_users:
            raise Exception("You are blacklisted from MrCookie.")

        # send the invite embed
        invite_embed = discord.Embed(
            description = "[Click here to invite MrCookie!](https://discord.com/api/oauth2/authorize?client_id=1133155318117957643&permissions=2550523984&scope=applications.commands%20bot)",
            color = 0x546e7a
            )
    
        # bot avatar + bot name at the top
        invite_embed.set_author(name = ctx.bot.user.name, icon_url = ctx.bot.user.avatar)

        await ctx.send(embed=invite_embed)
    
    except Exception as Error:
        await ctx.send(Error)




# connecting to main file

async def setup(bot):
    bot.add_command(invite)