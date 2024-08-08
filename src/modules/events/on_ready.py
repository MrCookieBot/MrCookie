from resources.mrcookie import instance as bot
from discord import CustomActivity, Status


@bot.event
async def on_ready():
    await bot.change_presence(
        activity = CustomActivity(name = "Baking cookies!"),
        status= Status.online,
    )

