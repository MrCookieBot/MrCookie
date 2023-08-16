import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random
from custom_messages import drop_list

lastUserDict = {}
userTime = {"time": datetime.now() + timedelta(seconds = 90)}

cooldownDict = {}

drop_list_dict = {}
dropData = {"msg": "hi", "cookies": 0, "embed_id": 0}

async def collect_cookie(message):
    try:
        cooldown = {"ExpTime": None}

        channel =  message.channel
        channel_id = message.channel.id
        currentUser = message.author.id


        # if active prompt, listen to it first
        if channel_id in drop_list_dict:
            await channel.fetch_message(drop_list_dict[channel_id]["embed_id"]) #try to fetch the message, if no fetch then it got deleted
            from cookie_trigger import cookie_trigger
            await cookie_trigger(message)
            return

        # add cooldown to channel if not in it already
        if channel_id not in cooldownDict:
            cooldownDict[channel_id] = {}
            cooldownDict[channel_id] = cooldown

        # check if cooldown ended, if not, stop the code
        if cooldownDict[channel_id]["ExpTime"] != None:
            if datetime.now() <= cooldownDict[channel_id]["ExpTime"]:
                return

        # add the channel_id to dictionary to track if it's not in it
        if channel_id not in lastUserDict:
            lastUserDict[channel_id] = {}
        
            # add the first user as well
            lastUserDict[channel_id][currentUser] = {}
            lastUserDict[channel_id][currentUser] = userTime
            return


        # if it's the same user, update the timer
        if currentUser in lastUserDict[channel_id]:
            lastUserDict[channel_id][currentUser]["time"] = datetime.now() + timedelta(seconds = 90)
            return

    
        # if 2 people spoke
        if currentUser not in lastUserDict[channel_id]:
            for key in lastUserDict[channel_id]: # get the old_user id
                old_user = key
            if datetime.now() < lastUserDict[channel_id][old_user]["time"]: # make sure it's within 90 seconds
                del lastUserDict[channel_id] # message sent, reset
                cooldownDict[channel_id]["ExpTime"] = datetime.now() + timedelta(minutes = 3) # add a 3 minute cooldown

                # build the cookie drop message
                drop_msg_chance = random.choice(range(0, len(drop_list))) # randomly pick which msg to use
                drop_msg = drop_list[drop_msg_chance]

                # pick random cookie amount
                cookie_amount = random.choice(range(1, 21))



                # build the cookie drop embed-----------
                drop_embed = discord.Embed(
                title = "Dropped My Cookies, Grab Them!",
                description = "> *Repeat the text or answer my question in chat*",
                color = 0x11806a,
                )

                drop_embed.set_footer(text = "Cookies will disappear in 75 seconds.") # footer msg

                # the two fields
                drop_embed.add_field(name = "⌨️ **Repeat this:**", value = str(drop_msg), inline = True)
                drop_embed.add_field(name = "🍪 **You earn:**", value = str(cookie_amount) + " cookies", inline = True)
            
                # send embed
                sent_message = await channel.send(embed=drop_embed, delete_after = 75)
                embed_id = sent_message.id


                # add the message 
                drop_list_dict[channel_id] = {}
                drop_list_dict[channel_id] = dropData

                drop_list_dict[channel_id]["msg"] = drop_msg
                drop_list_dict[channel_id]["cookies"] = int(cookie_amount)

                drop_list_dict[channel_id]["embed_id"] = int(embed_id)

                
            else:
                del lastUserDict[channel_id] # it's been over 3 minutes, reset


    except discord.NotFound:
        del drop_list_dict[channel_id]
        pass
    except Exception as Error:
        await channel.send(Error)