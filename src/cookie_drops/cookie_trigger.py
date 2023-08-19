import discord
from discord.ext import commands
from collect_cookie import drop_list_dict
from commands.daily import cookieDict


# userData dictionary

userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


async def cookie_trigger(message):
    try:
        # check if guild/user is in database
        if message.guild.id not in cookieDict:
            cookieDict[message.guild.id] = {}
        if message.author.id not in cookieDict[message.guild.id]: # add user to database if not in it
            cookieDict[message.guild.id][message.author.id] = {**userData}

        channel =  message.channel
        channel_id = message.channel.id
        currentUser = message.author
    
        # if the message matches the drop_msg, reward the first user who said it the cookies
        if message.content == str(drop_list_dict[channel_id]["msg"]):
            # reward the first user
            cookieDict[message.guild.id][currentUser.id]["Cookies"] = cookieDict[message.guild.id][currentUser.id]["Cookies"] + int(drop_list_dict[channel_id]["cookies"])

            # send who got the reward
            await channel.send(str(message.author.mention) + " (" + str(message.author.display_name) + ") collected " + str(drop_list_dict[channel_id]["cookies"]) + " cookies!", delete_after = 5)

            # delete the embed
            embed = await channel.fetch_message(drop_list_dict[channel_id]["embed_id"])
            await embed.delete()

            # delete the user's message
            await message.delete()

            # reset the drop_msg
            del drop_list_dict[channel_id]


        return
    
    except Exception as Error:
        await channel.send(Error)