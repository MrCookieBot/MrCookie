import discord
from discord.ext import commands
from daily import cookieDict
from datetime import datetime, timedelta

import random


@commands.command()
async def rob(ctx, user_id = "0"):

    try:
        # check if user is blacklisted
        from blacklist import blacklisted_users
        if ctx.author.id in blacklisted_users:
            raise Exception("You are blacklisted from MrCookie.")

        # check if guild/user is in database, if not add it
        if ctx.guild.id not in cookieDict:
            cookieDict[ctx.guild.id] = {}
        if ctx.author.id not in cookieDict[ctx.guild.id]:
            raise Exception("You need at least 15 cookies to rob someone.")
        
        # make sure their rob cooldown is over
        if cookieDict[ctx.guild.id][ctx.author.id]["RobExp"] == None or datetime.now() > cookieDict[ctx.guild.id][ctx.author.id]["RobExp"]:

            # check if the sender has enough cookies to rob
            if cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] < 15:
                raise Exception("You need at least 15 cookies to rob someone.")
    
            # check if user_id is valid
            user_id = user_id.strip("<@!>")
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                raise Exception("You sent an invalid user.")

            # if user didn't mention someone, find someone random to rob user
            if user_id == 0:
                if len(cookieDict[ctx.guild.id]) <= 2: # if no one is in the database, do not rob anyone
                    raise Exception("No one in the guild meets the rob requirements.")
                
                rob_list = []
                for person in cookieDict[ctx.guild.id]: # create a list of every user in the server who has over 15 cookies
                    if cookieDict[ctx.guild.id][person]["Cookies"] < 15:
                        continue
                    if ctx.author.id == person: # make sure the sender themself isn't added to the list
                        continue
                    else:
                        rob_list.append(person)
                random_user = random.choice(range(0, len(rob_list)))
                user_id = rob_list[random_user]

            # if user did mention someone, verify that user is real
            else:
                if len(str(user_id)) < 17:
                    raise Exception("You sent an invalid user.")
                
                # check if the user is themself
                if user_id == ctx.author.id:
                    raise Exception("You can't rob yourself, silly!")
            
                # check if user is in the guild
                guild = ctx.bot.get_guild(ctx.guild.id)
                if guild.get_member(user_id) is None:
                    raise Exception("User is not in the guild.")
                
                # if user is not in the database, they cannot be robbed
                if user_id not in cookieDict[ctx.guild.id]:
                    raise Exception("User doesn't have enough cookies to be robbed.")
                
                # if user has less than 15 cookies, they cannot be robbed
                if cookieDict[ctx.guild.id][user_id]["Cookies"] < 15:
                    raise Exception("User doesn't have enough cookies to be robbed.")

            # get_user's data to mention them in the rob message
            user = ctx.bot.get_user(user_id)
    
        
            # add 3 hours to their rob cooldown again
            cookieDict[ctx.guild.id][ctx.author.id]["RobExp"] = datetime.now() + timedelta(hours = 3)

            # go through the robbing process of the user

            selection = random.choice(range(0, 11))
            if selection > 7: # 30% chance of succesful robbery

                pass_list = ["you convinced them to invest in your stocks - which you trashed the next day.", "you stole their toilet and sold it on ebay, what's wrong with you??"] # list of pass messages
                pass_msg_chance = random.choice(range(0, len(pass_list))) # randomly pick which msg to use
                pass_msg = pass_list[pass_msg_chance]

                if cookieDict[ctx.guild.id][user_id]["Cookies"] <= 100: # if below 100 cookies, steal 1-10
                    lost_cookies = random.choice(range(0, 6))
                if cookieDict[ctx.guild.id][user_id]["Cookies"] > 100 and cookieDict[ctx.guild.id][user_id]["Cookies"] <= 1500: # if below 1,500 cookies, steal 0.8%
                    lost_cookies = int(0.008 * cookieDict[ctx.guild.id][ctx.author.id]["Cookies"])
                if cookieDict[ctx.guild.id][user_id]["Cookies"] > 1500: # if above 1,500 cookies, steal 0.16%
                    lost_cookies = int(0.0016 * cookieDict[ctx.guild.id][ctx.author.id]["Cookies"])

                extra_losses = random.choice(range(5, 11)) # take an extra 5-10 cookies randomly
                total_losses = lost_cookies + extra_losses # add all the losses up

                cookieDict[ctx.guild.id][user_id]["Cookies"] = cookieDict[ctx.guild.id][user_id]["Cookies"] - total_losses
                cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] = cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] + total_losses
                
                # send the succeed embed
                pass_embed = discord.Embed(
                title = "Robbery Succeeded!",
                description = "You stole ``" + str(total_losses) + "`` cookies from " + str(user.mention) + " (" + str(user.display_name) + ") because " + pass_msg,
                color = 0x2ecc71,
                )
            
                await ctx.send(embed=pass_embed)

            if selection <= 7: # 70% chance of failed robbery

                fail_list = ["you turned yourself into to the police, what a nice guy!", "you tripped on the way there, it was pretty funny."] # list of failure messages
                fail_msg_chance = random.choice(range(0, len(fail_list))) # randomly pick which msg to use
                fail_msg = fail_list[fail_msg_chance]

                lost_cookies = int(0.008 * cookieDict[ctx.guild.id][ctx.author.id]["Cookies"]) # take 0.8% of the robber's total cookies
                extra_losses = random.choice(range(5, 11)) # add an extra 5-10
                total_losses = lost_cookies + extra_losses # add it all up

                cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] = cookieDict[ctx.guild.id][ctx.author.id]["Cookies"] - total_losses # remove the cookies from robber
                cookieDict[ctx.guild.id][user_id]["Cookies"] = cookieDict[ctx.guild.id][user_id]["Cookies"] + total_losses # give the victim the cookies

                # send the fail embed
                fail_embed = discord.Embed(
                title = "Robbery Failed!",
                description = str(user.mention) + " (" + str(user.display_name) + ") stole ``" + str(total_losses) + "`` of your cookies because " + fail_msg,
                color = 0x992d22,
                )
            
                await ctx.send(embed=fail_embed)
    
        else:
            mathtime = int(cookieDict[ctx.guild.id][ctx.author.id]["RobExp"].timestamp()) # doing the math for embed timer
            timeout_embed = discord.Embed(
                description = "You can rob someone again " + "<t:" + str(mathtime) + ":R>",
                color = 0x992d22,
                timestamp = cookieDict[ctx.guild.id][ctx.author.id]["RobExp"]
                )

            timeout_embed.set_author(name = "Not so fast " + str(ctx.author.name), icon_url = ctx.author.display_avatar)
            
            await ctx.send(embed=timeout_embed)           

    except discord.NotFound:
        await ctx.send("You have sent an invalid user.")
    except Exception as Error:
        await ctx.send(Error)


# connecting to main file

async def setup(bot):
    bot.add_command(rob)