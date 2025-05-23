import asyncio
import random

import discord

from resources.id_cooldown import IDCooldown
from resources.mrcookie import instance as bot

from .prompts import user_prompts

# all units in seconds
PROMPT_TIMEOUT = 10
PROMPT_COOLDOWN = (3 * 60) + PROMPT_TIMEOUT
TIME_BETWEEN_MSGS = 90

# Handles cooldown logic
channel_cooldowns: IDCooldown = IDCooldown(PROMPT_COOLDOWN)
# Keeps track of which channels have an active prompt
channel_lock: set[str] = set()
# Keeps track of last sent message in a channel
channel_last_message: dict[str, discord.Message] = dict()


@bot.listen()
async def on_message(message: discord.Message):
    channel_id = str(message.channel.id)

    # Ignore bot messages, ignore when channel is locked.
    if message.author.bot or channel_id in channel_lock or type(message.channel) != discord.TextChannel:
        return

    last_msg = channel_last_message.get(channel_id)
    if (
        not last_msg
        or last_msg.author.id == message.author.id
        or (message.created_at - last_msg.created_at).seconds >= TIME_BETWEEN_MSGS
    ):
        channel_last_message[channel_id] = message
        # return

    # This applies the cooldown - so we don't need to update it elsewhere.
    if channel_cooldowns.check_for_id(message.channel.id):
        channel_last_message[channel_id] = message
        return

    asyncio.create_task(process_trigger(message.channel))
    del channel_last_message[channel_id]


async def process_trigger(channel: discord.TextChannel):
    # lock as soon as possible
    channel_lock.add(str(channel.id))

    ch_prsr = ChannelProcessor(str(channel.id))

    # Send prompt
    # channel.send()

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
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.prompt = random.choice(list(user_prompts.keys()))
        self.answer = user_prompts[self.prompt]
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
