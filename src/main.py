import discord
import asyncio
from discord.ext import commands
from resources.mrcookie import MrCookie

# env stuff
import os
from dotenv import load_dotenv
load_dotenv()

# for bot uptime tracking
start_time = []

# nub logging
discord.utils.setup_logging()

# intent
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def main():

    bot = MrCookie(
        command_prefix = ',',
        mongodb_url = os.getenv("uri_p"),
        intents=intents,
    )

    MODULES = ["modules/commands", "modules/events", "modules/commands/drops"]

    ## loop through all the files under the commands folder, that's how we check for commands
    for directory in MODULES:
        files = [
            name
            for name in os.listdir("src/" + directory.replace(".", "/"))
            if name[:1] != "." and name[:2] != "__" and name != "_DS_Store"
        ]

        for filename in [f.replace(".py", "") for f in files]:
            if filename in ("bot", "__init__"):
                continue

            bot.load_module(f"{directory.replace('/','.')}.{filename}")

    await bot.start(token = os.getenv("token"))


if __name__ == "__main__":
    asyncio.run(main())