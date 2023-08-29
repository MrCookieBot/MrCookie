import discord
from discord.ext import commands
from cookie_drops.collect_cookie import drop_list_dict

from misc.database import do_update, do_find_one, do_find_blacklist_user

# userData dictionary

userData = {"Streaks": 0, "ExpTime": None, "Cookies": 0, "Multiplier": 0, "RobExp": None}


async def cookie_trigger(message):
    try:
        channel =  message.channel
        channel_id = message.channel.id
        currentUser = message.author
    
        # if the message matches the drop_msg, reward the first user who said it the cookies
        if message.content == str(drop_list_dict[channel_id]["msg"]) and await do_find_blacklist_user({"_id": str(message.author.id)}) == None:
            # check if first user is in database, if not add them
            if await do_find_one({"_id": str(message.guild.id), "users." + str(message.author.id): {"$exists": True}}) == None:
                await do_update({"_id": str(message.guild.id)}, {'$set': {"users." + str(message.author.id) : {**userData}}})

            # reward the first user
            data = (await do_find_one({"_id": str(message.guild.id), "users." + str(message.author.id): {"$exists": True}})) # refresh the data dict with new database data

            new_cookies = int(data["users"][str(message.author.id)]["Cookies"]) + int(drop_list_dict[channel_id]["cookies"])
            await do_update({"_id": str(message.guild.id)}, {'$set': {"users." + str(message.author.id) + "." + "Cookies": new_cookies}})

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