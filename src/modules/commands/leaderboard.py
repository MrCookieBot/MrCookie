import math
from datetime import datetime, timezone
from typing import Optional

import discord
from attrs import define, field
from discord.ext import commands

from resources.checks import lookup_database, new_database
from resources.constants import UNICODE_LEFT, UNICODE_RIGHT
from resources.mrcookie import instance as bot

MAX_USERS_PER_PAGE = 2


@define()
class SimpleUser:
    uid: str
    cookies: int
    position: Optional[int] = field(default=0, kw_only=True)

    async def lb_output(self) -> str:
        user = bot.get_user(int(self.uid)) or await bot.fetch_user(int(self.uid))
        return (
            f"**#{self.position}. {user.global_name}**"
            f"\n{self.cookies} Cookie{'s' if self.cookies != 1 else ''}"
        )


@bot.command(aliases=["lb"])
async def leaderboard(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.reply("This command can only be run in a server!", delete_after=7)

    guild_data = await bot.db.get_guild_users(ctx.guild.id)
    if guild_data is None:
        return await ctx.reply("No data for this guild was found!", delete_after=7)

    guild_users: dict = guild_data.get("users", {})
    if not guild_users:
        return await ctx.reply("No users have cookies here!", delete_after=7)

    simplified_users: list[SimpleUser] = [
        SimpleUser(uid, data["Cookies"]) for uid, data in guild_users.items()
    ]
    simplified_users.sort(key=(lambda x: x.cookies), reverse=True)
    this_user = None
    for n, user in enumerate(simplified_users):
        user.position = n + 1
        if user.uid == str(ctx.author.id):
            this_user = user

    embed = await build_view_page(simplified_users)
    embed.set_thumbnail(url=ctx.guild.icon)
    if this_user:
        embed.description = f"Your position: **#{this_user.position}**\n**{'━' * 13}**"

    max_pages = math.ceil(len(simplified_users) / MAX_USERS_PER_PAGE)
    view = discord.ui.View(timeout=None)

    left_button = discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=UNICODE_LEFT,
        disabled=True,
        custom_id=f"lb-button:{ctx.author.id}:0:{max_pages}",
    )

    right_button = discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=UNICODE_RIGHT,
        disabled=True if max_pages == 1 else False,
        custom_id=f"lb-button:{ctx.author.id}:1:{max_pages}",
    )

    view.add_item(left_button)
    view.add_item(right_button)

    await ctx.send(embed=embed, view=view)


# Ref: https://github.com/One-Nub/helper-bot/blob/main/src/modules/auto_response/autoresponder.py
@bot.add_button_handler("lb-button")
async def page_buttons(interaction: discord.Interaction, view: discord.ui.View | None):
    custom_id_data = interaction.data["custom_id"].split(":")  # type: ignore
    custom_id_data.pop(0)
    original_author_id = custom_id_data[0]
    new_page_index = int(custom_id_data[1])
    max_pages = int(custom_id_data[2])

    if not interaction.message or not interaction.guild:
        return

    # Disable after 5 mins.
    if (datetime.now(timezone.utc) - interaction.message.created_at).seconds > 300:
        if view:
            for x in view.children:
                # Ignored because this is how d.py says to do it.
                x.disabled = True  # pyright: ignore[reportAttributeAccessIssue]

        return await interaction.response.edit_message(
            content="-# This prompt was disabled because 5 minutes have passed since its creation.",
            view=view,
        )

    if str(interaction.user.id) != original_author_id:
        return await interaction.response.send_message(
            f"You're not allowed to flip through this embed!", ephemeral=True
        )

    prev_page_index = 0 if new_page_index - 1 < 0 else new_page_index - 1
    next_page_index = max_pages if new_page_index + 1 >= max_pages else new_page_index + 1

    view = discord.ui.View()
    left_button = discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=UNICODE_LEFT,
        disabled=True if prev_page_index <= 0 and new_page_index != 1 else False,
        custom_id=f"lb-button:{interaction.user.id}:{prev_page_index}:{max_pages}",
    )

    right_button = discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=UNICODE_RIGHT,
        disabled=True if next_page_index == max_pages else False,
        custom_id=f"lb-button:{interaction.user.id}:{next_page_index}:{max_pages}",
    )

    view.add_item(left_button)
    view.add_item(right_button)

    guild_data = await bot.db.get_guild_users(interaction.guild.id)
    if guild_data is None:
        return await interaction.response.send_message("No data for this guild was found!", ephemeral=True)

    guild_users: dict = guild_data.get("users", {})
    if not guild_users:
        return await interaction.response.send_message("No users have cookies here!", ephemeral=True)

    simplified_users: list[SimpleUser] = [
        SimpleUser(uid, data["Cookies"]) for uid, data in guild_users.items()
    ]
    simplified_users.sort(key=(lambda x: x.cookies), reverse=True)
    this_user = None
    for n, user in enumerate(simplified_users):
        user.position = n + 1
        if user.uid == str(interaction.user.id):
            this_user = user

    embed = await build_view_page(simplified_users, page_num=new_page_index)
    embed.set_thumbnail(url=interaction.guild.icon)
    if this_user:
        embed.description = f"Your position: **#{this_user.position}**\n**{'━' * 13}**"

    await interaction.response.edit_message(embed=embed, view=view)


async def build_view_page(all_users: list[SimpleUser], page_num: int = 0) -> discord.Embed:
    max_pages = math.ceil(len(all_users) / MAX_USERS_PER_PAGE)
    # Grab the 10 elements that we care about
    offset = page_num * MAX_USERS_PER_PAGE
    selected_items = all_users[offset : offset + MAX_USERS_PER_PAGE]

    # Build the embed.
    embed = discord.Embed(title="Leaderboard", color=0x7688D4)

    user_strs = [await user.lb_output() for user in selected_items]

    embed.add_field(name=" ", value="\n\n".join(user_strs[:5]))
    if user_strs[5:]:
        embed.add_field(name=" ", value="\n\n".join(user_strs[5:]))

    # footer
    embed.set_footer(text=f"Page {page_num + 1}/{max_pages}")

    # return the entire embed
    return embed
