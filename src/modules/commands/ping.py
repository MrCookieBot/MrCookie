from resources.mrcookie import instance as bot

@bot.command()
async def ping(ctx):
    latency = round((ctx.bot.latency) * 1000)
    await ctx.reply("Pong! - " + str(latency) + "ms")