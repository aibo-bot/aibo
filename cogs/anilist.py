from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord import app_commands

from helpers import fmt
from helpers.views.pagination import EmbedPaginatorView
from helpers.constants import (
    ANILIST_ANIME_QUERY,
    ANILIST_MANGA_QUERY
)

if TYPE_CHECKING:
    from bot import BotBase


class Anilist(commands.GroupCog):
    def __init__(self, bot: BotBase):
        self.bot = bot

    @app_commands.command(
        description="Search for some anime on anilist.co"
    )
    async def anime(self, interaction: discord.Interaction, query: str):
        variables = {
            "search": query
        }
        url = "https://graphql.anilist.co"
        payload = {
            "query": ANILIST_ANIME_QUERY,
            "variables": variables
        }

        async with self.bot.session.post(url, json=payload) as resp:
            data = await resp.json()

        media = data["data"]["Page"]["media"]
        embeds = [fmt.fmt_anime_embed(i) for i in media]
        view = EmbedPaginatorView(embeds)

        embed = view.initial
        await interaction.response.send_message(
            view=view,
            embed=embed,
            ephemeral=True
        )

    @app_commands.command(
        description="Search for some manga on anilist.co"
    )
    async def manga(self, interaction: discord.Interaction, query: str):
        variables = {
            "search": query
        }
        url = "https://graphql.anilist.co"
        payload = {
            "query": ANILIST_MANGA_QUERY,
            "variables": variables
        }

        async with self.bot.session.post(url, json=payload) as resp:
            data = await resp.json()

        media = data["data"]["Page"]["media"]
        embeds = [fmt.fmt_manga_embed(i) for i in media]
        view = EmbedPaginatorView(embeds)

        embed = view.initial
        await interaction.response.send_message(
            view=view,
            embed=embed,
            ephemeral=True
        )

async def setup(bot: BotBase):
    await bot.add_cog(Anilist(bot))
    