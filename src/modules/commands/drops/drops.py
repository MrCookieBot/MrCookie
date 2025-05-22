import asyncio
import random
from datetime import datetime

import discord

from resources.mrcookie import instance as bot

channel_cooldowns: dict[str, datetime] = dict()
channel_last_message: dict[str, discord.Message] = dict()

# Format where the key is the question/prompt. The value is the accepted response.
user_prompts: dict[str, str] = {"question": "answer", "question2": "answer"}


@bot.listen()
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    asyncio.create_task(process_trigger(str(message.channel.id)))


async def process_trigger(channel_id: str):
    prompt = random.choice(list(user_prompts.keys()))
    answer = user_prompts[prompt]
    print(prompt)

    @bot.listen()
    async def on_message(message: discord.Message):
        # hopefully only exists for the runtime of the function?
        pass
