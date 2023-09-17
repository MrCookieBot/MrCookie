import discord
from discord.ext import commands
from misc.database import do_find_one, do_find_blacklist
import asyncio
from datetime import datetime, timedelta


# get the rank 

async def position(user_id, data, blacklist_data, guild):

    def sorting(values):
        return data["users"][str(values)]["Cookies"]


    cookielist = []
    raw_cookielist = list(data["users"])
    
    for id in raw_cookielist:
        # proceed if user is not blacklisted, and in guild, and has more than 0 cookies                
        if str(id) not in blacklist_data and  guild.get_member(int(id)) != None and int(data["users"][str(id)]["Cookies"]) > 0:
            cookielist.append(int(id))
        else:
            continue
    
    cookielist.sort(reverse = True, key = sorting)

    final_list = []

    # get the user's rank
    if int(user_id) not in cookielist:
        final_list.append("None")
        final_list.append(cookielist)
    else:
        final_list.append(cookielist.index(user_id) + 1)
        final_list.append(cookielist)

    return final_list


@commands.command(aliases = ["lb"])
@commands.cooldown(1, 45, commands.BucketType.member)
async def leaderboard(ctx):

    try:

        # get the data
        data = await do_find_one({"_id": str(ctx.guild.id), "users": {"$exists": True}})
        # get the guild
        guild = ctx.bot.get_guild(ctx.guild.id)
        # get the blacklisted users list
        blacklist_data = await do_find_blacklist()

        if len(data["users"]) < 1: # if no one is in the database, do not show a leaderboard
            raise Exception("There is no one in the leaderboard, run .daily to create one!")

        # get the rank of the user who ran the command, call the position method
        final_list = await position(ctx.author.id, data, blacklist_data, guild)
        pos = final_list[0]
        cookielist = final_list[1]

        # pages stuff
        count = 10
        pages = 1
        while len(cookielist) > count:
            count += 10
            pages += 1
    
        # each page has a different set of users
        cur_page = 1
        mainlist = []

        for current_page in range(0, pages):
            x = current_page * 10
            y = x + 10
            mainlist.append(cookielist[x:y])


    
        # build the embed ---------------------
        async def build_embed(cur_page):
            embed_leaderboard = discord.Embed(
                title = "Leaderboard",
                description = "Your position: **#" + str(pos) + "** \n" + "━━━━━━━━━━━━━",
                color = 0x7289da,
                )
    
            # set the server icon
            embed_leaderboard.set_thumbnail(url = ctx.guild.icon)

            currentlist = mainlist[cur_page - 1]

            mystr = ""
            # build the leaderboard
            for key in currentlist:
                # try to get_user, if none then fetch
                if ctx.bot.get_user(key) == None:
                    user = await ctx.bot.fetch_user(key)
                else:
                    user = ctx.bot.get_user(key)
        
                # setting variables for organization
                amount = data["users"][str(key)]["Cookies"]
                rank = cookielist.index(key) + 1
                index = currentlist.index(key) + 1


                # building the lines in an embed
                mystr += "**#" + str(rank) + ". " + str(user.display_name) + "** " + "\n" + str(amount) + " Cookies" + "\n" + "\n"

                if index == 5 or index == 10:
                    embed_leaderboard.add_field(name = "", value = mystr, inline = True)
                    mystr = ""

            # make sure the embeds send even if we didn't hit 5 or 10 users
            if len(currentlist) < 5:
                embed_leaderboard.add_field(name = " ", value = mystr, inline = True)
            if len(currentlist) > 5 and len(currentlist) < 10:
                embed_leaderboard.add_field(name = " ", value = mystr, inline = True)



            # footer
            embed_leaderboard.set_footer(text = f"Page {cur_page}/{pages}", icon_url = ctx.author.display_avatar)
            # return the entire embed
            return embed_leaderboard



        send_embed = await ctx.send(embed = await build_embed(cur_page))
        if pages != 1:
            await send_embed.add_reaction("◀️")
            await send_embed.add_reaction("🗑️")
            await send_embed.add_reaction("▶️")

            # This makes sure nobody except the command sender can interact with the menu
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "🗑️", "▶️"]
    
            while True:
                try:
                    reaction, user = await ctx.bot.wait_for("reaction_add", timeout=120, check=check)
                    # waiting for a reaction to be added - times out after 120 seconds
                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        await send_embed.edit(embed = (await build_embed(cur_page)))
                        await send_embed.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        await send_embed.edit(embed = (await build_embed(cur_page)))
                        await send_embed.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "🗑️" :
                        await send_embed.remove_reaction(reaction, user)
                        raise asyncio.TimeoutError
                
                    else:
                        await send_embed.remove_reaction(reaction, user)
                        # removes reactions if the user tries to go forward on the last page or backwards on the first page
                except asyncio.TimeoutError:
                    await send_embed.clear_reactions()
                    break
                    # ending the loop if user doesn't react after x seconds

    # exception handling
    except Exception as Error:
        await ctx.send(Error)


# leaderboard cooldown
@leaderboard.error
async def on_command_error(ctx,  error):
    if isinstance(error, commands.CommandOnCooldown):
        # send the cooldown embed
        timer = f"{error.retry_after:.0f}"
        cooldown_embed = discord.Embed(
            description = "You're on cooldown, please try again in ``" + timer + " seconds``.",
                color = 0x992d22
                )

        await ctx.send(embed=cooldown_embed)
        

# connecting to main file

async def setup(bot):
    bot.add_command(leaderboard)