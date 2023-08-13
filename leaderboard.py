import discord
from discord.ext import commands
from daily import cookieDict
import asyncio
from datetime import datetime, timedelta


# get the rank 

def position(guild_id, author_id):

    def sorting(values):
        return cookieDict[guild_id][values]['Cookies']

    cookielist = list(cookieDict[guild_id])
    cookielist.sort(reverse = True, key = sorting)

    final_list = []
    rank = 0

    for key in cookielist:
        if author_id not in cookieDict[guild_id]: # if they are no in database, they have no position
            final_list.append("None")
            final_list.append(cookielist)
            break
        if key == author_id:
            rank = cookielist.index(key) + 1
            final_list.append(rank)
            final_list.append(cookielist)
            break
    
    return final_list


@commands.command(aliases = ["lb"])
@commands.cooldown(1, 45, commands.BucketType.member)
async def leaderboard(ctx):

    try:
        # check if user is blacklisted
        from blacklist import blacklisted_users
        if ctx.author.id in blacklisted_users:
            raise Exception("You are blacklisted from MrCookie.")

        # check if guild is in dictionary
        if ctx.guild.id not in cookieDict:
            raise Exception("Leaderboard is empty, run .daily to create one.")

        # find the position of who made the cmd
        final_list = position(ctx.guild.id, ctx.author.id)
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
                amount = cookieDict[ctx.guild.id][key]["Cookies"]
                rank = cookielist.index(key) + 1
                index = currentlist.index(key) + 1


                # building the lines in an embed
                if index <= 5:
                    mystr += "**#" + str(rank) + "** " + str(user.mention) + "\n" + str(amount) + " Cookies" + "\n" + "\n"

                if index == 5:
                    embed_leaderboard.add_field(name = " ", value = mystr, inline = True)
                    mystr = ""

                if index > 5 and rank <= 10:
                    mystr += "**#" + str(rank) + "** " + str(user.mention) + "\n" + str(amount) + " Cookies" + "\n" + "\n"

                if index == 10:
                    embed_leaderboard.add_field(name = "\n", value = mystr, inline = True)

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