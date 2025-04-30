from resources.mrcookie import instance as bot
import discord
from datetime import datetime, timedelta

from resources.checks import lookup_database, new_database, update_database

@bot.command()
async def daily(ctx):
    try:
        userID = str(ctx.author.id)
        guildID = ctx.guild.id
        guild = ctx.bot.get_guild(guildID)
        user = guild.get_member(int(userID)) or await guild.fetch_member(int(userID))

        ## this block fetches user data from the database
        userData = await lookup_database(userID, guildID) 
        if userData == False:
            await new_database(userID, guildID)
            userData = await lookup_database(userID, guildID)

        ## this checks if they have a cooldown
        if datetime.now() < userData["users"][userID]["DailyExpire"]:
            timer = int(userData["users"][userID]["DailyExpire"].timestamp())

            cooldown_embed = discord.Embed(
                description = "You can collect your cookies again " + "<t:" + str(timer) + ":R>",
                color = 0x992d22,
                timestamp = userData["users"][userID]["DailyExpire"]
                )
            cooldown_embed.set_author(name = "Not yet " + str(user.display_name) + "!", icon_url = user.display_avatar)
            await ctx.send(embed=cooldown_embed)
            return
        
        ## calculate and give daily cookies
        BaseCookies = 15
        Multiplier = 0
        StreakCookies = int((userData["users"][userID]["Streaks"]/14) * 1.5)
        if userData["users"][userID]["DailyMultiplier"] > 0:
            if userData["users"][userID]["DailyMultExpire"] >= datetime.now(): Multiplier = userData["users"][userID]["DailyMultiplier"]
            else: userData["users"][userID]["DailyMultiplier"] = 0
        
        Temp = (BaseCookies + StreakCookies) * Multiplier
        TotalCookies = BaseCookies + StreakCookies + Temp
        userData["users"][userID]["Cookies"] += TotalCookies

        ## this block updates their streak and daily cooldown
        if datetime.now() > userData["users"][userID]["DailyExpire"] + timedelta(hours = 24): ## reset cooldown if 24 hours past expiration
            userData["users"][userID]["Streaks"] = 1
        else:
            userData["users"][userID]["Streaks"] += 1
        
        userData["users"][userID]["DailyExpire"] = datetime.now() + timedelta(hours = 23)

        ## send the final embed
        dailyembed = discord.Embed(
            description = "You have collected your daily ``" + str(TotalCookies) + "`` cookies!" + "\n" + 
            "You now have a streak of ``" + str(userData["users"][userID]["Streaks"]) + "``.", 
            color = 0x2ecc71,
            timestamp = userData["users"][userID]["DailyExpire"]
            )

        dailyembed.set_author(name = "Daily Cookies - " + str(user.display_name), icon_url = user.display_avatar)
        dailyembed.set_footer(text = "You can collect again in 23 hours.")
        await ctx.send(embed=dailyembed)

        ## update the database
        await update_database(userID, guildID, userData["users"][userID])
        
    except Exception as Error:
        await ctx.send(Error)