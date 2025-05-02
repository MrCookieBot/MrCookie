from resources.mrcookie import instance as bot
import discord

from resources.checks import lookup_database, new_database, update_database, is_blacklisted

@bot.command(aliases = ["transfer", "send"])
async def give(ctx, userID = '0', amount = "0"):
    try:
        ## check if user was mentioned, user is valid, user is in guild, and user isn't themself
        userID = userID.strip("<@!>")
        if userID == '0' or userID.isdigit() == False or len(userID) < 17 or ctx.guild.get_member(int(userID)) is None or userID == str(ctx.author.id):
            raise Exception("Invalid user, try again!")
        if await is_blacklisted(userID):
            raise Exception("Illegal activity! You can't give to a blacklisted user!")
        if amount.isdigit() == False or int(amount) <= 0:
            raise Exception("Invalid amount, try again!")
        
        ## set vars // userID == receiever, senderID == sender
        amount = int(amount)
        senderID = str(ctx.author.id)
        guildID = ctx.guild.id
        guild = ctx.bot.get_guild(guildID)
        user = guild.get_member(int(userID)) or await guild.fetch_member(int(userID))
        sender = guild.get_member(int(senderID)) or await guild.fetch_member(int(senderID))

        ## this block fetches both user's data from the database
        userData = await lookup_database(userID, guildID)
        if userData == False:
            await new_database(userID, guildID)
            userData = await lookup_database(userID, guildID)
        senderData = await lookup_database(senderID, guildID) 
        if senderData == False:
            await new_database(senderID, guildID)
            senderData = await lookup_database(senderID, guildID)

        ## check if sender has enough cookies
        if userData["users"][senderID]["Cookies"] < amount:
            raise Exception("Ahem- you don't have that many cookies..")
        
        ## transfer the cookies
        userData["users"][userID]["Cookies"] += amount
        senderData["users"][senderID]["Cookies"] -= amount

        ## send the embed
        give_embed = discord.Embed(
            title = "💨 " + str(amount) + " Cookies Transferring..",
            ##description = "------------------>", 
            color = 0x2ecc71,
            )

        give_embed.add_field(name = "", value = "🍪 " + user.display_name + " now has **" + str(userData["users"][userID]["Cookies"]) + " cookies!**", inline = False)
        give_embed.set_author(name = "", icon_url = sender.display_avatar)
        give_embed.set_footer(text = "Cookies delievered by Sam")
        await ctx.send(embed=give_embed)

        ## update the database
        await update_database(userID, guildID, userData["users"][userID])
        await update_database(senderID, guildID, senderData["users"][senderID])

    except Exception as Error:
        await ctx.send(Error)