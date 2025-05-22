import logging

from discord import CustomActivity, Status

from resources.mrcookie import instance as bot


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=CustomActivity(name="Baking cookies!"),
        status=Status.online,
    )
    logging.info(f"{bot.user.name}#{bot.user.discriminator} is now logged in & ready!")
