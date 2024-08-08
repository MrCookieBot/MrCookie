import discord
from resources.mrcookie import instance as bot

@bot.command()
async def invite(ctx):
    invite_embed = discord.Embed(
        description = "Invite goes here",
        color = 0x546e7a
        )
    invite_embed.set_author(name = ctx.bot.user.name, icon_url = ctx.bot.user.avatar)

    await ctx.send(embed=invite_embed)