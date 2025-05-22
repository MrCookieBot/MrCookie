import asyncio
import random
from datetime import datetime

import discord

from resources.mrcookie import instance as bot

channel_cooldowns: dict[str, datetime] = dict()
channel_lock: set[str] = set()
channel_last_message: dict[str, discord.Message] = dict()
PROMPT_TIMEOUT = 10

# Format where the key is the question/prompt. The value is the accepted response.
user_prompts: dict[str, str] = {"question": "answer", "question2": "answer"}


@bot.listen()
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    channel_id = str(message.channel.id)
    last_msg = channel_last_message.get(channel_id)
    if not last_msg or last_msg.author.id == message.author.id:
        channel_last_message[channel_id] = message
        # return

    # TODO: Check cooldown.

    # Don't let the bot try and run multiple listeners
    if channel_id in channel_lock:
        return

    asyncio.create_task(process_trigger(channel_id))


async def process_trigger(channel_id: str):
    # lock as soon as possible
    channel_lock.add(channel_id)

    prompt = random.choice(list(user_prompts.keys()))
    answer = user_prompts[prompt]

    ch_prsr = ChannelProcessor(channel_id, prompt, answer)

    # Send prompt

    # Listen for messages, then stop after asyncio.sleep.
    bot.add_listener(ch_prsr.message_listener, name="on_message")
    await asyncio.sleep(PROMPT_TIMEOUT)
    bot.remove_listener(ch_prsr.message_listener, name="on_message")

    if not ch_prsr.complete:
        # nobody answered, send a message saying what the correct answer was.
        # reply to prompt msg from the bot?
        # delete after N seconds?
        ...
    # Wait for the full timeout before we start listening to messages again

    channel_lock.remove(channel_id)
    # Set cooldown


class ChannelProcessor:
    def __init__(self, channel_id: str, prompt: str, answer: str):
        self.channel_id = channel_id
        self.prompt = prompt
        self.answer = answer
        self.queue = asyncio.Queue()
        self.complete = False

    async def message_listener(self, message: discord.Message):
        if message.author.bot or str(message.channel.id) != self.channel_id or self.complete:
            return

        print(f"received message {message.content}")

        content = message.content.lower()
        if content != self.answer:
            print(f"{content} != {self.answer}")
            return

        print(f"success! the user answered correctly - {self.answer}")
        self.complete = True
        await self.on_complete()

    async def on_complete(self):
        # Update user cookies in DB
        # Send successful grab message
        ...
