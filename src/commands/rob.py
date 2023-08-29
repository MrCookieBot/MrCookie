import discord
from discord.ext import commands
from misc.database import do_update, do_find_one
from datetime import datetime, timedelta
from misc.custom_messages import pass_list, fail_list

import random


@commands.command()
async def rob(ctx, user_id = "0"):

    try:
        # check if user is in database, if not add them
        if await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}}) == None:
            raise Exception("You need at least 15 cookies to rob someone.")
        
        # make sure their rob cooldown is over
        data = (await do_find_one({"_id": str(ctx.guild.id), "users." + str(ctx.author.id): {"$exists": True}})) # refresh the data dict with new database data

        if data["users"][str(ctx.author.id)]["RobExp"] == None or datetime.now() > data["users"][str(ctx.author.id)]["RobExp"]:
            # check if the sender has enough cookies to rob
            if int(data["users"][str(ctx.author.id)]["Cookies"]) < 15:
                raise Exception("You need at least 15 cookies to rob someone.")
    
            # check if user_id is valid
            user_id = user_id.strip("<@!>")
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                raise Exception("You sent an invalid user.")
            
            # check if user is blacklisted
            #from commands.blacklist import blacklisted_users
            #if user_id in blacklisted_users:
                #raise Exception("You can't rob a blacklisted user.")

            # if user didn't mention someone, find someone random to rob user
            if user_id == 0:
                if len(data["users"]) <= 2: # if no one is in the database, do not rob anyone
                    raise Exception("More than 2 people need at least 15 cookies to rob.")
                
                rob_list = []
                for person in data["users"]: # create a list of every user in the server who has over 15 cookies
                    if int(data["users"][str(person)]["Cookies"]) < 15:
                        continue
                    if ctx.author.id == int(person): # make sure the sender themself isn't added to the list
                        continue
                    else:
                        rob_list.append(int(person))
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
                if await do_find_one({"_id": str(ctx.guild.id), "users." + str(user_id): {"$exists": True}}) == None:
                    raise Exception("User doesn't have enough cookies to be robbed.")
                
                # if user has less than 15 cookies, they cannot be robbed
                if int(data["users"][str(user_id)]["Cookies"]) < 15:
                    raise Exception("User doesn't have enough cookies to be robbed.")

            # get_user's data to mention them in the rob message
            user = ctx.bot.get_user(user_id)
    
        
            # add 3 hours to their rob cooldown
            new_timer = datetime.now() + timedelta(hours = 3)
            await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "RobExp": new_timer}})

            # go through the robbing process of the user

            selection = random.choice(range(0, 11))
            if selection > 7: # 30% chance of succesful robbery

                pass_msg_chance = random.choice(range(0, len(pass_list))) # randomly pick which msg to use
                pass_msg = pass_list[pass_msg_chance]

                if int(data["users"][str(user_id)]["Cookies"]) <= 100: # if below 100 cookies, steal 1-10
                    lost_cookies = random.choice(range(0, 6))
                if int(data["users"][str(user_id)]["Cookies"]) > 100 and int(data["users"][str(user_id)]["Cookies"]) <= 1500: # if below 1,500 cookies, steal 0.8%
                    lost_cookies = int(0.008 * int(data["users"][str(ctx.author.id)]["Cookies"]))
                if int(data["users"][str(user_id)]["Cookies"]) > 1500: # if above 1,500 cookies, steal 0.16%
                    lost_cookies = int(0.0016 * int(data["users"][str(ctx.author.id)]["Cookies"]))

                extra_losses = random.choice(range(5, 11)) # take an extra 5-10 cookies randomly
                total_losses = lost_cookies + extra_losses # add all the losses up

                new_cookies = int(data["users"][str(user_id)]["Cookies"]) - total_losses
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) + "." + "Cookies": new_cookies}})

                new_cookies2 = int(data["users"][str(ctx.author.id)]["Cookies"]) + total_losses
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies2}})

                
                # send the succeed embed
                pass_embed = discord.Embed(
                title = "Robbery Succeeded!",
                description = "You stole ``" + str(total_losses) + "`` cookies from " + str(user.mention) + " (" + str(user.display_name) + ") by " + pass_msg,
                color = 0x2ecc71,
                )
            
                await ctx.send(embed=pass_embed)

            if selection <= 7: # 70% chance of failed robbery

                fail_msg_chance = random.choice(range(0, len(fail_list))) # randomly pick which msg to use
                fail_msg = fail_list[fail_msg_chance]

                lost_cookies = int(0.008 * int(data["users"][str(ctx.author.id)]["Cookies"])) # take 0.8% of the robber's total cookies
                extra_losses = random.choice(range(5, 11)) # add an extra 5-10
                total_losses = lost_cookies + extra_losses # add it all up

                new_cookies = int(data["users"][str(ctx.author.id)]["Cookies"]) - total_losses
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(ctx.author.id) + "." + "Cookies": new_cookies}})

                new_cookies2 = int(data["users"][str(user_id)]["Cookies"]) + total_losses
                await do_update({"_id": str(ctx.guild.id)}, {'$set': {"users." + str(user_id) + "." + "Cookies": new_cookies2}})

                # send the fail embed
                fail_embed = discord.Embed(
                title = "Robbery Failed!",
                description = str(user.mention) + " (" + str(user.display_name) + ") stole ``" + str(total_losses) + "`` of your cookies because " + fail_msg,
                color = 0x992d22,
                )
            
                await ctx.send(embed=fail_embed)
    
        else:
            mathtime = int(data["users"][str(ctx.author.id)]["RobExp"].timestamp()) # doing the math for embed timer
            timeout_embed = discord.Embed(
                description = "You can rob someone again " + "<t:" + str(mathtime) + ":R>",
                color = 0x992d22,
                timestamp = data["users"][str(ctx.author.id)]["RobExp"]
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