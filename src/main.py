import discord
from discord.ext import commands
from cookie_drops.collect_cookie import collect_cookie
from misc.database import do_insert, do_find_one

# env stuff
import os
from dotenv import load_dotenv
load_dotenv()

# for bot uptime tracking
start_time = []

# intent

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# connect other commands

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("commands.ping")
        await self.load_extension("commands.say")
        await self.load_extension("commands.daily")
        await self.load_extension("commands.bal")
        await self.load_extension("commands.leaderboard")
        await self.load_extension("commands.give")
        await self.load_extension("commands.eat")
        await self.load_extension("commands.generate")
        await self.load_extension("commands.info")
        await self.load_extension("commands.invite")
        await self.load_extension("commands.rob")
        await self.load_extension("commands.blacklist")
        await self.load_extension("commands.unblacklist")
        bot.remove_command('help') # remove the default help command
        await self.load_extension("commands.help") # add my own help command

    # send a msg when bot goes online
    async def on_ready(self):
        channel = bot.get_channel(1138945384094388384)
        await channel.send("CookieBot has restarted and is back online.") # post message upon turning on
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".help")) # change bot status

    # on_guild_join
    async def on_guild_join(self, guild):
        if await do_find_one({"_id": str(guild.id)}) == None:
            await do_insert({"_id": str(guild.id)})



# prefix

bot = MyBot(command_prefix='!!', intents=intents)


# on_message
@bot.event
async def on_message(message):
    if not message.author.bot:
        from commands.blacklist import blacklisted_users
        if message.author.id not in blacklisted_users:
            await collect_cookie(message)
            await bot.process_commands(message)


# token
if __name__ == "__main__":
    token = os.getenv("token")
    bot.run(token)
