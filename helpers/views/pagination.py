from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from discord import ui

if TYPE_CHECKING:
    import discord


class EmbedPaginatorView(ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        self._embeds = embeds
        self._queue = deque(embeds) # collections.deque
        self._initial = embeds[0]
        self._len = len(embeds)

        super().__init__(timeout=90)

    @ui.button(emoji='\N{LEFTWARDS BLACK ARROW}')
    async def previous_embed(self, interaction: discord.Interaction, _):
        self._queue.rotate(-1)
        embed = self._queue[0]
        await interaction.response.edit_message(embed=embed)


    @ui.button(emoji='\N{BLACK RIGHTWARDS ARROW}')
    async def next_embed(self, interaction: discord.Interaction, _):
        self._queue.rotate(1)
        embed = self._queue[0]
        await interaction.response.edit_message(embed=embed)

    @property
    def initial(self) -> discord.Embed:
        return self._initial