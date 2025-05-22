from resources.mrcookie import instance as bot
from resources.checks import lookup_counter
import discord

@bot.command()
async def setcounter(ctx):
    counter_embed = discord.Embed(
        title = "Counter Channel Set!",
        description = "Want to change your counter channel? Run this command again in that channel.",
        color = 0x2ecc71,
        )

    counter_embed.set_footer(text = 'To find out how counting works, run ".help counter"')
    await ctx.send(embed=counter_embed)


@bot.listen()
async def on_message(message):
    if message.content.isdigit():
        counterData = await lookup_counter(message.guild.id)
        if message.channel.id == counterData["settings"]["counter"]["Channel"]:
            if message == counterData["settings"]["counter"]["Counter"] + 1:
                if message.author.id != counterData["settings"]["counter"]["lastUser"]:
                    counterData["settings"]["counter"]["Counter"] += 1
                    counterData["settings"]["counter"]["lastUser"] = message.author.id
                    message.send("saved, keep counting!")
                else:
                    message.send("test, you failed") ## failed msg --
                    counterData["settings"]["counter"]["lastUser"] = 0
                    counterData["settings"]["counter"]["Counter"] = 0
            else:
                message.send("test, you failed") ## failed msg --
                counterData["settings"]["counter"]["lastUser"] = 0
                counterData["settings"]["counter"]["Counter"] = 0