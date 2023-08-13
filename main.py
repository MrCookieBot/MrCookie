import discord
from discord.ext import commands
from config import token

# for bot uptime tracking
start_time = []

# intent

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# connect other commands

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("ping")
        await self.load_extension("say")
        await self.load_extension("daily")
        await self.load_extension("bal")
        await self.load_extension("leaderboard")
        await self.load_extension("give")
        await self.load_extension("eat")
        await self.load_extension("generate")
        await self.load_extension("info")
        await self.load_extension("invite")
        await self.load_extension("rob")
        await self.load_extension("blacklist")
        await self.load_extension("unblacklist")
        bot.remove_command('help') # remove the default help command
        await self.load_extension("help") # add my own help command

    # send a msg when bot goes online
    async def on_ready(self):
        channel = bot.get_channel(1138945384094388384)
        await channel.send("CookieBot has restarted and is back online.") # post message upon turning on
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".help")) # change bot status


# prefix

bot = MyBot(command_prefix='!!', intents=intents)


# token

bot.run(token)
