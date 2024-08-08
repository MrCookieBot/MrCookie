from resources.checks import is_blacklisted
from resources.mrcookie import instance as bot



@bot.event
async def on_message(message):
    if message.author.bot or await is_blacklisted(message.author.id) == True:
        return
    await bot.process_commands(message)