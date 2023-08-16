import discord
from discord.ext import commands

Admins = [194962036784889858, 156872400145874944, 84117866944663552] # admin list, these users can run say and generate in any server

# say command

@commands.command()
async def say(ctx, *message):

    try:
        # check if user has manage_guild perms or is in admin list
        if ctx.message.author.guild_permissions.manage_guild == False or ctx.message.author.id not in Admins:
            raise Exception("You don't have permission to run this command.")

        await ctx.message.delete()

        channel_id = message[0].strip("<>#")

        if channel_id.isdigit():
            if ctx.bot.get_channel(int(channel_id)) != None:
                channel = ctx.bot.get_channel(int(channel_id))
            else:
                channel = ctx.bot.get_channel(ctx.channel.id)
        else:
            channel = ctx.bot.get_channel(ctx.channel.id)

        mystr = ""
        for value in message:
            if value == "<#" + str(channel_id) + ">":
                continue
            else:
                mystr += value + " "
        if mystr == "":
            raise Exception("You forgot to include the message.")


        await channel.send(mystr)

    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(say)